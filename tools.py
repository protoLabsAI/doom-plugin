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
        # Drive the UI: tell the console to open + focus the DOOM view. The panel's
        # js-dos boots the game automatically (autoStart). Fire-and-forget — if no
        # console is connected, the answer is still returned.
        registry.emit("play", {"view": "doom", "episode": 1, "level": "E1M1"})
        return ("Yes — I can run DOOM. Opening it now and dropping into E1M1. "
                "Rip and tear. \U0001f52b")

    return [can_you_play_doom]
