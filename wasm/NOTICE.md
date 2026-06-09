# Vendored engine — attribution & license

This directory vendors a **prboom** DOOM engine compiled to WebAssembly:

- `websockets-doom.js`, `websockets-doom.wasm` — prboom built for the browser via
  Emscripten, from **[cloudflare/doom-wasm](https://github.com/cloudflare/doom-wasm)**.
  prboom (and prboom-plus) is licensed **GPL-2.0-or-later**. The complete corresponding
  source is the cloudflare/doom-wasm repository (and its prboom upstream). This plugin
  redistributes the unmodified built artifacts under the GPL; see that repository for the
  source and build instructions.
- `boot.js` — a small single-player launcher written for this plugin (loads the WAD and
  runs prboom windowed; no multiplayer/websocket code).

`doom1.wad` is id Software's **shareware** DOOM episode-1 IWAD, freely redistributable
unmodified under id's shareware terms. DOOM © id Software.

The plugin's own code (`__init__.py`, `doom_panel.py`, `tools.py`) is part of the
protoAgent plugin ecosystem; the GPL applies to the vendored prboom artifacts above.
