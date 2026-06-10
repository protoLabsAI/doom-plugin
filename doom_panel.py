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
<!-- protoLabs design-system plugin-kit (served same-origin by the console, ADR 0038).
     Slug-aware (ADR 0042): the iframe lives at /plugins/… (host window) or
     /agents/<slug>/plugins/… (peer window), so derive the base from the path and link
     same-origin — never hardcode /_ds/… (that pins the HUB's DS, not this agent's). -->
<script>
  (function () {
    var base = location.pathname.split("/plugins/")[0]; // "" on host, "/agents/<slug>" proxied
    var l = document.createElement("link");
    l.rel = "stylesheet"; l.href = base + "/_ds/plugin-kit.css";
    document.head.appendChild(l);
  })();
</script>
<style>
  /* Page / framing chrome — themed by the DS tokens. The DOOM canvas viewport
     keeps its own fixed black background (the game palette is NOT themeable). */
  html,body{margin:0;height:100%;background:var(--pl-color-bg-inset,#000);overflow:hidden;
    font-family:var(--pl-font-mono,ui-monospace,SFMono-Regular,Menlo,monospace);
    color:var(--pl-color-fg-muted)}
  #canvas{display:block;width:100vw;height:100vh;background:#000;cursor:crosshair;
    image-rendering:pixelated;image-rendering:crisp-edges;outline:none}
  /* Loading chrome (#status): DS empty-state. boot.js drives its textContent + hides
     it on runtime init; :has() collapses the whole slot once it's hidden. */
  #loading{position:fixed;left:var(--pl-space-3,12px);top:var(--pl-space-2,10px);z-index:5;
    display:flex;align-items:center;gap:var(--pl-space-2,8px)}
  #loading:has(#status[style*="display: none"]){display:none}
  #loading .pl-spinner{width:14px;height:14px}
  #status{font-size:12px}
  /* Controls hint (#hint): DS info callout. */
  #hint{position:fixed;left:var(--pl-space-3,12px);bottom:var(--pl-space-2,9px);z-index:6;
    pointer-events:none;max-width:none;font-size:11px}
  #hint .pl-callout__body{font-size:11px;line-height:1.5;letter-spacing:.02em}
  #hint .pl-kbd{font-size:.82em}
  #hint .pl-dot-row{margin-right:.45rem}
  #hint b{color:var(--pl-color-accent)}
</style></head>
<body>
  <canvas id="canvas" tabindex="0"></canvas>
  <div id="loading" class="pl-empty pl-empty--slotted">
    <span class="pl-spinner" aria-hidden="true"></span>
    <span id="status">loading DOOM…</span>
  </div>
  <div id="hint" class="pl-callout pl-callout--info">
    <div class="pl-callout__body">
      <span class="pl-dot-row"><span class="pl-dot pl-dot--info pl-dot--pulse"></span></span>
      <b>DOOM</b> — <span class="pl-kbd">↑</span><span class="pl-kbd">↓</span><span class="pl-kbd">←</span><span class="pl-kbd">→</span> move ·
      <span class="pl-kbd">Ctrl</span> fire · <span class="pl-kbd">Alt</span> strafe ·
      <span class="pl-kbd">Space</span> use · click the canvas to play
    </div>
  </div>
  <script>
  // ADR 0038 handshake — the console posts protoagent:init {token, theme} on load and
  // protoagent:theme {theme} live; theme is a curated {bg,bgPanel,fg,fgMuted,brand,border}.
  // We fan each curated key out onto the matching --pl-* token(s) on :root.
  const TMAP={bg:["--pl-color-bg"],bgPanel:["--pl-color-bg-raised","--pl-color-bg-subtle"],fg:["--pl-color-fg"],fgMuted:["--pl-color-fg-muted"],brand:["--pl-color-accent"],border:["--pl-color-border"]};
  let TOKEN=null;
  function applyTheme(t){const r=document.documentElement;for(const[k,v] of Object.entries(t||{}))(TMAP[k]||(k.startsWith("--pl-")?[k]:[])).forEach(p=>v&&r.style.setProperty(p,v));}
  window.addEventListener("message",(e)=>{const d=e.data||{};
    if(d.type==="protoagent:init"){if(d.token)TOKEN=d.token;applyTheme(d.theme);}
    else if(d.type==="protoagent:theme")applyTheme(d.theme);});
  </script>
  <script src="boot.js"></script>
  <script src="websockets-doom.js"></script>
</body></html>
"""
