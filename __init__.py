"""doom — but can it run DOOM? Yes.

It contributes a **DOOM panel** view that runs the shareware DOOM (Episode 1) in the
operator's browser via a **WebAssembly prboom** engine (no DOS layer). The engine
(`wasm/websockets-doom.{js,wasm}`, GPL prboom) and the freely-redistributable shareware
`doom1.wad` are self-hosted by the plugin and served same-origin — no external runtime.

Plus the `can_you_play_doom` tool, which answers the question and opens the view (ADR
0044 plugin-driven navigation). Ships DISABLED; enable with
``plugins: { enabled: [doom] }``.
"""

from __future__ import annotations

import logging

log = logging.getLogger("protoagent.plugins.doom")


def register(registry) -> None:
    cfg = registry.config or {}
    try:
        from .doom_panel import build_panel_router
        registry.register_router(build_panel_router(cfg))
        log.info("[doom] DOOM panel registered — rip and tear.")
    except Exception:  # noqa: BLE001 — the panel is the whole plugin; log loudly if it fails
        log.exception("[doom] mounting the DOOM panel failed")

    # The "can you play DOOM?" tool — answers yes AND drives the UI (emits doom.play so
    # the console opens the DOOM view + starts the game). Needs the registry to emit.
    try:
        from .tools import make_tools
        registry.register_tools(make_tools(registry))
        log.info("[doom] can_you_play_doom tool registered")
    except Exception:  # noqa: BLE001 — the panel still serves even if the tool fails
        log.exception("[doom] registering the DOOM tool failed")
