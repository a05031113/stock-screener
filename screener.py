"""
Early Momentum Stock Screener v2
策略：Finviz 粗篩 → 技術面計分(12) + 基本面計分(7) → 候選名單

技術面（滿分 12 + 波動加分 2）：
  A. Base Formation (3)：底部結構完整
  B. Stage 2 Entry  (4)：均線多頭排列剛形成
  C. Volume         (3)：量能異動
  D. Relative Str.  (2)：相對大盤強勢

基本面（滿分 7）：
  A. 營收動能 (3)：成長 + 加速
  B. 獲利品質 (3)：EPS beat + 毛利 + 正 EPS
  C. 機構動向 (1)：機構有在買
"""

import yfinance as yf
import pandas as pd
import numpy as np
import logging
import time
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# yfinance 對已下市股票會印 ERROR，屬預期情況
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

TECH_THRESHOLD = 8   # /12
FUND_THRESHOLD = 4   # /7


# ── ATR 計算 ──────────────────────────────────────────────────────────────

def _atr(df: pd.DataFrame, period: int) -> pd.Series:
    high  = df["High"]
    low   = df["Low"]
    close = df["Close"]
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


# ── 指標計算 ──────────────────────────────────────────────────────────────

def compute_indicators(df: pd.DataFrame, spy_close: pd.Series | None = None) -> pd.DataFrame:
    df = df.copy()
    close  = df["Close"]
    volume = df["Volume"]

    # ── 移動平均 ──
    df["MA50"]  = close.rolling(50).mean()
    df["MA150"] = close.rolling(150).mean()
    df["MA200"] = close.rolling(200).mean()

    # MA150 斜率（近 20 日變化率）
    ma150 = df["MA150"]
    df["MA150_Slope"] = (ma150 - ma150.shift(20)) / ma150.shift(20)

    # MA50 穿越 MA150 的天數（找最近一次 golden cross）
    cross = (df["MA50"] > df["MA150"]) & (df["MA50"].shift(1) <= df["MA150"].shift(1))
    if cross.any():
        last_cross_idx = cross[cross].index[-1]
        df["MA50_Cross_Days"] = (df.index[-1] - last_cross_idx).days
    else:
        df["MA50_Cross_Days"] = 999

    # ── 52 週指標 ──
    df["High_52W"]      = close.rolling(252).max()
    df["Low_52W"]       = close.rolling(252).min()
    df["Pct_From_High"] = (close - df["High_52W"]) / df["High_52W"]
    df["Pct_From_Low"]  = (close - df["Low_52W"])  / df["Low_52W"]

    # 6 個月 high-low range（底部結構緊密度）
    high_6m = close.rolling(126).max()
    low_6m  = close.rolling(126).min()
    df["Range_6M"] = (high_6m - low_6m) / low_6m.replace(0, 1)

    # ── 量能 ──
    df["AvgVol5"]  = volume.rolling(5).mean()
    df["AvgVol50"] = volume.rolling(50).mean()
    df["RelVol"]   = df["AvgVol5"] / df["AvgVol50"].replace(0, 1)

    # 上漲日 vs 下跌日的成交量比（近 20 日）
    price_up = close > close.shift(1)
    up_vol   = volume.where(price_up, 0).rolling(20).sum()
    down_vol = volume.where(~price_up, 0).rolling(20).sum()
    df["UpDownVolRatio"] = up_vol / down_vol.replace(0, 1)

    # 最近 5 日中最大量那天是否為上漲日
    if len(df) >= 5:
        recent = df.iloc[-5:]
        max_vol_idx = recent["Volume"].idxmax()
        df["LastVolSurgeUp"] = close.loc[max_vol_idx] > close.shift(1).loc[max_vol_idx]
    else:
        df["LastVolSurgeUp"] = False

    # ── 漲跌幅 ──
    df["Return_1W"] = close.pct_change(5)
    df["Return_1M"] = close.pct_change(21)
    df["Return_3M"] = close.pct_change(63)

    # ── 波動收縮 ──
    df["BB_Width"]      = (close.rolling(20).std() * 2) / close.rolling(20).mean()
    df["BB_Percentile"] = df["BB_Width"].rolling(126).rank(pct=True)
    df["ATR_14"]        = _atr(df, 14)
    df["ATR_60"]        = _atr(df, 60)
    df["ATR_Ratio"]     = df["ATR_14"] / df["ATR_60"].replace(0, 1)

    # ── Relative Strength vs SPY ──
    if spy_close is not None and len(spy_close) >= 63:
        spy_aligned = spy_close.reindex(close.index, method="ffill")
        stock_ret_3m = close.pct_change(63)
        spy_ret_3m   = spy_aligned.pct_change(63)
        df["RS_vs_SPY"] = stock_ret_3m - spy_ret_3m

        rs_line = close / spy_aligned.replace(0, 1)
        df["RS_Line_Slope"] = (rs_line - rs_line.shift(20)) / rs_line.shift(20).replace(0, 1)
    else:
        df["RS_vs_SPY"]     = 0.0
        df["RS_Line_Slope"] = 0.0

    return df


# ── 技術面計分 ────────────────────────────────────────────────────────────

def score_technical(row: pd.Series, price: float) -> tuple[int, list[str]]:
    """
    技術面計分（滿分 12）
    A. Base Formation (3)  B. Stage 2 Entry (4)
    C. Volume (3)          D. Relative Strength (2)
    """
    checks = {
        # A. Base Formation
        "base_tight":        row["Range_6M"] < 0.40,
        "above_low_20_80":   0.20 < row["Pct_From_Low"] < 0.80,
        "within_high_75":    row["Pct_From_High"] > -0.25,

        # B. Stage 2 Entry
        "price_above_ma150": price > row["MA150"],
        "ma150_rising":      row["MA150_Slope"] > 0,
        "ma_aligned":        row["MA50"] > row["MA150"] > row["MA200"],
        "ma50_cross_recent": row["MA50_Cross_Days"] <= 30,

        # C. Volume Accumulation
        "rel_vol_high":      row["RelVol"] > 1.5,
        "up_down_vol":       row["UpDownVolRatio"] > 1.2,
        "last_vol_surge_up": bool(row["LastVolSurgeUp"]),

        # D. Relative Strength
        "rs_vs_spy":         row["RS_vs_SPY"] > 0,
        "rs_line_rising":    row["RS_Line_Slope"] > 0,
    }

    score  = sum(checks.values())
    labels = [k for k, v in checks.items() if v]
    return score, labels


def score_volatility_bonus(row: pd.Series) -> tuple[int, list[str]]:
    """波動收縮加分（滿分 2），不設門檻"""
    checks = {
        "bb_compressed":  row["BB_Percentile"] < 0.25,
        "atr_contracted": row["ATR_Ratio"] < 0.8,
    }
    score  = sum(checks.values())
    labels = [k for k, v in checks.items() if v]
    return score, labels


# ── 基本面資料取得 ────────────────────────────────────────────────────────

def fetch_fundamentals(ticker_obj: yf.Ticker) -> dict:
    """從 yfinance 取得基本面資料，取不到的欄位填 None"""
    info: dict = {}

    try:
        raw = ticker_obj.info
        info["gross_margins"]   = raw.get("grossMargins")
        info["revenue_growth"]  = raw.get("revenueGrowth")
        info["earnings_growth"] = raw.get("earningsGrowth")
    except Exception:
        pass

    # EPS Surprise
    try:
        earnings = ticker_obj.get_earnings_dates(limit=8)
        if earnings is not None and not earnings.empty:
            if "Reported EPS" in earnings.columns and "EPS Estimate" in earnings.columns:
                recent = earnings.dropna(subset=["Reported EPS", "EPS Estimate"]).head(1)
                if not recent.empty:
                    info["eps_actual"]   = float(recent["Reported EPS"].iloc[0])
                    info["eps_estimate"] = float(recent["EPS Estimate"].iloc[0])
    except Exception:
        pass

    # 機構持股數量
    try:
        holders = ticker_obj.institutional_holders
        if holders is not None and not holders.empty:
            info["inst_holder_count"] = len(holders)
    except Exception:
        pass

    return info


# ── 基本面計分 ────────────────────────────────────────────────────────────

def score_fundamental(info: dict) -> tuple[int, list[str]]:
    """
    基本面計分（滿分 7）
    A. 營收動能 (3)  B. 獲利品質 (3)  C. 機構動向 (1)
    """
    checks: dict[str, bool] = {}

    # A. 營收動能
    rev_growth  = info.get("revenue_growth")
    earn_growth = info.get("earnings_growth")

    checks["revenue_yoy_10pct"] = rev_growth is not None and rev_growth > 0.10
    checks["earnings_accelerating"] = (
        earn_growth is not None and rev_growth is not None
        and earn_growth > rev_growth and earn_growth > 0
    )
    checks["revenue_positive"] = rev_growth is not None and rev_growth > 0

    # B. 獲利品質
    eps_actual   = info.get("eps_actual")
    eps_estimate = info.get("eps_estimate")

    checks["eps_beat"] = (
        eps_actual is not None and eps_estimate is not None
        and eps_estimate != 0 and eps_actual > eps_estimate
    )
    checks["gross_margin_healthy"] = (
        info.get("gross_margins") is not None and info["gross_margins"] > 0.30
    )
    checks["eps_positive"] = eps_actual is not None and eps_actual > 0

    # C. 機構動向
    checks["inst_holders"] = info.get("inst_holder_count", 0) >= 5

    score  = sum(checks.values())
    labels = [k for k, v in checks.items() if v]
    return score, labels


# ── 主流程 ────────────────────────────────────────────────────────────────

def screen_ticker(ticker: str, spy_close: pd.Series | None = None) -> dict | None:
    try:
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(period="2y")

        if len(df) < 252:  # 需要至少 1 年完整資料
            return None

        df = compute_indicators(df, spy_close)
        row   = df.iloc[-1]
        price = float(row["Close"])

        if price <= 0 or np.isnan(price):
            return None

        # Layer 1: 技術面
        tech_score, tech_labels = score_technical(row, price)
        vol_bonus, vol_labels   = score_volatility_bonus(row)

        if tech_score < TECH_THRESHOLD:
            return None

        # Layer 2: 基本面（只有技術面通過才跑，節省 API calls）
        fundamentals = fetch_fundamentals(ticker_obj)
        fund_score, fund_labels = score_fundamental(fundamentals)

        if fund_score < FUND_THRESHOLD:
            return None

        total_score = tech_score + vol_bonus + fund_score

        return {
            "ticker":         ticker,
            "price":          round(price, 2),
            "tech_score":     tech_score,
            "fund_score":     fund_score,
            "vol_bonus":      vol_bonus,
            "total_score":    total_score,
            "rel_vol":        round(float(row["RelVol"]), 2),
            "return_1w":      f"{row['Return_1W']:.1%}",
            "return_1m":      f"{row['Return_1M']:.1%}",
            "return_3m":      f"{row['Return_3M']:.1%}",
            "pct_from_high":  f"{row['Pct_From_High']:.1%}",
            "rs_vs_spy":      round(float(row["RS_vs_SPY"]), 3),
            "revenue_growth": fundamentals.get("revenue_growth"),
            "gross_margins":  fundamentals.get("gross_margins"),
            "tech_signals":   ", ".join(tech_labels + vol_labels),
            "fund_signals":   ", ".join(fund_labels),
        }

    except (KeyError, ValueError, IndexError) as e:
        logger.debug(f"Skip {ticker}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error for {ticker}: {e}")
        return None


def run_screener(tickers: list[str], batch_delay: float = 0.3) -> pd.DataFrame:
    # 先下載 SPY 資料用於 Relative Strength 計算
    logger.info("Downloading SPY benchmark data...")
    spy_close = yf.Ticker("SPY").history(period="2y")["Close"]

    candidates = []
    total = len(tickers)
    logger.info(f"Screening {total} tickers...")

    for i, ticker in enumerate(tickers, 1):
        result = screen_ticker(ticker, spy_close)
        if result:
            candidates.append(result)
            logger.info(
                f"[{i}/{total}] ✅ {ticker}"
                f" | T={result['tech_score']} F={result['fund_score']}"
                f" | total={result['total_score']}"
            )
        else:
            if i % 50 == 0:
                logger.info(f"[{i}/{total}] processed...")

        time.sleep(batch_delay)

    df = pd.DataFrame(candidates)
    if not df.empty:
        df = df.sort_values("total_score", ascending=False)

    return df


def save_results(df: pd.DataFrame) -> Path:
    date_str = datetime.now().strftime("%Y%m%d")
    csv_path = OUTPUT_DIR / f"candidates_{date_str}.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved {len(df)} candidates → {csv_path}")
    return csv_path


def main() -> pd.DataFrame:
    from universe import get_prefiltered_universe
    tickers = get_prefiltered_universe()

    if not tickers:
        logger.error("No tickers from Finviz pre-filter")
        return pd.DataFrame()

    df = run_screener(tickers)

    if df.empty:
        logger.warning("No candidates found this week.")
        return df

    save_results(df)

    logger.info("\n=== Top 20 Candidates ===")
    print(df.head(20).to_string(index=False))

    return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    main()
