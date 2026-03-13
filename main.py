"""
Entry point：screener + notify 一鍵執行
"""

import logging
from screener import main as run_screener
from notify import notify_results

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

if __name__ == "__main__":
    df = run_screener()
    notify_results(df)
