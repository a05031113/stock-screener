"""
Finviz Pre-Filter
用 Finviz screener 做粗篩，取代 Wikipedia 爬蟲
篩選條件：美股、價格 > $5、有基本量能、技術面初步符合
"""

import logging
import time
import pandas as pd
from finvizfinance.screener.overview import Overview

logger = logging.getLogger(__name__)


def _run_finviz_screen(filters: dict, description: str) -> list[str]:
    """執行單次 Finviz screener 並回傳 ticker list"""
    try:
        screener = Overview()
        screener.set_filter(filters_dict=filters)
        df = screener.screener_view()
        if df is None or df.empty:
            logger.warning(f"Finviz {description}: no results")
            return []
        tickers = df["Ticker"].tolist()
        logger.info(f"Finviz {description}: {len(tickers)} tickers")
        return tickers
    except Exception as e:
        logger.error(f"Finviz {description} failed: {e}")
        return []


def get_prefiltered_universe() -> list[str]:
    """
    用多組 Finviz filter 取得候選股票，合併去重。
    分成兩組篩選以捕捉不同階段的動能股：
      1. Stage 2 起步型：均線開始多頭排列
      2. 底部突破型：從低點回升 + 放量
    """

    # ── Filter A: Stage 2 起步型 ──
    # 價格站上 SMA50，SMA50 > SMA200，相對量高
    stage2_filters = {
        "Price": "Over $5",
        "Average Volume": "Over 200K",
        "Relative Volume": "Over 1.5",
        "50-Day Simple Moving Average": "Price above SMA50",
        "200-Day Simple Moving Average": "Price above SMA200",
        "Current Volume": "Over 200K",
    }

    # ── Filter B: 底部突破型 ──
    # 從 52 週低點回升 + 量能放大
    base_breakout_filters = {
        "Price": "Over $5",
        "Average Volume": "Over 200K",
        "Relative Volume": "Over 2",
        "52-Week High/Low": "20% or more above Low",
    }

    # 執行兩組篩選
    stage2_tickers = _run_finviz_screen(stage2_filters, "Stage 2")
    time.sleep(2)  # Finviz rate limit between requests
    base_tickers = _run_finviz_screen(base_breakout_filters, "Base Breakout")

    # 合併去重（保序）
    all_tickers = list(dict.fromkeys(stage2_tickers + base_tickers))
    logger.info(f"Total pre-filtered universe: {len(all_tickers)} unique tickers")
    return all_tickers


def get_weekly_up_universe() -> tuple[list[str], dict]:
    """
    Finviz 預篩：本週上漲 + 月漲的股票
    回傳 (ticker list, metadata dict)
    metadata: {ticker: {sector, industry, market_cap_label}}
    """
    filters = {
        "Price": "Over $5",
        "Performance": "Week Up",
        "Performance 2": "Month Up",
    }
    try:
        screener = Overview()
        screener.set_filter(filters_dict=filters)
        df = screener.screener_view()
        if df is None or df.empty:
            logger.warning("Finviz Weekly Up: no results")
            return [], {}

        tickers = df["Ticker"].tolist()
        logger.info(f"Finviz Weekly Up: {len(tickers)} tickers")

        # 解析 metadata
        metadata = {}
        for _, row in df.iterrows():
            mc = row.get("Market Cap")
            metadata[row["Ticker"]] = {
                "sector": row.get("Sector", ""),
                "industry": row.get("Industry", ""),
                "market_cap": mc if pd.notna(mc) else 0,
            }
        return tickers, metadata

    except Exception as e:
        logger.error(f"Finviz Weekly Up failed: {e}")
        return [], {}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tickers = get_prefiltered_universe()
    print(f"Universe size: {len(tickers)}")
    print(tickers[:20])
