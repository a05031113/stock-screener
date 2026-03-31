"""
Entry point：
  1. Finviz pre-filter → technical + fundamental scoring → Telegram
  2. Finviz weekly-up → 週 K 連三漲篩選 → Telegram
"""

import logging
from screener import main as run_screener, run_weekly_streak_screener
from universe import get_weekly_up_universe
from notify import notify_results, notify_streak_results

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

if __name__ == "__main__":
    # 1. 原有的技術+基本面計分
    df = run_screener()
    notify_results(df)

    # 2. 週 K 連三漲（個股 + ETF 分開發）
    streak_tickers, metadata = get_weekly_up_universe()
    if streak_tickers:
        stocks_df, etfs_df = run_weekly_streak_screener(streak_tickers, metadata)
        notify_streak_results(stocks_df, etfs_df)
    else:
        logging.getLogger(__name__).warning("No weekly-up tickers from Finviz")
