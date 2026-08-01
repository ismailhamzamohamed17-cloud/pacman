import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Coconut Hunter: Maze Arcade",
    page_icon="🥥",
    layout="wide"
)

# Strip Streamlit's own chrome/padding so the game can truly fill the screen
st.markdown("""<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    div[data-testid="stAppViewContainer"] { padding: 0 !important; }
    div[data-testid="stVerticalBlock"] { gap: 0 !important; }
    iframe { display:block; }
    body { overflow: hidden !important; }
</style>""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no,viewport-fit=cover">
<style>
    html, body {
        height: 100%; margin:0; padding:0; overflow:hidden;
        font-family: 'Trebuchet MS', monospace;
        -webkit-user-select:none; user-select:none;
    }
    body {
        width:100vw; height:100dvh;
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        position:relative;
        background:
            radial-gradient(circle at 78% 18%, rgba(255,224,140,0.9) 0%, rgba(255,180,90,0.55) 8%, rgba(255,140,60,0) 20%),
            linear-gradient(180deg, #1c2b52 0%, #3a3f7a 18%, #7a4f6f 38%, #d97b52 55%, #f4b860 65%, #2b6f6a 66%, #123f45 100%);
    }
    /* distant island silhouettes */
    .island { position:absolute; bottom:32%; opacity:0.55; filter:blur(0.3px); pointer-events:none; }
    .island.i1 { left:2%; width:26vw; height:9vh; background:#0d2f33; border-radius:50% 50% 0 0 / 100% 100% 0 0; }
    .island.i2 { right:4%; width:34vw; height:12vh; background:#0a2529; border-radius:50% 50% 0 0 / 100% 100% 0 0; opacity:0.7; }

    /* drifting clouds, parallax layer behind everything */
    .cloud { position:absolute; border-radius:50%; z-index:1; pointer-events:none; filter:blur(1.5px);
        background: radial-gradient(ellipse at 50% 50%, rgba(255,255,255,0.92), rgba(255,255,255,0.18) 60%, transparent 76%); }
    .cloud.c1 { top:8%; width:24vw; height:6vh; opacity:0.85; animation: driftCloud 46s linear infinite; }
    .cloud.c2 { top:16%; width:16vw; height:4.5vh; opacity:0.65; animation: driftCloud 62s linear infinite; animation-delay:-18s; }
    .cloud.c3 { top:5%; width:30vw; height:7vh; opacity:0.5; animation: driftCloud 78s linear infinite; animation-delay:-40s; }
    @keyframes driftCloud { from { transform:translateX(-32vw); } to { transform:translateX(132vw); } }

    .palm { position:absolute; bottom:31%; width:6vw; max-width:60px; min-width:26px; opacity:0.85; pointer-events:none;
        filter:drop-shadow(0 0 6px rgba(0,0,0,0.4)); z-index:2; }
    .palm svg { width:100%; height:auto; display:block; }
    .palm.p1 { left:4%; bottom:30%; transform:scale(1.3); }
    .palm.p2 { left:12%; bottom:28%; transform:scale(0.85) scaleX(-1); }
    .palm.p3 { right:6%; bottom:29%; transform:scale(1.1) scaleX(-1); }
    .palm.p4 { right:16%; bottom:26%; transform:scale(0.7); }
    /* the fronds sway independently of the outer positioning/scale transform */
    .palm-sway { transform-origin:50% 100%; animation: swayTree 4.2s ease-in-out infinite; }
    .palm-sway.sway-a { animation-duration:4.3s; }
    .palm-sway.sway-b { animation-duration:3.6s; animation-delay:-1.1s; }
    .palm-sway.sway-c { animation-duration:5.1s; animation-delay:-2.4s; }
    .palm-sway.sway-d { animation-duration:3.9s; animation-delay:-0.6s; }
    @keyframes swayTree { 0%,100% { transform: rotate(-4deg); } 50% { transform: rotate(4deg); } }

    /* ocean shimmer, animated to look like flowing water */
    .ocean-shine { position:absolute; left:0; right:0; bottom:0; height:34%; background-size:200% 100%;
        background-image: repeating-linear-gradient(100deg, rgba(255,255,255,0.06) 0px, rgba(255,255,255,0.06) 2px, transparent 2px, transparent 40px);
        pointer-events:none; mix-blend-mode: screen; animation: waveFlow 5s linear infinite; }
    @keyframes waveFlow { 0% { background-position: 0 0; } 100% { background-position: -160px 0; } }
    .sand-strip { position:absolute; left:0; right:0; bottom:0; height:6%;
        background: linear-gradient(180deg, #d9b06a 0%, #b98a4a 100%); pointer-events:none; }

    /* ---------- Loading screen ---------- */
    .loading-overlay {
        position:fixed; inset:0; z-index:99999;
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        background: radial-gradient(circle at 50% 32%, #2a5d6b 0%, #143548 45%, #081521 100%);
        transition: opacity 0.7s ease, visibility 0.7s ease;
    }
    .loading-overlay.hide { opacity:0; visibility:hidden; pointer-events:none; }
    .loading-coconut { font-size:clamp(46px,11vw,84px); animation: bounceCoconut 1.15s ease-in-out infinite;
        filter: drop-shadow(0 10px 12px rgba(0,0,0,0.55)); }
    @keyframes bounceCoconut { 0%,100% { transform: translateY(0) rotate(-10deg); } 50% { transform: translateY(-18px) rotate(10deg); } }
    .loading-title { color:#ffe9b0; font-size:clamp(18px,4.6vw,30px); font-weight:bold; letter-spacing:2px;
        margin-top:16px; text-shadow:0 2px 6px rgba(0,0,0,0.6); text-align:center; }
    .loading-sub { color:#a9c4d4; font-size:clamp(10px,2.3vw,13px); margin-top:6px; letter-spacing:1px; text-align:center; }
    .loading-bar-track { width:min(70vw,300px); height:10px; background:rgba(255,255,255,0.14);
        border-radius:6px; margin-top:24px; overflow:hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.5); }
    .loading-bar-fill { height:100%; width:0%; border-radius:6px;
        background: linear-gradient(90deg, #ffce6b, #7be39a); transition: width 1.9s cubic-bezier(.2,.7,.3,1); }

    .loading-tap-prompt { display:none; flex-direction:column; align-items:center; margin-top:26px; cursor:pointer; }
    .loading-tap-title { color:#7be39a; font-size:clamp(18px,4.4vw,28px); font-weight:bold; letter-spacing:2px;
        text-shadow:0 2px 8px rgba(0,0,0,0.6); animation: pulseTap 1.3s ease-in-out infinite; }
    .loading-tap-sub { color:#a9c4d4; font-size:clamp(10px,2.2vw,12px); margin-top:6px; letter-spacing:0.5px; }
    #loadingOverlay.ready { cursor:pointer; }
    @keyframes pulseTap { 0%,100% { transform:scale(1); opacity:1; } 50% { transform:scale(1.06); opacity:0.8; } }

    #hud {
        position:relative; z-index:5; width:min(96vw, 620px);
        display:flex; flex-direction:column; align-items:center; margin-bottom: 0.4vh;
    }
    #ticketVault { color:#ffe9b0; font-size:clamp(11px,2.4vw,14px); font-weight:bold; width:100%; text-align:left;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6); margin-bottom:2px; }
    #ui { color:#fff; font-size:clamp(12px,2.6vw,15px); font-weight:bold; width:100%;
        display:flex; justify-content:space-between; text-shadow: 0 1px 3px rgba(0,0,0,0.7); }

    #arenaWrapper {
        position:relative; z-index:4;
        display:flex; align-items:center; justify-content:center;
        flex:1 1 auto; width:100%; min-height:0;
    }
    canvas {
        border:3px solid #6b4226; border-radius:14px;
        background:#0e1a12;
        box-shadow: 0 20px 50px rgba(0,0,0,0.7), inset 0 0 40px rgba(0,0,0,0.5);
        touch-action:none; cursor:crosshair;
    }
    .msg-overlay { position:absolute; inset:0; background:rgba(10,14,10,0.94); border-radius:14px;
        display:none; flex-direction:column; align-items:center; justify-content:center; z-index:100; color:#fff; text-align:center; padding:15px; }
    .msg-title { font-size:clamp(18px,4vw,26px); font-weight:bold; margin-bottom:8px; letter-spacing:1px; }
    .msg-btn { margin-top:15px; padding:10px 24px; font-size:14px; font-weight:bold; border-radius:8px; border:none; cursor:pointer;
        text-transform:uppercase; font-family:inherit; box-shadow:0 4px 0 rgba(0,0,0,0.35); }
    .overlay-clear { color:#7be39a; text-shadow:0 0 10px rgba(123,227,154,0.5); }
    .overlay-fail { color:#ff8578; text-shadow:0 0 10px rgba(255,133,120,0.5); }
    .overlay-win { color:#ffce6b; text-shadow:0 0 12px rgba(255,206,107,0.5); }
    .overlay-warn { color:#ffce6b; text-shadow:0 0 10px rgba(255,206,107,0.4); }
    #hint { color:#f1e4c8; font-size:clamp(9px,2vw,11px); margin:4px 0 2px; text-shadow:0 1px 2px rgba(0,0,0,0.6); z-index:5; }
</style></head>
<body>
    <div id="loadingOverlay" class="loading-overlay">
        <div class="loading-coconut">🥥</div>
        <div class="loading-title">COCONUT HUNTER</div>
        <div class="loading-sub">Charting the maze islands...</div>
        <div class="loading-bar-track"><div id="loadingBarFill" class="loading-bar-fill"></div></div>
        <div id="loadingTapPrompt" class="loading-tap-prompt">
            <div class="loading-tap-title">TAP TO BEGIN</div>
            <div class="loading-tap-sub">Swipe, drag, or use arrow keys once inside</div>
        </div>
    </div>

    <div class="cloud c1"></div>
    <div class="cloud c2"></div>
    <div class="cloud c3"></div>
    <div class="island i1"></div>
    <div class="island i2"></div>
    <div class="palm p1"><div class="palm-sway sway-a"><svg viewBox="0 0 60 100"><path d="M30 100 L33 40" stroke="#3a2317" stroke-width="4" fill="none"/><g fill="#1e4d2b"><path d="M33 40 Q5 25 2 45 Q20 40 33 42Z"/><path d="M33 40 Q60 20 58 42 Q38 38 33 42Z"/><path d="M33 38 Q15 10 8 22 Q25 28 33 40Z"/><path d="M33 38 Q52 8 58 20 Q40 26 33 40Z"/><path d="M33 36 Q30 4 22 8 Q28 24 33 38Z"/></g></svg></div></div>
    <div class="palm p2"><div class="palm-sway sway-b"><svg viewBox="0 0 60 100"><path d="M30 100 L33 40" stroke="#3a2317" stroke-width="4" fill="none"/><g fill="#194023"><path d="M33 40 Q5 25 2 45 Q20 40 33 42Z"/><path d="M33 40 Q60 20 58 42 Q38 38 33 42Z"/><path d="M33 38 Q15 10 8 22 Q25 28 33 40Z"/><path d="M33 38 Q52 8 58 20 Q40 26 33 40Z"/></g></svg></div></div>
    <div class="palm p3"><div class="palm-sway sway-c"><svg viewBox="0 0 60 100"><path d="M30 100 L33 40" stroke="#3a2317" stroke-width="4" fill="none"/><g fill="#1e4d2b"><path d="M33 40 Q5 25 2 45 Q20 40 33 42Z"/><path d="M33 40 Q60 20 58 42 Q38 38 33 42Z"/><path d="M33 38 Q15 10 8 22 Q25 28 33 40Z"/><path d="M33 38 Q52 8 58 20 Q40 26 33 40Z"/></g></svg></div></div>
    <div class="palm p4"><div class="palm-sway sway-d"><svg viewBox="0 0 60 100"><path d="M30 100 L33 40" stroke="#3a2317" stroke-width="4" fill="none"/><g fill="#194023"><path d="M33 40 Q5 25 2 45 Q20 40 33 42Z"/><path d="M33 40 Q60 20 58 42 Q38 38 33 42Z"/></g></svg></div></div>
    <div class="ocean-shine"></div>
    <div class="sand-strip"></div>

    <div id="hud">
        <div id="ticketVault">🎟️ ECO VAULT TICKETS: <span id="tix">0</span></div>
        <div id="ui"><div id="stg">LEVEL 1</div><div>🥇 SCORE: <span id="sc">0</span></div><div>❤️ LIVES: <span id="lv">3</span></div></div>
    </div>

    <div id="arenaWrapper">
        <canvas id="cv"></canvas>
        <div id="clearScreen" class="msg-overlay">
            <div class="msg-title overlay-clear">LEVEL CLEARED! 🌴</div>
            <div style="color:#cbd5c9;font-size:12px;">Maze secured. Hunters regroup and speed up next round.</div>
            <button class="msg-btn" style="background:#4fae6d;color:#08210f;" onclick="confirmAdvance()">NEXT LEVEL ➡️</button>
        </div>
        <div id="caughtScreen" class="msg-overlay">
            <div class="msg-title overlay-warn">INTERCEPTED! 💥</div>
            <div style="color:#cbd5c9;font-size:12px;">A rival hunter caught you. Resetting position.</div>
            <button class="msg-btn" style="background:#e8a13e;color:#2a1600;" onclick="confirmRespawn()">REDEPLOY HUNTER 🥥</button>
        </div>
        <div id="failScreen" class="msg-overlay">
            <div class="msg-title overlay-fail">GAME OVER 💀</div>
            <div id="finalScoreInfo" style="color:#cbd5c9;font-size:12px;margin-bottom:5px;">Your final harvest has been logged.</div>
            <button class="msg-btn" style="background:#d9534f;color:#fff;" onclick="confirmRestart()">RETRY HARVEST 🔄</button>
        </div>
        <div id="victoryScreen" class="msg-overlay">
            <div class="msg-title overlay-win">GRAND CHAMPION! 👑</div>
            <div style="color:#fff;font-size:13px;font-weight:bold;line-height:1.4;">YOU CLEARED EVERY MAZE LEVEL!<br>You dominate the global leaderboard!</div>
            <button class="msg-btn" style="background:#e8a13e;color:#2a1600;" onclick="confirmRestart()">RESTART CAMPAIGN 🎮</button>
        </div>
    </div>
    <div id="hint">Swipe / drag on the maze, or use arrow keys, to steer.</div>

<script>
(function(){
"use strict";

// ================= FULL-SCREEN IFRAME TAKEOVER =================
// Streamlit embeds components.html() content in an iframe with a fixed height
// set from Python. To get genuine full-screen (PC + mobile) we reach out to
// that iframe element itself (same-origin) and stretch it to the viewport.
try {
  const frame = window.frameElement;
  if (frame) {
    frame.style.position = "fixed";
    frame.style.top = "0";
    frame.style.left = "0";
    frame.style.width = "100vw";
    frame.style.height = "100dvh";
    frame.style.zIndex = "999999";
    frame.style.border = "none";
    if (window.parent && window.parent.document && window.parent.document.body) {
      window.parent.document.body.style.overflow = "hidden";
      window.parent.document.documentElement.style.overflow = "hidden";
    }
  }
} catch(e){ /* cross-origin fallback: game still fills its own iframe */ }

// ---------- Loading screen: bar fills, "tap to begin" appears INSIDE it, then the
// overlay itself fades out into the game once tapped ----------
(function(){
  const overlay = document.getElementById("loadingOverlay");
  const fill = document.getElementById("loadingBarFill");
  const tapPrompt = document.getElementById("loadingTapPrompt");
  let ready = false;
  requestAnimationFrame(() => { fill.style.width = "100%"; });
  setTimeout(() => {
    tapPrompt.style.display = "flex";
    overlay.classList.add("ready");
    ready = true;
  }, 2100);
  overlay.addEventListener("pointerdown", function onTap(){
    if (!ready) return;
    overlay.removeEventListener("pointerdown", onTap);
    overlay.classList.add("hide");
    setTimeout(beginGame, 650);
  });
})();

// ---------- Grid / maze setup ----------
const COLS = 15, ROWS = 15, CELL = 24; // logical drawing units, scaled to fit screen
const canvas = document.getElementById("cv"), ctx = canvas.getContext("2d");
const bgCanvas = document.createElement("canvas");
bgCanvas.width = COLS*CELL; bgCanvas.height = ROWS*CELL;
const bgCtx = bgCanvas.getContext("2d");
const scEl = document.getElementById("sc"), lvEl = document.getElementById("lv"), stgEl = document.getElementById("stg"), tixEl = document.getElementById("tix");
const clearScreen = document.getElementById("clearScreen"), failScreen = document.getElementById("failScreen"),
      victoryScreen = document.getElementById("victoryScreen"), caughtScreen = document.getElementById("caughtScreen"),
      finalScoreInfo = document.getElementById("finalScoreInfo");
const arenaWrapper = document.getElementById("arenaWrapper"), hud = document.getElementById("hud");

const MAX_LEVEL = 7;
const HOUSE_R = 7, HOUSE_C = 7;
const TUNNEL_R = 7;
const PLAYER_START = { r: 11, c: 7 };
const POWER_CELLS = [[1,1],[1,13],[13,1],[13,13]];

let grid = [];
let dotsRemaining = 0;

function buildMaze(){
  grid = [];
  for (let r = 0; r < ROWS; r++){
    const row = [];
    for (let c = 0; c < COLS; c++){
      let wall = (r === 0 || r === ROWS-1 || c === 0 || c === COLS-1);
      if (!wall && r % 2 === 0 && c % 2 === 0) wall = true;
      row.push(wall ? "#" : ".");
    }
    grid.push(row);
  }
  grid[TUNNEL_R][0] = " ";
  grid[TUNNEL_R][COLS-1] = " ";
  [[HOUSE_R-1,HOUSE_C],[HOUSE_R,HOUSE_C-1],[HOUSE_R,HOUSE_C],[HOUSE_R,HOUSE_C+1],[HOUSE_R+1,HOUSE_C]]
    .forEach(([r,c]) => { grid[r][c] = " "; });
  grid[PLAYER_START.r][PLAYER_START.c] = " ";
  POWER_CELLS.forEach(([r,c]) => { grid[r][c] = "o"; });
}

function countDots(){
  let n = 0;
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
    if (grid[r][c] === "." || grid[r][c] === "o") n++;
  return n;
}

function wrapCol(c){ if (c < 0) return COLS - 1; if (c >= COLS) return 0; return c; }
function isWall(r, c){
  if (r < 0 || r >= ROWS) return true;
  c = wrapCol(c);
  return grid[r][c] === "#";
}
function cellCenter(r, c){ return { x: c*CELL + CELL/2, y: r*CELL + CELL/2 }; }

// ---------- Directions ----------
const DIRS = { up:{x:0,y:-1}, down:{x:0,y:1}, left:{x:-1,y:0}, right:{x:1,y:0}, none:{x:0,y:0} };
function isNoneDir(d){ return d.x === 0 && d.y === 0; }
function canMove(row, col, dir){
  if (isNoneDir(dir)) return false;
  return !isWall(row + dir.y, col + dir.x);
}

// ---------- Tile-based mover ----------
function tryStep(e, speedCellsPerSec, dt, onArrive){
  e.justArrived = false;
  if (isNoneDir(e.dir)){
    if (canMove(e.row, e.col, e.nextDir)){
      e.dir = e.nextDir;
      e.moveProgress = 0;
    } else {
      return;
    }
  }
  e.moveProgress += speedCellsPerSec * dt / 1000;
  let guard = 0;
  while (e.moveProgress >= 1 && guard < 4){
    guard++;
    e.moveProgress -= 1;
    e.row += e.dir.y;
    e.col = wrapCol(e.col + e.dir.x);
    e.justArrived = true;
    if (onArrive) onArrive(e);
    if (canMove(e.row, e.col, e.nextDir)){
      e.dir = e.nextDir;
    }
    if (!canMove(e.row, e.col, e.dir)){
      e.dir = DIRS.none;
      e.moveProgress = 0;
      break;
    }
  }
}

function entityPixelPos(e){
  const base = cellCenter(e.row, e.col);
  let x = base.x + e.dir.x * e.moveProgress * CELL;
  let y = base.y + e.dir.y * e.moveProgress * CELL;
  if (x < 0) x += COLS*CELL;
  if (x > COLS*CELL) x -= COLS*CELL;
  return { x, y };
}

// ---------- Responsive full-screen canvas ----------
let drawScale = 1;
function resizeCanvas(){
  const hudH = hud.offsetHeight;
  const hintH = document.getElementById("hint").offsetHeight;
  const availW = window.innerWidth;
  const availH = (window.visualViewport ? window.visualViewport.height : window.innerHeight) - hudH - hintH - 18;
  const size = Math.max(220, Math.floor(Math.min(availW * 0.98, availH * 0.98)));
  canvas.style.width = size + "px";
  canvas.style.height = size + "px";
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.floor(size * dpr);
  canvas.height = Math.floor(size * dpr);
  drawScale = (size * dpr) / (COLS * CELL);
  ctx.setTransform(drawScale, 0, 0, drawScale, 0, 0);
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
}
window.addEventListener("resize", resizeCanvas);
if (window.visualViewport) window.visualViewport.addEventListener("resize", resizeCanvas);

// ---------- Game state ----------
let score = 0, lives = 3, level = 1, gameRunning = false, lastTime = 0;
let frightenedTimer = 0, frightenedTotal = 0;
let arcadeTickets = 0;
try { arcadeTickets = parseInt(localStorage.getItem("arcade_tix_vault") || "0", 10); } catch(e){ arcadeTickets = 0; }
tixEl.innerText = arcadeTickets;

function makePlayer(){
  return { row: PLAYER_START.r, col: PLAYER_START.c, dir: DIRS.none, nextDir: DIRS.none, moveProgress: 0, mouth: 0.2, mouthDir: 1 };
}

const GHOST_COLORS = ["#ef4444", "#f472b6", "#22d3ee", "#f59e0b"];
function makeGhosts(n){
  const list = [];
  for (let i = 0; i < n; i++){
    list.push({
      row: HOUSE_R, col: HOUSE_C, dir: DIRS.up, nextDir: DIRS.up, moveProgress: 0,
      color: GHOST_COLORS[i % GHOST_COLORS.length],
      mode: "house", releaseAt: i * 1800, bob: Math.random()*Math.PI*2
    });
  }
  return list;
}

let player = makePlayer();
let ghostCount = 2;
let ghosts = makeGhosts(ghostCount);
let houseTimer = 0;

function levelSpeeds(lvl){
  return {
    player: 4.0,
    ghost: 2.6 + lvl * 0.25,
    frightened: 1.9,
    eaten: 6.6,
    frightenedDuration: Math.max(2500, 7000 - lvl*550)
  };
}
let speeds = levelSpeeds(level);

function startLevel(lvl){
  level = lvl;
  buildMaze();
  renderMazeBackground();
  dotsRemaining = countDots();
  ghostCount = Math.min(4, 1 + Math.ceil(lvl/2));
  ghosts = makeGhosts(ghostCount);
  houseTimer = 0;
  player = makePlayer();
  speeds = levelSpeeds(lvl);
  frightenedTimer = 0; frightenedTotal = 0;
  stgEl.innerText = "LEVEL " + lvl;
}

// ---------- Audio (re-themed: woody / tropical, not classic arcade bleeps) ----------
let audioCtx = null;
function setupAudio(){ if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
function noiseBurst(duration, filterFreq, gainVal){
  const bufferSize = Math.floor(audioCtx.sampleRate * duration);
  const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) data[i] = (Math.random()*2 - 1) * (1 - i/bufferSize);
  const src = audioCtx.createBufferSource(); src.buffer = buffer;
  const filt = audioCtx.createBiquadFilter(); filt.type = "bandpass"; filt.frequency.value = filterFreq; filt.Q.value = 1.1;
  const gain = audioCtx.createGain(); gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
  src.connect(filt); filt.connect(gain); gain.connect(audioCtx.destination);
  src.start();
}
function sound(type){
  setupAudio(); if (!audioCtx) return;
  const t = audioCtx.currentTime;
  if (type === "waka"){
    noiseBurst(0.07, 900, 0.35);
  } else if (type === "power"){
    const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = "sine"; osc.frequency.setValueAtTime(180, t); osc.frequency.linearRampToValueAtTime(110, t+0.35);
    gain.gain.setValueAtTime(0.001, t); gain.gain.linearRampToValueAtTime(0.22, t+0.06); gain.gain.linearRampToValueAtTime(0.001, t+0.4);
    osc.start(); osc.stop(t+0.4);
  } else if (type === "eatghost"){
    const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = "sawtooth"; osc.frequency.setValueAtTime(160,t); osc.frequency.exponentialRampToValueAtTime(760,t+0.18);
    gain.gain.setValueAtTime(0.18,t); gain.gain.exponentialRampToValueAtTime(0.001,t+0.2);
    osc.start(); osc.stop(t+0.2);
  } else if (type === "lose"){
    const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = "triangle"; osc.frequency.setValueAtTime(300,t); osc.frequency.exponentialRampToValueAtTime(70,t+0.4);
    gain.gain.setValueAtTime(0.22,t); gain.gain.exponentialRampToValueAtTime(0.001,t+0.4);
    osc.start(); osc.stop(t+0.4);
    noiseBurst(0.12, 500, 0.15);
  } else if (type === "boom"){
    const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = "sine"; osc.frequency.setValueAtTime(120,t); osc.frequency.exponentialRampToValueAtTime(35,t+0.5);
    gain.gain.setValueAtTime(0.5,t); gain.gain.exponentialRampToValueAtTime(0.001,t+0.55);
    osc.start(); osc.stop(t+0.55);
    noiseBurst(0.25, 200, 0.25);
  } else if (type === "level"){
    [392.0, 493.88, 587.33, 783.99].forEach((f, i) => {
      const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.type = "sine"; osc.frequency.setValueAtTime(f, t + i*0.09);
      gain.gain.setValueAtTime(0.001, t + i*0.09);
      gain.gain.linearRampToValueAtTime(0.2, t + i*0.09 + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, t + i*0.09 + 0.25);
      osc.start(t + i*0.09); osc.stop(t + i*0.09 + 0.28);
    });
  }
}

// ---------- Input ----------
let dragStart = null;
function setPlayerDir(dx, dy){
  if (Math.abs(dx) > Math.abs(dy)) player.nextDir = dx > 0 ? DIRS.right : DIRS.left;
  else if (dy !== 0) player.nextDir = dy > 0 ? DIRS.down : DIRS.up;
}
canvas.addEventListener("pointerdown", (e) => { dragStart = { x: e.clientX, y: e.clientY }; setupAudio(); });
canvas.addEventListener("pointerup", (e) => {
  if (!dragStart || !gameRunning) return;
  const dx = e.clientX - dragStart.x, dy = e.clientY - dragStart.y;
  if (Math.hypot(dx, dy) < 12){
    const rect = canvas.getBoundingClientRect();
    const pos = entityPixelPos(player);
    const scaleX = rect.width / (COLS*CELL), scaleY = rect.height / (ROWS*CELL);
    const cx = rect.left + pos.x*scaleX, cy = rect.top + pos.y*scaleY;
    setPlayerDir(e.clientX - cx, e.clientY - cy);
  } else {
    setPlayerDir(dx, dy);
  }
  dragStart = null;
});
window.addEventListener("keydown", (e) => {
  if (!gameRunning) return;
  if (e.key === "ArrowUp" || e.key === "w") player.nextDir = DIRS.up;
  else if (e.key === "ArrowDown" || e.key === "s") player.nextDir = DIRS.down;
  else if (e.key === "ArrowLeft" || e.key === "a") player.nextDir = DIRS.left;
  else if (e.key === "ArrowRight" || e.key === "d") player.nextDir = DIRS.right;
});

// ---------- Overlays / flow control ----------
window.confirmAdvance = function(){
  clearScreen.style.display = "none";
  gameRunning = true; lastTime = 0;
  if (level >= MAX_LEVEL){ victoryScreen.style.display = "flex"; gameRunning = false; return; }
  startLevel(level + 1);
  requestAnimationFrame(loop);
};
window.confirmRestart = function(){
  failScreen.style.display = "none"; victoryScreen.style.display = "none";
  score = 0; scEl.innerText = 0; lives = 3; lvEl.innerText = 3;
  gameRunning = true; lastTime = 0;
  startLevel(1);
  requestAnimationFrame(loop);
};
window.confirmRespawn = function(){
  caughtScreen.style.display = "none";
  gameRunning = true; lastTime = 0;
  player = makePlayer();
  ghosts.forEach(g => { g.mode = "house"; g.row = HOUSE_R; g.col = HOUSE_C; g.dir = DIRS.up; g.nextDir = DIRS.up; g.moveProgress = 0; });
  houseTimer = 0;
  requestAnimationFrame(loop);
};

// ---------- Ghost AI ----------
function chooseGhostDir(g, target, avoid){
  const opts = ["up","down","left","right"].map(k => DIRS[k]).filter(d => canMove(g.row, g.col, d));
  if (opts.length === 0) return DIRS.none;
  const reverse = { x: -g.dir.x, y: -g.dir.y };
  let filtered = opts.filter(d => !(d.x === reverse.x && d.y === reverse.y));
  if (filtered.length === 0) filtered = opts;
  let best = filtered[0], bestScore = -Infinity;
  filtered.forEach(d => {
    const nx = g.col + d.x, ny = g.row + d.y;
    const dist = Math.hypot(nx - target.c, ny - target.r);
    const score = avoid ? dist : -dist;
    const jitter = Math.random() * 0.35;
    if (score + jitter > bestScore){ bestScore = score + jitter; best = d; }
  });
  return best;
}

function updateGhost(g, dt){
  if (g.mode === "house"){
    g.bob += dt * 0.006;
    if (houseTimer >= g.releaseAt){
      g.mode = "chase";
      g.row = HOUSE_R; g.col = HOUSE_C; g.moveProgress = 0;
      g.dir = DIRS.up; g.nextDir = DIRS.up;
    }
    return;
  }
  let speed, target, avoid = false;
  if (g.mode === "eaten"){
    speed = speeds.eaten; target = { r: HOUSE_R, c: HOUSE_C };
  } else if (g.mode === "frightened"){
    speed = speeds.frightened; target = { r: player.row, c: player.col }; avoid = true;
  } else {
    speed = speeds.ghost; target = { r: player.row, c: player.col };
  }
  tryStep(g, speed, dt, (ghost) => {
    ghost.nextDir = chooseGhostDir(ghost, target, avoid);
    if (ghost.mode === "eaten" && ghost.row === HOUSE_R && ghost.col === HOUSE_C){
      ghost.mode = "chase";
      ghost.dir = DIRS.up; ghost.nextDir = DIRS.up;
    }
  });
}

// ---------- Themed maze backgrounds ----------
// Each level gets a distinct material (not just a re-tinted version of the same
// blocky wall) rendered once into an offscreen canvas -- floor grain, wall
// bevels/shadows and per-theme decoration (moss, wood grain, coral, lava
// cracks, ice shine, sand ripples, gold filigree) are baked in a single time
// per level instead of redrawn every frame, which keeps it both nicer-looking
// and cheap to render at 60fps.
const THEMES = [
  { label:"mossy temple",   wall:["#5b6b4a","#26301f"], floor:["#182a1c","#070d08"], accent:"#9fce6a", decor:"moss"  },
  { label:"bamboo grove",   wall:["#8a6a3c","#402d16"], floor:["#28200f","#100b05"], accent:"#d9b25f", decor:"wood"  },
  { label:"coral reef",     wall:["#4d7691","#1c2e3d"], floor:["#0c2230","#03090d"], accent:"#7fe0d1", decor:"coral" },
  { label:"volcanic rock",  wall:["#6b3324","#2a120c"], floor:["#1c0c09","#090302"], accent:"#ff8a4c", decor:"lava"  },
  { label:"ice cavern",     wall:["#6a97b3","#233f52"], floor:["#0e1e28","#040b10"], accent:"#e6f6ff", decor:"ice"   },
  { label:"desert dune",    wall:["#b08a44","#4f3a1a"], floor:["#2a2010","#0f0a04"], accent:"#f0d089", decor:"sand"  },
  { label:"golden temple",  wall:["#9c7a1e","#3a2c09"], floor:["#241b06","#0c0902"], accent:"#ffe27a", decor:"gold"  }
];

function currentTheme(){ return THEMES[(level-1) % THEMES.length]; }

function decorateWallCell(c, x, y, theme, seed){
  const rnd = (n) => { const v = Math.sin(seed*127.1 + n*311.7) * 43758.5453; return v - Math.floor(v); };
  c.save();
  c.beginPath(); c.rect(x+1, y+1, CELL-2, CELL-2); c.clip();
  if (theme.decor === "moss"){
    if (rnd(1) > 0.45){
      c.fillStyle = "rgba(140,190,90,0.35)";
      c.beginPath(); c.arc(x+CELL*rnd(2), y+CELL*rnd(3), 4+rnd(4)*3, 0, Math.PI*2); c.fill();
    }
  } else if (theme.decor === "wood"){
    c.strokeStyle = "rgba(0,0,0,0.28)"; c.lineWidth = 1;
    for (let i=0;i<3;i++){ const gy = y+5+i*7; c.beginPath(); c.moveTo(x+1,gy); c.lineTo(x+CELL-1,gy+(rnd(i+5)-0.5)*2); c.stroke(); }
  } else if (theme.decor === "coral"){
    c.fillStyle = "rgba(255,255,255,0.14)";
    for (let i=0;i<3;i++){ c.beginPath(); c.arc(x+CELL*rnd(i+2), y+CELL*rnd(i+6), 2.2, 0, Math.PI*2); c.fill(); }
  } else if (theme.decor === "lava"){
    c.strokeStyle = "rgba(255,138,76,0.85)"; c.lineWidth = 1.4;
    c.shadowColor = "rgba(255,120,50,0.9)"; c.shadowBlur = 4;
    c.beginPath(); c.moveTo(x+3, y+3+rnd(1)*6); c.lineTo(x+CELL*0.5, y+CELL*0.5+(rnd(2)-0.5)*8); c.lineTo(x+CELL-3, y+CELL-4-rnd(3)*6); c.stroke();
  } else if (theme.decor === "ice"){
    c.strokeStyle = "rgba(255,255,255,0.35)"; c.lineWidth = 1;
    c.beginPath(); c.moveTo(x+2, y+CELL-2); c.lineTo(x+CELL-2, y+2); c.stroke();
    c.fillStyle = "rgba(255,255,255,0.5)";
    c.beginPath(); c.arc(x+CELL*rnd(4), y+CELL*rnd(5), 1.1, 0, Math.PI*2); c.fill();
  } else if (theme.decor === "sand"){
    c.strokeStyle = "rgba(0,0,0,0.18)"; c.lineWidth = 1;
    for (let i=0;i<2;i++){ const gy=y+8+i*9; c.beginPath(); c.moveTo(x+1,gy); c.quadraticCurveTo(x+CELL/2, gy-3, x+CELL-1, gy); c.stroke(); }
  } else if (theme.decor === "gold"){
    c.strokeStyle = "rgba(255,226,122,0.55)"; c.lineWidth = 1;
    c.beginPath(); c.moveTo(x+3,y+CELL-3); c.lineTo(x+CELL-3,y+3); c.stroke();
    c.fillStyle = "rgba(255,226,122,0.45)";
    c.beginPath(); c.arc(x+CELL/2, y+CELL/2, 1.6, 0, Math.PI*2); c.fill();
  }
  c.restore();
}

function drawThemedWall(c, x, y, theme, seed){
  c.save();
  c.shadowColor = "rgba(0,0,0,0.55)"; c.shadowBlur = 4; c.shadowOffsetY = 3;
  const g = c.createLinearGradient(x, y, x, y+CELL);
  g.addColorStop(0, theme.wall[0]); g.addColorStop(1, theme.wall[1]);
  c.fillStyle = g;
  c.fillRect(x+1, y+1, CELL-2, CELL-2);
  c.restore();
  decorateWallCell(c, x, y, theme, seed);
  // bevel highlight (light source top-left) + shadow (bottom-right) for a carved 3D look
  c.strokeStyle = "rgba(255,255,255,0.16)"; c.lineWidth = 1.1;
  c.beginPath(); c.moveTo(x+1, y+CELL-2); c.lineTo(x+1, y+1); c.lineTo(x+CELL-2, y+1); c.stroke();
  c.strokeStyle = "rgba(0,0,0,0.55)"; c.lineWidth = 1.1;
  c.beginPath(); c.moveTo(x+CELL-1, y+1); c.lineTo(x+CELL-1, y+CELL-1); c.lineTo(x+1, y+CELL-1); c.stroke();
}

function renderMazeBackground(){
  const theme = currentTheme();
  const W = COLS*CELL, H = ROWS*CELL;
  bgCtx.clearRect(0, 0, W, H);
  const floorGrad = bgCtx.createRadialGradient(W/2, H/2, 20, W/2, H/2, W*0.75);
  floorGrad.addColorStop(0, theme.floor[0]);
  floorGrad.addColorStop(1, theme.floor[1]);
  bgCtx.fillStyle = floorGrad; bgCtx.fillRect(0, 0, W, H);
  // subtle floor grain for texture instead of a flat fill
  for (let i = 0; i < 260; i++){
    const gx = Math.random()*W, gy = Math.random()*H;
    bgCtx.fillStyle = "rgba(255,255,255," + (Math.random()*0.035).toFixed(3) + ")";
    bgCtx.fillRect(gx, gy, 1, 1);
  }
  for (let r = 0; r < ROWS; r++){
    for (let c2 = 0; c2 < COLS; c2++){
      if (grid[r][c2] === "#"){
        drawThemedWall(bgCtx, c2*CELL, r*CELL, theme, r*COLS + c2 + level*97);
      }
    }
  }
  bgCtx.strokeStyle = theme.accent; bgCtx.lineWidth = 2.4; bgCtx.globalAlpha = 0.8;
  bgCtx.strokeRect(1.5, 1.5, W-3, H-3);
  bgCtx.globalAlpha = 1;
}

// ---------- Drawing ----------
function drawMaze(){
  ctx.drawImage(bgCanvas, 0, 0);

  for (let r = 0; r < ROWS; r++){
    for (let c = 0; c < COLS; c++){
      const cell = grid[r][c];
      const cx = c*CELL+CELL/2, cy = r*CELL+CELL/2;
      if (cell === "."){
        drawCoconutDot(cx, cy, 3.4);
      } else if (cell === "o"){
        const pulse = 5.6 + Math.sin(performance.now()*0.006)*1.2;
        drawCoconutDot(cx, cy, pulse, true);
      }
    }
  }
}

function drawCoconutDot(cx, cy, r, glow){
  ctx.save();
  if (glow){
    ctx.shadowColor = "rgba(255,224,150,0.7)";
    ctx.shadowBlur = 8;
  }
  const grad = ctx.createRadialGradient(cx-r*0.35, cy-r*0.35, r*0.15, cx, cy, r);
  grad.addColorStop(0, "#8a5a34");
  grad.addColorStop(0.55, "#5c3a20");
  grad.addColorStop(1, "#2e1c10");
  ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI*2); ctx.fillStyle = grad; ctx.fill();
  ctx.restore();
  ctx.fillStyle = "rgba(20,10,5,0.65)";
  const s = r * 0.28;
  ctx.beginPath(); ctx.arc(cx - r*0.28, cy - r*0.05, s*0.4, 0, Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.arc(cx + r*0.05, cy - r*0.3, s*0.4, 0, Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.arc(cx + r*0.25, cy + r*0.15, s*0.4, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = "rgba(255,240,210,0.5)";
  ctx.beginPath(); ctx.arc(cx - r*0.4, cy - r*0.4, r*0.22, 0, Math.PI*2); ctx.fill();
  ctx.strokeStyle = "rgba(255,255,255,0.22)"; ctx.lineWidth = Math.max(0.6, r*0.14);
  ctx.beginPath(); ctx.arc(cx, cy, r*0.9, Math.PI*1.1, Math.PI*1.6); ctx.stroke();
}

function drawShadowUnder(x, y, r){
  ctx.save();
  ctx.beginPath();
  ctx.ellipse(x, y + r*0.75, r*0.9, r*0.32, 0, 0, Math.PI*2);
  ctx.fillStyle = "rgba(0,0,0,0.45)";
  ctx.fill();
  ctx.restore();
}

function drawPlayer(){
  player.mouth += player.mouthDir * 0.012;
  if (player.mouth > 0.42 || player.mouth < 0.04) player.mouthDir *= -1;
  const pos = entityPixelPos(player);
  const d = player.dir;
  const rot = d.x>0?0:(d.x<0?Math.PI:(d.y>0?Math.PI/2:(d.y<0?Math.PI*1.5:0)));

  drawShadowUnder(pos.x, pos.y, 10);

  // husk body with deeper, more natural coconut-brown shading
  ctx.save();
  ctx.shadowColor = "rgba(0,0,0,0.55)";
  ctx.shadowBlur = 6;
  ctx.shadowOffsetY = 2.5;
  ctx.beginPath();
  const grad = ctx.createRadialGradient(pos.x-4, pos.y-4.5, 1.5, pos.x, pos.y, 10.5);
  grad.addColorStop(0, "#a9754a");
  grad.addColorStop(0.35, "#7c4f2c");
  grad.addColorStop(0.72, "#4c2f1a");
  grad.addColorStop(1, "#2a1a0d");
  ctx.arc(pos.x, pos.y, 10.5, rot+player.mouth, rot+Math.PI*2-player.mouth);
  ctx.lineTo(pos.x, pos.y); ctx.fillStyle = grad; ctx.fill();
  ctx.restore();

  // fibrous husk striations, clipped to the body so they follow the sphere
  ctx.save();
  ctx.beginPath();
  ctx.arc(pos.x, pos.y, 10.3, rot+player.mouth, rot+Math.PI*2-player.mouth);
  ctx.lineTo(pos.x, pos.y);
  ctx.clip();
  ctx.strokeStyle = "rgba(0,0,0,0.28)"; ctx.lineWidth = 0.6;
  for (let i=0;i<7;i++){
    const a = (i/7) * Math.PI*2;
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 4+(i%3)*2, a, a+0.5);
    ctx.stroke();
  }
  ctx.restore();

  // pale coconut flesh visible in the "bite" opening
  ctx.beginPath();
  ctx.moveTo(pos.x, pos.y);
  ctx.arc(pos.x, pos.y, 9.6, rot-player.mouth, rot+player.mouth);
  ctx.closePath();
  const fleshGrad = ctx.createRadialGradient(pos.x, pos.y, 1, pos.x, pos.y, 9.6);
  fleshGrad.addColorStop(0, "#fdf6e8");
  fleshGrad.addColorStop(1, "#e8d7ae");
  ctx.fillStyle = fleshGrad;
  ctx.fill();

  // soft moving specular highlight for a glossy, lit-from-above look
  ctx.beginPath();
  ctx.arc(pos.x-3, pos.y-4, 2.6, 0, Math.PI*2);
  ctx.fillStyle = "rgba(255,240,220,0.55)";
  ctx.fill();
}

function drawGhost(g){
  const r = 10;
  let pos;
  if (g.mode === "house"){
    const hc = cellCenter(HOUSE_R, HOUSE_C);
    pos = { x: hc.x, y: hc.y + Math.sin(g.bob) * 3 };
  } else {
    pos = entityPixelPos(g);
  }

  if (g.mode !== "house") drawShadowUnder(pos.x, pos.y, 10);

  ctx.beginPath();
  let color = g.color;
  if (g.mode === "frightened"){
    const flashing = frightenedTimer < 1500 && Math.floor(frightenedTimer/200)%2===0;
    color = flashing ? "#e0f2fe" : "#1d4ed8";
  }
  if (g.mode === "eaten"){
    ctx.fillStyle = "#e5e7eb";
    ctx.beginPath(); ctx.arc(pos.x-3.5, pos.y-2, 2.4, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    ctx.beginPath(); ctx.arc(pos.x+3.5, pos.y-2, 2.4, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    ctx.fillStyle = "#0f172a";
    ctx.beginPath(); ctx.arc(pos.x-3.5, pos.y-2, 1.1, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    ctx.beginPath(); ctx.arc(pos.x+3.5, pos.y-2, 1.1, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    return;
  }
  ctx.save();
  ctx.shadowColor = "rgba(0,0,0,0.45)"; ctx.shadowBlur = 5; ctx.shadowOffsetY = 2;
  const grad = ctx.createRadialGradient(pos.x-3, pos.y-3, 1, pos.x, pos.y, r);
  grad.addColorStop(0, "#ffffff"); grad.addColorStop(0.3, color); grad.addColorStop(1, "#020617");
  ctx.arc(pos.x, pos.y, r, Math.PI, 0);
  const wob = Math.sin(performance.now()*0.01 + pos.x*0.2) * 2;
  ctx.lineTo(pos.x+r, pos.y+r);
  ctx.lineTo(pos.x+r*0.5, pos.y+r-wob);
  ctx.lineTo(pos.x, pos.y+r);
  ctx.lineTo(pos.x-r*0.5, pos.y+r-wob);
  ctx.lineTo(pos.x-r, pos.y+r);
  ctx.closePath();
  ctx.fillStyle = grad; ctx.fill();
  ctx.restore();

  // rim light echoing the current maze's theme accent color, for cohesive lighting
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  ctx.strokeStyle = currentTheme().accent;
  ctx.globalAlpha = 0.28;
  ctx.lineWidth = 1.4;
  ctx.beginPath(); ctx.arc(pos.x, pos.y-1, r-1, Math.PI*1.15, Math.PI*1.85); ctx.stroke();
  ctx.restore();

  ctx.fillStyle = "#ffffff";
  ctx.beginPath(); ctx.arc(pos.x-3.5, pos.y-1, 2.6, 0, Math.PI*2); ctx.fill(); ctx.closePath();
  ctx.beginPath(); ctx.arc(pos.x+3.5, pos.y-1, 2.6, 0, Math.PI*2); ctx.fill(); ctx.closePath();
  ctx.save();
  ctx.shadowColor = "rgba(120,200,255,0.9)"; ctx.shadowBlur = 3;
  ctx.fillStyle = "#0f172a";
  const ex = g.dir.x*1.2, ey = g.dir.y*1.2;
  ctx.beginPath(); ctx.arc(pos.x-3.5+ex, pos.y-1+ey, 1.2, 0, Math.PI*2); ctx.fill(); ctx.closePath();
  ctx.beginPath(); ctx.arc(pos.x+3.5+ex, pos.y-1+ey, 1.2, 0, Math.PI*2); ctx.fill(); ctx.closePath();
  ctx.restore();
}

// cinematic vignette + soft top-light wash, drawn over the whole scene each
// frame so it reads less like a flat sprite sheet and more like a lit diorama
function drawVignette(){
  const W = COLS*CELL, H = ROWS*CELL;
  const light = ctx.createRadialGradient(W*0.5, H*0.18, 4, W*0.5, H*0.5, H*0.62);
  light.addColorStop(0, "rgba(255,255,255,0.06)");
  light.addColorStop(0.5, "rgba(255,255,255,0)");
  light.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = light;
  ctx.fillRect(0, 0, W, H);
  const vg = ctx.createRadialGradient(W/2, H*0.46, H*0.18, W/2, H/2, H*0.74);
  vg.addColorStop(0, "rgba(0,0,0,0)");
  vg.addColorStop(0.72, "rgba(0,0,0,0.06)");
  vg.addColorStop(1, "rgba(0,0,0,0.4)");
  ctx.fillStyle = vg;
  ctx.fillRect(0, 0, W, H);
}

// ---------- Main loop ----------
function loop(timestamp){
  if (!gameRunning) return;
  if (!lastTime) lastTime = timestamp;
  let dt = timestamp - lastTime;
  if (dt > 60) dt = 60;
  lastTime = timestamp;

  if (frightenedTimer > 0){
    frightenedTimer -= dt;
    if (frightenedTimer <= 0){
      frightenedTimer = 0;
      ghosts.forEach(g => { if (g.mode === "frightened") g.mode = "chase"; });
    }
  }

  drawMaze();

  houseTimer += dt;

  tryStep(player, speeds.player, dt, (p) => {
    const cell = grid[p.row] ? grid[p.row][p.col] : undefined;
    if (cell === "."){
      grid[p.row][p.col] = " "; dotsRemaining--; score += 10; scEl.innerText = score; sound("waka");
      arcadeTickets += 1; try { localStorage.setItem("arcade_tix_vault", arcadeTickets.toString()); } catch(e){}
      tixEl.innerText = arcadeTickets;
    } else if (cell === "o"){
      grid[p.row][p.col] = " "; dotsRemaining--; score += 50; scEl.innerText = score; sound("power");
      frightenedTimer = speeds.frightenedDuration; frightenedTotal = speeds.frightenedDuration;
      ghosts.forEach(g => { if (g.mode !== "house" && g.mode !== "eaten") g.mode = "frightened"; });
    }
  });

  ghosts.forEach(g => updateGhost(g, dt));

  drawPlayer();
  ghosts.forEach(drawGhost);
  drawVignette();

  const playerPos = entityPixelPos(player);
  for (const g of ghosts){
    if (g.mode === "house") continue;
    const gPos = entityPixelPos(g);
    if (Math.hypot(playerPos.x - gPos.x, playerPos.y - gPos.y) < 13){
      if (g.mode === "frightened"){
        g.mode = "eaten"; score += 200; scEl.innerText = score; sound("eatghost");
      } else if (g.mode === "chase"){
        lives--; lvEl.innerText = lives;
        gameRunning = false;
        if (lives <= 0){ sound("boom"); finalScoreInfo.innerText = "Final Operation Score: " + score; failScreen.style.display = "flex"; }
        else { sound("lose"); caughtScreen.style.display = "flex"; }
        return;
      }
    }
  }

  if (dotsRemaining <= 0){
    gameRunning = false; sound("level");
    if (level >= MAX_LEVEL) victoryScreen.style.display = "flex";
    else clearScreen.style.display = "flex";
    return;
  }

  requestAnimationFrame(loop);
}

// ---------- Begin flow (triggered from the loading overlay's own tap prompt) ----------
function beginGame(){
  setupAudio(); sound("level");
  gameRunning = true; startLevel(1); lastTime = 0;
  requestAnimationFrame(loop);
}

buildMaze();
renderMazeBackground();
resizeCanvas();
drawMaze();
drawVignette();
setTimeout(resizeCanvas, 60); // second pass once layout has settled (mobile browser chrome)

})();
</script></body></html>
"""

components.html(game_html, height=900, scrolling=False)
