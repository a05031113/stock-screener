#!/bin/bash
# launchd 包裝腳本：與 .github/workflows/screener.yml 的步驟一對一對應。
#   1. git pull --ff-only 同步遠端
#   2. freshness check：本週兩份 CSV 都在就跳過
#   3. 跑 main.py（記錄 exit code，不立刻結束）
#   4. 不論成敗都 commit / push output/（對應 workflow 的 if: always()）
#   5. 以 main.py 的 exit code 結束
set -u

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$REPO_DIR/.venv/bin/python"

log() { printf '%s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2"; }

cd "$REPO_DIR" || exit 1
log INFO "run_screener start (repo=$REPO_DIR)"

# ── 1. 同步遠端；output/ 以外有未提交變更就不硬跑 ──
dirty=$(git status --porcelain | grep -v '^?? ' | grep -v ' output/' || true)
if [ -n "$dirty" ]; then
  log ERROR "working tree has uncommitted changes outside output/, aborting:"
  printf '%s\n' "$dirty"
  exit 2
fi
if ! git pull --ff-only origin main; then
  log ERROR "git pull --ff-only failed (local and remote diverged?), aborting"
  exit 2
fi

# ── 2. freshness check：candidates + streak 同日 CSV 都在且 ≤3 天 → 本週已完成 ──
latest=$(ls output/candidates_*.csv 2>/dev/null | sort | tail -1)
if [ -n "$latest" ]; then
  file_date=$(basename "$latest" .csv | cut -d_ -f2)
  file_ts=$(date -j -f '%Y%m%d' "$file_date" '+%s' 2>/dev/null || echo 0)
  age_days=$(( ( $(date '+%s') - file_ts ) / 86400 ))
  if [ "$age_days" -le 3 ] && [ -f "output/streak_${file_date}.csv" ]; then
    log INFO "results for $file_date already complete (${age_days}d old), skipping run"
    exit 0
  fi
fi

# ── 3. 執行 screener ──
if [ ! -x "$PYTHON" ]; then
  log ERROR "venv python not found at $PYTHON — run: uv venv --python 3.13 .venv && uv pip install -r requirements.txt"
  exit 2
fi
log INFO "running main.py"
"$PYTHON" main.py
rc=$?
log INFO "main.py exited with $rc"

# ── 4. 不論成敗都提交已產出的結果 ──
git add output/
if git diff --cached --quiet; then
  log INFO "no new output to commit"
else
  git -c user.name="stock-screener launchd" -c user.email="a05031113@gmail.com" \
    commit -q -m "screener: $(date '+%Y-%m-%d') results"
  if git push origin main; then
    log INFO "pushed results to origin/main"
  else
    log ERROR "git push failed; commit is kept locally, next run will retry after pull"
    [ "$rc" -eq 0 ] && rc=3
  fi
fi

log INFO "run_screener end (exit $rc)"
exit "$rc"
