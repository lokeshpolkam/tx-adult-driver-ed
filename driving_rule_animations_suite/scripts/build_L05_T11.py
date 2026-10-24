import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return "data:image/png;base64," + base64.b64encode(img_file.read()).decode('utf-8')

def get_base64_jpg(image_path):
    with open(image_path, "rb") as img_file:
        return "data:image/jpeg;base64," + base64.b64encode(img_file.read()).decode('utf-8')

def build_simulation():
    # Assets
    highway_bg_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\roads\texas_highway_3lane_corridor.jpg"
    car_red_ne_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_red_ne.png"
    car_blue_ne_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_blue_ne.png"
    car_yellow_ne_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_yellow_ne.png"

    print("Encoding Lesson 19 assets to base64...")
    bg_b64 = get_base64_jpg(highway_bg_path)
    car_red_ne_b64 = get_base64_image(car_red_ne_path)
    car_blue_ne_b64 = get_base64_image(car_blue_ne_path)
    car_yellow_ne_b64 = get_base64_image(car_yellow_ne_path)
    print("Assets successfully encoded.")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson 19: Freeway Entry, Travel & Exit — Acceleration & Deceleration Lanes (TTC § 545.154 & § 545.060)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #0B0F17;
      color: #E2E8F0;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .custom-slider {{
      -webkit-appearance: none;
      height: 6px;
      border-radius: 3px;
      background: #1F2937;
      outline: none;
    }}
    .custom-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #10B981;
      cursor: pointer;
      border: 2px solid #064E3B;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.7);
    }}
    .custom-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.15);
      background: #34D399;
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.25; filter: drop-shadow(0 0 4px #10B981); }}
      50% {{ opacity: 0.65; filter: drop-shadow(0 0 12px #34D399); }}
    }}
    .merge-pulse {{
      animation: pulseGlow 2.4s ease-in-out infinite;
    }}
    @keyframes dangerPulse {{
      0%, 100% {{ transform: scale(1); opacity: 0.8; }}
      50% {{ transform: scale(1.18); opacity: 1.0; filter: drop-shadow(0 0 16px #EF4444); }}
    }}
    .danger-pulse {{
      animation: dangerPulse 1.2s ease-in-out infinite;
      transform-origin: center;
    }}
  </style>
</head>
<body class="p-3 md:p-6 flex flex-col items-center min-h-screen">

  <main class="w-full max-w-5xl flex flex-col gap-4">

    <!-- HEADER BAR -->
    <header class="bg-[#121824] border border-[#1E293B] rounded-2xl p-4 md:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
      <div>
        <div class="flex items-center space-x-2 mb-1">
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">TDLR ADE-1317</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 19</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L05-T11: Freeway Entry, Travel & Exit — Acceleration & Deceleration Lanes
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Driver Handbook Ch. 5 • TTC § 545.154 (Freeway On-Ramp Yield & Merge) & § 545.060 (Safe Lane Changing)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
          1: On-Ramp Acceleration & Merge
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: Deceleration Lane & Exit
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Dead Stop on Ramp
        </button>
        <div class="h-4 w-px bg-gray-700 mx-1"></div>
        <label class="flex items-center space-x-1.5 text-xs font-medium text-gray-300 cursor-pointer pr-1">
          <input type="checkbox" id="auto-loop-toggle" checked class="rounded bg-gray-800 border-gray-700 text-emerald-500 focus:ring-0">
          <span>Auto-Loop</span>
        </label>
      </div>
    </header>

    <!-- INTERACTIVE STEPPER CARDS -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <button class="step-card bg-[#121824] border border-blue-500/40 rounded-xl p-2.5 text-left transition hover:border-blue-400 group relative overflow-hidden" data-step="1">
        <div class="text-[10px] font-bold text-blue-400 mono flex items-center justify-between">
          <span>STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        </div>
        <div id="step-title-1" class="text-xs font-bold text-white mt-1 group-hover:text-blue-200">Ramp Curve & Signal (45 MPH)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Brisk Acceleration (58 MPH)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Speed Matched & Merge (65 MPH)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Mainlane Central Discipline</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG VECTOR OVERLAYS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <linearGradient id="accel-glow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.10" />
            <stop offset="60%" stop-color="#10B981" stop-opacity="0.25" />
            <stop offset="100%" stop-color="#10B981" stop-opacity="0.05" />
          </linearGradient>

          <linearGradient id="decel-glow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.22" />
            <stop offset="100%" stop-color="#F59E0B" stop-opacity="0.05" />
          </linearGradient>
        </defs>

        <!-- ACCELERATION LANE OVERLAY (Mode 1 & 3) -->
        <g id="accel-lane-group" opacity="1.0">
          <!-- Parallel Acceleration Runway along right shoulder (x=310 to x=685) -->
          <polygon points="310,480 640,281 685,356 355,555" fill="url(#accel-glow)" stroke="#10B981" stroke-width="1.5" stroke-dasharray="10,6" class="merge-pulse" />
          
          <!-- Dashed Merge Dividing Line (between Lane 1 and Accel Lane) -->
          <line x1="310" y1="480" x2="640" y2="281" stroke="#FFFFFF" stroke-width="2.5" stroke-dasharray="12,12" />
        </g>

        <!-- DECELERATION LANE OVERLAY (Mode 2) -->
        <g id="decel-lane-group" opacity="0.0">
          <polygon points="410,420 670,263 710,332 450,489" fill="url(#decel-glow)" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="10,6" />
          <line x1="410" y1="420" x2="670" y2="263" stroke="#FFFFFF" stroke-width="2.5" stroke-dasharray="12,12" />
          
          <!-- Texas Exit Advisory Sign -->
          <g id="sign-exit-post" transform="translate(685, 300)">
            <rect x="-1" y="0" width="3" height="26" fill="#94A3B8" />
            <rect x="-22" y="-30" width="44" height="30" rx="3" fill="#047857" stroke="#FFFFFF" stroke-width="1.2" />
            <text x="0" y="-19" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">EXIT 144</text>
            <rect x="-18" y="-12" width="36" height="10" fill="#F59E0B" />
            <text x="0" y="-4" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">30 MPH</text>
          </g>
        </g>

        <!-- DYNAMIC TRAFFIC GAP BRACKET ON FREEWAY (Between Lead Blue & Trail Yellow) -->
        <g id="gap-bracket-group" opacity="1.0">
          <path id="gap-line" d="M0,0 L0,0" stroke="#10B981" stroke-width="2" stroke-dasharray="8,6" />
          <circle id="gap-dot-lead" cx="0" cy="0" r="3.5" fill="#10B981" stroke="#064E3B" stroke-width="1.5" />
          <circle id="gap-dot-trail" cx="0" cy="0" r="3.5" fill="#10B981" stroke="#064E3B" stroke-width="1.5" />
          
          <!-- Gap Metric Badge (Floats in empty Lane 2, well above Lane 1 cars) -->
          <rect id="gap-badge-bg" x="0" y="0" width="205" height="19" rx="9.5" fill="#062418" stroke="#10B981" stroke-width="1.5" />
          <text id="gap-badge-text" x="0" y="0" fill="#6EE7B7" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">MERGE GAP: 4.5 SEC (430 FT)</text>
        </g>

        <!-- MODE 3: DEAD STOP IMPACT HAZARD CIRCLE -->
        <g id="hazard-impact-group" opacity="0.0">
          <circle id="hazard-circle" cx="0" cy="0" r="38" fill="#EF4444" fill-opacity="0.3" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="6,4" class="danger-pulse" />
          <polygon id="hazard-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- LEAD FREEWAY VEHICLE (BLUE SEDAN - LANE 1 AT 65 MPH) -->
      <div id="veh-lead" class="absolute z-20 pointer-events-none transition-transform" style="left: 60.0%; top: 46.6%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_ne_b64}" alt="Lead Freeway Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-lead" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          LEAD FREEWAY: 65 MPH (LANE 1)
        </div>
      </div>

      <!-- TRAILING FREEWAY VEHICLE (YELLOW SEDAN - LANE 1 AT 65 MPH) -->
      <div id="veh-trail" class="absolute z-20 pointer-events-none transition-transform" style="left: 22.0%; top: 84.8%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Trailing Freeway Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-trail" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          TRAILING FREEWAY: 65 MPH (LANE 1)
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - MERGING FROM ACCEL LANE INTO LANE 1) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none transition-transform" style="left: 35.0%; top: 83.1%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_ne_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          
          <!-- Left Turn Blinker -->
          <div id="blinker-left" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 25%; left: 72%;"></div>
          <!-- Right Turn Blinker -->
          <div id="blinker-right" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="bottom: 25%; right: 8%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2 h-2 rounded-full bg-red-500 filter blur-[1px] opacity-0" style="top: 35%; left: 10%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: RAMP APPROACH (45 MPH) • SIGNAL ACTIVE
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TTC § 545.154 MANDATE: MATCH FREEWAY FLOW SPEED & MERGE SAFELY</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#081C15]/90 border border-emerald-500/50 text-emerald-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="compliance-text">TTC § 545.154 FREEWAY MERGE COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & FREEWAY DYNAMICS HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[275px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">FREEWAY TELEMETRY HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">SPEED: MATCHING</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-speed">45 MPH</span>

          <span class="text-gray-400">Freeway Flow:</span>
          <span class="font-bold text-blue-400 mono text-right" id="telem-flow">65 MPH (LANE 1)</span>

          <span class="text-gray-400">Target Gap:</span>
          <span class="font-bold text-amber-400 mono text-right" id="telem-gap">4.5 SEC (430 FT)</span>

          <span class="text-gray-400">Signal Status:</span>
          <span class="font-bold text-yellow-400 mono text-right" id="telem-signal">LEFT BLINKER [ON]</span>

          <span class="text-gray-400">Lane Position:</span>
          <span class="font-bold text-emerald-300 mono text-right" id="telem-lane">ENTRANCE RAMP CURVE</span>

          <span class="text-gray-400">Merge Status:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-merge">SCANNING GAP</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Driver navigates entrance ramp curve at 45 MPH. Left turn signal active; scans mirrors to identify incoming traffic gaps on mainlanes.
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER (Positioned below status pill in clear air space) -->
      <div id="hazard-banner" class="absolute z-35 max-w-lg bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[11px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL HAZARD: NEVER COME TO A DEAD STOP ON AN ACCELERATION RAMP</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>UNLAWFUL RAMP STOPPING (TTC § 545.154 & § 545.401)</strong><br>
          Stopping dead on an entrance ramp eliminates the ability to match 65 MPH highway speed, creating severe rear-end crash risks from following ramp traffic and catastrophic collisions when pulling into high-speed mainlanes.
        </div>
      </div>

    </div>

    <!-- TIMELINE & PLAYBACK CONTROLS -->
    <footer class="bg-[#121824] border border-[#1E293B] rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <button id="play-pause-btn" class="w-10 h-10 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white flex items-center justify-center shadow-lg transition" title="Play/Pause">
          <svg id="icon-play" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          <svg id="icon-pause" class="w-4 h-4 hidden" fill="currentColor" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
        </button>
        <button id="reset-btn" class="w-10 h-10 rounded-xl bg-[#1A2333] hover:bg-[#253248] text-gray-300 hover:text-white flex items-center justify-center border border-[#2B3548] transition" title="Reset Simulation">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
        <span class="mono text-xs font-bold text-gray-400 w-16" id="time-display">0.00s</span>
      </div>

      <!-- Scrubber -->
      <div class="flex items-center space-x-3 w-full">
        <span class="text-[10px] font-bold text-gray-500 mono uppercase">Timeline</span>
        <input id="timeline-slider" type="range" min="0" max="6.0" step="0.05" value="0.0" class="custom-slider flex-1" />
        <span class="text-[10px] font-bold text-gray-500 mono">6.0s</span>
      </div>
    </footer>

  </main>

  <script>
    // --- SIMULATION STATE ---
    let currentMode = 1; // 1: Accel Merge, 2: Decel Exit, 3: Dead Stop Hazard
    let currentTime = 0.0;
    const duration = 6.0;
    let isPlaying = true;
    let lastTimestamp = null;

    // DOM Elements
    const vehEgo = document.getElementById('veh-ego');
    const vehLead = document.getElementById('veh-lead');
    const vehTrail = document.getElementById('veh-trail');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehLead = document.getElementById('tag-veh-lead');
    const tagVehTrail = document.getElementById('tag-veh-trail');

    const blinkerLeft = document.getElementById('blinker-left');
    const blinkerRight = document.getElementById('blinker-right');
    const brakeLights = document.getElementById('brake-lights');

    const accelLaneGroup = document.getElementById('accel-lane-group');
    const decelLaneGroup = document.getElementById('decel-lane-group');
    const gapBracketGroup = document.getElementById('gap-bracket-group');
    const gapLine = document.getElementById('gap-line');
    const gapDotLead = document.getElementById('gap-dot-lead');
    const gapDotTrail = document.getElementById('gap-dot-trail');
    const gapBadgeBg = document.getElementById('gap-badge-bg');
    const gapBadgeText = document.getElementById('gap-badge-text');

    const hazardImpactGroup = document.getElementById('hazard-impact-group');
    const hazardCircle = document.getElementById('hazard-circle');
    const hazardStar = document.getElementById('hazard-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const telemSpeed = document.getElementById('telem-speed');
    const telemFlow = document.getElementById('telem-flow');
    const telemGap = document.getElementById('telem-gap');
    const telemSignal = document.getElementById('telem-signal');
    const telemLane = document.getElementById('telem-lane');
    const telemMerge = document.getElementById('telem-merge');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const hudNarrative = document.getElementById('hud-narrative');

    const playPauseBtn = document.getElementById('play-pause-btn');
    const iconPlay = document.getElementById('icon-play');
    const iconPause = document.getElementById('icon-pause');
    const resetBtn = document.getElementById('reset-btn');
    const timelineSlider = document.getElementById('timeline-slider');
    const timeDisplay = document.getElementById('time-display');
    const autoLoopToggle = document.getElementById('auto-loop-toggle');

    // Highway Geometry Equations:
    // Slope m = -1.005 (in % units: y = Y0 - 1.005 * (x - 50.0))
    function getLane1Y(x) {{
      return 56.62 - 1.005 * (x - 50.0);
    }}
    function getLane2Y(x) {{
      return 42.56 - 1.005 * (x - 50.0);
    }}
    function getAccelLaneY(x) {{
      return 68.00 - 1.005 * (x - 50.0);
    }}

    // Step definitions for each mode
    const stepConfigs = {{
      1: [
        {{ time: 0.8, title: "Ramp Curve & Signal (45 MPH)" }},
        {{ time: 2.2, title: "Brisk Acceleration (58 MPH)" }},
        {{ time: 3.6, title: "Speed Matched & Merge (65 MPH)" }},
        {{ time: 5.0, title: "Mainlane Central Discipline" }}
      ],
      2: [
        {{ time: 0.8, title: "Exit Approach (65 MPH No Tap)" }},
        {{ time: 2.2, title: "Decel Runway Egress (65 MPH)" }},
        {{ time: 3.8, title: "Controlled Decel in Runway" }},
        {{ time: 5.2, title: "Ramp Curve Advisory (30 MPH)" }}
      ],
      3: [
        {{ time: 0.8, title: "Timid Ramp Speed (30 MPH)" }},
        {{ time: 2.2, title: "Panic Braking on Runway" }},
        {{ time: 3.6, title: "DEAD STOP ON RAMP (0 MPH)" }},
        {{ time: 5.0, title: "Critical Rear-End Crash Hazard" }}
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40';
          else if (m === 2) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500 bg-red-600 text-white shadow-md shadow-red-900/40';
        }} else {{
          if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60';
          else btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white';
        }}
      }});

      // Update step button labels
      const steps = stepConfigs[mode];
      steps.forEach((cfg, idx) => {{
        const titleElem = document.getElementById(`step-title-${{idx + 1}}`);
        if (titleElem) titleElem.textContent = cfg.title;
      }});

      // Show/hide lane overlays
      if (mode === 1 || mode === 3) {{
        accelLaneGroup.setAttribute('opacity', '1.0');
        decelLaneGroup.setAttribute('opacity', '0.0');
      }} else if (mode === 2) {{
        accelLaneGroup.setAttribute('opacity', '0.0');
        decelLaneGroup.setAttribute('opacity', '1.0');
      }}

      currentTime = 0.0;
      updateSimulation(currentTime);
    }}

    function jumpToStep(stepIdx) {{
      const steps = stepConfigs[currentMode];
      if (steps && steps[stepIdx - 1]) {{
        currentTime = steps[stepIdx - 1].time;
        timelineSlider.value = currentTime.toFixed(2);
        updateSimulation(currentTime);
      }}
    }}

    function updateSimulation(t) {{
      timeDisplay.textContent = `${{t.toFixed(2)}}s`;
      timelineSlider.value = t.toFixed(2);

      // Blinker flash tick
      const blinkOn = (Math.sin(t * 12) > 0);

      // =========================================================================
      // MODE 1: PROPER ON-RAMP ACCELERATION & SPEED-MATCHED MERGE (TTC § 545.154)
      // =========================================================================
      if (currentMode === 1) {{
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        vehLead.style.opacity = '1.0';
        vehTrail.style.opacity = '1.0';

        // Vehicle Progress
        // Blue Lead: 65 MPH in Lane 1
        const blueX = 62.0 + (t / duration) * 11.0; // 62% to 73%
        const blueY = getLane1Y(blueX);

        // Yellow Trail: 65 MPH in Lane 1
        const yellowX = 20.0 + (t / duration) * 11.0; // 20% to 31%
        const yellowY = getLane1Y(yellowX);

        // Ego Car: Accel Lane then Merge into Lane 1
        let egoX, egoY, egoSpeed, mergeStatus, laneText;
        if (t < 2.8) {{
          // Phase 1: In Acceleration Runway (x = 40% to 49%)
          const progress = t / 2.8;
          egoX = 40.0 + progress * 9.0;
          egoY = getAccelLaneY(egoX);
          egoSpeed = Math.round(45 + progress * 17); // 45 -> 62 MPH
          blinkerLeft.style.opacity = blinkOn ? '1.0' : '0.0';
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          mergeStatus = 'ACCELERATING';
          laneText = 'ACCELERATION RUNWAY';
        }} else if (t < 4.2) {{
          // Phase 2: Smooth Transition into Lane 1 Gap
          const progress = (t - 2.8) / 1.4;
          egoX = 49.0 + progress * 5.0; // 49% to 54%
          const yAccel = getAccelLaneY(egoX);
          const yLane1 = getLane1Y(egoX);
          egoY = yAccel + progress * (yLane1 - yAccel);
          egoSpeed = 65;
          blinkerLeft.style.opacity = blinkOn ? '1.0' : '0.0';
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          mergeStatus = 'MERGING INTO GAP';
          laneText = 'MERGING INTO LANE 1';
        }} else {{
          // Phase 3: Established in Lane 1 with Safe Buffer
          const progress = (t - 4.2) / 1.8;
          egoX = 54.0 + progress * 4.0; // 54% to 58%
          egoY = getLane1Y(egoX);
          egoSpeed = 65;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          mergeStatus = 'MERGE COMPLETE';
          laneText = 'LANE 1 (CRUISING)';
        }}

        // Position vehicle sprites
        vehLead.style.left = `${{blueX}}%`;
        vehLead.style.top = `${{blueY}}%`;
        tagVehLead.textContent = 'LEAD FREEWAY: 65 MPH (LANE 1)';

        vehTrail.style.left = `${{yellowX}}%`;
        vehTrail.style.top = `${{yellowY}}%`;
        tagVehTrail.textContent = 'TRAILING FREEWAY: 65 MPH (LANE 1)';

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        // Update Dynamic Traffic Gap Bracket
        if (t < 4.0) {{
          gapBracketGroup.setAttribute('opacity', '1.0');
          const blueSvgX = blueX * 10;
          const blueSvgY = blueY * 6;
          const yellowSvgX = yellowX * 10;
          const yellowSvgY = yellowY * 6;
          gapLine.setAttribute('d', `M ${{blueSvgX}},${{blueSvgY}} L ${{yellowSvgX}},${{yellowSvgY}}`);
          gapDotLead.setAttribute('cx', blueSvgX);
          gapDotLead.setAttribute('cy', blueSvgY);
          gapDotTrail.setAttribute('cx', yellowSvgX);
          gapDotTrail.setAttribute('cy', yellowSvgY);

          // Badge in Lane 2 (empty middle lane)
          const midX = (blueX + yellowX) / 2;
          const badgeSvgX = midX * 10;
          const badgeSvgY = getLane2Y(midX) * 6;
          gapBadgeBg.setAttribute('x', badgeSvgX - 102.5);
          gapBadgeBg.setAttribute('y', badgeSvgY - 9.5);
          gapBadgeText.setAttribute('x', badgeSvgX);
          gapBadgeText.setAttribute('y', badgeSvgY + 4);
        }} else {{
          gapBracketGroup.setAttribute('opacity', '0.0');
        }}

        // HUD & Narrative
        telemSpeed.textContent = `${{egoSpeed}} MPH`;
        telemFlow.textContent = '65 MPH (LANE 1)';
        telemGap.textContent = '4.5 SEC (430 FT)';
        telemLane.textContent = laneText;
        telemMerge.textContent = mergeStatus;

        if (t < 1.5) {{
          tagVehEgo.textContent = 'EGO: RAMP APPROACH (45 MPH) • SIGNAL ACTIVE';
          pillStatusText.textContent = 'TTC § 545.154 MANDATE: MATCH FREEWAY FLOW SPEED & MERGE SAFELY';
          hudNarrative.textContent = 'Step 1: Driver navigates entrance ramp curve at 45 MPH. Left turn signal active; scans mirrors to identify incoming traffic gaps on mainlanes.';
          signalStateBadge.textContent = 'RAMP SCAN';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        }} else if (t < 3.0) {{
          tagVehEgo.textContent = `EGO: BRISK ACCELERATION (${{egoSpeed}} MPH) • MATCHING FLOW`;
          pillStatusText.textContent = 'DEDICATED ACCELERATION RUNWAY: ACCELERATE BRISKLY TO 65 MPH';
          hudNarrative.textContent = 'Step 2: Entering dedicated acceleration runway! Driver accelerates firmly to match 65 MPH highway speed before attempting merge.';
          signalStateBadge.textContent = 'ACCELERATING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else if (t < 4.5) {{
          tagVehEgo.textContent = 'EGO: 65 MPH • SMOOTH MERGE INTO LANE 1 GAP';
          pillStatusText.textContent = 'GAP ACHIEVED: SEAMLESS 65 MPH ENTRY (TTC § 545.154)';
          hudNarrative.textContent = 'Step 3: Speed perfectly matched at 65 MPH. Driver executes physical blind spot check and glides smoothly into the 4.5-sec gap between Blue and Yellow vehicles.';
          signalStateBadge.textContent = 'MERGE EXECUTED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: 65 MPH • CENTRAL DISCIPLINE & 3-SEC BUFFER';
          pillStatusText.textContent = 'ESTABLISHED CRUISE: 3-SECOND BUFFER FRONT & REAR';
          hudNarrative.textContent = 'Step 4: Turn signal cancelled. Driver settles into center of Lane 1, maintaining safe 3-second space cushion ahead and behind.';
          signalStateBadge.textContent = 'CRUISING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 2: FREEWAY EXIT & DECELERATION LANE (NO BRAKING IN MAINLANES)
      // =========================================================================
      else if (currentMode === 2) {{
        gapBracketGroup.setAttribute('opacity', '0.0');
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        // Vehicle Progress
        // Yellow car follows in Lane 1 at constant 65 MPH
        const yellowX = 22.0 + (t / duration) * 20.0; // 22% to 42%
        const yellowY = getLane1Y(yellowX);
        vehTrail.style.left = `${{yellowX}}%`;
        vehTrail.style.top = `${{yellowY}}%`;
        vehTrail.style.opacity = '1.0';
        tagVehTrail.textContent = 'TRAILING TRAFFIC: 65 MPH (LANE 1)';

        // Blue car is cruising ahead in Lane 2 at 65 MPH
        const blueX = 54.0 + (t / duration) * 14.0; // 54% to 68%
        const blueY = getLane2Y(blueX);
        vehLead.style.left = `${{blueX}}%`;
        vehLead.style.top = `${{blueY}}%`;
        vehLead.style.opacity = '1.0';
        tagVehLead.textContent = 'THRU TRAFFIC: 65 MPH (LANE 2)';

        // Ego Vehicle: Starts in Lane 1, enters Decel Lane at 65 MPH, THEN brakes
        let egoX, egoY, egoSpeed, mergeStatus, laneText;
        if (t < 1.6) {{
          // Phase 1: Lane 1 approach at 65 MPH (No brake lights!)
          const progress = t / 1.6;
          egoX = 36.0 + progress * 6.0; // 36% to 42%
          egoY = getLane1Y(egoX);
          egoSpeed = 65;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          brakeLights.style.opacity = '0.0';
          mergeStatus = 'APPROACHING EXIT';
          laneText = 'LANE 1 (MAINLANE)';
        }} else if (t < 3.2) {{
          // Phase 2: Transition into Deceleration Lane at full 65 MPH
          const progress = (t - 1.6) / 1.6;
          egoX = 42.0 + progress * 10.0; // 42% to 52%
          const yLane1 = getLane1Y(egoX);
          const yDecel = getAccelLaneY(egoX);
          egoY = yLane1 + progress * (yDecel - yLane1);
          egoSpeed = 65;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          brakeLights.style.opacity = '0.0';
          mergeStatus = 'EGRESS TO RUNWAY';
          laneText = 'DECELERATION RUNWAY';
        }} else if (t < 4.8) {{
          // Phase 3: Controlled Braking INSIDE Decel Lane (65 -> 40 MPH)
          const progress = (t - 3.2) / 1.6;
          egoX = 52.0 + progress * 8.0; // 52% to 60%
          egoY = getAccelLaneY(egoX);
          egoSpeed = Math.round(65 - progress * 25); // 65 -> 40 MPH
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          brakeLights.style.opacity = '1.0'; // Brakes active!
          mergeStatus = 'BRAKING IN RUNWAY';
          laneText = 'DECELERATION RUNWAY';
        }} else {{
          // Phase 4: Ramp Advisory Curve (30 MPH)
          const progress = (t - 4.8) / 1.2;
          egoX = 60.0 + progress * 5.0; // 60% to 65%
          egoY = getAccelLaneY(egoX);
          egoSpeed = 30;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          mergeStatus = 'RAMP ADVISORY 30 MPH';
          laneText = 'EXIT RAMP CURVE';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        telemSpeed.textContent = `${{egoSpeed}} MPH`;
        telemFlow.textContent = '65 MPH (MAINLANES)';
        telemGap.textContent = 'CLEAR RAMP';
        telemSignal.textContent = 'RIGHT BLINKER [ON]';
        telemLane.textContent = laneText;
        telemMerge.textContent = mergeStatus;

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: 65 MPH • SIGNALING EXIT (NO BRAKING IN MAINLANE)';
          pillStatusText.textContent = 'MANDATE: NEVER SLOW DOWN IN FREEWAY TRAVEL LANES';
          hudNarrative.textContent = 'Step 1: Driver signals right 100 FT before exit. Crucially, speed is held at 65 MPH — never tap brakes in main travel lanes.';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: 65 MPH • ENTERING DECELERATION RUNWAY';
          pillStatusText.textContent = 'TTC § 545.154 MANDATE: EXIT INTO DECELERATION LANE BEFORE BRAKING';
          hudNarrative.textContent = 'Step 2: Smooth transition across gore line into deceleration runway at full 65 MPH. Mainlane flow behind Ego is completely unobstructed.';
        }} else if (t < 4.8) {{
          tagVehEgo.textContent = `EGO: CONTROLLED BRAKING (${{egoSpeed}} MPH) IN DECEL LANE`;
          pillStatusText.textContent = 'BRAKING AUTHORIZED: INSIDE DEDICATED DECELERATION RUNWAY';
          hudNarrative.textContent = 'Step 3: Once fully within the deceleration runway, apply firm, progressive braking to scrub speed safely off the highway.';
        }} else {{
          tagVehEgo.textContent = 'EGO: 30 MPH • EXIT RAMP CURVE ADVISORY';
          pillStatusText.textContent = 'RAMP ADVISORY COMPLIANCE: 30 MPH SPEED LIMIT';
          hudNarrative.textContent = 'Step 4: Reaching the curve of Exit 144, driver conforms strictly to the 30 MPH advisory speed to prevent rollover or departure.';
        }}
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: DEAD STOP ON ACCELERATION RAMP (TTC § 545.154 & § 545.401)
      // =========================================================================
      else if (currentMode === 3) {{
        gapBracketGroup.setAttribute('opacity', '0.0');

        // Blue car rushes past in Lane 1 at 65 MPH
        const blueX = 56.0 + (t / duration) * 14.0;
        const blueY = getLane1Y(blueX);
        vehLead.style.left = `${{blueX}}%`;
        vehLead.style.top = `${{blueY}}%`;
        tagVehLead.textContent = 'MAINLANE FLOW: 65 MPH (NO STOPPING GAP)';

        // Ego Car: Enters ramp timidly at 30 MPH, panics, and STOPS at 0 MPH!
        let egoX, egoY, egoSpeed;
        if (t < 1.8) {{
          const progress = t / 1.8;
          egoX = 40.0 + progress * 8.0; // 40% to 48%
          egoY = getAccelLaneY(egoX);
          egoSpeed = 30;
          brakeLights.style.opacity = '0.0';
          blinkerLeft.style.opacity = blinkOn ? '1.0' : '0.0';
        }} else if (t < 3.0) {{
          // Panic Braking
          const progress = (t - 1.8) / 1.2;
          egoX = 48.0 + progress * 4.0; // 48% to 52%
          egoY = getAccelLaneY(egoX);
          egoSpeed = Math.round(30 * (1 - progress)); // 30 -> 0 MPH
          brakeLights.style.opacity = '1.0';
          blinkerLeft.style.opacity = blinkOn ? '1.0' : '0.0';
        }} else {{
          // Complete Dead Stop at 0 MPH
          egoX = 52.0;
          egoY = getAccelLaneY(egoX);
          egoSpeed = 0;
          brakeLights.style.opacity = '1.0';
          blinkerLeft.style.opacity = '0.0';
        }}

        // Trailing ramp vehicle follows behind and must panic brake to avoid crushing Ego
        let yellowX, yellowY;
        if (t < 2.0) {{
          const progress = t / 2.0;
          yellowX = 26.0 + progress * 10.0; // 26% to 36%
          yellowY = getAccelLaneY(yellowX);
        }} else {{
          const progress = Math.min(1.0, (t - 2.0) / 1.4);
          yellowX = 36.0 + progress * 6.0; // stops at 42%
          yellowY = getAccelLaneY(yellowX);
        }}

        vehTrail.style.left = `${{yellowX}}%`;
        vehTrail.style.top = `${{yellowY}}%`;
        tagVehTrail.textContent = (t >= 2.4) ? 'TRAILING RAMP: PANIC EMERGENCY STOP!' : 'TRAILING RAMP TRAFFIC (45 MPH)';

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        const egoSvgX = egoX * 10;
        const egoSvgY = egoY * 6;

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (DEAD STOP)' : `${{egoSpeed}} MPH`;
        telemFlow.textContent = '65 MPH (RUSHING)';
        telemGap.textContent = (egoSpeed === 0) ? 'TRAPPED (NO GAP)' : 'NARROWING';
        telemLane.textContent = 'ACCEL RAMP BLOCKED';
        telemMerge.textContent = (egoSpeed === 0) ? 'ZERO ACCELERATION!' : 'DECELERATING ON RAMP';

        pillStatusText.textContent = 'CRITICAL FREEWAY HAZARD: NEVER COME TO A DEAD STOP ON AN ACCELERATION RAMP';

        if (t < 1.8) {{
          tagVehEgo.textContent = 'EGO: TIMID RAMP SPEED (30 MPH) • FAILURE TO ACCELERATE';
          hudNarrative.textContent = 'Step 1: Driver approaches freeway timidly at only 30 MPH instead of accelerating. Failing to match highway speed creates an immediate merge hazard.';
          hazardImpactGroup.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
        }} else if (t < 3.0) {{
          tagVehEgo.textContent = `EGO: PANIC BRAKING (${{egoSpeed}} MPH) ON ACCELERATION RUNWAY`;
          hudNarrative.textContent = 'Step 2: Seeing 65 MPH highway traffic, driver panics and slams on brakes in the middle of the acceleration runway! Speed drops to 0 MPH.';
          hazardImpactGroup.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
        }} else {{
          tagVehEgo.textContent = 'EGO: DEAD STOP (0 MPH) • EXTREME REAR-END COLLISION RISK';
          hudNarrative.textContent = 'Step 3 & 4: Trapped at 0 MPH! It is impossible to merge into 65 MPH traffic without an enormous gap. Trailing ramp cars face catastrophic rear-end collisions.';
          hazardImpactGroup.setAttribute('opacity', '1.0');
          hazardCircle.setAttribute('cx', egoSvgX);
          hazardCircle.setAttribute('cy', egoSvgY);
          hazardStar.setAttribute('transform', `translate(${{egoSvgX}}, ${{egoSvgY}})`);
          hazardBanner.style.opacity = '1.0';
        }}
      }}

      // Update Stepper active state
      const steps = stepConfigs[currentMode];
      let currentStepIdx = 1;
      for (let i = steps.length - 1; i >= 0; i--) {{
        if (t >= steps[i].time - 0.1) {{
          currentStepIdx = i + 1;
          break;
        }}
      }}

      document.querySelectorAll('.step-card').forEach((card, idx) => {{
        const isCurrent = (idx + 1 === currentStepIdx);
        if (isCurrent) {{
          card.classList.remove('border-[#1E293B]');
          card.classList.add('border-blue-500/60', 'bg-blue-950/20');
        }} else {{
          card.classList.remove('border-blue-500/60', 'bg-blue-950/20');
          card.classList.add('border-[#1E293B]');
        }}
      }});
    }}

    // Animation Loop
    function animate(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = (timestamp - lastTimestamp) / 1000;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += dt;
        if (currentTime > duration) {{
          if (autoLoopToggle.checked) {{
            currentTime = 0.0;
          }} else {{
            currentTime = duration;
            isPlaying = false;
            updatePlayPauseButton();
          }}
        }}
        updateSimulation(currentTime);
      }}

      requestAnimationFrame(animate);
    }}

    function updatePlayPauseButton() {{
      if (isPlaying) {{
        iconPlay.classList.add('hidden');
        iconPause.classList.remove('hidden');
      }} else {{
        iconPlay.classList.remove('hidden');
        iconPause.classList.add('hidden');
      }}
    }}

    playPauseBtn.addEventListener('click', () => {{
      isPlaying = !isPlaying;
      lastTimestamp = null;
      updatePlayPauseButton();
    }});

    resetBtn.addEventListener('click', () => {{
      currentTime = 0.0;
      updateSimulation(currentTime);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    document.querySelectorAll('.mode-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const mode = parseInt(btn.dataset.mode);
        setMode(mode);
      }});
    }});

    document.querySelectorAll('.step-card').forEach(card => {{
      card.addEventListener('click', () => {{
        const step = parseInt(card.dataset.step);
        jumpToStep(step);
      }});
    }});

    // Initialize
    setMode(1);
    requestAnimationFrame(animate);
  </script>
</body>
</html>
"""

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L05_T11_freeway_entry_exit.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 19 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_simulation()
