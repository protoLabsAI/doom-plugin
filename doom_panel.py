"""DOOM console panel — runs shareware DOOM in-browser via a WASM prboom build.

No DOS layer, no DOSBox: the engine (vendored ``wasm/websockets-doom.{js,wasm}`` — GPL
prboom compiled to WebAssembly, github.com/cloudflare/doom-wasm) loads the shareware
``doom1.wad`` directly and renders to a ``<canvas>``. ``wasm/boot.js`` runs it
single-player. Everything is self-hosted and served same-origin under ``/plugins/doom``
(ADR 0026), so there's no cross-origin fetch and no external runtime.
"""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger("protoagent.plugins.doom")

_WASM = Path(__file__).parent / "wasm"

# Served same-origin to the panel — an allowlist, so the route never serves arbitrary
# files from the plugin dir.
_ASSETS = {
    "boot.js": "application/javascript",
    "websockets-doom.js": "application/javascript",
    "websockets-doom.wasm": "application/wasm",
    "doom1.wad": "application/octet-stream",
}


def build_panel_router(cfg: dict | None):
    from fastapi import APIRouter
    from fastapi.responses import FileResponse, HTMLResponse, Response

    router = APIRouter()

    @router.get("/panel")
    async def _panel():
        return HTMLResponse(_PAGE)

    @router.get("/{asset}")
    async def _asset(asset: str):
        media = _ASSETS.get(asset)
        if media is None:
            return Response(status_code=404)
        f = _WASM / asset
        if not f.exists():
            return Response(status_code=404,
                            content=f"{asset} not vendored — see the plugin's wasm/ dir")
        return FileResponse(f, media_type=media)

    return router


_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>DOOM</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  html,body{margin:0;height:100%;background:#000;overflow:hidden;
    font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#9a9a9a}
  #doom{display:block;width:100vw;height:100vh;background:#000;cursor:crosshair;
    image-rendering:pixelated;image-rendering:crisp-edges;outline:none}
  #status{position:fixed;left:12px;top:10px;font-size:12px;opacity:.7;z-index:5}
  #hint{position:fixed;left:12px;bottom:9px;font-size:11px;opacity:.55;z-index:6;
    pointer-events:none;letter-spacing:.02em}
  #hint b{color:#c0392b}
</style></head>
<body>
  <canvas id="doom" tabindex="0"></canvas>
  <div id="status">loading DOOM…</div>
  <div id="hint"><b>DOOM</b> — ↑↓←→ move · Ctrl fire · Alt strafe · Space use · click the canvas to play</div>
  <script src="boot.js"></script>
  <script src="websockets-doom.js"></script>
</body></html>
"""
