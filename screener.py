"""
Weekly Momentum Stock Screener
策略：技術面過濾 → 輸出候選名單 → 手動確認基本面

條件說明：
  突破型 (Breakout)：接近 52 週高點 + 近期放量 + 月線漲幅合理
  蓄力型 (Coiling) ：底部橫盤後突然放量，均線剛開始多頭排列
"""

import yfinance as yf
import pandas as pd
import numpy as np
import logging
import time
from datetime import datetime
from pathlib import Path
from universe import get_universe

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ── 指標計算 ──────────────────────────────────────────────────────────────

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    close  = df["Close"]
    volume = df["Volume"]

    # 移動平均
    df["MA5"]  = close.rolling(5).mean()
    df["MA10"] = close.rolling(10).mean()
    df["MA20"] = close.rolling(20).mean()
    df["MA60"] = close.rolling(60).mean()

    # 相對成交量
    df["AvgVol20"] = volume.rolling(20).mean()
    df["RelVol"]   = volume / df["AvgVol20"]

    # 漲跌幅
    df["Return_1W"] = close.pct_change(5)
    df["Return_1M"] = close.pct_change(21)
    df["Return_3M"] = close.pct_change(63)

    # 52 週指標
    df["High_52W"]       = close.rolling(252).max()
    df["Low_52W"]        = close.rolling(252).min()
    df["Pct_From_High"]  = (close - df["High_52W"]) / df["High_52W"]
    df["Pct_From_Low"]   = (close - df["Low_52W"])  / df["Low_52W"]

    # 價格波動收縮（布林帶寬度，用來找蓄力型）
    df["BB_Mid"]   = close.rolling(20).mean()
    df["BB_Std"]   = close.rolling(20).std()
    df["BB_Width"] = (df["BB_Std"] * 2) / df["BB_Mid"]   # 越小 = 越壓縮

    return df


# ── Screener 條件 ─────────────────────────────────────────────────────────

def check_breakout(row: pd.Series, price: float) -> tuple[bool, int, list]:
    """突破型：接近高點 + 放量 + 月線剛起漲"""
    checks = {
        "price_ok":         price > 10,
        "near_52w_high":    row["Pct_From_High"] > -0.12,   # 距高點 12% 內
        "return_1m_ok":     0.07 < row["Return_1M"] < 0.50, # 月漲 7~50%
        "return_3m_ok":     row["Return_3M"] < 1.50,        # 沒有已經暴漲太多
        "rel_vol_high":     row["RelVol"] > 1.5,            # 近日量異常
        "ma_bullish":       row["MA5"] > row["MA20"],        # 均線多頭
    }
    passed  = sum(checks.values())
    labels  = [k for k, v in checks.items() if v]
    return passed >= 5, passed, labels


def check_coiling(row: pd.Series, price: float) -> tuple[bool, int, list]:
    """蓄力型：底部橫盤壓縮 + 剛開始放量突破"""
    checks = {
        "price_ok":         price > 5,
        "pct_from_low":     0.10 < row["Pct_From_Low"] < 0.60,  # 離低點 10~60%
        "return_3m_flat":   -0.10 < row["Return_3M"] < 0.30,    # 3 個月沒怎麼動
        "bb_compressed":    row["BB_Width"] < 0.15,              # 波動收縮
        "rel_vol_surge":    row["RelVol"] > 2.0,                 # 放量明顯
        "ma5_cross_ma20":   row["MA5"] > row["MA20"],            # 剛穿越
        "price_above_ma10": price > row["MA10"],
    }
    passed  = sum(checks.values())
    labels  = [k for k, v in checks.items() if v]
    return passed >= 5, passed, labels


# ── 主流程 ────────────────────────────────────────────────────────────────

def screen_ticker(ticker: str) -> dict | None:
    try:
        df = yf.Ticker(ticker).history(period="2y")

        if len(df) < 120:  # 資料不足
            return None

        df = compute_indicators(df)
        row   = df.iloc[-1]
        price = float(row["Close"])

        if price <= 0 or np.isnan(price):
            return None

        is_breakout, b_score, b_labels = check_breakout(row, price)
        is_coiling,  c_score, c_labels = check_coiling(row, price)

        if not (is_breakout or is_coiling):
            return None

        pattern = []
        if is_breakout: pattern.append("Breakout")
        if is_coiling:  pattern.append("Coiling")

        return {
            "ticker":       ticker,
            "price":        round(price, 2),
            "rel_vol":      round(float(row["RelVol"]), 2),
            "return_1w":    f"{row['Return_1W']:.1%}",
            "return_1m":    f"{row['Return_1M']:.1%}",
            "return_3m":    f"{row['Return_3M']:.1%}",
            "pct_from_high":f"{row['Pct_From_High']:.1%}",
            "pct_from_low": f"{row['Pct_From_Low']:.1%}",
            "bb_width":     round(float(row["BB_Width"]), 3),
            "pattern":      "+".join(pattern),
            "score":        max(b_score, c_score),
            "signals":      ", ".join(sorted(set(b_labels + c_labels))),
        }

    except (KeyError, ValueError, IndexError) as e:
        logger.debug(f"Skip {ticker}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error for {ticker}: {e}")
        return None


def run_screener(tickers: list[str], batch_delay: float = 0.3) -> pd.DataFrame:
    candidates = []
    total = len(tickers)

    logger.info(f"Screening {total} tickers...")

    for i, ticker in enumerate(tickers, 1):
        result = screen_ticker(ticker)
        if result:
            candidates.append(result)
            logger.info(f"[{i}/{total}] ✅ {ticker} | {result['pattern']} | score={result['score']}")
        else:
            if i % 100 == 0:
                logger.info(f"[{i}/{total}] processed...")

        # Rate limit 保護
        time.sleep(batch_delay)

    df = pd.DataFrame(candidates)
    if not df.empty:
        df = df.sort_values(["score", "rel_vol"], ascending=False)

    return df


def save_results(df: pd.DataFrame) -> Path:
    date_str  = datetime.now().strftime("%Y%m%d")
    csv_path  = OUTPUT_DIR / f"candidates_{date_str}.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved {len(df)} candidates → {csv_path}")
    return csv_path


def main() -> pd.DataFrame:
    tickers = get_universe(include_russell=True)
    df      = run_screener(tickers)

    if df.empty:
        logger.warning("No candidates found this week.")
        return df

    csv_path = save_results(df)

    # 印出 Top 20
    logger.info("\n=== Top 20 Candidates ===")
    print(df.head(20).to_string(index=False))

    return df


if __name__ == "__main__":
    main()
