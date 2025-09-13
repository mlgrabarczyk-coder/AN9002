#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv311"

if ! command -v python3.11 >/dev/null 2>&1; then
  echo "python3.11 not found. Please install Python 3.11." >&2
  exit 1
fi

# Create venv if missing
if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "[setup] Creating Python 3.11 venv at $VENV_DIR"
  python3.11 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Ensure deps are present
python - <<'PY' || DEP_MISSING=1
import sys
try:
    import matplotlib  # noqa
    import bleak  # noqa
except Exception as e:
    sys.exit(1)
PY

if [[ "${DEP_MISSING:-0}" == "1" ]]; then
  echo "[setup] Installing/upgrading matplotlib and bleak"
  python -m pip install --upgrade pip
  python -m pip install matplotlib bleak
fi

echo "[run] Starting BLE multimeter (Ctrl+C to stop)"
exec python "$ROOT_DIR/picoscope/ble_multimeter.py" "$@"

