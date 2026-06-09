# DOOM — a protoAgent plugin

> *But can it run DOOM?* **Yes.**

A console-only protoAgent plugin (ADR 0026) that adds a **DOOM** view to the operator
console. It runs the shareware **DOOM (Episode 1)** in your browser via
[js-dos](https://js-dos.com) (DOSBox-X compiled to WebAssembly) — you play in-panel
with the keyboard.

The game itself (`DOOM.EXE` + `DOOM1.WAD`, id Software's freely-redistributable
shareware) is **self-hosted** by the plugin and served same-origin; only the js-dos
runtime loads from the js-dos CDN. No tools, no agent surface, no network egress for
the game data — pure operator fun.

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
