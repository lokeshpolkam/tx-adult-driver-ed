import os
import base64

diorama_path = 'driving_rule_animations/asset_library/roads/uncontrolled_intersection_final.png'
car_red_ne_path = 'driving_rule_animations/asset_library/vehicles/car_red_clean_ne.png'
car_red_nw_path = 'driving_rule_animations/asset_library/vehicles/car_red_clean_nw.png'
car_blue_ne_path = 'driving_rule_animations/asset_library/vehicles/car_blue_clean_ne.png'

print("Encoding Lesson 12 assets to base64...")
with open(diorama_path, 'rb') as f:
    diorama_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

with open(car_red_ne_path, 'rb') as f:
    car_red_ne_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

with open(car_red_nw_path, 'rb') as f:
    car_red_nw_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

with open(car_blue_ne_path, 'rb') as f:
    car_blue_ne_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T03: Signaling &amp; Communication — The 100-Foot Continuous Turn Signal Rule</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0B0E14;
      color: #E6EDF3;
      user-select: none;
      -webkit-user-select: none;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .pulse-danger {{
      animation: pulseDanger 0.8s infinite alternate;
    }}
    @keyframes pulseDanger {{
      0% {{ transform: scale(1.0); opacity: 0.85; }}
      100% {{ transform: scale(1.08); opacity: 1.0; }}
    }}
  </style>
</head>
<body class="w-screen h-screen overflow-hidden flex flex-col justify-between p-3 bg-[#0B0E14]">

  <!-- TOP HEADER / METADATA -->
  <header class="flex items-center justify-between px-3 py-1.5 bg-[#121620] border border-[#212836] rounded-xl shadow-md z-30">
    <div>
      <div class="flex items-center space-x-2">
        <span class="text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 mono">TDLR ADE-1317 • 2.5D VECTOR ENGINE</span>
        <span class="text-[10px] text-gray-400 mono">LESSON 12</span>
      </div>
      <h1 class="text-sm font-black text-white tracking-tight flex items-center space-x-2">
        <span>L05-T03: Signaling &amp; Communication — The 100-Foot Continuous Turn Signal Rule</span>
      </h1>
      <p class="text-[10px] text-gray-400 mono">Texas Transportation Code &sect; 545.104 &bull; &sect; 545.106</p>
    </div>

    <!-- Multi-Scenario Mode Selector -->
    <div class="flex items-center space-x-2 bg-[#171C26] p-1 rounded-lg border border-[#283244] text-xs">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded font-bold transition text-black bg-emerald-400 shadow" data-mode="1">
        1: Lawful 100-Ft Signal (Turn Execution)
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded font-semibold text-gray-400 hover:text-white transition" data-mode="2">
        2: Lane Change Advance Signal
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded font-semibold text-red-400 hover:text-red-300 transition" data-mode="3">
        Hazard: Sudden Turn Without Signal
      </button>
      <div class="h-4 w-px bg-gray-700 mx-1"></div>
      <label class="flex items-center space-x-1.5 text-xs text-gray-300 cursor-pointer pr-1">
        <input type="checkbox" id="auto-loop-toggle" checked class="rounded border-gray-700 text-blue-500 focus:ring-0">
        <span class="mono text-[11px]">Auto-Loop</span>
      </label>
    </div>
  </header>

  <!-- CANONICAL 4-STEP STEPPER -->
  <nav class="grid grid-cols-4 gap-2 my-1 z-30">
    <button data-step="1" class="step-btn px-2.5 py-1.5 rounded-lg border border-blue-500/60 bg-blue-500/15 text-left transition shadow">
      <div class="text-[9px] mono text-blue-400 font-bold uppercase tracking-wider">STEP 1</div>
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">Approach Corridor (150 FT)</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">100-FT Statutory Trigger</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">Continuous Signal &amp; Decel</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Turn &amp; Auto-Cancellation</div>
    </button>
  </nav>

  <!-- MAIN SIMULATION VIEWPORT -->
  <main class="relative flex-1 w-full bg-[#0E121A] rounded-xl border border-[#1E2634] overflow-hidden flex items-center justify-center shadow-inner min-h-0">
    
    <!-- 35° ARCHITECTURAL ISOMETRIC STAGE -->
    <div id="isometric-stage" class="relative overflow-hidden shadow-2xl rounded-lg" style="height: calc(100% - 16px); aspect-ratio: 1024 / 667; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: Roadway Base -->
      <img src="{diorama_b64}" alt="Texas Roadway Intersection" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none z-0" />

      <!-- LAYER 1: SVG STATUTORY DISTANCE THRESHOLDS & MARKERS -->
      <svg id="stage-svg-overlay" class="absolute inset-0 w-full h-full z-10 pointer-events-none" viewBox="0 0 1024 667">
        <defs>
          <linearGradient id="corridor-gradient" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.12" />
            <stop offset="100%" stop-color="#F59E0B" stop-opacity="0.35" />
          </linearGradient>
          <marker id="arrow-turn" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 6 3, 0 6" fill="#F59E0B" />
          </marker>
        </defs>

        <!-- 150 FT Threshold Marker (Approach) -->
        <line x1="170" y1="585" x2="240" y2="545" stroke="#6B7280" stroke-width="2" stroke-dasharray="4,4" opacity="0.65" />
        <text x="160" y="570" fill="#9CA3AF" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="700">150 FT</text>

        <!-- 100 FT MANDATORY SIGNAL THRESHOLD (TTC § 545.104) -->
        <!-- Highlighted Corridor Polygon from 100 FT to Turn (Stop Bar) -->
        <polygon id="statutory-100ft-zone" points="250,540 325,495 425,445 355,485" fill="url(#corridor-gradient)" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.8" />
        
        <!-- 100 FT Transverse Line -->
        <line x1="250" y1="540" x2="325" y2="495" stroke="#F59E0B" stroke-width="3.5" stroke-linecap="round" />
        <g transform="translate(180, 515)">
          <rect x="0" y="-10" width="105" height="15" rx="3" fill="#181507" fill-opacity="0.9" stroke="#F59E0B" stroke-width="1" />
          <text x="52" y="1" fill="#FBBF24" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">▼ 100 FT LAWFUL SIGNAL</text>
        </g>

        <!-- 50 FT Deceleration Marker -->
        <line x1="305" y1="510" x2="375" y2="470" stroke="#F59E0B" stroke-width="2" stroke-dasharray="3,3" opacity="0.7" />
        <text x="290" y="490" fill="#FCD34D" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="700">50 FT</text>

        <!-- 0 FT Turn Apex (Intersection Stop Bar) -->
        <line x1="355" y1="485" x2="425" y2="445" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.95" />
        <text x="345" y="445" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="800">0 FT (TURN)</text>

        <!-- Left Turn Arc Trajectory -->
        <path id="turn-trajectory-arc" d="M 380 470 Q 440 430, 470 400 Q 480 375, 410 330 L 260 250" fill="none" stroke="#F59E0B" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-turn)" opacity="0.0" />

        <!-- HAZARD DEMO: CRITICAL REAR-END CONFLICT ZONE -->
        <g id="hazard-conflict-zone" opacity="0.0">
          <circle cx="370" cy="480" r="48" fill="#EF4444" fill-opacity="0.25" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" class="pulse-danger" />
          <line x1="290" y1="530" x2="350" y2="495" stroke="#1F2430" stroke-width="3.5" stroke-linecap="round" />
          <line x1="305" y1="540" x2="365" y2="505" stroke="#1F2430" stroke-width="3.5" stroke-linecap="round" />
          <polygon points="370,455 380,473 400,470 385,485 395,505 370,493 345,505 355,485 340,470 360,473" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- EGO VEHICLE (Red Sedan, Turning Left SW to NW) -->
      <div id="veh-ego-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 20.0%; top: 84.0%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img id="veh-ego-img" src="{car_red_ne_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Glowing Left Turn Signal Blinkers -->
          <div id="blinker-front-left" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 24%; left: 74%;"></div>
          <div id="blinker-rear-left" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 18%; left: 24%;"></div>

          <!-- Glowing Brake Lights -->
          <div id="veh-ego-brake-1" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 18%; left: 16%;"></div>
          <div id="veh-ego-brake-2" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 27%; left: 30%;"></div>
        </div>

        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: 150 FT (APPROACHING)
        </div>
      </div>

      <!-- TRAILING VEHICLE (Blue Sedan, Following in Same Lane) -->
      <div id="veh-trail-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 2.0%; top: 98.0%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_ne_b64}" alt="Trailing Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Glowing Brake Lights -->
          <div id="veh-trail-brake-1" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 18%; left: 16%;"></div>
          <div id="veh-trail-brake-2" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 27%; left: 30%;"></div>
        </div>

        <div id="tag-veh-trail" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          TRAILING VEHICLE (SAFE BUFFER)
        </div>
      </div>

      <!-- LAYER 3: TOP-RIGHT STATUS NOTIFICATION PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 10px; right: 10px;">
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
        <span id="pill-status-text">100-FT STATUTORY THRESHOLD TRIGGERED: CONTINUOUS BLINKER ACTIVE</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div class="absolute bottom-2.5 right-2.5 z-25 px-3 py-1.5 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[10px] font-bold shadow-lg tracking-wider flex items-center space-x-2 pointer-events-none">
        <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TTC &sect; 545.104(b) 100-FT RULE VERIFIED</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER -->
      <div id="hazard-banner" class="absolute bottom-14 left-1/2 -translate-x-1/2 z-30 px-5 py-2 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300" style="opacity: 0.0;">
        <div class="text-xs font-black tracking-widest text-red-400 flex items-center justify-center space-x-1.5">
          <span>&#9888;</span>
          <span>CRITICAL STATUTORY VIOLATION</span>
          <span>&#9888;</span>
        </div>
        <div class="text-xs font-bold text-white">FAILURE TO SIGNAL CONTINUOUSLY FOR 100 FEET</div>
        <div class="text-[10px] text-red-300">
          TTC &sect; 545.104: Sudden deceleration and turning without the mandatory 100-ft signal<br>
          deprives trailing traffic of reaction time, resulting in a severe rear-end collision!
        </div>
      </div>

      <!-- LAYER 4: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
      <div id="telemetry-hud-card" class="absolute top-2.5 left-2.5 z-30 max-w-[280px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-2 space-y-1 shadow-xl pointer-events-none">
        <div class="flex items-center justify-between border-b border-[#222B38] pb-1">
          <span class="text-[10px] font-bold text-gray-400 mono uppercase tracking-wider">Communication Telemetry</span>
          <span id="signal-state-badge" class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono">
            SIGNAL: ACTIVE (100 FT)
          </span>
        </div>

        <div class="space-y-0.5 text-xs mono">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Distance to Turn:</span>
            <span id="telem-dist" class="text-amber-400 font-bold">100 FT</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Ego Speed:</span>
            <span id="telem-speed" class="text-emerald-400 font-bold">25 MPH</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Trailing Gap:</span>
            <span id="telem-gap" class="text-blue-400 font-bold">75 FT (SAFE)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Mandate:</span>
            <span id="telem-statute" class="text-emerald-300 font-bold">TTC &sect; 545.104(b)</span>
          </div>
        </div>

        <div class="pt-1 border-t border-[#1F2633] text-[10px] text-gray-300 leading-snug font-sans" id="hud-narrative">
          An operator intending to turn right or left shall signal continuously for not less than the last 100 feet of movement before the turn.
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM SCRUBBABLE TIMELINE & PLAYBACK CONTROLS -->
  <footer class="bg-[#121620] border border-[#212836] rounded-xl px-4 py-2.5 shadow-lg flex flex-col gap-2 mt-1 z-30">
    <div class="flex items-center space-x-3">
      <!-- Play/Pause Button -->
      <button id="play-pause-btn" class="w-8 h-8 rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center font-bold shadow transition">
        <svg id="play-icon" class="w-4 h-4 fill-current hidden" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        <svg id="pause-icon" class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
      </button>

      <!-- Reset Button -->
      <button id="reset-btn" class="w-8 h-8 rounded-lg bg-[#1C2331] hover:bg-[#252F42] text-gray-300 flex items-center justify-center transition border border-[#2B3548]">
        <svg class="w-4 h-4 stroke-current fill-none" viewBox="0 0 24 24" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
      </button>

      <!-- Time Display -->
      <span id="time-display" class="mono text-xs text-blue-400 font-bold w-12">0.00s</span>

      <!-- Scrubber Slider -->
      <div class="flex-1 relative flex items-center">
        <input type="range" id="timeline-slider" min="0" max="8.0" step="0.01" value="0" class="w-full h-1.5 bg-[#212836] rounded-lg appearance-none cursor-pointer accent-blue-500" />
      </div>

      <span class="mono text-xs text-gray-400">8.00s</span>

      <!-- Speed Selector -->
      <div class="flex items-center bg-[#18202F] p-0.5 rounded border border-[#2B3548] text-xs mono">
        <button data-speed="0.5" class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white">0.5x</button>
        <button data-speed="1.0" class="speed-btn px-2 py-0.5 rounded bg-blue-600 text-white font-bold">1.0x</button>
        <button data-speed="1.5" class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white">1.5x</button>
      </div>
    </div>

    <!-- Timeline Keyframe Legend Markers -->
    <div class="flex justify-between text-[10px] mono text-gray-500 px-1 pt-0.5">
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-1-text">0.8s 150 FT Approach</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-2-text">2.0s 100 FT Signal Trigger</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-3-text">4.2s Continuous 50 FT Decel</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="keyframe-4-text">6.8s Turn &amp; Cancel</span>
      </span>
      <span class="text-blue-400 font-semibold" id="legend-statute">TTC &sect; 545.104(b) Continuous Signal</span>
    </div>
  </footer>

  <!-- =============================================================== -->
  <!-- SIMULATION SCRIPT: 60 FPS DETERMINISTIC ENGINE                  -->
  <!-- =============================================================== -->
  <script>
    const DURATION = 8.0;
    let currentTime = 0.0;
    let isPlaying = true;
    let playbackSpeed = 1.0;
    let currentMode = 1;
    let lastTimestamp = null;
    let autoLoop = true;

    // Assets B64
    const carRedNeSrc = "{car_red_ne_b64}";
    const carRedNwSrc = "{car_red_nw_b64}";

    // DOM Elements
    const playPauseBtn = document.getElementById('play-pause-btn');
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');
    const resetBtn = document.getElementById('reset-btn');
    const timeDisplay = document.getElementById('time-display');
    const timelineSlider = document.getElementById('timeline-slider');
    const autoLoopToggle = document.getElementById('auto-loop-toggle');

    const vehEgo = document.getElementById('veh-ego-container');
    const vehEgoImg = document.getElementById('veh-ego-img');
    const vehTrail = document.getElementById('veh-trail-container');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehTrail = document.getElementById('tag-veh-trail');
    const blinkerFront = document.getElementById('blinker-front-left');
    const blinkerRear = document.getElementById('blinker-rear-left');
    const brakeEgo1 = document.getElementById('veh-ego-brake-1');
    const brakeEgo2 = document.getElementById('veh-ego-brake-2');
    const brakeTrail1 = document.getElementById('veh-trail-brake-1');
    const brakeTrail2 = document.getElementById('veh-trail-brake-2');

    const turnTrajectoryArc = document.getElementById('turn-trajectory-arc');
    const statutory100ftZone = document.getElementById('statutory-100ft-zone');
    const hazardConflictZone = document.getElementById('hazard-conflict-zone');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemDist = document.getElementById('telem-dist');
    const telemSpeed = document.getElementById('telem-speed');
    const telemGap = document.getElementById('telem-gap');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceText = document.getElementById('compliance-text');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    function smoothCos(p) {{
      return 0.5 * (1 - Math.cos(Math.PI * Math.max(0, Math.min(1, p))));
    }}

    // ===============================================================
    // MODE 1: LAWFUL 100-FT CONTINUOUS TURN SIGNAL
    // ===============================================================
    function updateMode1(t) {{
      hazardConflictZone.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      statutory100ftZone.setAttribute('opacity', '0.8');

      let distFt = 150, egoSpeed = 25, blinkerActive = false, brakeGlowEgo = 0.0;
      let egoX = 20.0, egoY = 84.0;

      if (t < 2.0) {{
        // Approach from 150 FT (20, 84) to 100 FT (28, 77)
        const p = t / 2.0;
        distFt = Math.round(150 - p * 50);
        egoSpeed = 25;
        egoX = 20.0 + p * (28.0 - 20.0);
        egoY = 84.0 - p * (84.0 - 77.0);
        blinkerActive = false;
        brakeGlowEgo = 0.0;
        vehEgoImg.src = carRedNeSrc;
        tagVehEgo.textContent = `EGO: ${{distFt}} FT (APPROACHING THRESHOLD)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else if (t < 5.2) {{
        // Continuous signaling corridor (100 FT to 0 FT stop bar at 38, 69)
        const p = (t - 2.0) / (5.2 - 2.0);
        const ease = smoothCos(p);
        distFt = Math.round(100 * (1 - p));
        egoSpeed = Math.round(25 - ease * 15); // Decelerating 25 -> 10 MPH for turn
        egoX = 28.0 + ease * (38.0 - 28.0);
        egoY = 77.0 - ease * (77.0 - 69.0);
        blinkerActive = true;
        brakeGlowEgo = (p > 0.2) ? 0.9 : 0.0;
        vehEgoImg.src = carRedNeSrc;
        tagVehEgo.textContent = `EGO: ${{distFt}} FT (SIGNALING CONTINUOUSLY)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
      }} else if (t < 7.0) {{
        // Executing Left Turn into NW Cross Street
        const p = (t - 5.2) / (7.0 - 5.2);
        const ease = smoothCos(p);
        distFt = 0;
        egoSpeed = 12;
        egoX = 38.0 + ease * (46.0 - 38.0) - p * (46.0 - 30.0);
        egoY = 69.0 - ease * (69.0 - 56.0) - p * (56.0 - 42.0);
        blinkerActive = (p < 0.6); // Auto-cancels as turn completes
        brakeGlowEgo = 0.0;
        vehEgoImg.src = (p > 0.35) ? carRedNwSrc : carRedNeSrc;
        tagVehEgo.textContent = blinkerActive ? 'EGO: EXECUTING TURN' : 'EGO: SIGNAL AUTO-CANCELED';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else {{
        // Cleared NW street
        const p = (t - 7.0) / (8.0 - 7.0);
        distFt = 0;
        egoSpeed = 22;
        egoX = 30.0 - p * (30.0 - 18.0);
        egoY = 42.0 - p * (42.0 - 32.0);
        blinkerActive = false;
        brakeGlowEgo = 0.0;
        vehEgoImg.src = carRedNwSrc;
        tagVehEgo.textContent = 'EGO: TURN COMPLETED (TTC § 545.104 COMPLIANT)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }}

      // Trailing Vehicle (Blue Sedan) maintains defensive buffer & holds at approach line
      let trailX = 2.0, trailY = 98.0, trailGap = 80, brakeGlowTrail = 0.0;
      if (t < 2.0) {{
        const p = t / 2.0;
        trailX = 2.0 + p * (10.0 - 2.0);
        trailY = 98.0 - p * (98.0 - 91.0);
        trailGap = 80;
        brakeGlowTrail = 0.0;
        tagVehTrail.textContent = 'TRAILING: 80 FT BUFFER';
      }} else if (t < 5.0) {{
        const p = (t - 2.0) / (5.0 - 2.0);
        const ease = smoothCos(p);
        trailX = 10.0 + ease * (26.0 - 10.0);
        trailY = 91.0 - ease * (91.0 - 78.0);
        trailGap = 75;
        brakeGlowTrail = (p > 0.3) ? 0.8 : 0.0;
        tagVehTrail.textContent = 'TRAILING: DECEL (75 FT GAP)';
      }} else if (t < 7.0) {{
        // Holds stationary behind stop bar while Ego completes turn!
        trailX = 26.0; trailY = 78.0;
        trailGap = 90;
        brakeGlowTrail = 0.9;
        tagVehTrail.textContent = 'TRAILING: HOLDING CUSHION';
      }} else {{
        // Proceeds NE after Ego clears intersection
        const p = (t - 7.0) / (8.0 - 7.0);
        trailX = 26.0 + p * (50.0 - 26.0);
        trailY = 78.0 - p * (78.0 - 58.0);
        trailGap = 120;
        brakeGlowTrail = 0.0;
        tagVehTrail.textContent = 'TRAILING: PROCEEDING NE SAFELY';
      }}
      if (t < 3.0) {{
        tagVehTrail.className = 'absolute left-0 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
      }} else {{
        tagVehTrail.className = 'absolute left-0 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
      }}

      // Blinker Flash Rate
      const flash = blinkerActive && (Math.sin(t * 14) > 0);
      blinkerFront.style.opacity = flash ? '1.0' : '0.0';
      blinkerRear.style.opacity = flash ? '1.0' : '0.0';

      vehEgo.style.left = `${{egoX}}%`; vehEgo.style.top = `${{egoY}}%`;
      vehTrail.style.left = `${{trailX}}%`; vehTrail.style.top = `${{trailY}}%`;
      vehEgo.style.opacity = '1.0'; vehTrail.style.opacity = '1.0';
      tagVehEgo.style.opacity = '1.0'; tagVehTrail.style.opacity = '1.0';

      brakeEgo1.style.opacity = brakeGlowEgo; brakeEgo2.style.opacity = brakeGlowEgo;
      brakeTrail1.style.opacity = brakeGlowTrail; brakeTrail2.style.opacity = brakeGlowTrail;

      turnTrajectoryArc.setAttribute('opacity', (t >= 2.0 && t <= 6.5) ? '1.0' : '0.0');

      telemDist.textContent = `${{distFt}} FT`;
      telemDist.className = (distFt <= 100 && distFt > 0) ? 'text-amber-400 font-black animate-pulse' : 'text-emerald-400 font-bold';
      telemSpeed.textContent = `${{egoSpeed}} MPH`;
      telemGap.textContent = `${{trailGap}} FT (SAFE BUFFER)`;
      telemGap.className = 'text-blue-400 font-bold';

      if (t < 2.0) {{
        signalStateBadge.innerHTML = 'SIGNAL: PENDING (APPROACH)';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-gray-500/20 text-gray-300 border border-gray-500/30 mono';
        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#141C2B]/95 border border-blue-400 text-blue-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'APPROACHING 100-FT STATUTORY SIGNAL LINE (TTC § 545.104)';
        hudNarrative.textContent = 'Vehicle approaches turn. Texas Transportation Code § 545.104(b) requires initiating turn signals not less than 100 feet before turning.';
      }} else if (t < 5.2) {{
        signalStateBadge.innerHTML = 'SIGNAL: CONTINUOUS ACTIVE';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '100-FT MANDATORY SIGNAL ACTIVE: DOWNSTREAM INTENT BROADCASTED';
        hudNarrative.textContent = 'Continuous 100-ft signaling alerts trailing traffic early. The trailing driver smoothly decelerates, maintaining safe 75-ft cushion.';
      }} else {{
        signalStateBadge.innerHTML = 'SIGNAL: AUTO-CANCELED';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'TURN EXECUTED: POST-MANEUVER SIGNAL CANCELLATION COMPLETE';
        hudNarrative.textContent = 'Turn completed safely into cross street. Blinker cancels immediately after turn execution to avoid confusing downstream drivers.';
      }}
      complianceText.textContent = 'TTC § 545.104(b) 100-FT CONTINUOUS RULE VERIFIED';
    }}

    // ===============================================================
    // MODE 2: MULTI-LANE FREEWAY LANE CHANGE WITH 100-FT ADVANCE
    // ===============================================================
    function updateMode2(t) {{
      hazardConflictZone.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      statutory100ftZone.setAttribute('opacity', '0.0');

      let distFt = 100, egoSpeed = 45, blinkerActive = false;
      let egoX = 20.0, egoY = 84.0;

      if (t < 2.5) {{
        const p = t / 2.5;
        distFt = Math.round(100 - p * 100);
        egoX = 20.0 + p * (35.0 - 20.0);
        egoY = 84.0 - p * (84.0 - 72.0);
        blinkerActive = true;
        vehEgoImg.src = carRedNeSrc;
        tagVehEgo.textContent = `EGO: LANE CHANGE SIGNAL (${{100 - distFt}} FT SIGNALED)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
      }} else if (t < 5.5) {{
        const p = (t - 2.5) / (5.5 - 2.5);
        const ease = smoothCos(p);
        egoX = 35.0 + ease * 15.0;
        egoY = 72.0 - ease * 22.0;
        blinkerActive = (p < 0.7);
        vehEgoImg.src = carRedNeSrc;
        tagVehEgo.textContent = blinkerActive ? 'EGO: LATERAL MERGE INTO LEFT LANE' : 'EGO: LANE CHANGE COMPLETE';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else {{
        const p = (t - 5.5) / (8.0 - 5.5);
        egoX = 50.0 + p * 20.0;
        egoY = 50.0 - p * 16.0;
        blinkerActive = false;
        vehEgoImg.src = carRedNeSrc;
        tagVehEgo.textContent = 'EGO: STABILIZED IN LEFT LANE';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }}

      // Trailing vehicle in right lane stays back safely
      let trailX = 4.0 + (t / 8.0) * 35.0;
      let trailY = 96.0 - (t / 8.0) * 28.0;
      tagVehTrail.textContent = 'TRAILING: RIGHT LANE BUFFER';
      tagVehTrail.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      const flash = blinkerActive && (Math.sin(t * 14) > 0);
      blinkerFront.style.opacity = flash ? '1.0' : '0.0';
      blinkerRear.style.opacity = flash ? '1.0' : '0.0';

      vehEgo.style.left = `${{egoX}}%`; vehEgo.style.top = `${{egoY}}%`;
      vehTrail.style.left = `${{trailX}}%`; vehTrail.style.top = `${{trailY}}%`;
      vehEgo.style.opacity = '1.0'; vehTrail.style.opacity = '1.0';
      tagVehEgo.style.opacity = '1.0'; tagVehTrail.style.opacity = '1.0';

      brakeEgo1.style.opacity = '0.0'; brakeEgo2.style.opacity = '0.0';
      brakeTrail1.style.opacity = '0.0'; brakeTrail2.style.opacity = '0.0';
      turnTrajectoryArc.setAttribute('opacity', '0.0');

      signalStateBadge.innerHTML = 'SIGNAL: 100-FT LANE CHANGE';
      signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-sky-500/20 text-sky-400 border border-sky-500/30 mono';

      telemDist.textContent = '100 FT (SIGNALED)';
      telemDist.className = 'text-sky-400 font-bold';
      telemSpeed.textContent = '45 MPH (CRUISE)';
      telemGap.textContent = '85 FT (SAFE GAP)';
      telemGap.className = 'text-blue-400 font-bold';

      hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#06182B]/95 border border-sky-400 text-sky-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TTC § 545.104(a): 100-FT ADVANCE SIGNAL BEFORE LANE CHANGE';
      hudNarrative.textContent = 'Texas statute requires signaling intent before changing lanes. Broadcasting intent for 100 feet allows adjacent traffic to adjust spacing smoothly.';
      complianceText.textContent = 'TTC § 545.104(a) LANE CHANGE COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (SUDDEN TURN WITHOUT SIGNAL)
    // ===============================================================
    function updateMode3(t) {{
      statutory100ftZone.setAttribute('opacity', '0.8');
      blinkerFront.style.opacity = '0.0';
      blinkerRear.style.opacity = '0.0';

      let egoX = 20.0, egoY = 84.0, egoSpeed = 30, brakeGlowEgo = 0.0;
      if (t < 2.8) {{
        const p = t / 2.8;
        egoX = 20.0 + p * (38.0 - 20.0);
        egoY = 84.0 - p * (84.0 - 69.0);
        egoSpeed = 30;
        brakeGlowEgo = 0.0;
        tagVehEgo.textContent = 'EGO: 30 MPH (NO SIGNAL ACTIVE!)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';
      }} else {{
        egoX = 38.0; egoY = 69.0; egoSpeed = 0; brakeGlowEgo = 1.0;
      }}

      // Trailing vehicle follows closely
      let trailX = 8.0, trailY = 93.0, brakeGlowTrail = 0.0;
      if (t < 2.8) {{
        const p = t / 2.8;
        trailX = 8.0 + p * (26.0 - 8.0);
        trailY = 93.0 - p * (93.0 - 78.0);
        brakeGlowTrail = 0.0;
        tagVehTrail.textContent = 'TRAILING: UNAWARE OF IMMINENT TURN';
      }} else if (t <= 3.5) {{
        const p = (t - 2.8) / (3.5 - 2.8);
        trailX = 26.0 + p * (37.0 - 26.0);
        trailY = 78.0 - p * (78.0 - 70.0);
        brakeGlowTrail = 1.0;
        tagVehTrail.textContent = 'TRAILING: EMERGENCY PANIC BRAKING!';
      }} else {{
        trailX = 37.0; trailY = 70.0; brakeGlowTrail = 1.0;
      }}
      tagVehTrail.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      vehEgo.style.left = `${{egoX}}%`; vehEgo.style.top = `${{egoY}}%`;
      vehTrail.style.left = `${{trailX}}%`; vehTrail.style.top = `${{trailY}}%`;
      vehEgo.style.opacity = '1.0'; vehTrail.style.opacity = '1.0';

      brakeEgo1.style.opacity = brakeGlowEgo; brakeEgo2.style.opacity = brakeGlowEgo;
      brakeTrail1.style.opacity = brakeGlowTrail; brakeTrail2.style.opacity = brakeGlowTrail;

      turnTrajectoryArc.setAttribute('opacity', '0.0');

      if (t >= 3.2 && t <= 6.5) {{
        tagVehEgo.style.opacity = '0.0';
        tagVehTrail.style.opacity = '0.0';
        hazardConflictZone.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';

        signalStateBadge.innerHTML = 'SIGNAL: VIOLATION (NO SIGNAL)';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        telemDist.textContent = '0 FT (FAILED TO SIGNAL)';
        telemDist.className = 'text-red-500 font-black animate-pulse';
        telemSpeed.textContent = 'CRASH IMPACT (REAR-END)';
        telemSpeed.className = 'text-red-400 font-bold';
        telemGap.textContent = '0 FT (COLLISION)';
        telemGap.className = 'text-red-500 font-black';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ CRITICAL HAZARD: SUDDEN TURN WITHOUT 100-FT SIGNAL ✕';
        hudNarrative.textContent = 'CRITICAL HAZARD: Failing to broadcast intention for 100 feet eliminates trailing driver reaction buffer, resulting in devastating rear-end collision!';
        complianceText.textContent = 'CRITICAL VIOLATION: FAILURE TO SIGNAL CONTINUOUSLY FOR 100 FT';
      }} else {{
        tagVehEgo.style.opacity = '1.0';
        tagVehTrail.style.opacity = '1.0';
        hazardConflictZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        signalStateBadge.innerHTML = 'SIGNAL: INACTIVE (VIOLATION)';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'WARNING: NO SIGNAL BROADCASTED WITHIN 100-FT ZONE';
      }}
    }}

    // ===============================================================
    // MAIN UPDATE DISPATCHER
    // ===============================================================
    function updateSimulation(t) {{
      timeDisplay.textContent = t.toFixed(2) + 's';
      timelineSlider.value = t;

      if (currentMode === 1) {{
        updateMode1(t);
      }} else if (currentMode === 2) {{
        updateMode2(t);
      }} else {{
        updateMode3(t);
      }}

      // Step Buttons Sync
      let activeStep = 1;
      if (currentMode === 1) {{
        if (t < 2.0) activeStep = 1;
        else if (t < 4.5) activeStep = 2;
        else if (t < 6.5) activeStep = 3;
        else activeStep = 4;
      }} else if (currentMode === 2) {{
        if (t < 2.5) activeStep = 1;
        else if (t < 4.5) activeStep = 2;
        else if (t < 6.5) activeStep = 3;
        else activeStep = 4;
      }} else {{
        if (t < 1.8) activeStep = 1;
        else if (t < 2.8) activeStep = 2;
        else if (t < 5.0) activeStep = 3;
        else activeStep = 4;
      }}

      stepBtns.forEach((btn, idx) => {{
        const s = idx + 1;
        if (s === activeStep) {{
          btn.className = 'step-btn px-2.5 py-1.5 rounded-lg border border-blue-500/60 bg-blue-500/15 text-left transition shadow';
          btn.querySelector('div:first-child').className = 'text-[9px] mono text-blue-400 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-white truncate';
        }} else {{
          btn.className = 'step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600';
          btn.querySelector('div:first-child').className = 'text-[9px] mono text-gray-500 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-gray-300 truncate';
        }}
      }});
    }}

    // ===============================================================
    // REQUEST ANIMATION FRAME LOOP
    // ===============================================================
    function tick(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const delta = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += delta * playbackSpeed;
        if (currentTime > DURATION) {{
          if (autoLoop) {{
            currentTime = 0.0;
          }} else {{
            currentTime = DURATION;
            isPlaying = false;
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
          }}
        }}
        updateSimulation(currentTime);
      }}

      requestAnimationFrame(tick);
    }}

    requestAnimationFrame(tick);

    // ===============================================================
    // USER CONTROLS & LISTENERS
    // ===============================================================
    playPauseBtn.addEventListener('click', () => {{
      isPlaying = !isPlaying;
      playIcon.classList.toggle('hidden', isPlaying);
      pauseIcon.classList.toggle('hidden', !isPlaying);
    }});

    resetBtn.addEventListener('click', () => {{
      currentTime = 0.0;
      updateSimulation(currentTime);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    autoLoopToggle.addEventListener('change', (e) => {{
      autoLoop = e.target.checked;
    }});

    speedBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        speedBtns.forEach(b => {{
          b.className = 'speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white';
        }});
        btn.className = 'speed-btn px-2 py-0.5 rounded bg-blue-600 text-white font-bold';
        playbackSpeed = parseFloat(btn.dataset.speed);
      }});
    }});

    modeBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        modeBtns.forEach(b => {{
          b.className = 'mode-btn px-3 py-1 rounded font-semibold text-gray-400 hover:text-white transition';
        }});
        currentMode = parseInt(btn.dataset.mode);
        if (currentMode === 1) {{
          btn.className = 'mode-btn px-3 py-1 rounded font-bold transition text-black bg-emerald-400 shadow';
        }} else if (currentMode === 2) {{
          btn.className = 'mode-btn px-3 py-1 rounded font-bold transition text-black bg-sky-400 shadow';
        }} else {{
          btn.className = 'mode-btn px-3 py-1 rounded font-bold transition text-white bg-red-600 shadow';
        }}

        const step1Lbl = document.getElementById('step-label-1');
        const step2Lbl = document.getElementById('step-label-2');
        const step3Lbl = document.getElementById('step-label-3');
        const step4Lbl = document.getElementById('step-label-4');

        if (currentMode === 1) {{
          step1Lbl.textContent = 'Approach Corridor (150 FT)';
          step2Lbl.textContent = '100-FT Statutory Trigger';
          step3Lbl.textContent = 'Continuous Signal & Decel';
          step4Lbl.textContent = 'Turn & Auto-Cancellation';
        }} else if (currentMode === 2) {{
          step1Lbl.textContent = 'Pre-Merge Inspection';
          step2Lbl.textContent = '100-FT Advance Signal';
          step3Lbl.textContent = 'Lateral Merge Execution';
          step4Lbl.textContent = 'Post-Merge Stabilization';
        }} else {{
          step1Lbl.textContent = '30 MPH Unannounced Approach';
          step2Lbl.textContent = 'Zero-Signal Threshold Breach';
          step3Lbl.textContent = 'Sudden Brake & Lockup';
          step4Lbl.textContent = 'Devastating Rear-End Crash';
        }}

        currentTime = 0.0;
        updateSimulation(currentTime);
      }});
    }});

    stepBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        const step = parseInt(btn.dataset.step);
        if (currentMode === 1) {{
          if (step === 1) currentTime = 0.8;
          else if (step === 2) currentTime = 2.2;
          else if (step === 3) currentTime = 4.2;
          else currentTime = 6.8;
        }} else if (currentMode === 2) {{
          if (step === 1) currentTime = 0.8;
          else if (step === 2) currentTime = 2.5;
          else if (step === 3) currentTime = 4.5;
          else currentTime = 6.8;
        }} else {{
          if (step === 1) currentTime = 0.8;
          else if (step === 2) currentTime = 2.4;
          else if (step === 3) currentTime = 3.4;
          else currentTime = 6.0;
        }}
        updateSimulation(currentTime);
      }});
    }});

    updateSimulation(0.0);
  </script>
</body>
</html>
'''

output_path = 'driving_rule_animations_suite/simulations/L05_T03_signaling_and_communication.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 12 simulation rebuilt successfully at: {output_path}")
