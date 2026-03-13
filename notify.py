"""
Telegram 通知模組
把 screener 結果整理成可讀訊息發送
"""

import os
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def send_message(text: str) -> bool:
    token   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return False

    url  = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": "HTML",
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(url, data=data, timeout=10)
            resp.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429 and attempt < MAX_RETRIES:
                wait = 2 ** attempt
                logger.warning(f"Rate limited, retrying in {wait}s (attempt {attempt}/{MAX_RETRIES})")
                import time
                time.sleep(wait)
                continue
            logger.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    return False


def format_candidate(row: pd.Series) -> str:
    """單一候選股的格式"""
    pattern_emoji = {
        "Breakout":         "🚀",
        "Coiling":          "🔋",
        "Breakout+Coiling": "💥",
    }
    emoji = pattern_emoji.get(row["pattern"], "📈")

    return (
        f"{emoji} <b>${row['ticker']}</b> | {row['pattern']}\n"
        f"   價格: ${row['price']} | 相對量: {row['rel_vol']}x\n"
        f"   1W: {row['return_1w']} | 1M: {row['return_1m']} | 3M: {row['return_3m']}\n"
        f"   距高點: {row['pct_from_high']} | 訊號: {row['signals']}\n"
    )


def build_summary(df: pd.DataFrame) -> list[str]:
    """
    把候選名單切成多則訊息（Telegram 單則上限 4096 字元）
    """
    date_str = datetime.now().strftime("%Y/%m/%d")
    header   = (
        f"📊 <b>每週動能掃描結果</b>\n"
        f"🗓 {date_str} | 共 {len(df)} 檔候選\n"
        f"{'─' * 30}\n"
    )

    messages = []
    current  = header

    # 分類顯示
    for pattern in ["Breakout+Coiling", "Breakout", "Coiling"]:
        subset = df[df["pattern"] == pattern]
        if subset.empty:
            continue

        section_title = f"\n<b>── {pattern} ({len(subset)}檔) ──</b>\n"
        if len(current) + len(section_title) > 3800:
            messages.append(current)
            current = section_title
        else:
            current += section_title

        for _, row in subset.iterrows():
            block = format_candidate(row)
            if len(current) + len(block) > 3800:
                messages.append(current)
                current = block
            else:
                current += block

    # 結尾提醒
    footer = (
        f"\n{'─' * 30}\n"
        f"⚠️ 以上僅為技術面初篩\n"
        f"📋 請手動確認：Earnings transcript、業務邏輯、機構持股變化"
    )

    if len(current) + len(footer) > 3800:
        messages.append(current)
        messages.append(footer)
    else:
        messages.append(current + footer)

    return messages


def notify_results(df: pd.DataFrame) -> None:
    if df.empty:
        send_message("📊 本週動能掃描完成，<b>無候選股票</b>。\n市場可能整體偏弱或條件過嚴。")
        return

    # 只取 Top 20 避免訊息太多
    df_top = df.head(20)
    messages = build_summary(df_top)

    for i, msg in enumerate(messages, 1):
        logger.info(f"Sending message {i}/{len(messages)}")
        success = send_message(msg)
        if not success:
            logger.error(f"Failed to send message {i}")
            break

    logger.info(f"Notification sent: {len(messages)} messages")


if __name__ == "__main__":
    # 測試用：讀最新的 CSV 來發送
    import sys
    logging.basicConfig(level=logging.INFO)

    output_dir = Path("output")
    csv_files  = sorted(output_dir.glob("candidates_*.csv"), reverse=True)

    if not csv_files:
        print("No CSV files found in output/")
        sys.exit(1)

    latest = csv_files[0]
    print(f"Loading {latest}")
    df = pd.read_csv(latest)
    notify_results(df)
