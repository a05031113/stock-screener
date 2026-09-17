"""run_screener 的防線：universe 大半在 Yahoo 沒有價格資料時要大聲失敗，
不能靜默寫出 0 檔（2026-07~09 的 finvizfinance ticker 解析 bug 就是這樣躲了 7 週）。

執行：.venv/bin/python -m unittest discover -s tests -v
"""

import unittest
from unittest import mock

import pandas as pd

import screener


def _history(n: int) -> pd.DataFrame:
    idx = pd.date_range("2024-01-01", periods=n, freq="B")
    return pd.DataFrame(
        {
            "Open": 100.0, "High": 101.0, "Low": 99.0, "Close": 100.0, "Volume": 1e6,
        },
        index=idx,
    )


class _FakeTicker:
    """'EMPTY*' 回空 df（Yahoo 404 時 yfinance 的行為），其餘回 300 天正常資料"""

    def __init__(self, ticker: str):
        self.ticker = ticker

    def history(self, period: str = "2y") -> pd.DataFrame:
        if self.ticker.startswith("EMPTY"):
            return pd.DataFrame()
        return _history(300)


class RunScreenerGuardTest(unittest.TestCase):
    def setUp(self):
        mock.patch.object(screener.time, "sleep").start()
        mock.patch.object(screener.yf, "Ticker", _FakeTicker).start()
        self.addCleanup(mock.patch.stopall)

    def test_mostly_empty_universe_raises(self):
        tickers = [f"EMPTY{i}" for i in range(8)] + ["T0", "T1"]
        with self.assertRaises(RuntimeError):
            screener.run_screener(tickers)

    def test_some_empty_is_fine(self):
        tickers = ["EMPTY0", "EMPTY1"] + [f"T{i}" for i in range(8)]
        df = screener.run_screener(tickers)  # 沒有候選也不該 raise
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
