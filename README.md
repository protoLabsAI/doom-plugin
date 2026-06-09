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

## Config (`doom:` in `langgraph-config.yaml`)

| key | default | meaning |
|---|---|---|
| `bundle_url` | `""` | Override the js-dos game bundle URL. Blank = the self-hosted shareware DOOM bundled with the plugin. Point it at the registered DOOM (`DOOM2.WAD`/`doom.wad` packaged as a `.jsdos`) to play the full game. |

## How it works

- `protoagent.plugin.yaml` declares one view → the host mounts the plugin's router at
  `/plugins/doom` and shows a rail icon that iframes `/plugins/doom/panel`.
- `doom_panel.py` serves that HTML (js-dos boot) + the `.jsdos` bundle at
  `/plugins/doom/doom.jsdos`.
- js-dos extracts the bundle in the browser and runs `DOOM.EXE` under DOSBox-X/WASM.

## Legal

`DOOM1.WAD` and the DOS `DOOM.EXE` shipped here are id Software's **shareware**
release of DOOM, which the shareware license permits redistributing unmodified. DOOM
© id Software. To play the full registered game, supply your own WAD via `bundle_url`.

A `protoagent-plugin` for the [protoAgent](https://github.com/protoLabsAI/protoAgent)
fleet.
