"""
Entry point：
  1. Finviz pre-filter → technical + fundamental scoring → CSV
  2. Finviz weekly-up → 週 K 連三漲篩選 → CSV
結果由 GitHub Action commit 到 output/；
敘事發酵評估與 Telegram 通知由下游雲端 routine + report-notify workflow 承接。
"""

import logging
from screener import main as run_screener, run_weekly_streak_screener
from universe import get_weekly_up_universe

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

if __name__ == "__main__":
    # 1. 原有的技術+基本面計分
    run_screener()

    # 2. 週 K 連三漲（個股 + ETF 分開存）
    streak_tickers, metadata = get_weekly_up_universe()
    if streak_tickers:
        run_weekly_streak_screener(streak_tickers, metadata)
    else:
        logging.getLogger(__name__).warning("No weekly-up tickers from Finviz")
