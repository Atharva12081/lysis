#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
if command -v uv >/dev/null 2>&1; then
	uv sync --locked
	exec uv run --locked app.py
fi
if [ ! -x .venv/bin/python ]; then
	python3 -m venv .venv
fi
if ! .venv/bin/python -c 'import numpy' >/dev/null 2>&1; then
	.venv/bin/python -m pip install -r requirements.txt
fi
exec .venv/bin/python app.py
