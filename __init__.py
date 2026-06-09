"""doom — but can it run DOOM? Yes.

A console-only plugin: it contributes a single **DOOM panel** view that runs the
shareware DOOM (Episode 1) in the operator's browser via js-dos (DOSBox-X in
WebAssembly). The game (DOOM.EXE + DOOM1.WAD — freely redistributable id Software
shareware) is self-hosted by the plugin; only the js-dos runtime loads from CDN.

No tools, no agent surface — pure operator fun. Ships DISABLED; enable with
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
