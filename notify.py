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
    rev_growth = row.get("revenue_growth")
    rev_str = f"{rev_growth:.0%}" if pd.notna(rev_growth) else "N/A"

    gm = row.get("gross_margins")
    gm_str = f"{gm:.0%}" if pd.notna(gm) else "N/A"

    sector = row.get("sector", "")
    sector_str = f" | {sector}" if sector else ""
    repeat_str = " [連續上榜]" if row.get("repeat") else ""

    return (
        f"<b>${row['ticker']}</b> | 總分 {row['total_score']}{sector_str}{repeat_str}\n"
        f"  ${row['price']} | 相對量 {row['rel_vol']}x\n"
        f"  技術 {row['tech_score']}/12 | 基本面 {row['fund_score']}/7 | VCP +{row['vol_bonus']}\n"
        f"  1W {row['return_1w']} | 1M {row['return_1m']} | 3M {row['return_3m']}\n"
        f"  營收 {rev_str} | 毛利率 {gm_str} | RS {row['rs_vs_spy']}\n"
        f"  訊號: {row['tech_signals']}\n"
    )


def build_summary(df: pd.DataFrame) -> list[str]:
    """
    把候選名單切成多則訊息（Telegram 單則上限 4096 字元）
    """
    date_str = datetime.now().strftime("%Y/%m/%d")
    header = (
        f"<b>每週早期動能掃描 v2</b>\n"
        f"{date_str} | 共 {len(df)} 檔候選\n"
        f"技術面 ≥8/12 + 基本面 ≥4/7\n"
        f"{'─' * 30}\n"
    )

    messages = []
    current = header

    for _, row in df.iterrows():
        block = format_candidate(row)
        if len(current) + len(block) > 3800:
            messages.append(current)
            current = block
        else:
            current += block

    # 結尾提醒
    footer = (
        f"\n{'─' * 30}\n"
        f"以上為技術+基本面自動篩選\n"
        f"請手動確認：業務故事、earnings call、機構持股趨勢"
    )

    if len(current) + len(footer) > 3800:
        messages.append(current)
        messages.append(footer)
    else:
        messages.append(current + footer)

    return messages


def format_streak_candidate(row: pd.Series) -> str:
    """週 K 連漲候選股的格式"""
    sector = row.get("sector", "")
    sector_str = f" | {sector}" if sector else ""
    repeat_str = " [連續上榜]" if row.get("repeat") else ""

    return (
        f"<b>${row['ticker']}</b> ${row['price']}"
        f" | 三週 {row['total_gain']}{sector_str}{repeat_str}\n"
        f"  W: {row['w1']} | {row['w2']} | {row['w3']}\n"
        f"  M: {row['m1']} | {row['m2']}\n"
    )


def build_streak_summary(df: pd.DataFrame, title: str) -> list[str]:
    """週 K 連漲結果，按市值分類切成多則訊息"""
    date_str = datetime.now().strftime("%Y/%m/%d")
    header = (
        f"<b>{title}</b>\n"
        f"{date_str} | 共 {len(df)} 檔\n"
        f"{'─' * 30}\n"
    )

    messages = []
    current = header

    # 如果有 cap_label 欄位，按市值分組
    has_cap = "cap_label" in df.columns
    if has_cap:
        cap_order = ["Large", "Mid", "Small"]
        for cap in cap_order:
            group = df[df["cap_label"] == cap]
            if group.empty:
                continue
            cap_header = f"\n<b>[{cap} Cap] {len(group)} 檔</b>\n"
            if len(current) + len(cap_header) > 3800:
                messages.append(current)
                current = cap_header
            else:
                current += cap_header

            for _, row in group.iterrows():
                block = format_streak_candidate(row)
                if len(current) + len(block) > 3800:
                    messages.append(current)
                    current = block
                else:
                    current += block
    else:
        for _, row in df.iterrows():
            block = format_streak_candidate(row)
            if len(current) + len(block) > 3800:
                messages.append(current)
                current = block
            else:
                current += block

    if current:
        messages.append(current)

    return messages


def _top_per_cap(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """每個市值分類取前 n 檔（按三週漲幅排序）"""
    if "cap_label" not in df.columns:
        return df.head(n * 3)
    groups = []
    for cap in ["Large", "Mid", "Small"]:
        group = df[df["cap_label"] == cap].head(n)
        groups.append(group)
    return pd.concat(groups, ignore_index=True)


def notify_streak_results(stocks_df: pd.DataFrame, etfs_df: pd.DataFrame) -> None:
    """分別發送個股與 ETF 的週 K 連漲結果"""
    if stocks_df.empty and etfs_df.empty:
        send_message("本週無連三週上漲的股票。")
        return

    # 個股：每個市值分類取前 10（最多 30）
    if not stocks_df.empty:
        top_stocks = _top_per_cap(stocks_df, n=10)
        messages = build_streak_summary(top_stocks, "月K連二 + 週K連三 - 個股")
        for i, msg in enumerate(messages, 1):
            logger.info(f"Sending streak stocks {i}/{len(messages)}")
            if not send_message(msg):
                logger.error(f"Failed to send streak stocks message {i}")
                break

    # ETF（前 20）
    if not etfs_df.empty:
        messages = build_streak_summary(etfs_df.head(20), "月K連二 + 週K連三 - ETF 族群趨勢")
        for i, msg in enumerate(messages, 1):
            logger.info(f"Sending streak ETFs {i}/{len(messages)}")
            if not send_message(msg):
                logger.error(f"Failed to send streak ETFs message {i}")
                break


def notify_results(df: pd.DataFrame) -> None:
    if df.empty:
        send_message("本週動能掃描完成，<b>無候選股票</b>。\n市場可能整體偏弱或條件過嚴。")
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
