"""DOOM console panel — runs the shareware DOOM in-browser via js-dos (DOSBox-X/WASM).

The panel serves an HTML page that boots js-dos pointed at a self-hosted ``.jsdos``
bundle (``DOOM.EXE`` + ``DOOM1.WAD``, freely redistributable id Software shareware).
The game runs entirely in the operator's browser; only the js-dos runtime loads from
the js-dos CDN. ``doom.bundle_url`` overrides the bundle (e.g. to point at the
registered DOOM, or a self-hosted js-dos runtime).

The router is mounted by the host under ``/plugins/doom`` (ADR 0026), so the panel is
``/plugins/doom/panel`` and the bundle is served same-origin at
``/plugins/doom/doom.jsdos`` — no cross-origin fetch for the game data.
"""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger("protoagent.plugins.doom")

_HERE = Path(__file__).parent
_BUNDLE = _HERE / "doom.jsdos"

# Bump when the bundle changes — js-dos caches by URL (browser + IndexedDB), so a new
# version string forces a fresh fetch instead of replaying a stale cached game.
_BUNDLE_VERSION = "2"


def build_panel_router(cfg: dict | None):
    from fastapi import APIRouter
    from fastapi.responses import FileResponse, HTMLResponse, Response

    cfg = cfg or {}
    override = str(cfg.get("bundle_url") or "").strip()  # blank = the self-hosted bundle
    router = APIRouter()

    @router.get("/panel")
    async def _panel():
        # relative → /plugins/doom/doom.jsdos; ?v busts js-dos's URL-keyed cache.
        bundle = override or f"doom.jsdos?v={_BUNDLE_VERSION}"
        return HTMLResponse(_PAGE.replace("__BUNDLE__", bundle))

    @router.get("/doom.jsdos")
    async def _bundle():
        if not _BUNDLE.exists():
            return Response(
                status_code=404,
                content="doom.jsdos not bundled — set `doom.bundle_url` to a js-dos bundle.")
        return FileResponse(_BUNDLE, media_type="application/zip", filename="doom.jsdos")

    return router


_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>DOOM</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://v8.js-dos.com/latest/js-dos.css">
<style>
  html,body{margin:0;height:100%;background:#000;overflow:hidden;
    font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#9a9a9a}
  #dos{width:100vw;height:100vh}
  #hint{position:fixed;left:10px;bottom:8px;font-size:11px;opacity:.55;
    z-index:6;pointer-events:none;letter-spacing:.02em}
  #hint b{color:#c0392b}
</style></head>
<body>
  <div id="dos"></div>
  <div id="hint"><b>DOOM</b> — ↑↓←→ move · Ctrl fire · Alt strafe · Space use · click to grab keyboard</div>
  <script src="https://v8.js-dos.com/latest/js-dos.js"></script>
  <script>
    Dos(document.getElementById("dos"), {
      url: "__BUNDLE__",
      theme: "dark",
      autoStart: true,   // boot straight into the game
      kiosk: true,       // skip the js-dos config UI
      noCloud: true,     // no cloud-save prompts
      backend: "dosboxX",
    });
  </script>
</body></html>
"""
