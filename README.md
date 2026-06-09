# DOOM — a protoAgent plugin

> *But can it run DOOM?* **Yes.**

A console-only protoAgent plugin (ADR 0026) that adds a **DOOM** view to the operator
console. It runs the shareware **DOOM (Episode 1)** in your browser via a **WebAssembly prboom**
engine (no DOS layer) — you play in-panel with the keyboard.

The engine (GPL prboom compiled to WASM, [cloudflare/doom-wasm](https://github.com/cloudflare/doom-wasm))
and the freely-redistributable shareware `doom1.wad` are **self-hosted** by the plugin and
served same-origin — no external runtime, no network egress. See `wasm/NOTICE.md` for engine
attribution + license (GPL-2.0). The `can_you_play_doom` tool answers the question and opens
the view via plugin-driven navigation (ADR 0044).

## Install

```bash
python -m server plugin install https://github.com/protoLabsAI/doom-plugin
```

Then enable it and open the **DOOM** rail icon (a crosshair) in the console:

```yaml
# langgraph-config.yaml
plugins:
  enabled: [doom]
```

## Controls

| | |
|---|---|
| Move | ↑ ↓ ← → |
| Fire | Ctrl |
| Strafe | Alt + ← / → |
| Use / open doors | Space |
| Run | Shift |
| Weapons | 1–7 |

Click the panel first to grab the keyboard.

No config — the engine and WAD are vendored; there's nothing to tune.

## How it works

- `protoagent.plugin.yaml` declares one view → the host mounts the plugin's router at
  `/plugins/doom` and shows a rail icon that iframes `/plugins/doom/panel`.
- `doom_panel.py` serves the panel HTML plus the WASM engine + WAD **same-origin**
  (`wasm/websockets-doom.{js,wasm}`, `wasm/doom1.wad`) behind an allowlist.
- `wasm/boot.js` boots **prboom** single-player: it preloads `doom1.wad` into the
  engine's in-memory filesystem and runs the game windowed, rendering to a `<canvas>`.
  **No DOS, no DOSBox** — pure WebAssembly.

## Legal

The shareware `doom1.wad` shipped here is id Software's freely-redistributable shareware
DOOM episode-1 IWAD, which the shareware license permits redistributing unmodified. DOOM
© id Software. The WASM engine (`wasm/websockets-doom.{js,wasm}`) is **prboom** compiled to
WebAssembly, **GPL-2.0** — see [`wasm/NOTICE.md`](./wasm/NOTICE.md) for attribution + the
corresponding source. To play the full game, drop your own registered WAD into `wasm/`.

A `protoagent-plugin` for the [protoAgent](https://github.com/protoLabsAI/protoAgent)
fleet.
