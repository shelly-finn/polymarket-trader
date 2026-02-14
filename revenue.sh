#!/usr/bin/env bash
# revenue.sh - Quick commands for the revenue system

cd "$(dirname "$0")" || exit

case "${1:-status}" in
  status)
    python3 scripts/status.py
    ;;
  monitor-gmail)
    python3 scripts/gmail-monitor.py
    ;;
  heartbeat)
    python3 scripts/heartbeat-monitor.py
    ;;
  setup)
    echo "Revenue system already set up."
    echo "Workspace: $(pwd)"
    echo "Components: scripts/, databases/, projects/, drafts/, research/"
    ;;
  commit)
    git add -A && git commit -m "Revenue update: ${2:-auto-commit}"
    ;;
  log)
    cat databases/activity.log | tail -20
    ;;
  *)
    echo "Usage: $0 {status|monitor-gmail|heartbeat|setup|commit|log}"
    ;;
esac
