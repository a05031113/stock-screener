# Early Momentum Screener v2 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Wikipedia scraping + brute-force scanning with Finviz pre-filter + yfinance deep scoring, adding fundamental analysis layer to catch stocks in early-stage momentum (like LITE before its parabolic move).

**Architecture:** Finviz screener handles coarse technical filtering (universe from ~7000 → ~100-200 candidates). yfinance then computes custom technical scores (12-point) and fundamental scores (7-point) on that smaller set. Results are ranked by total score and sent via Telegram.

**Tech Stack:** finvizfinance (Finviz screener), yfinance (price history + fundamentals), pandas, requests

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `universe.py` | **Rewrite** | Finviz pre-filter replaces Wikipedia scraping |
| `screener.py` | **Rewrite** | New technical scoring (12-point) + fundamental scoring (7-point) |
| `notify.py` | **Modify** | Updated message format with tech + fundamental scores |
| `main.py` | **Modify** | Updated pipeline flow |
| `requirements.txt` | **Modify** | Add finvizfinance, remove lxml |
| `.github/workflows/screener.yml` | **Modify** | Reduce timeout, add failure notification |
| `CLAUDE.md` | **Modify** | Update architecture docs |

---

## Chunk 1: Finviz Pre-Filter (universe.py rewrite)

### Task 1: Replace universe.py with Finviz screener

**Files:**
- Rewrite: `universe.py`
- Modify: `requirements.txt`

- [ ] **Step 1: Update requirements.txt**

```
yfinance>=0.2.40
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
finvizfinance>=0.14
```

Remove `lxml` (no longer scraping Wikipedia).

- [ ] **Step 2: Rewrite universe.py with Finviz pre-filter**

Replace all Wikipedia/iShares scraping with Finviz screener. The Finviz filters should do coarse technical filtering to narrow from ~7000 US stocks down to ~100-200 candidates.

```python
"""
Finviz Pre-Filter
用 Finviz screener 做粗篩，取代 Wikipedia 爬蟲
篩選條件：美股、價格 > $5、有基本量能、技術面初步符合
"""

import logging
import time
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
    time.sleep(1)  # Finviz rate limit

    # ── Filter B: 底部突破型 ──
    # 從 52 週低點回升 + 量能放大
    base_breakout_filters = {
        "Price": "Over $5",
        "Average Volume": "Over 200K",
        "Relative Volume": "Over 2",
        "52-Week Low": "20% or more above Low",
        "52-Week High": "30% or more below High",
    }

    # 執行兩組篩選
    stage2_tickers = _run_finviz_screen(stage2_filters, "Stage 2")
    time.sleep(2)  # Finviz rate limit between requests
    base_tickers = _run_finviz_screen(base_breakout_filters, "Base Breakout")

    # 合併去重（保序）
    all_tickers = list(dict.fromkeys(stage2_tickers + base_tickers))
    logger.info(f"Total pre-filtered universe: {len(all_tickers)} unique tickers")
    return all_tickers


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tickers = get_prefiltered_universe()
    print(f"Universe size: {len(tickers)}")
    print(tickers[:20])
```

**注意：** Finviz 的 filter value 名稱需要與 finvizfinance 支援的完全匹配。Step 3 會驗證這些 filter 是否正確。

- [ ] **Step 3: 本地測試 Finviz pre-filter**

```bash
pip install finvizfinance>=0.14
python universe.py
```

預期：印出 universe size（應在 50-500 之間），以及前 20 支 ticker。
如果 filter value 名稱不對，finvizfinance 會報錯，需要根據錯誤訊息調整 filter dict 的 value。

- [ ] **Step 4: Commit**

```bash
git add universe.py requirements.txt
git commit -m "feat: replace Wikipedia scraping with Finviz pre-filter"
```

---

## Chunk 2: Technical Scoring (screener.py - Layer 1)

### Task 2: Rewrite technical indicator computation

**Files:**
- Rewrite: `screener.py`

- [ ] **Step 1: Rewrite compute_indicators with new indicators**

保留有用的舊指標，新增 Stage 2 / VCP / RS 相關指標：

```python
def compute_indicators(df: pd.DataFrame, spy_close: pd.Series | None = None) -> pd.DataFrame:
    df = df.copy()
    close  = df["Close"]
    volume = df["Volume"]

    # ── 移動平均 ──
    df["MA50"]  = close.rolling(50).mean()
    df["MA150"] = close.rolling(150).mean()
    df["MA200"] = close.rolling(200).mean()

    # MA150 斜率（近 20 日變化）
    ma150 = df["MA150"]
    df["MA150_Slope"] = (ma150 - ma150.shift(20)) / ma150.shift(20)

    # MA50 穿越 MA150 的天數
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

    # 6 個月 high-low range（底部結構）
    df["Range_6M"] = (close.rolling(126).max() - close.rolling(126).min()) / close.rolling(126).min()

    # ── 量能 ──
    df["AvgVol5"]  = volume.rolling(5).mean()
    df["AvgVol50"] = volume.rolling(50).mean()
    df["RelVol"]   = df["AvgVol5"] / df["AvgVol50"]

    # 上漲日 vs 下跌日的成交量比（近 20 日）
    up_vol   = volume.where(close > close.shift(1), 0).rolling(20).sum()
    down_vol = volume.where(close <= close.shift(1), 0).rolling(20).sum()
    df["UpDownVolRatio"] = up_vol / down_vol.replace(0, 1)

    # 最近一次放量日是否為上漲日
    recent_high_vol_day = volume.iloc[-5:].idxmax()
    df["LastVolSurgeUp"] = close.loc[recent_high_vol_day] > close.shift(1).loc[recent_high_vol_day]

    # ── 漲跌幅 ──
    df["Return_1W"] = close.pct_change(5)
    df["Return_1M"] = close.pct_change(21)
    df["Return_3M"] = close.pct_change(63)

    # ── 波動收縮 ──
    df["BB_Width"]     = (close.rolling(20).std() * 2) / close.rolling(20).mean()
    bb_6m              = df["BB_Width"].rolling(126)
    df["BB_Percentile"] = df["BB_Width"].rolling(126).rank(pct=True)
    df["ATR_14"]       = _atr(df, 14)
    df["ATR_60"]       = _atr(df, 60)
    df["ATR_Ratio"]    = df["ATR_14"] / df["ATR_60"].replace(0, 1)

    # ── Relative Strength vs SPY ──
    if spy_close is not None and len(spy_close) >= 63:
        stock_ret_3m = close.pct_change(63)
        spy_ret_3m   = spy_close.pct_change(63)
        df["RS_vs_SPY"]    = stock_ret_3m - spy_ret_3m
        rs_line            = close / spy_close.reindex(close.index, method="ffill")
        df["RS_Line_Slope"] = (rs_line - rs_line.shift(20)) / rs_line.shift(20)
    else:
        df["RS_vs_SPY"]     = 0.0
        df["RS_Line_Slope"] = 0.0

    return df


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
```

- [ ] **Step 2: Implement new technical scoring function**

Replace `check_breakout` + `check_coiling` with unified 12-point scoring:

```python
def score_technical(row: pd.Series, price: float) -> tuple[int, list[str]]:
    """
    技術面計分（滿分 12）
    門檻：≥ 8 分通過

    A. Base Formation (3 分)
    B. Stage 2 Entry (4 分)
    C. Volume Accumulation (3 分)
    D. Relative Strength (2 分)
    """
    checks = {
        # A. Base Formation
        "base_tight":       row["Range_6M"] < 0.40,
        "above_low_20_80":  0.20 < row["Pct_From_Low"] < 0.80,
        "within_high_75":   row["Pct_From_High"] > -0.25,

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
```

- [ ] **Step 3: Add volatility contraction bonus**

```python
def score_volatility_bonus(row: pd.Series) -> tuple[int, list[str]]:
    """波動收縮加分（滿分 2），不設門檻"""
    checks = {
        "bb_compressed":  row["BB_Percentile"] < 0.25,
        "atr_contracted": row["ATR_Ratio"] < 0.8,
    }
    score  = sum(checks.values())
    labels = [k for k, v in checks.items() if v]
    return score, labels
```

- [ ] **Step 4: Commit**

```bash
git add screener.py
git commit -m "feat: rewrite technical scoring with 12-point system + VCP/RS indicators"
```

---

## Chunk 3: Fundamental Scoring (screener.py - Layer 2)

### Task 3: Add fundamental analysis

**Files:**
- Modify: `screener.py`

- [ ] **Step 1: Implement fundamental data fetching**

```python
def fetch_fundamentals(ticker_obj: yf.Ticker) -> dict:
    """
    從 yfinance 取得基本面資料
    回傳 dict，取不到的欄位填 None
    """
    info = {}
    try:
        raw = ticker_obj.info
        info["gross_margins"]   = raw.get("grossMargins")
        info["revenue_growth"]  = raw.get("revenueGrowth")
        info["earnings_growth"] = raw.get("earningsGrowth")
    except Exception:
        pass

    # 季度營收（判斷加速）
    try:
        inc = ticker_obj.quarterly_income_stmt
        if inc is not None and not inc.empty and "Total Revenue" in inc.index:
            revenues = inc.loc["Total Revenue"].dropna().sort_index()
            if len(revenues) >= 3:
                # YoY growth for recent quarters (需要至少 5 季才能算 2 季的 YoY)
                # 簡化：用 revenueGrowth from info + 趨勢判斷
                info["revenues"] = revenues.tolist()  # newest first in yfinance
    except Exception:
        pass

    # EPS Surprise
    try:
        earnings = ticker_obj.get_earnings_dates(limit=8)
        if earnings is not None and not earnings.empty:
            # 找最近有實際值的那一季
            cols = earnings.columns.tolist()
            if "Reported EPS" in cols and "EPS Estimate" in cols:
                recent = earnings.dropna(subset=["Reported EPS", "EPS Estimate"]).head(1)
                if not recent.empty:
                    info["eps_actual"]   = float(recent["Reported EPS"].iloc[0])
                    info["eps_estimate"] = float(recent["EPS Estimate"].iloc[0])
    except Exception:
        pass

    # 機構持股
    try:
        holders = ticker_obj.institutional_holders
        if holders is not None and not holders.empty:
            info["inst_holder_count"] = len(holders)
    except Exception:
        pass

    return info
```

- [ ] **Step 2: Implement fundamental scoring function**

```python
def score_fundamental(info: dict) -> tuple[int, list[str]]:
    """
    基本面計分（滿分 7）
    門檻：≥ 4 分通過

    A. 營收動能 (3 分)
    B. 獲利品質 (3 分)
    C. 機構動向 (1 分)
    """
    checks = {}

    # A. 營收動能
    rev_growth = info.get("revenue_growth")
    checks["revenue_yoy_10pct"] = rev_growth is not None and rev_growth > 0.10

    # 營收加速：earningsGrowth > revenueGrowth 暗示 operating leverage
    earn_growth = info.get("earnings_growth")
    checks["earnings_accelerating"] = (
        earn_growth is not None and rev_growth is not None
        and earn_growth > rev_growth and earn_growth > 0
    )

    # 連續正成長（用 revenue_growth > 0 作為 proxy）
    checks["revenue_positive"] = rev_growth is not None and rev_growth > 0

    # B. 獲利品質
    eps_actual   = info.get("eps_actual")
    eps_estimate = info.get("eps_estimate")
    checks["eps_beat"] = (
        eps_actual is not None and eps_estimate is not None
        and eps_estimate != 0 and eps_actual > eps_estimate
    )

    gm = info.get("gross_margins")
    checks["gross_margin_healthy"] = gm is not None and gm > 0.30

    checks["eps_positive"] = eps_actual is not None and eps_actual > 0

    # C. 機構動向
    checks["inst_holders"] = info.get("inst_holder_count", 0) >= 5

    score  = sum(checks.values())
    labels = [k for k, v in checks.items() if v]
    return score, labels
```

- [ ] **Step 3: Rewrite screen_ticker to combine both layers**

```python
TECH_THRESHOLD = 8     # /12
FUND_THRESHOLD = 4     # /7

def screen_ticker(ticker: str, spy_close: pd.Series | None = None) -> dict | None:
    try:
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(period="2y")

        if len(df) < 252:  # 需要至少 1 年資料
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
            "ticker":        ticker,
            "price":         round(price, 2),
            "tech_score":    tech_score,
            "fund_score":    fund_score,
            "vol_bonus":     vol_bonus,
            "total_score":   total_score,
            "rel_vol":       round(float(row["RelVol"]), 2),
            "return_1w":     f"{row['Return_1W']:.1%}",
            "return_1m":     f"{row['Return_1M']:.1%}",
            "return_3m":     f"{row['Return_3M']:.1%}",
            "pct_from_high": f"{row['Pct_From_High']:.1%}",
            "rs_vs_spy":     round(float(row["RS_vs_SPY"]), 3),
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
```

- [ ] **Step 4: Update run_screener and main**

```python
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
                f"[{i}/{total}] ✅ {ticker} "
                f"| T={result['tech_score']} F={result['fund_score']} "
                f"| total={result['total_score']}"
            )
        else:
            if i % 50 == 0:
                logger.info(f"[{i}/{total}] processed...")
        time.sleep(batch_delay)

    df = pd.DataFrame(candidates)
    if not df.empty:
        df = df.sort_values("total_score", ascending=False)
    return df


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
```

- [ ] **Step 5: Commit**

```bash
git add screener.py
git commit -m "feat: add fundamental scoring layer and combined tech+fund pipeline"
```

---

## Chunk 4: Notification & CI Updates

### Task 4: Update Telegram notification format

**Files:**
- Modify: `notify.py`

- [ ] **Step 1: Update format_candidate for new fields**

```python
def format_candidate(row: pd.Series) -> str:
    """單一候選股的格式"""
    rev_growth = row.get("revenue_growth")
    rev_str = f"{rev_growth:.0%}" if pd.notna(rev_growth) else "N/A"

    gm = row.get("gross_margins")
    gm_str = f"{gm:.0%}" if pd.notna(gm) else "N/A"

    return (
        f"📈 <b>${row['ticker']}</b> | 總分 {row['total_score']}\n"
        f"   💰 ${row['price']} | 相對量 {row['rel_vol']}x\n"
        f"   📊 技術 {row['tech_score']}/12 | 基本面 {row['fund_score']}/7 | VCP +{row['vol_bonus']}\n"
        f"   📈 1W {row['return_1w']} | 1M {row['return_1m']} | 3M {row['return_3m']}\n"
        f"   🏢 營收成長 {rev_str} | 毛利率 {gm_str} | RS {row['rs_vs_spy']}\n"
        f"   🎯 {row['tech_signals']}\n"
    )
```

- [ ] **Step 2: Update build_summary header and remove pattern-based grouping**

改為按 total_score 排序顯示，不再分 Breakout/Coiling 類別：

```python
def build_summary(df: pd.DataFrame) -> list[str]:
    date_str = datetime.now().strftime("%Y/%m/%d")
    header = (
        f"📊 <b>每週早期動能掃描 v2</b>\n"
        f"🗓 {date_str} | 共 {len(df)} 檔候選\n"
        f"📋 技術面 ≥8/12 + 基本面 ≥4/7\n"
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

    footer = (
        f"\n{'─' * 30}\n"
        f"⚠️ 以上為技術+基本面自動篩選\n"
        f"📋 請手動確認：業務故事、earnings call、機構持股趨勢"
    )

    if len(current) + len(footer) > 3800:
        messages.append(current)
        messages.append(footer)
    else:
        messages.append(current + footer)

    return messages
```

- [ ] **Step 3: Commit**

```bash
git add notify.py
git commit -m "feat: update Telegram notification with tech+fund scores"
```

### Task 5: Update main.py and CI

**Files:**
- Modify: `main.py`
- Modify: `.github/workflows/screener.yml`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Simplify main.py**

```python
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
```

(基本不變，只更新 docstring)

- [ ] **Step 2: Update CI workflow**

```yaml
name: Weekly Early Momentum Screener

on:
  schedule:
    - cron: '0 21 * * 5'
  workflow_dispatch:

jobs:
  screener:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # Finviz pre-filter 大幅縮短執行時間

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run screener
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID:   ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python main.py

      - name: Commit results
        run: |
          git config user.name  "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add output/
          git diff --cached --quiet || git commit -m "screener: $(date +'%Y-%m-%d') results"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Notify on failure
        if: failure()
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID:   ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="${TELEGRAM_CHAT_ID}" \
            -d text="❌ Weekly screener failed! Check: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

- [ ] **Step 3: Update CLAUDE.md**

更新 Architecture 和 Commands section 以反映新的 pipeline。

- [ ] **Step 4: Commit**

```bash
git add main.py .github/workflows/screener.yml CLAUDE.md
git commit -m "chore: update CI (30min timeout, failure alert) and docs"
```

---

## Chunk 5: Local Testing & Push

### Task 6: End-to-end local test

- [ ] **Step 1: Install new dependencies**

```bash
pip install -r requirements.txt
```

- [ ] **Step 2: Test Finviz pre-filter**

```bash
python universe.py
```

預期：印出 50-500 支 ticker。

- [ ] **Step 3: Test full pipeline (without Telegram)**

```bash
python screener.py
```

預期：在 output/ 產生 CSV，包含 tech_score, fund_score, total_score 等欄位。

- [ ] **Step 4: Review CSV output sanity check**

確認：
- total_score 排序正確
- tech_score 都 ≥ 8
- fund_score 都 ≥ 4
- revenue_growth / gross_margins 有值（非全 None）

- [ ] **Step 5: Push to GitHub**

```bash
git push
```

- [ ] **Step 6: Trigger GitHub Actions workflow**

```bash
gh workflow run screener.yml
```

觀察 Actions log 確認全流程正常。
