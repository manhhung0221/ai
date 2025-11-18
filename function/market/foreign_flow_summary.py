"""
Foreign flow summary utilities that follow the meta_context specification provided
by the user. The builder aggregates:

1. Latest trading date based on VNINDEX entries in :class:`Model.model_eod.EodStock`.
2. Net foreign value across VNINDEX, HNXINDEX, and UPINDEX (converted to VND billions).
3. Per-sector net foreign value sourced from eod.eod_icb_agg_v1, enriched with
   :class:`Model.model_info.IcbInfo` and :class:`Model.model_info.StockInfo`.
4. Sector-level top stocks plus breadth metrics (count/value based) with the
   declared bucket thresholds.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from Model.model_eod import EodStock, get_EodStock
from Model.model_info import IcbInfo, StockInfo

MARKET_CODE = "VN"
INDEX_TICKERS = ("VNINDEX", "HNXINDEX", "UPINDEX")
TOP_SECTOR_LIMIT = 3
TOP_STOCK_LIMIT = 5
FOREIGN_VALUE_SCALE = 1_000_000_000  # raw VND -> billion VND
STRONG_THRESHOLD_BILLION = 300.0
SIGNIFICANT_THRESHOLD_BILLION = 500.0
EPSILON = 0
THREADSOLD_VALUE_STOCK_SECTOR=30
SECTOR_TABLE = "eod.eod_icb_agg_v1"


def build_foreign_flow_summary(
    *,
    market_code: str = MARKET_CODE,
    index_tickers: Sequence[str] = INDEX_TICKERS,
    top_sector_limit: int = TOP_SECTOR_LIMIT,
    top_stock_limit: int = TOP_STOCK_LIMIT,
) -> dict:
    """
    Build the foreign flow payload that complies with the supplied meta_context.

    Parameters
    ----------
    market_code:
        Logical identifier for the consolidated market scope. Defaults to "VN".
    index_tickers:
        Sequence of benchmark tickers whose combined foreign net value represents
        the market headline.
    top_sector_limit:
        Maximum number of sectors returned for each of the buy/sell groupings.
    top_stock_limit:
        Maximum number of stocks returned per sector (ranked by |net value|).
    """
    with get_EodStock() as session:
        latest_dt = _latest_trading_date(session)
        if latest_dt is None:
            return _empty_payload(market_code)

        net_total_raw = _aggregate_index_net_value(session, latest_dt, index_tickers)
        net_total_billion = _to_billion(net_total_raw)
        net_total_display = _round_half_up(net_total_billion, 1)

        sector_raw_map = _fetch_sector_flows(session, latest_dt)
        sector_billion_map = {
            code: _to_billion(value)
            for code, value in sector_raw_map.items()
            if code and value is not None
        }

        icb_codes = list(sector_billion_map.keys())
        icb_names = _fetch_icb_names(session, icb_codes)
        sector_members = _fetch_sector_members(session, icb_codes)
        ticker_flows = _fetch_stock_flows(
            session,
            {meta["symbol"] for members in sector_members.values() for meta in members},
            latest_dt,
        )

        sector_items_with_value: List[Tuple[float, dict]] = []
        for icb_code, net_value in sector_billion_map.items():
            payload = {
                "icb_code": icb_code,
                "sector_name": icb_names.get(icb_code, icb_code),
                "net_value_billion": _round_half_up(net_value, 1),
                "dir": _direction_from_value(net_value),
                "magnitude_bucket": _magnitude_bucket(net_value),
                "top_stocks": _build_top_stocks(
                    sector_members.get(icb_code, []), ticker_flows, top_stock_limit,_round_half_up(net_value, 1)>0
                ),
            }
            sector_items_with_value.append((net_value, payload))

        sector_values = [value for value, _ in sector_items_with_value]
        breadth = _compute_breadth(sector_values)

        return {
            "as_of": latest_dt.date().isoformat(),
            "market": market_code,
            "net_value_billion_total": net_total_display,
            "dir_total": _direction_from_value(net_total_billion),
            "magnitude_bucket_total": _magnitude_bucket(net_total_billion),
            "top_buy_sectors": _select_top_sectors(
                sector_items_with_value, True, top_sector_limit
            ),
            "top_sell_sectors": _select_top_sectors(
                sector_items_with_value, False, top_sector_limit
            ),
            "foreign_breadth": breadth,
        }


def _latest_trading_date(session: Session):
    return (
        session.query(func.max(EodStock.DateTime))
        .filter(EodStock.ticker == "VNINDEX")
        .scalar()
    )


def _aggregate_index_net_value(
    session: Session, trading_date, tickers: Sequence[str]
) -> float:
    if not tickers:
        return 0.0

    rows = (
        session.query(
            (
                func.coalesce(EodStock.buyForeignValue, 0)
                - func.coalesce(EodStock.sellForeignValue, 0)
            ).label("net_value")
        )
        .filter(EodStock.DateTime == trading_date)
        .filter(EodStock.ticker.in_(list(tickers)))
        .all()
    )
    return float(sum(row.net_value or 0.0 for row in rows))


def _fetch_sector_flows(session: Session, trading_date) -> Dict[str, float]:
    stmt = text(
        f"""
        SELECT "icbCode" AS icb_code,
               COALESCE("buyForeignValue", 0) - COALESCE("sellForeignValue", 0) AS net_value
        FROM {SECTOR_TABLE}
        WHERE "DateTime" = :dt
        """
    )
    rows = session.execute(stmt, {"dt": trading_date}).mappings().all()
    return {
        row["icb_code"]: float(row["net_value"])
        for row in rows
        if row["icb_code"]
    }


def _fetch_icb_names(session: Session, icb_codes: Sequence[str]) -> Mapping[str, str]:
    if not icb_codes:
        return {}
    rows = (
        session.query(IcbInfo.icbCode, IcbInfo.icbName)
        .filter(IcbInfo.icbCode.in_(list(icb_codes)))
        .all()
    )
    mapping: Dict[str, str] = {}
    for code,  official in rows:
        mapping[code] =  official or code
    return mapping


def _fetch_sector_members(
    session: Session, icb_codes: Sequence[str]
) -> Mapping[str, List[dict]]:
    if not icb_codes:
        return {}
    rows = (
        session.query(
            StockInfo.icbCode,
            StockInfo.ticker,
            StockInfo.organShortName,
            StockInfo.organName,
        )
        .filter(StockInfo.icbCode.in_(list(icb_codes)))
        .all()
    )
    mapping: MutableMapping[str, List[dict]] = defaultdict(list)
    for icb_code, ticker, short_name, org_name in rows:
        mapping[icb_code].append(
            {
                "symbol": ticker,
                "name": short_name or org_name,
            }
        )
    return mapping


def _fetch_stock_flows(
    session: Session, tickers: Iterable[str], trading_date
) -> Mapping[str, float]:
    ticker_list = list(tickers)
    if not ticker_list:
        return {}
    rows = (
        session.query(
            EodStock.ticker,
            (
                func.coalesce(EodStock.buyForeignValue, 0)
                - func.coalesce(EodStock.sellForeignValue, 0)
            ).label("net_value"),
        )
        .filter(EodStock.DateTime == trading_date)
        .filter(EodStock.ticker.in_(ticker_list))
        .all()
    )
    return {row.ticker: _to_billion(row.net_value or 0.0) for row in rows}


def _build_top_stocks(
    members: Sequence[dict],
    ticker_flows: Mapping[str, float],
    limit: int,
    isPossitive:bool # Kiểm tra xem giá trị dòng tiền nước ngoài ròng dương hay âm
) -> dict:
    ranked: List[dict] = []
    for meta in members:
        symbol = meta["symbol"]
        net_value = ticker_flows.get(symbol)
        if isPossitive:
            if net_value is None or net_value<0 or abs(net_value) < THREADSOLD_VALUE_STOCK_SECTOR:
                continue
        else:
            if net_value is None or net_value>0 or abs(net_value) < THREADSOLD_VALUE_STOCK_SECTOR:
                continue
        ranked.append(
            {
                "symbol": symbol,
                "name": meta.get("name"),
                "_net_raw": net_value,
                "net_value_billion": _round_half_up(net_value, 1),
            }
        )
    if isPossitive:
        ranked.sort(key=lambda item: item["_net_raw"], reverse=True)
    else:
        ranked.sort(key=lambda item: item["_net_raw"], reverse=False)
    result = []
    for idx, item in enumerate(ranked[:limit], start=1):
        result.append(
            {
                "symbol": item["symbol"],
                "name": item["name"],
                "net_value_billion": item["net_value_billion"],
                "rank": idx,
            }
        )

    return {"items": result}


def _select_top_sectors(
    sector_items_with_value: Sequence[Tuple[float, dict]],
    positive: bool,
    limit: int,
) -> dict:
    filtered = [
        (value, payload)
        for value, payload in sector_items_with_value
        if (value > EPSILON if positive else value < -EPSILON)
    ]
    
    filtered.sort(key=lambda item: abs(item[0]), reverse=True)
    return {"items": [payload for _, payload in filtered[:limit]]}


def _compute_breadth(values: Sequence[float]) -> dict:
    positives = sum(1 for v in values if v > EPSILON)
    negatives = sum(1 for v in values if v < -EPSILON)
    total = positives + negatives
    breadth_index = 0.0 if total == 0 else (positives - negatives) / total
    breadth_index = _round_half_up(breadth_index, 3)

    pos_abs = sum(abs(v) for v in values if v > EPSILON)
    neg_abs = sum(abs(v) for v in values if v < -EPSILON)
    total_abs = pos_abs + neg_abs
    if total_abs == 0:
        buy_share = sell_share = 0.0
    else:
        buy_share = pos_abs / total_abs
        sell_share = neg_abs / total_abs

    value_breadth_index = buy_share - sell_share

    buy_share_display = _round_half_up(buy_share, 2)
    sell_share_display = _round_half_up(sell_share, 2)
    value_bucket = _breadth_bucket(value_breadth_index)
    count_bucket = _breadth_bucket(breadth_index)
    breadth_bucket = value_bucket or count_bucket
    if breadth_bucket != count_bucket and value_bucket:
        breadth_bucket = value_bucket

    return {
        "count_buy": positives,
        "count_sell": negatives,
        "breadth_index": breadth_index,
        "breadth_bucket": breadth_bucket or "neutral",
        "buy_value_share": buy_share_display,
        "sell_value_share": sell_share_display,
        "value_breadth_bucket": value_bucket or "neutral",
    }


def _breadth_bucket(value: Optional[float]) -> Optional[str]:
    if value is None:
        return None
    if value <= -0.50:
        return "bearish"
    if -0.50 < value <= -0.20:
        return "slightly_bearish"
    if -0.20 < value < 0.20:
        return "neutral"
    if 0.20 <= value < 0.50:
        return "slightly_bullish"
    return "bullish"


def _direction_from_value(value: Optional[float]) -> str:
    if value is None or abs(value) < EPSILON:
        return "neutral"
    return "net_buy" if value > 0 else "net_sell"


def _magnitude_bucket(value: Optional[float]) -> str:
    if value is None:
        return "neutral"
    abs_value = abs(value)
    if abs_value < SIGNIFICANT_THRESHOLD_BILLION:
        return "neutral"
    if abs_value >= STRONG_THRESHOLD_BILLION:
        return "strongly_positive" if value > 0 else "strongly_negative"
    return "positive" if value > 0 else "negative"


def _to_billion(value: Optional[float]) -> float:
    if value is None:
        return 0.0
    return float(value) / FOREIGN_VALUE_SCALE


def _round_half_up(value: Optional[float], digits: int) -> float:
    if value is None:
        return 0.0
    quant = Decimal("1").scaleb(-digits)
    return float(Decimal(value).quantize(quant, rounding=ROUND_HALF_UP))


def _empty_payload(market_code: str) -> dict:
    return {
        "as_of": None,
        "market": market_code,
        "net_value_billion_total": 0.0,
        "dir_total": "neutral",
        "magnitude_bucket_total": "neutral",
        "top_buy_sectors": {"items": []},
        "top_sell_sectors": {"items": []},
        "foreign_breadth": {
            "count_buy": 0,
            "count_sell": 0,
            "breadth_index": 0.0,
            "breadth_bucket": "neutral",
            "buy_value_share": 0.0,
            "sell_value_share": 0.0,
            "value_breadth_bucket": "neutral",
        },
    }


if __name__ == "__main__":
    import json

    payload = build_foreign_flow_summary()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
