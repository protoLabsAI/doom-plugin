// Single-player boot for the prboom WASM engine (websockets-doom.js — GPL prboom
// compiled to WebAssembly, github.com/cloudflare/doom-wasm). The engine reads
// window.Module; we preload the shareware WAD into its in-memory FS and run prboom
// windowed. The reference's multiplayer/websocket path is dropped — this is pure
// single-player, no network, no DOS layer.
window.Module = {
  // prboom args: shareware IWAD, windowed, skip the startup GUI, music off (SFX stay).
  arguments: ["-iwad", "doom1.wad", "-window", "-nogui", "-nomusic"],

  // Fetch the WAD (same-origin, served by the plugin) into the engine FS before main.
  preRun: [
    function () {
      Module.FS.createPreloadedFile("", "doom1.wad", "doom1.wad", true, true);
    },
  ],

  canvas: (function () {
    // NB: the engine hardcodes document.getElementById("canvas") for input handler
    // registration (websockets-doom.js), so the canvas MUST be id="canvas".
    var c = document.getElementById("canvas");
    // Don't pop the browser menu on right-click (DOOM uses it), and take keyboard focus.
    c.addEventListener("contextmenu", function (e) { e.preventDefault(); });
    c.addEventListener("click", function () { c.focus(); });
    return c;
  })(),

  // The .wasm sits next to the panel page (served by the plugin) — resolve by name.
  locateFile: function (path) { return path; },

  setStatus: function (text) {
    var el = document.getElementById("status");
    if (el) el.textContent = text || "";
  },
  printErr: function (text) { try { console.warn("[doom]", text); } catch (e) {} },

  onRuntimeInitialized: function () {
    var el = document.getElementById("status");
    if (el) el.style.display = "none";
  },
};
