# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Early momentum stock screener that finds stocks in the early stage of major moves (like LITE before its parabolic run). Uses Finviz for pre-filtering, then applies a two-layer scoring system: technical (12-point) + fundamental (7-point). Sends results via Telegram every Friday after US market close via GitHub Actions.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline (Finviz filter → scoring → Telegram)
python main.py

# Run screener only (no notification)
python screener.py

# Test notification with latest CSV
python notify.py

# Test Finviz pre-filter only
python universe.py
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications |
| `TELEGRAM_CHAT_ID` | Target Telegram chat ID |

Both are required for notifications. Set as GitHub Secrets for CI.

## Architecture

**Pipeline flow:** `universe.py` (Finviz pre-filter) → `screener.py` (tech + fundamental scoring) → `notify.py` (Telegram)

- **`universe.py`** — Finviz pre-filter with two filter sets:
  - **Stage 2**: Price > SMA50, SMA50 > SMA200, relative volume > 1.5
  - **Base Breakout**: 20%+ above 52W low, relative volume > 2
  - Narrows universe from ~7000 US stocks to ~200-300 candidates

- **`screener.py`** — Two-layer scoring on pre-filtered candidates:
  - **Technical (12 pts, threshold ≥8)**: Base formation (3), Stage 2 entry (4), volume accumulation (3), relative strength vs SPY (2)
  - **Volatility bonus (2 pts)**: BB width percentile, ATR contraction
  - **Fundamental (7 pts, threshold ≥4)**: Revenue growth/acceleration (3), EPS beat + margin + profitability (3), institutional holders (1)
  - Only runs fundamental analysis on tickers that pass technical threshold

- **`notify.py`** — Formats top 20 candidates with tech/fund scores into HTML messages, splits at 3800 chars for Telegram's 4096 limit, sends via Telegram Bot API with retry.

## Key Design Decisions

- Finviz pre-filter reduces universe from ~7000 to ~300, cutting execution time from 60-80 min to ~10 min
- Technical scoring runs before fundamental to minimize yfinance API calls
- SPY benchmark downloaded once and reused for all relative strength calculations
- GitHub Actions workflow has 30-minute timeout
- CI sends Telegram alert on failure
- Output CSVs are committed back to the repo by the CI bot
