"""DOOM agent tools — the one that answers the eternal question.

``can_you_play_doom`` does two things when the agent calls it: answers *yes*, and
**drives the UI** — it emits a ``doom.play`` event on the server→console bus (ADR
0003/0039) so the console opens the DOOM view, where the panel auto-starts the game.

This is the first instance of "the AI navigates the UI for us": a tool emits a UI
intent on the event bus, and the console (subscribed via ``lib/events.ts``) acts on it.
The emit is fire-and-forget and namespaced to this plugin (``doom.*``).
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
