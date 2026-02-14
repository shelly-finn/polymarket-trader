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
  execute)
    python3 scripts/heartbeat-execute.py
    ;;
  implement)
    python3 scripts/idea-implementer.py
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
    tail -20 databases/activity.log
    ;;
  *)
    echo "Usage: $0 {status|execute|implement|monitor-gmail|setup|commit|log}"
    echo ""
    echo "Commands:"
    echo "  status     - Show revenue dashboard (ideas, leads, completed)"
    echo "  execute    - Run full heartbeat loop (advance ideas, scan leads)"
    echo "  implement  - Create prototype/deliverables for next idea"
    echo "  log        - View recent activity log"
    ;;
esac
