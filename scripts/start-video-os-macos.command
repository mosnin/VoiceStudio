#!/bin/sh
# Run the official Electron shell with this fork's backend and installed dependencies.
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
python_bin="$HOME/Library/Application Support/VoiceStudio/runtime/project/.venv/bin/python"
app_bin="/Applications/VoiceStudio.app/Contents/MacOS/VoiceStudio"
if [ ! -x "$python_bin" ] || [ ! -x "$app_bin" ]; then
  echo 'Install VoiceStudio Electron and its local runtime first.' >&2
  exit 1
fi
if curl -fsS --max-time 2 http://127.0.0.1:3900/health >/dev/null 2>&1; then
  echo 'VoiceStudio is already running. Quit it before selecting the fork backend.' >&2
  exit 1
fi
OMNIVOICE_BACKEND_CMD=$("$python_bin" -c 'import json,sys; print(json.dumps([sys.executable,"-m","uvicorn","main:app","--app-dir",sys.argv[1],"--host","127.0.0.1","--port","3900"]))' "$repo_dir/backend")
export OMNIVOICE_BACKEND_CMD
exec "$app_bin"
