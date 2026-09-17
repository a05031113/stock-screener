"""_download_daily_closes 的行為測試：純序列、永不批次、限流冷卻、覆蓋率門檻。

執行：.venv/bin/python -m unittest discover -s tests -v
"""

import unittest
from unittest import mock

import pandas as pd

import screener


def _closes(n: int = 5) -> pd.DataFrame:
    idx = pd.date_range("2026-01-01", periods=n, freq="B")
    return pd.DataFrame({"Close": [100.0 + i for i in range(n)]}, index=idx)


class _FakeTicker:
    """依 ticker 名稱決定 history() 行為：'EMPTY*' 回空、'RAISE*' 拋錯、其餘正常"""

    def __init__(self, ticker: str):
        self.ticker = ticker

    def history(self, period: str = "8mo") -> pd.DataFrame:
        if self.ticker.startswith("EMPTY"):
            return pd.DataFrame()
        if self.ticker.startswith("RAISE"):
            raise RuntimeError("Too Many Requests. Rate limited.")
        return _closes()


class DownloadDailyClosesTest(unittest.TestCase):
    def setUp(self):
        self.sleep = mock.patch.object(screener.time, "sleep").start()
        self.download = mock.patch.object(screener.yf, "download").start()
        mock.patch.object(screener.yf, "Ticker", _FakeTicker).start()
        self.addCleanup(mock.patch.stopall)

    def _cooldown_sleeps(self) -> list[float]:
        # 冷卻用長 sleep；檔間 pause 是短 sleep，用秒數區分
        return [c.args[0] for c in self.sleep.call_args_list if c.args[0] >= 60]

    def test_all_ok_serial_never_batches(self):
        tickers = [f"T{i}" for i in range(10)]
        closes = screener._download_daily_closes(tickers)
        self.assertEqual(set(closes), set(tickers))
        self.assertEqual(len(closes["T0"]), 5)
        self.download.assert_not_called()
        self.assertEqual(self._cooldown_sleeps(), [])

    def test_sustained_failures_trigger_cooldown_then_continue(self):
        # 30 檔連續回空 → 冷卻一次 → 後面的正常檔仍要抓到
        tickers = [f"EMPTY{i}" for i in range(30)] + [f"T{i}" for i in range(40)]
        closes = screener._download_daily_closes(
            tickers, fail_streak_limit=30, cooldown_sec=120
        )
        # 第一輪撞到 30 連敗要冷卻；補抓那輪對同一批永久壞檔再冷卻一次也可接受
        self.assertGreaterEqual(len(self._cooldown_sleeps()), 1)
        self.assertTrue(all(c == 120 for c in self._cooldown_sleeps()))
        self.assertEqual(set(closes), {f"T{i}" for i in range(40)})

    def test_exceptions_count_toward_fail_streak(self):
        tickers = [f"RAISE{i}" for i in range(30)] + [f"T{i}" for i in range(40)]
        screener._download_daily_closes(tickers, fail_streak_limit=30)
        self.assertGreaterEqual(len(self._cooldown_sleeps()), 1)

    def test_failed_tickers_get_one_retry_pass(self):
        # 第一輪失敗的 ticker 要在第二輪補抓；用 side_effect 讓第二次呼叫成功
        calls = {"FLAKY": 0}

        class Flaky(_FakeTicker):
            def history(self, period="8mo"):
                if self.ticker == "FLAKY":
                    calls["FLAKY"] += 1
                    if calls["FLAKY"] == 1:
                        return pd.DataFrame()
                return super().history(period)

        with mock.patch.object(screener.yf, "Ticker", Flaky):
            closes = screener._download_daily_closes(["A", "FLAKY", "B"])
        self.assertIn("FLAKY", closes)
        self.assertEqual(calls["FLAKY"], 2)

    def test_low_coverage_raises(self):
        tickers = [f"EMPTY{i}" for i in range(8)] + ["T0", "T1"]
        with self.assertRaises(RuntimeError):
            screener._download_daily_closes(tickers, fail_streak_limit=100)

    def test_cooldowns_exhausted_aborts_early(self):
        tickers = [f"EMPTY{i}" for i in range(200)]
        with self.assertRaises(RuntimeError):
            screener._download_daily_closes(
                tickers, fail_streak_limit=30, max_cooldowns=2
            )
        # 30×3 = 90 檔後放棄，不會磨完 200 檔（含第二輪）
        self.assertLess(self.sleep.call_count, 200)


if __name__ == "__main__":
    unittest.main()
