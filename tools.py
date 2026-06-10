"""DOOM agent tools — the one that answers the eternal question.

``can_you_play_doom`` does two things when the agent calls it: answers *yes*, and
**drives the UI** — it calls ``registry.navigate("panel")`` (ADR 0044 plugin-driven
navigation) so the console opens this plugin's DOOM view, where the panel auto-starts
the game.

This is "the AI navigates the UI for us": a tool issues a host navigation intent
naming one of the plugin's own views, and the console acts on it. ``navigate`` is
fire-and-forget — if no console is connected the answer is still returned. It's a host
intent, not a plugin event, so the plugin declares nothing under ``emits``.
"""

from __future__ import annotations


def make_tools(registry):
    from langchain_core.tools import tool

    @tool
    def can_you_play_doom() -> str:
        """Answer the question "can you run/play DOOM?" — and prove it.

        Use this whenever the operator asks whether you can run DOOM, play DOOM, or
        "but can it run DOOM". It opens the DOOM view in the console and starts a game
        (Episode 1, E1M1). Returns a short confirmation to say back to the operator.
        """
        # Plugin-driven UI navigation (ADR 0044): ask the console to open this plugin's
        # DOOM view. The panel's WASM prboom engine boots the game automatically.
        # Fire-and-forget — if no console is connected, the answer is still returned.
        registry.navigate("panel")
        return ("Yes — I can run DOOM. Opening it now and dropping into E1M1. "
                "Rip and tear. \U0001f52b")

    return [can_you_play_doom]
