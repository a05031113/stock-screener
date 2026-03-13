# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Weekly momentum stock screener that scans S&P500 + Nasdaq100 + Russell 2000 for breakout and coiling patterns, then sends results via Telegram. Runs automatically every Friday after US market close via GitHub Actions.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline (screener + Telegram notification)
python main.py

# Run screener only (no notification)
python screener.py

# Test notification with latest CSV
python notify.py

# Test universe fetching
python universe.py
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications |
| `TELEGRAM_CHAT_ID` | Target Telegram chat ID |

Both are required for notifications. Set as GitHub Secrets for CI.

## Architecture

**Pipeline flow:** `main.py` → `screener.py` (scan) → `notify.py` (Telegram)

- **`universe.py`** — Fetches ticker lists from Wikipedia (S&P500, Nasdaq100) and iShares (Russell 2000 via IWM ETF holdings CSV). Deduplicates and merges into a single universe.
- **`screener.py`** — Downloads 2 years of price history per ticker via `yfinance`, computes technical indicators (MAs, relative volume, Bollinger Band width, returns), then applies two pattern filters:
  - **Breakout**: near 52-week high + volume surge + reasonable monthly gain (≥5/6 conditions)
  - **Coiling**: compressed volatility + sudden volume + MA crossover (≥5/7 conditions)
- **`notify.py`** — Formats top 20 candidates into HTML messages, splits at 3800 chars for Telegram's 4096 limit, sends via Telegram Bot API.

## Key Design Decisions

- Sequential ticker processing with `time.sleep(0.3)` rate limiting for yfinance API
- Russell 2000 fetching has iShares primary + yfinance fallback (fallback currently returns empty)
- GitHub Actions workflow has 90-minute timeout to accommodate ~2000+ ticker scans
- Output CSVs are committed back to the repo by the CI bot
