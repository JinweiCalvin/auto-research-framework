#!/bin/bash
cd "$(dirname "$0")"
PYTHON="$(pwd)/idea2paper/.venv/bin/python"
if [ -x "$PYTHON" ]; then
  exec "$PYTHON" tools/start_dashboard.py
fi
exec python3 tools/start_dashboard.py
