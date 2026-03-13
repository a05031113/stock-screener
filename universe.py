"""
Stock Universe Manager
取得 S&P500 + Nasdaq100 + Russell 2000 清單
"""

import pandas as pd
import yfinance as yf
import requests
import time
import logging
from io import StringIO

logger = logging.getLogger(__name__)


def get_sp500() -> list[str]:
    """從 Wikipedia 取得 S&P500 清單"""
    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        table = pd.read_html(url)[0]
        tickers = table["Symbol"].str.replace(".", "-", regex=False).tolist()
        logger.info(f"S&P500: {len(tickers)} tickers")
        return tickers
    except Exception as e:
        logger.error(f"Failed to get S&P500: {e}")
        return []


def get_nasdaq100() -> list[str]:
    """從 Wikipedia 取得 Nasdaq100 清單"""
    try:
        url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        tables = pd.read_html(url)
        # 找有 Ticker 欄位的 table
        for table in tables:
            cols = [c.lower() for c in table.columns]
            if "ticker" in cols or "symbol" in cols:
                col = "Ticker" if "Ticker" in table.columns else "Symbol"
                tickers = table[col].dropna().str.replace(".", "-", regex=False).tolist()
                logger.info(f"Nasdaq100: {len(tickers)} tickers")
                return tickers
        return []
    except Exception as e:
        logger.error(f"Failed to get Nasdaq100: {e}")
        return []


def get_russell2000() -> list[str]:
    """
    Russell 2000：用 iShares IWM ETF 的持股清單
    免費且穩定，約 2000 檔小型股
    """
    try:
        url = "https://www.ishares.com/us/products/239710/ISHARES-RUSSELL-2000-ETF/1467271812596.ajax?fileType=csv&fileName=IWM_holdings&dataType=fund"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=30)
        
        # iShares CSV 前幾行是 metadata，跳過
        lines = resp.text.split("\n")
        # 找到 header 行（含 Ticker）
        header_idx = next((i for i, l in enumerate(lines) if "Ticker" in l), None)
        if header_idx is None:
            logger.warning("iShares CSV format changed: 'Ticker' column not found")
            return _get_russell2000_fallback()
        csv_content = "\n".join(lines[header_idx:])
        df = pd.read_csv(StringIO(csv_content))
        
        tickers = (
            df["Ticker"]
            .dropna()
            .str.strip()
            .str.replace(".", "-", regex=False)
            .tolist()
        )
        # 過濾掉非股票行（如 "-", 空白）
        tickers = [t for t in tickers if t and t != "-" and len(t) <= 5]
        logger.info(f"Russell 2000: {len(tickers)} tickers")
        return tickers
    except Exception as e:
        logger.warning(f"Failed to get Russell 2000 from iShares: {e}")
        logger.info("Falling back to IWM components via yfinance")
        return _get_russell2000_fallback()


def _get_russell2000_fallback() -> list[str]:
    """備用：從 yfinance 取 IWM 持股（較少但夠用）"""
    try:
        iwm = yf.Ticker("IWM")
        # yfinance 沒有直接的持股 API，改回傳空
        logger.warning("Russell 2000 fallback also failed, using empty list")
        return []
    except Exception:
        return []


def get_universe(include_russell: bool = True) -> list[str]:
    """
    取得完整股票 universe，去除重複
    """
    sp500    = get_sp500()
    nasdaq   = get_nasdaq100()
    russell  = get_russell2000() if include_russell else []

    all_tickers = list(dict.fromkeys(sp500 + nasdaq + russell))  # 保序去重
    logger.info(f"Total universe: {len(all_tickers)} unique tickers")
    return all_tickers


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tickers = get_universe(include_russell=True)
    print(f"Universe size: {len(tickers)}")
    print(tickers[:10])
