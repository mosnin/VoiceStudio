# Video OS local setup

The Video OS integration is maintained at https://github.com/mosnin/video-gen-os
on `codex/voicestudio-integration`. It provides a local REST client, recorded
narration takes, FFmpeg mixing, and agent skills. VoiceStudio remains the local
speech service; no cloud provider is required.

## Compact first-run setup

An explicitly selected TTS engine with resident model state satisfies the setup
wizard's speech-readiness gate. For example, install KittenTTS, select it and run
a short API generation or engine test before continuing through the wizard.
There is no need to install OmniVoice's larger weights solely to finish setup
when the selected engine already works. Missing/unloaded engines still use the
normal required-model gate. The check reads resident instances without importing
or probing every optional engine during setup polling.

After installing the official Electron app and its Python runtime, quit the app
and launch `scripts/start-video-os-macos.command`. It uses Electron's supported
`OMNIVOICE_BACKEND_CMD` override to supervise this fork's backend with the installed
runtime interpreter. It refuses to start alongside a running backend. The official
app bundle stays intact. Keep the checkout in place; use this launcher whenever
you want the fork backend. Opening the ordinary app uses its bundled backend.
No app version or release channel changes are made.

## Agent files on macOS

Set `OMNIVOICE_MCP_OUTPUT_MODE=files` and point `OMNIVOICE_MCP_BASE_PATH` at
`~/Library/Application Support/OmniVoice/agent-outputs` (expanded to an absolute
path) in the durable user environment. This directory is inside VoiceStudio's
own data area and can also be read by local agents. A directory under Documents
can stall a background file open behind macOS file-access controls; do not
weaken permissions or block the event loop waiting for that location.

The MCP endpoint is `http://127.0.0.1:3900/mcp/`. Keep it on loopback and use the
`X-OmniVoice-Client-Id: video-os` header. KittenTTS is a CPU engine even when the
host's health endpoint reports that Apple MPS is available. Verify the selected
engine and actual generated files, not merely host GPU detection.
