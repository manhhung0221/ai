"""
Utilities to compose a market summary for key Vietnamese indices using
end-of-day data sourced from :class:`Model.model_eod.EodStock`.

Typical usage
-------------
>>> from Model.market_summary import build_market_summary
>>> summary = build_market_summary()
>>> print(summary["vnindex"]["index_value"])
"""
from __future__ import annotations

from collections import OrderedDict
from statistics import mean, pstdev
from typing import Dict, Mapping, MutableMapping, Optional, Sequence, Tuple
import math
from Model.model_eod import EodStock, get_EodStock

TOTAL_VALUE_SCALE = 1_000_000_000  # convert raw value (VND) to billions
TOTAL_VOLUME_SCALE = 1_000_000     # convert raw volume to millions
ROUND_DIGITS = 2
ROLLING_WINDOW = 20

# Mapping between the public-facing index key and the ticker stored in eod.eod_stock_v2.
DEFAULT_INDEX_TICKERS: Mapping[str, str] = OrderedDict(
    [
        ("vnindex", "VNINDEX"),
        ("vn30", "VN30"),
        ("hnx", "HNXINDEX"),
        ("upcom", "UPINDEX"),  # provided by user
    ]
)

MarketSummary = Dict[str, Dict[str, Optional[float]]]


def build_market_summary(
    index_tickers: Optional[Mapping[str, str]] = None,
    rolling_window: int = ROLLING_WINDOW,
) -> MarketSummary:
    """
    Build the market summary dictionary for the requested indices.

    Parameters
    ----------
    index_tickers:
        Optional mapping of logical names to tickers in eod_stock_v2. Defaults to
        :data:`DEFAULT_INDEX_TICKERS`.
    rolling_window:
        Number of recent sessions used to calculate the rolling average/std-dev of total value.

    Returns
    -------
    dict
        Nested dictionary keyed by logical index names.
    """
    if rolling_window < 2:
        raise ValueError("rolling_window must be at least 2 to compute meaningful stats")

    tickers = index_tickers or DEFAULT_INDEX_TICKERS
    summary: MutableMapping[str, Dict[str, Optional[float]]] = OrderedDict()

    with get_EodStock() as session:
        for alias, ticker in tickers.items():
            rows = (
                session.query(EodStock)
                .filter(EodStock.ticker == ticker)
                .order_by(EodStock.DateTime.desc())
                .limit(rolling_window)
                .all()
            )
            summary[alias] = _summarize_rows(rows)

    return dict(summary)
def _pct_vs_avg(val, avg):
    if val is None or avg in (None, 0):
        return None
    return round((val - avg) / avg * 100, 2)

def _z_score(val, avg, std):
    if val is None or avg is None or std in (None, 0):
        return None
    return round((val - avg) / std, 2)

def _sigma_bucket(z: float | None) -> str | None:
    if z is None or math.isnan(z):
        return None
    if z <= -2: return "rất thấp (≤ -2σ)"
    if -2 < z <= -1: return "thấp (-2σ ~ -1σ)"
    if -1 < z < 1: return "trung tính (-1σ ~ +1σ)"
    if 1 <= z < 2: return "cao (+1σ ~ +2σ)"
    return "rất cao (≥ +2σ)"

def _summarize_rows(rows: Sequence[EodStock]) -> Dict[str, Optional[float]]:
    if not rows:
        return _empty_summary()

    latest = rows[0]
    previous = rows[1] if len(rows) > 1 else None

    latest_close = getattr(latest, "Close", None)
    previous_close = getattr(previous, "Close", None) if previous else None

    change_points, change_percent = _calc_change(latest_close, previous_close)

    total_values = [float(row.totalValue) for row in rows if row.totalValue is not None]
    avg_value_raw, std_value_raw = _compute_value_stats(total_values)
    z = _z_score(_scale_value(getattr(latest, "totalValue", None), 
                            TOTAL_VALUE_SCALE), _scale_value(avg_value_raw, TOTAL_VALUE_SCALE), 
                            _scale_value(std_value_raw, TOTAL_VALUE_SCALE)
                        )
    return {
        "index_value": _round_or_none(latest_close),
        "change_points_vs_prev_day": change_points,
        "change_percent_vs_prev_day": change_percent,
        "total_value_billion": _scale_value(getattr(latest, "totalValue", None), TOTAL_VALUE_SCALE),
        "total_volume_million": _scale_value(getattr(latest, "Volume", None), TOTAL_VOLUME_SCALE),
        "avg_20d_value_billion": _scale_value(avg_value_raw, TOTAL_VALUE_SCALE),
        "std_20d_value_billion": _scale_value(std_value_raw, TOTAL_VALUE_SCALE),
        "z_score_liquidity": z,                           # (val-avg)/std
        "z_bucket": _sigma_bucket(z)                     # nhãn cấp độ đột biến
    }


def _empty_summary() -> Dict[str, Optional[float]]:
    return {
        "index_value": None,
        "change_points_vs_prev_day": None,
        "change_percent_vs_prev_day": None,
        "total_value_billion": None,
        "total_volume_million": None,
        "avg_20d_value_billion": None,
        "std_20d_value_billion": None,
        "z_score_liquidity":None,
        "z_bucket":None
    }


def _calc_change(
    latest_close: Optional[float],
    previous_close: Optional[float],
) -> Tuple[Optional[float], Optional[float]]:
    if latest_close is None or previous_close is None or previous_close == 0:
        return None, None

    diff = float(latest_close) - float(previous_close)
    pct = (diff / float(previous_close)) * 100
    return round(diff, ROUND_DIGITS), round(pct, ROUND_DIGITS)


def _compute_value_stats(
    values: Sequence[float],
) -> Tuple[Optional[float], Optional[float]]:
    if not values:
        return None, None

    avg = mean(values)
    std = pstdev(values) if len(values) > 1 else None
    return avg, std


def _scale_value(value: Optional[float], scale: float) -> Optional[float]:
    if value is None:
        return None
    return round(float(value) / scale, ROUND_DIGITS)


def _round_or_none(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    return round(float(value), ROUND_DIGITS)


if __name__ == "__main__":
    import json

    result = build_market_summary()
    print(json.dumps(result, ensure_ascii=False, indent=4))
