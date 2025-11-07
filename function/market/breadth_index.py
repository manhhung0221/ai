"""
Market breadth utilities that rely on the legacy ORM models from Model.model_eod
and Model.model_info. The breadth index for each market gauge is calculated as:
    (advancers - decliners) / (advancers + decliners)
and bucketed into qualitative labels that describe underlying participation.
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Dict, Mapping, MutableMapping, Optional, Sequence

import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from Model.model_eod import EodStock, get_EodStock
from Model.model_info import StockInfo

EPSILON = 1e-6
ROUND_DIGITS = 2

DEFAULT_INDEX_MAPPING: Mapping[str, str] = OrderedDict(
    [
        ("VNINDEX", "VNINDEX"),
        ("HNX", "HNXIndex"),
        ("UPCOM", "UpcomIndex"),
    ]
)

ADV_DESC = "Số lượng cổ phiếu tăng giá so với giá tham chiếu"
DEC_DESC = "Số lượng cổ phiếu giảm giá so với giá tham chiếu"
UNCH_DESC = "Số lượng cổ phiếu giữ nguyên giá so với giá tham chiếu"


def build_market_breadth(
    index_mapping: Optional[Mapping[str, str]] = None,
) -> Dict[str, dict]:
    """
    Build breadth details for the supplied market indices.

    Parameters
    ----------
    index_mapping:
        Mapping of output index codes -> StockInfo.comGroupCode. Defaults to
        Vietnamese benchmarks (VNINDEX, HNX, UPCOM).

    Returns
    -------
    dict
        Mapping of index_code -> breadth payload.
    """
    mapping = OrderedDict(index_mapping or DEFAULT_INDEX_MAPPING)
    summary: MutableMapping[str, dict] = OrderedDict()

    with get_EodStock() as session:
        latest_dt = (
            session.query(func.max(EodStock.DateTime))
            .filter(EodStock.ticker == "VNINDEX")
            .scalar()
        )

        if latest_dt is None:
            for alias in mapping.keys():
                summary[alias] = _empty_payload(alias)
            return dict(summary)

        for alias, com_group in mapping.items():
            tickers = _tickers_for_comgroup(session, com_group)
            if not tickers:
                summary[alias] = _empty_payload(alias)
                continue

            df = _fetch_prices_df(session, tickers, latest_dt)
            advancers, decliners, unchanged = _count_breadth_df(df)
            breadth_value = _calc_breadth(advancers, decliners)
            summary[alias] = _build_payload(
                index_code=alias,
                advancers=advancers,
                decliners=decliners,
                unchanged=unchanged,
                breadth_value=breadth_value,
            )

    return dict(summary)


def _tickers_for_comgroup(session:Session, com_group: str) -> Sequence[str]:
    rows = (
        session.query(StockInfo.ticker)
        .filter(StockInfo.comGroupCode == com_group)
        .all()
    )
    return [row.ticker for row in rows]


def _fetch_prices_df(session:Session, tickers: Sequence[str], trading_date) -> pd.DataFrame:
    if not tickers:
        return pd.DataFrame(columns=["ticker", "Close", "priceBasic"])

    stmt = (
        select(EodStock.ticker, EodStock.Close, EodStock.priceBasic)
        .where(EodStock.DateTime == trading_date)
        .where(EodStock.ticker.in_(list(tickers)))
    )
    tickers_query="'"+("','").join(tickers)+"'"
    stmt=f"""SELECT ticker,"Close","priceBasic" FROM eod.eod_stock_v2 WHERE "DateTime"='{trading_date}' AND ticker IN ({tickers_query}) """
    engine = session.get_bind()
    if engine is None:
        return pd.DataFrame(columns=["ticker", "Close", "priceBasic"])
    
    return pd.read_sql(stmt, engine)


def _count_breadth_df(df: pd.DataFrame) -> tuple[int, int, int]:
    if df.empty:
        return 0, 0, 0

    working = df.dropna(subset=["Close", "priceBasic"]).copy()
    if working.empty:
        return 0, 0, 0

    working["delta"] = working["Close"] - working["priceBasic"]

    adv = int((working["delta"] > EPSILON).sum())
    dec = int((working["delta"] < -EPSILON).sum())
    unch = int((working["delta"].abs() <= EPSILON).sum())
    return adv, dec, unch


def _calc_breadth(advancers: int, decliners: int) -> Optional[float]:
    denominator = advancers + decliners
    if denominator == 0:
        return None
    breadth = (advancers - decliners) / denominator
    return round(breadth, ROUND_DIGITS)


def _build_payload(
    *,
    index_code: str,
    advancers: int,
    decliners: int,
    unchanged: int,
    breadth_value: Optional[float],
) -> dict:
    return {
        "index_code": index_code,
        "advancers": {"value": advancers, "description": ADV_DESC},
        "decliners": {"value": decliners, "description": DEC_DESC},
        "unchanged": {"value": unchanged, "description": UNCH_DESC},
        "breadth_index": breadth_value,
        "breadth_bucket": _bucketize(breadth_value),
    }


def _bucketize(breadth: Optional[float]) -> Optional[dict]:
    if breadth is None:
        return None

    if breadth <= -0.5:
        return {
            "label": "bearish",
            "description": "Độ rộng tiêu cực, phần lớn cổ phiếu giảm giá",
        }
    if -0.5 < breadth <= -0.2:
        return {
            "label": "slightly_bearish",
            "description": "Độ rộng nghiêng về giảm, sắc đỏ nhỉnh hơn",
        }
    if -0.2 < breadth < 0.2:
        return {
            "label": "neutral",
            "description": "Độ rộng cân bằng, thị trường giằng co",
        }
    if 0.2 <= breadth < 0.5:
        return {
            "label": "slightly_bullish",
            "description": "Độ rộng tích cực nhẹ, lực mua đang cải thiện",
        }
    return {
        "label": "bullish",
        "description": "Độ rộng tích cực, phần lớn cổ phiếu tăng giá",
    }


def _empty_payload(index_code: str) -> dict:
    return {
        "index_code": index_code,
        "advancers": {"value": 0, "description": ADV_DESC},
        "decliners": {"value": 0, "description": DEC_DESC},
        "unchanged": {"value": 0, "description": UNCH_DESC},
        "breadth_index": None,
        "breadth_bucket": None,
    }


if __name__ == "__main__":
    import json

    result = build_market_breadth()
    print(json.dumps(result, ensure_ascii=False, indent=4))
