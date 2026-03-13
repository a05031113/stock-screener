"""
Entry point：Finviz pre-filter → technical + fundamental scoring → Telegram
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
