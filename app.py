<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>Coconut Hunter: Maze Arcade</title>
<style>
  html,body { background:#030712; margin:0; padding:0; }
  body { min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:'Courier New',monospace; user-select:none; -webkit-user-select:none; padding:14px 0 30px; }
  .cab { background:#060913; padding:14px; border-radius:18px; border:2px solid #1e1b4b; text-align:center; max-width:400px; margin:auto; box-shadow:0 20px 60px rgba(0,0,0,0.6); }
  .bn { background:#0f172a; padding:12px; border-radius:10px; color:#e2e8f0; font-size:12px; text-align:left; margin-bottom:12px; border:1px solid #334155; }
  .bn b { color:#facc15; }
  #ticketVault { color:#10b981; font-size:13px; font-weight:bold; text-align:left; margin-bottom:4px; }
  #ui { color:#fff; font-size:14px; font-weight:bold; display:flex; justify-content:space-between; margin:6px 0; letter-spacing:0.5px; }
  #arenaWrapper { position:relative; width:360px; height:360px; margin:auto; }
  canvas { border:3px solid #10b981; background:#020617; border-radius:12px; width:360px; height:360px; box-shadow:0 16px 40px rgba(0,0,0,0.85); touch-action:none; cursor:crosshair; display:block; }
  .msg-overlay { position:absolute; inset:0; background:rgba(2,6,23,0.94); border-radius:12px; display:none; flex-direction:column; align-items:center; justify-content:center; z-index:100; color:#fff; text-align:center; padding:15px; }
  .msg-title { font-size:24px; font-weight:bold; margin-bottom:8px; font-family:sans-serif; letter-spacing:1px; }
  .msg-btn { margin-top:15px; padding:10px 24px; font-size:14px; font-weight:bold; border-radius:6px; border:none; cursor:pointer; text-transform:uppercase; font-family:monospace; }
  .overlay-clear { color:#10b981; text-shadow:0 0 10px rgba(16,185,129,0.4); }
  .overlay-fail { color:#ef4444; text-shadow:0 0 10px rgba(239,68,68,0.4); }
  .overlay-win { color:#f59e0b; text-shadow:0 0 12px rgba(245,158,11,0.5); }
  .overlay-warn { color:#f59e0b; text-shadow:0 0 10px rgba(245,158,11,0.4); }
  .ad-slot { width:360px; height:50px; background:#0f172a; border:1px dashed #1e293b; border-radius:6px; margin-top:15px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#475569; font-size:10px; }
  #hint { color:#64748b; font-size:11px; margin-top:8px; }
</style>
</head>
<body>
<div class="cab">
  <div class="bn"><b>🥥 COCONUT HUNTER: MAZE PROTOCOL</b><br>Real corridors, real walls, a ghost den in the center, and side tunnels that wrap around. Grab a power pellet to turn the hunters blue and eat them back.</div>
  <div id="ticketVault">🎟️ ECO VAULT TICKETS: <span id="tix">0</span></div>
  <div id="ui"><div id="stg">LEVEL 1</div><div>🥇 SCORE: <span id="sc">0</span></div><div>❤️ LIVES: <span id="lv">3</span></div></div>
  <div id="arenaWrapper">
    <canvas id="cv" width="360" height="360"></canvas>
    <div id="clearScreen" class="msg-overlay">
      <div class="msg-title overlay-clear">LEVEL CLEARED! 🌴</div>
      <div style="color:#94a3b8;font-size:12px;">Maze secured. Hunters regroup and speed up next round.</div>
      <button class="msg-btn" style="background:#10b981;color:#000;" onclick="confirmAdvance()">NEXT LEVEL ➡️</button>
    </div>
    <div id="caughtScreen" class="msg-overlay">
      <div class="msg-title overlay-warn">INTERCEPTED! 💥</div>
      <div style="color:#94a3b8;font-size:12px;">A rival hunter caught you. Resetting position.</div>
      <button class="msg-btn" style="background:#f59e0b;color:#000;" onclick="confirmRespawn()">REDEPLOY HUNTER 🥥</button>
    </div>
    <div id="failScreen" class="msg-overlay">
      <div class="msg-title overlay-fail">GAME OVER 💀</div>
      <div id="finalScoreInfo" style="color:#94a3b8;font-size:12px;margin-bottom:5px;">Your final harvest has been logged.</div>
      <button class="msg-btn" style="background:#ef4444;color:#fff;" onclick="confirmRestart()">RETRY HARVEST 🔄</button>
    </div>
    <div id="victoryScreen" class="msg-overlay">
      <div class="msg-title overlay-win">GRAND CHAMPION! 👑</div>
      <div style="color:#fff;font-size:13px;font-weight:bold;line-height:1.4;">YOU CLEARED EVERY MAZE LEVEL!<br>You dominate the global leaderboard!</div>
      <button class="msg-btn" style="background:#f59e0b;color:#000;" onclick="confirmRestart()">RESTART CAMPAIGN 🎮</button>
    </div>
  </div>
  <div id="hint">Swipe / drag on the maze, or use arrow keys, to steer.</div>
  <div class="ad-slot">
    <div style="font-weight:bold;color:#475569;">ADVERTISEMENT REVENUE STREAM</div>
    <div style="font-size:8px;color:#334155;">Google AdSense Mobile H5 SDK Container Slot</div>
  </div>
</div>

<script>
(function(){
"use strict";

// ---------- Grid / maze setup ----------
const COLS = 15, ROWS = 15, CELL = 24;
const canvas = document.getElementById("cv"), ctx = canvas.getContext("2d");
const scEl = document.getElementById("sc"), lvEl = document.getElementById("lv"), stgEl = document.getElementById("stg"), tixEl = document.getElementById("tix");
const clearScreen = document.getElementById("clearScreen"), failScreen = document.getElementById("failScreen"),
      victoryScreen = document.getElementById("victoryScreen"), caughtScreen = document.getElementById("caughtScreen"),
      finalScoreInfo = document.getElementById("finalScoreInfo");

const MAX_LEVEL = 7;
const HOUSE_R = 7, HOUSE_C = 7; // center of a 15x15 grid
const TUNNEL_R = 7;
const PLAYER_START = { r: 11, c: 7 };
const POWER_CELLS = [[1,1],[1,13],[13,1],[13,13]];

let grid = [];        // grid[r][c] = '#' wall, '.' dot, 'o' power pellet, ' ' empty path
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
  // tunnel openings on the middle row
  grid[TUNNEL_R][0] = " ";
  grid[TUNNEL_R][COLS-1] = " ";
  // ghost house: plus-shape naturally framed by the lattice pillars
  [[HOUSE_R-1,HOUSE_C],[HOUSE_R,HOUSE_C-1],[HOUSE_R,HOUSE_C],[HOUSE_R,HOUSE_C+1],[HOUSE_R+1,HOUSE_C]]
    .forEach(([r,c]) => { grid[r][c] = " "; });
  // player start, no dot sitting under the player at spawn
  grid[PLAYER_START.r][PLAYER_START.c] = " ";
  // power pellets
  POWER_CELLS.forEach(([r,c]) => { grid[r][c] = "o"; });
}

function countDots(){
  let n = 0;
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
    if (grid[r][c] === "." || grid[r][c] === "o") n++;
  return n;
}

function isWall(r, c){
  if (r < 0 || r >= ROWS) return true;
  if (c < 0) c = COLS - 1;      // tunnel wrap
  if (c >= COLS) c = 0;
  return grid[r][c] === "#";
}

function cellCenter(r, c){ return { x: c*CELL + CELL/2, y: r*CELL + CELL/2 }; }

// ---------- Game state ----------
let score = 0, lives = 3, level = 1, gameRunning = false, lastTime = 0;
let frightenedTimer = 0, frightenedTotal = 0;
let arcadeTickets = 0;
try { arcadeTickets = parseInt(localStorage.getItem("arcade_tix_vault") || "0", 10); } catch(e){ arcadeTickets = 0; }
tixEl.innerText = arcadeTickets;

const DIRS = { up:{x:0,y:-1}, down:{x:0,y:1}, left:{x:-1,y:0}, right:{x:1,y:0}, none:{x:0,y:0} };

function makePlayer(){
  const c = cellCenter(PLAYER_START.r, PLAYER_START.c);
  return { col: PLAYER_START.c, row: PLAYER_START.r, px: c.x, py: c.y, dir: DIRS.none, nextDir: DIRS.none, mouth: 0.2, mouthDir: 1 };
}

const GHOST_COLORS = ["#ef4444", "#f472b6", "#22d3ee", "#f59e0b"];
function makeGhosts(n){
  const c = cellCenter(HOUSE_R, HOUSE_C);
  const list = [];
  for (let i = 0; i < n; i++){
    list.push({
      col: HOUSE_C, row: HOUSE_R, px: c.x, py: c.y,
      dir: DIRS.up, nextDir: DIRS.up,
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
    player: 0.095,
    ghost: 0.062 + lvl * 0.006,
    frightened: 0.045,
    eaten: 0.16,
    frightenedDuration: Math.max(2500, 7000 - lvl*550)
  };
}
let speeds = levelSpeeds(level);

function startLevel(lvl, keepScore){
  level = lvl;
  buildMaze();
  dotsRemaining = countDots();
  ghostCount = Math.min(4, 1 + Math.ceil(lvl/2));
  ghosts = makeGhosts(ghostCount);
  houseTimer = 0;
  player = makePlayer();
  speeds = levelSpeeds(lvl);
  frightenedTimer = 0; frightenedTotal = 0;
  stgEl.innerText = "LEVEL " + lvl;
  if (!keepScore){ /* score persists across levels by design */ }
}

// ---------- Audio ----------
let audioCtx = null;
function setupAudio(){ if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
function sound(type){
  setupAudio(); if (!audioCtx) return;
  const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
  osc.connect(gain); gain.connect(audioCtx.destination);
  const t = audioCtx.currentTime;
  if (type === "waka"){ osc.type="triangle"; osc.frequency.setValueAtTime(420,t); osc.frequency.linearRampToValueAtTime(700,t+0.06); gain.gain.setValueAtTime(0.12,t); osc.start(); osc.stop(t+0.06); }
  else if (type === "power"){ osc.type="square"; osc.frequency.setValueAtTime(300,t); osc.frequency.linearRampToValueAtTime(150,t+0.25); gain.gain.setValueAtTime(0.15,t); osc.start(); osc.stop(t+0.25); }
  else if (type === "eatghost"){ osc.type="square"; osc.frequency.setValueAtTime(200,t); osc.frequency.linearRampToValueAtTime(900,t+0.15); gain.gain.setValueAtTime(0.2,t); osc.start(); osc.stop(t+0.15); }
  else if (type === "lose"){ osc.type="sawtooth"; osc.frequency.setValueAtTime(350,t); osc.frequency.exponentialRampToValueAtTime(60,t+0.35); gain.gain.setValueAtTime(0.25,t); osc.start(); osc.stop(t+0.35); }
  else if (type === "boom"){ osc.type="sawtooth"; osc.frequency.setValueAtTime(90,t); osc.frequency.exponentialRampToValueAtTime(20,t+0.5); gain.gain.setValueAtTime(0.4,t); osc.start(); osc.stop(t+0.5); }
  else if (type === "level"){ osc.type="sine"; osc.frequency.setValueAtTime(523.25,t); osc.frequency.setValueAtTime(659.25,t+0.1); osc.frequency.setValueAtTime(783.99,t+0.2); gain.gain.setValueAtTime(0.2,t); osc.start(); osc.stop(t+0.35); }
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
    // tap: steer relative to the player's current position
    const rect = canvas.getBoundingClientRect();
    const cx = rect.left + player.px, cy = rect.top + player.py;
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
  startLevel(level + 1, true);
  requestAnimationFrame(loop);
};
window.confirmRestart = function(){
  failScreen.style.display = "none"; victoryScreen.style.display = "none";
  score = 0; scEl.innerText = 0; lives = 3; lvEl.innerText = 3;
  gameRunning = true; lastTime = 0;
  startLevel(1, false);
  requestAnimationFrame(loop);
};
window.confirmRespawn = function(){
  caughtScreen.style.display = "none";
  gameRunning = true; lastTime = 0;
  player = makePlayer();
  ghosts.forEach(g => { g.mode = "house"; const c = cellCenter(HOUSE_R, HOUSE_C); g.col=HOUSE_C; g.row=HOUSE_R; g.px=c.x; g.py=c.y; });
  houseTimer = 0;
  requestAnimationFrame(loop);
};

// ---------- Movement helpers ----------
function canMove(col, row, dir){
  if (dir.x === 0 && dir.y === 0) return false;
  return !isWall(row + dir.y, col + dir.x);
}
function wrapCol(c){ if (c < 0) return COLS - 1; if (c >= COLS) return 0; return c; }

function advanceEntity(e, speed, dt){
  const center = cellCenter(e.row, e.col);
  const atCenter = Math.abs(e.px - center.x) < speed*dt + 0.5 && Math.abs(e.py - center.y) < speed*dt + 0.5;
  if (atCenter){
    e.px = center.x; e.py = center.y;
    if (canMove(e.col, e.row, e.nextDir)) e.dir = e.nextDir;
    if (!canMove(e.col, e.row, e.dir)) e.dir = DIRS.none;
  }
  e.px += e.dir.x * speed * dt;
  e.py += e.dir.y * speed * dt;
  // tunnel wrap in pixel space
  if (e.px < -CELL*0.5) e.px += COLS*CELL;
  if (e.px > COLS*CELL - CELL*0.5) e.px -= COLS*CELL;
  e.col = wrapCol(Math.round((e.px - CELL/2) / CELL));
  e.row = Math.round((e.py - CELL/2) / CELL);
}

function chooseGhostDir(g, target, avoid){
  const opts = ["up","down","left","right"].map(k => DIRS[k]).filter(d => canMove(g.col, g.row, d));
  if (opts.length === 0) return DIRS.none;
  // don't reverse unless it's the only option
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
    g.py = cellCenter(HOUSE_R, HOUSE_C).y + Math.sin(g.bob) * 3;
    if (houseTimer >= g.releaseAt){
      g.mode = "chase";
      g.col = HOUSE_C; g.row = HOUSE_R;
      const c = cellCenter(HOUSE_R, HOUSE_C); g.px = c.x; g.py = c.y;
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
  const center = cellCenter(g.row, g.col);
  const atCenter = Math.abs(g.px - center.x) < speed*dt + 0.5 && Math.abs(g.py - center.y) < speed*dt + 0.5;
  if (atCenter) g.nextDir = chooseGhostDir(g, target, avoid);
  advanceEntity(g, speed, dt);
  if (g.mode === "eaten" && g.col === HOUSE_C && g.row === HOUSE_R){
    g.mode = "chase"; g.dir = DIRS.up; g.nextDir = DIRS.up;
  }
}

// ---------- Drawing ----------
function drawMaze(){
  ctx.fillStyle = "#020617"; ctx.fillRect(0, 0, COLS*CELL, ROWS*CELL);
  const wallColor = ["#1e40af","#7c3aed","#0891b2","#b45309","#15803d","#be185d","#0369a1"][(level-1) % 7];
  for (let r = 0; r < ROWS; r++){
    for (let c = 0; c < COLS; c++){
      if (grid[r][c] === "#"){
        ctx.fillStyle = "#050b1f";
        ctx.fillRect(c*CELL, r*CELL, CELL, CELL);
        ctx.strokeStyle = wallColor;
        ctx.lineWidth = 2;
        ctx.strokeRect(c*CELL+1.5, r*CELL+1.5, CELL-3, CELL-3);
      }
    }
  }
  // outer border glow
  ctx.strokeStyle = wallColor; ctx.lineWidth = 3;
  ctx.strokeRect(1.5, 1.5, COLS*CELL-3, ROWS*CELL-3);

  for (let r = 0; r < ROWS; r++){
    for (let c = 0; c < COLS; c++){
      const cell = grid[r][c];
      if (cell === "."){
        ctx.beginPath(); ctx.fillStyle = "#fbbf24";
        ctx.arc(c*CELL+CELL/2, r*CELL+CELL/2, 2, 0, Math.PI*2); ctx.fill(); ctx.closePath();
      } else if (cell === "o"){
        const pulse = 4 + Math.sin(performance.now()*0.006)*1.5;
        ctx.beginPath(); ctx.fillStyle = "#fde047";
        ctx.arc(c*CELL+CELL/2, r*CELL+CELL/2, pulse, 0, Math.PI*2); ctx.fill(); ctx.closePath();
      }
    }
  }
}

function drawPlayer(){
  player.mouth += player.mouthDir * 0.012;
  if (player.mouth > 0.42 || player.mouth < 0.04) player.mouthDir *= -1;
  const d = player.dir;
  const rot = d.x>0?0:(d.x<0?Math.PI:(d.y>0?Math.PI/2:(d.y<0?Math.PI*1.5:0)));
  ctx.beginPath();
  const grad = ctx.createRadialGradient(player.px-4, player.py-4, 2, player.px, player.py, 10);
  grad.addColorStop(0, "#fff7cc"); grad.addColorStop(0.4, "#fbbf24"); grad.addColorStop(1, "#b45309");
  ctx.arc(player.px, player.py, 10, rot+player.mouth, rot+Math.PI*2-player.mouth);
  ctx.lineTo(player.px, player.py); ctx.fillStyle = grad; ctx.fill(); ctx.closePath();
}

function drawGhost(g){
  const r = 10;
  ctx.beginPath();
  let color = g.color;
  if (g.mode === "frightened"){
    const flashing = frightenedTimer < 1500 && Math.floor(frightenedTimer/200)%2===0;
    color = flashing ? "#e0f2fe" : "#1d4ed8";
  }
  if (g.mode === "eaten"){
    // just eyes
    ctx.fillStyle = "#e5e7eb";
    ctx.beginPath(); ctx.arc(g.px-3.5, g.py-2, 2.4, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    ctx.beginPath(); ctx.arc(g.px+3.5, g.py-2, 2.4, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    ctx.fillStyle = "#0f172a";
    ctx.beginPath(); ctx.arc(g.px-3.5, g.py-2, 1.1, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    ctx.beginPath(); ctx.arc(g.px+3.5, g.py-2, 1.1, 0, Math.PI*2); ctx.fill(); ctx.closePath();
    return;
  }
  const grad = ctx.createRadialGradient(g.px-3, g.py-3, 1, g.px, g.py, r);
  grad.addColorStop(0, "#ffffff"); grad.addColorStop(0.3, color); grad.addColorStop(1, "#020617");
  ctx.arc(g.px, g.py, r, Math.PI, 0);
  const wob = Math.sin(performance.now()*0.01 + g.px*0.2) * 2;
  ctx.lineTo(g.px+r, g.py+r);
  ctx.lineTo(g.px+r*0.5, g.py+r-wob);
  ctx.lineTo(g.px, g.py+r);
  ctx.lineTo(g.px-r*0.5, g.py+r-wob);
  ctx.lineTo(g.px-r, g.py+r);
  ctx.closePath();
  ctx.fillStyle = grad; ctx.fill();
  ctx.fillStyle = "#ffffff";
  ctx.beginPath(); ctx.arc(g.px-3.5, g.py-1, 2.6, 0, Math.PI*2); ctx.fill(); ctx.closePath();
  ctx.beginPath(); ctx.arc(g.px+3.5, g.py-1, 2.6, 0, Math.PI*2); ctx.fill(); ctx.closePath();
  ctx.fillStyle = "#0f172a";
  const ex = g.dir.x*1.2, ey = g.dir.y*1.2;
  ctx.beginPath(); ctx.arc(g.px-3.5+ex, g.py-1+ey, 1.2, 0, Math.PI*2); ctx.fill(); ctx.closePath();
  ctx.beginPath(); ctx.arc(g.px+3.5+ex, g.py-1+ey, 1.2, 0, Math.PI*2); ctx.fill(); ctx.closePath();
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

  // player movement + eating
  advanceEntity(player, speeds.player, dt);
  const cell = grid[player.row] ? grid[player.row][player.col] : undefined;
  if (cell === "."){
    grid[player.row][player.col] = " "; dotsRemaining--; score += 10; scEl.innerText = score; sound("waka");
    arcadeTickets += 1; try { localStorage.setItem("arcade_tix_vault", arcadeTickets.toString()); } catch(e){}
    tixEl.innerText = arcadeTickets;
  } else if (cell === "o"){
    grid[player.row][player.col] = " "; dotsRemaining--; score += 50; scEl.innerText = score; sound("power");
    frightenedTimer = speeds.frightenedDuration; frightenedTotal = speeds.frightenedDuration;
    ghosts.forEach(g => { if (g.mode !== "house" && g.mode !== "eaten") g.mode = "frightened"; });
  }

  ghosts.forEach(g => updateGhost(g, dt));

  drawPlayer();
  ghosts.forEach(drawGhost);

  // collisions
  for (const g of ghosts){
    if (g.mode === "house") continue;
    if (Math.hypot(player.px - g.px, player.py - g.py) < 13){
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

// ---------- Launch button ----------
const launchBtn = document.createElement("button");
launchBtn.innerText = "🥥 LAUNCH COCONUT HUNTER";
Object.assign(launchBtn.style, {
  position:"absolute", top:"40%", left:"6%", width:"88%", padding:"15px",
  fontSize:"15px", fontWeight:"bold", background:"#10b981", color:"#000",
  border:"2px solid #34d399", borderRadius:"8px", zIndex:"999", fontFamily:"monospace", cursor:"pointer"
});
document.getElementById("arenaWrapper").appendChild(launchBtn);
launchBtn.onclick = () => {
  launchBtn.remove(); setupAudio(); sound("level");
  gameRunning = true; startLevel(1, false); lastTime = 0;
  requestAnimationFrame(loop);
};

buildMaze(); // draw an initial static preview behind the launch button
drawMaze();

})();
</script>
</body>
</html>
