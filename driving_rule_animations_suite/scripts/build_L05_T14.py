import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return "data:image/png;base64," + base64.b64encode(img_file.read()).decode('utf-8')

def get_base64_jpg(image_path):
    with open(image_path, "rb") as img_file:
        return "data:image/jpeg;base64," + base64.b64encode(img_file.read()).decode('utf-8')

def build_simulation():
    highway_bg_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\roads\texas_highway_3lane_corridor.jpg"
    car_red_ne_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_red_ne.png"
    car_blue_ne_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_blue_ne.png"
    car_yellow_ne_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_yellow_ne.png"

    print("Encoding Lesson 21 assets to base64...")
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
  <title>Lesson 21: Blowouts, Skids, and Loss of Traction (TTC § 545.351 & § 545.401)</title>
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
      0%, 100% {{ opacity: 0.35; filter: drop-shadow(0 0 4px #10B981); }}
      50% {{ opacity: 0.85; filter: drop-shadow(0 0 14px #34D399); }}
    }}
    .safe-pulse {{
      animation: pulseGlow 2.0s ease-in-out infinite;
    }}
    @keyframes dangerPulse {{
      0%, 100% {{ transform: scale(1); opacity: 0.75; }}
      50% {{ transform: scale(1.15); opacity: 1.0; filter: drop-shadow(0 0 16px #EF4444); }}
    }}
    .danger-pulse {{
      animation: dangerPulse 1.2s ease-in-out infinite;
      transform-origin: center;
    }}
    @keyframes steeringWiggle {{
      0%, 100% {{ transform: rotate(0deg); }}
      25% {{ transform: rotate(-10deg); }}
      75% {{ transform: rotate(10deg); }}
    }}
    .steer-pulse {{
      animation: steeringWiggle 0.8s ease-in-out infinite;
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
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-purple-500/20 text-purple-400 border border-purple-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 21</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L05-T14: Blowouts, Skids, and Loss of Traction — Emergency Control
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Driver Handbook Ch. 5 • TTC § 545.351 (Basic Speed & Control Law) & § 545.401 (Reckless Driving Prevention)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
          1: Rear Skid Control ("Steer Into Skid")
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: High-Speed Tire Blowout
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Panic Braking in Skid
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
        <div id="step-title-1" class="text-xs font-bold text-white mt-1 group-hover:text-blue-200">Rear Skid Yaw (+18°)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Ease Off Gas (No Brakes!)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Steer in Direction of Skid</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Straighten Wheels & Recover</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG VECTOR OVERLAYS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <!-- Skid tire marks pattern -->
          <linearGradient id="skid-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#1F2937" stop-opacity="0.2" />
            <stop offset="50%" stop-color="#111827" stop-opacity="0.7" />
            <stop offset="100%" stop-color="#1F2937" stop-opacity="0.1" />
          </linearGradient>

          <!-- Counter-Steer Direction Arrow Marker -->
          <marker id="arrow-counter" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#10B981" />
          </marker>
          <marker id="arrow-danger" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#EF4444" />
          </marker>
        </defs>

        <!-- SKID TIRE TRACKS (Dynamic SVG arcs) -->
        <g id="skid-tracks-group" opacity="0.0">
          <path id="track-rear-left" d="M 420,320 Q 450,290 480,265" stroke="#1F2937" stroke-width="4.5" stroke-linecap="round" fill="none" opacity="0.65" />
          <path id="track-rear-right" d="M 435,335 Q 465,305 495,280" stroke="#1F2937" stroke-width="4.5" stroke-linecap="round" fill="none" opacity="0.65" />
        </g>

        <!-- COUNTER-STEER VECTOR CALLOUT (Mode 1 Step 3) -->
        <g id="counter-steer-group" opacity="0.0" class="transition-opacity duration-300">
          <path id="steer-vector-arc" d="M 480,310 C 510,315 540,305 560,285" stroke="#10B981" stroke-width="3" stroke-dasharray="6,4" fill="none" marker-end="url(#arrow-counter)" />
          <g transform="translate(545, 325)">
            <rect x="-65" y="-12" width="130" height="18" rx="9" fill="#062418" stroke="#10B981" stroke-width="1.2" />
            <text x="0" y="0" fill="#6EE7B7" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">STEER INTO SKID &rarr;</text>
          </g>
        </g>

        <!-- BLOWOUT FORCE VECTOR CALLOUT (Mode 2) -->
        <g id="blowout-vector-group" opacity="0.0" class="transition-opacity duration-300">
          <circle id="blowout-spark" cx="0" cy="0" r="16" fill="#F59E0B" fill-opacity="0.4" stroke="#D97706" stroke-width="2" class="danger-pulse" />
          <g id="blowout-badge" transform="translate(490, 420)">
            <rect x="-65" y="-14" width="130" height="18" rx="9" fill="#2B1B05" stroke="#F59E0B" stroke-width="1.2" />
            <text x="0" y="-2" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">BLOWOUT: FIRM GRIP</text>
          </g>
        </g>

        <!-- MODE 3: SPIN-OUT DANGER HALO & ROTATION TRACKS -->
        <g id="spin-hazard-group" opacity="0.0">
          <!-- 360 degree spin skid arcs -->
          <ellipse cx="480" cy="270" rx="60" ry="32" fill="none" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="8,6" class="danger-pulse" />
          <polygon id="hazard-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- BLUE THRU HIGHWAY VEHICLE (LANE 2 AHEAD AT 65 MPH) -->
      <div id="veh-blue" class="absolute z-20 pointer-events-none transition-transform" style="left: 64.0%; top: 28.5%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_ne_b64}" alt="Thru Vehicle Lane 2" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          THRU FLOW: 65 MPH (LANE 2)
        </div>
      </div>

      <!-- YELLOW TRAFFIC VEHICLE (LANE 1 TRAILING AT 65 MPH) -->
      <div id="veh-yellow" class="absolute z-20 pointer-events-none transition-transform" style="left: 22.0%; top: 84.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Highway Traffic Lane 1" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          FOLLOWING FLOW: 65 MPH (LANE 1)
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - DYNAMIC YAW / ROTATION SIMULATION) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none" style="left: 46.0%; top: 46.6%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_red_ne_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          
          <!-- Hazard Flashers Front & Rear -->
          <div id="flasher-front" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 25%; left: 75%;"></div>
          <div id="flasher-rear" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 35%; left: 10%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 35%; left: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: REAR SKID DETECTED • YAW +18°
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS SKID RULE: EASE OFF GAS • NEVER SLAM BRAKES • STEER INTO SKID</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#081C15]/90 border border-emerald-500/50 text-emerald-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="compliance-text">TTC § 545.351 VEHICLE CONTROL COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & TRACTION DYNAMICS HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[275px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">TRACTION DYNAMICS HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono">SKID DETECTED</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-speed">48 MPH</span>

          <span class="text-gray-400">Yaw Angle:</span>
          <span class="font-bold text-amber-400 mono text-right" id="telem-yaw">+18° (REAR RIGHT)</span>

          <span class="text-gray-400">Throttle Input:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-throttle">OFF ACCELERATOR</span>

          <span class="text-gray-400">Braking Action:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-brake">NO BRAKES (SAFE)</span>

          <span class="text-gray-400">Steering Input:</span>
          <span class="font-bold text-emerald-300 mono text-right" id="telem-steer">TURN INTO SKID →</span>

          <span class="text-gray-400">Traction Status:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-traction">REGAINING GRIP</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Rear tires lose adhesion on slippery pavement. Rear end slides right (+18° yaw angle). Driver immediately feels steering lighten.
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER (Positioned below status pill in clear air space) -->
      <div id="hazard-banner" class="absolute z-35 w-[350px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10.5px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL HAZARD: NEVER SLAM BRAKES IN A SKID</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>TOTAL CONTROL LOSS (TTC § 545.351 & § 545.401)</strong><br>
          Slamming brakes while skidding locks wheels and destroys all steering control, provoking an uncontrollable 360° spin into oncoming highway traffic.
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
    let currentMode = 1; // 1: Rear Skid Control, 2: Tire Blowout, 3: Panic Brake Spin-Out
    let currentTime = 0.0;
    const duration = 6.0;
    let isPlaying = true;
    let lastTimestamp = null;

    // DOM Elements
    const vehEgo = document.getElementById('veh-ego');
    const vehEgoSprite = document.getElementById('veh-ego-sprite');
    const vehBlue = document.getElementById('veh-blue');
    const vehYellow = document.getElementById('veh-yellow');

    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehBlue = document.getElementById('tag-veh-blue');
    const tagVehYellow = document.getElementById('tag-veh-yellow');

    const flasherFront = document.getElementById('flasher-front');
    const flasherRear = document.getElementById('flasher-rear');
    const brakeLights = document.getElementById('brake-lights');

    const skidTracksGroup = document.getElementById('skid-tracks-group');
    const counterSteerGroup = document.getElementById('counter-steer-group');
    const blowoutVectorGroup = document.getElementById('blowout-vector-group');
    const blowoutSpark = document.getElementById('blowout-spark');
    const blowoutBadge = document.getElementById('blowout-badge');

    const spinHazardGroup = document.getElementById('spin-hazard-group');
    const hazardStar = document.getElementById('hazard-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const telemSpeed = document.getElementById('telem-speed');
    const telemYaw = document.getElementById('telem-yaw');
    const telemThrottle = document.getElementById('telem-throttle');
    const telemBrake = document.getElementById('telem-brake');
    const telemSteer = document.getElementById('telem-steer');
    const telemTraction = document.getElementById('telem-traction');
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
    function getLane3Y(x) {{
      return 28.50 - 1.005 * (x - 50.0);
    }}
    function getShoulderY(x) {{
      return 68.50 - 1.005 * (x - 50.0);
    }}

    // Step definitions for each mode
    const stepConfigs = {{
      1: [
        {{ time: 0.8, title: "Rear Skid Yaw (+18°)" }},
        {{ time: 2.2, title: "Ease Off Gas (No Brakes!)" }},
        {{ time: 3.6, title: "Steer in Direction of Skid" }},
        {{ time: 5.0, title: "Straighten Wheels & Recover" }}
      ],
      2: [
        {{ time: 0.8, title: "Blowout: Violent Pull Force" }},
        {{ time: 2.2, title: "Firm 2-Hand Wheel Grip" }},
        {{ time: 3.6, title: "Coast Straight (No Panic Tap)" }},
        {{ time: 5.0, title: "Gentle Stop on Shoulder" }}
      ],
      3: [
        {{ time: 0.8, title: "Initial Rear Skid (+18°)" }},
        {{ time: 2.2, title: "Panic Slam on Brakes!" }},
        {{ time: 3.6, title: "Fatal 360° Spin-Out" }},
        {{ time: 5.0, title: "Multi-Lane Crash Hazard" }}
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

      // Blinker tick
      const blinkOn = (Math.sin(t * 10) > 0);

      // =========================================================================
      // MODE 1: REAR-WHEEL OVERSTEER SKID & RECOVERY ("STEER INTO SKID")
      // =========================================================================
      if (currentMode === 1) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        blowoutVectorGroup.setAttribute('opacity', '0.0');
        brakeLights.style.opacity = '0.0';
        flasherFront.style.opacity = '0.0';
        flasherRear.style.opacity = '0.0';

        // Blue Car in Lane 2 ahead at 65 MPH
        const blueX = 66.0 + (t / duration) * 10.0; // 66% to 76%
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 65 MPH (LANE 2)';

        // Yellow Car in Lane 1 trailing at 65 MPH
        const yellowX = 26.0 + (t / duration) * 12.0; // 26% to 38%
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'FOLLOWING FLOW: 65 MPH (LANE 1)';

        // Ego Car: Yaw dynamics and recovery in Lane 2
        let egoX, egoY, yawAngle, egoSpeed;
        if (t < 1.6) {{
          // Phase 1: Skid breaks loose (+18 deg yaw)
          const progress = t / 1.6;
          egoX = 42.0 + progress * 4.0; // 42% to 46%
          egoY = getLane2Y(egoX);
          yawAngle = progress * 18.0; // 0 -> +18 deg
          egoSpeed = Math.round(50 - progress * 4); // 50 -> 46 MPH
          skidTracksGroup.setAttribute('opacity', `${{progress * 0.7}}`);
          counterSteerGroup.setAttribute('opacity', '0.0');
        }} else if (t < 3.0) {{
          // Phase 2: Peak skid (+22 deg), easing off gas, no brakes
          const progress = (t - 1.6) / 1.4;
          egoX = 46.0 + progress * 3.0; // 46% to 49%
          egoY = getLane2Y(egoX);
          yawAngle = 18.0 + progress * 4.0; // 18 -> 22 deg
          egoSpeed = Math.round(46 - progress * 4); // 46 -> 42 MPH
          skidTracksGroup.setAttribute('opacity', '0.7');
          counterSteerGroup.setAttribute('opacity', '0.0');
        }} else if (t < 4.4) {{
          // Phase 3: Counter-steering into direction of skid
          const progress = (t - 3.0) / 1.4;
          egoX = 49.0 + progress * 3.0; // 49% to 52%
          egoY = getLane2Y(egoX);
          yawAngle = 22.0 - progress * 17.0; // 22 -> 5 deg
          egoSpeed = Math.round(42 - progress * 4); // 42 -> 38 MPH
          skidTracksGroup.setAttribute('opacity', '0.5');
          counterSteerGroup.setAttribute('opacity', '1.0');
        }} else {{
          // Phase 4: Straightening wheels, full recovery
          const progress = (t - 4.4) / 1.6;
          egoX = 52.0 + progress * 3.0; // 52% to 55%
          egoY = getLane2Y(egoX);
          yawAngle = Math.max(0, 5.0 - progress * 5.0); // 5 -> 0 deg
          egoSpeed = 35;
          skidTracksGroup.setAttribute('opacity', `${{0.5 * (1 - progress)}}`);
          counterSteerGroup.setAttribute('opacity', '0.0');
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = `rotate(${{yawAngle.toFixed(1)}}deg)`;

        telemSpeed.textContent = `${{egoSpeed}} MPH`;
        telemYaw.textContent = `+${{yawAngle.toFixed(1)}}° (${{yawAngle > 2 ? 'REAR RIGHT' : 'STABILIZED'}})`;
        telemThrottle.textContent = (t < 1.6) ? 'EASING OFF GAS' : 'OFF ACCELERATOR';
        telemBrake.textContent = 'NO BRAKES (CORRECT)';
        telemSteer.textContent = (t >= 3.0 && t < 4.4) ? 'STEERING INTO SKID →' : ((t >= 4.4) ? 'STRAIGHTENED' : 'AWAITING RECOVERY');
        telemTraction.textContent = (t >= 4.4) ? '100% REGAINED' : ((t >= 3.0) ? 'TRACTION RETURNING' : 'SLIPPING (+22°)');

        if (t < 1.6) {{
          tagVehEgo.textContent = `EGO: REAR SKID DETECTED (+${{yawAngle.toFixed(0)}}°) • DO NOT PANIC`;
          pillStatusText.textContent = 'TEXAS SKID RULE: EASE OFF GAS • NEVER SLAM BRAKES • STEER INTO SKID';
          hudNarrative.textContent = 'Step 1: Rear tires lose adhesion on slippery pavement. Rear end slides right (+18° yaw angle). Driver immediately feels steering lighten.';
          signalStateBadge.textContent = 'SKID DETECTED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.0) {{
          tagVehEgo.textContent = 'EGO: WEIGHT TRANSFER STABILIZED • NO BRAKE PEDAL TAP';
          pillStatusText.textContent = 'CRITICAL RULE: DO NOT TOUCH BRAKES! BRAKING CAUSES A COMPLETE SPIN';
          hudNarrative.textContent = 'Step 2: Driver takes foot off gas pedal. Does NOT hit brakes suddenly. Weight transfers smoothly forward to restore tire adhesion.';
          signalStateBadge.textContent = 'OFF ACCELERATOR';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        }} else if (t < 4.4) {{
          tagVehEgo.textContent = 'EGO: STEERING SMOOTHLY IN DIRECTION OF SKID (RIGHT)';
          pillStatusText.textContent = 'COUNTER-STEER: TURN WHEEL IN THE EXACT DIRECTION REAR IS SKIDDING';
          hudNarrative.textContent = 'Step 3: Driver turns steering wheel smoothly in the direction of the skid (to the right). Front tires align with rotational momentum, neutralizing the slide.';
          signalStateBadge.textContent = 'COUNTER-STEERING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: WHEELS STRAIGHTENED • FULL HIGHWAY CONTROL RESTORED';
          pillStatusText.textContent = 'SKID RECOVERED: STRAIGHTEN WHEELS GENTLY AS VEHICLE REALIGNS';
          hudNarrative.textContent = 'Step 4: As rear wheels re-grip asphalt, driver gently straightens steering wheel. Vehicle realigns cleanly in Lane 2 at safe controlled speed.';
          signalStateBadge.textContent = 'CONTROL RESTORED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 2: HIGH-SPEED TIRE BLOWOUT (FIRM GRIP & STRAIGHT COAST TO SHOULDER)
      // =========================================================================
      else if (currentMode === 2) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        skidTracksGroup.setAttribute('opacity', '0.0');
        counterSteerGroup.setAttribute('opacity', '0.0');

        // Blue Car in Lane 2 ahead
        const blueX = 64.0 + (t / duration) * 12.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 65 MPH (LANE 2)';

        // Yellow Car in Lane 1 trailing
        const yellowX = 25.0 + (t / duration) * 12.0;
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'FOLLOWING FLOW: 65 MPH (LANE 1)';

        // Ego Car: Blowout at 60 MPH in Lane 1, straight coast, then pull to shoulder
        let egoX, egoY, yawAngle, egoSpeed;
        if (t < 1.6) {{
          // Blowout occurs: violent drag pull
          const progress = t / 1.6;
          egoX = 38.0 + progress * 5.0; // 38% to 43%
          egoY = getLane1Y(egoX);
          yawAngle = (Math.sin(t * 18) * 3.5); // subtle wheel shimmy / drag
          egoSpeed = Math.round(60 - progress * 10); // 60 -> 50 MPH
          brakeLights.style.opacity = '0.0';
          flasherFront.style.opacity = '0.0';
          flasherRear.style.opacity = '0.0';
          blowoutVectorGroup.setAttribute('opacity', '1.0');
          const egoSvgX = egoX * 10 + 25;
          const egoSvgY = egoY * 6 - 5;
          blowoutSpark.setAttribute('cx', egoSvgX);
          blowoutSpark.setAttribute('cy', egoSvgY);
        }} else if (t < 3.2) {{
          // Firm 2-hand grip: resists pull, maintains straight tracking
          const progress = (t - 1.6) / 1.6;
          egoX = 43.0 + progress * 6.0; // 43% to 49%
          egoY = getLane1Y(egoX);
          yawAngle = (Math.sin(t * 10) * 1.5);
          egoSpeed = Math.round(50 - progress * 15); // 50 -> 35 MPH
          brakeLights.style.opacity = '0.0';
          flasherFront.style.opacity = '0.0';
          flasherRear.style.opacity = '0.0';
          blowoutVectorGroup.setAttribute('opacity', '0.0');
        }} else if (t < 4.8) {{
          // Gentle coasting transition onto wide shoulder
          const progress = (t - 3.2) / 1.6;
          egoX = 49.0 + progress * 4.0; // 49% to 53%
          const yLane = getLane1Y(egoX);
          const yShld = getShoulderY(egoX);
          egoY = yLane + progress * (yShld - yLane);
          yawAngle = 0;
          egoSpeed = Math.round(35 - progress * 20); // 35 -> 15 MPH
          brakeLights.style.opacity = '0.8'; // gentle progressive brake
          flasherFront.style.opacity = blinkOn ? '1.0' : '0.0';
          flasherRear.style.opacity = blinkOn ? '1.0' : '0.0';
          blowoutVectorGroup.setAttribute('opacity', '0.0');
        }} else {{
          // Complete stop on shoulder
          egoX = 53.0;
          egoY = getShoulderY(egoX);
          yawAngle = 0;
          egoSpeed = 0;
          brakeLights.style.opacity = '0.0';
          flasherFront.style.opacity = blinkOn ? '1.0' : '0.0';
          flasherRear.style.opacity = blinkOn ? '1.0' : '0.0';
          blowoutVectorGroup.setAttribute('opacity', '0.0');
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = `rotate(${{yawAngle.toFixed(1)}}deg)`;

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (PARKED)' : `${{egoSpeed}} MPH`;
        telemYaw.textContent = (egoSpeed === 0) ? '0° (PARKED)' : 'STRAIGHT TRACKING';
        telemThrottle.textContent = 'OFF ACCELERATOR';
        telemBrake.textContent = (t < 3.2) ? 'NO BRAKES (COAST)' : ((egoSpeed > 0) ? 'GENTLE BRAKING' : 'PARK BRAKE SET');
        telemSteer.textContent = 'FIRM 2-HAND GRIP';
        telemTraction.textContent = (t < 3.2) ? 'BLOWOUT DRAG RESISTED' : 'SHOULDER SECURED';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: 60 MPH TIRE BLOWOUT • VIOLENT PULL FORCE';
          pillStatusText.textContent = 'BLOWOUT RULE: GRIP WHEEL FIRMLY • DO NOT SLAM BRAKES • COAST STRAIGHT';
          hudNarrative.textContent = 'Step 1: Sudden explosive tire blowout at 60 MPH creates strong drag pulling vehicle. Driver resists impulse to slam brakes or swerve.';
          signalStateBadge.textContent = 'BLOWOUT PULL';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: FIRM 2-HAND GRIP • MAINTAINING STRAIGHT PATH';
          pillStatusText.textContent = 'MAINTAIN TRACKING: KEEP WHEEL STRAIGHT UNTIL SPEED DROPS BELOW 30 MPH';
          hudNarrative.textContent = 'Step 2: Driver grips steering wheel firmly with both hands, keeping vehicle tracking straight in lane while letting momentum bleed off naturally.';
          signalStateBadge.textContent = 'STRAIGHT COAST';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else if (t < 4.8) {{
          tagVehEgo.textContent = `EGO: GENTLE BRAKING (${{egoSpeed}} MPH) • PULLING ONTO SHOULDER`;
          pillStatusText.textContent = 'CONTROLLED STOP: GENTLY APPLY BRAKES ONCE SPEED IS CONTROLLED';
          hudNarrative.textContent = 'Step 3: Once vehicle speed drops below 30 MPH, driver signals and gently applies brakes while easing onto the wide right shoulder.';
          signalStateBadge.textContent = 'GENTLE BRAKE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: STOPPED ON SHOULDER (0 MPH) • HAZARDS ACTIVE';
          pillStatusText.textContent = 'SHOULDER SECURED: VEHICLE 100% CLEAR OF HIGHWAY TRAVEL LANES';
          hudNarrative.textContent = 'Step 4: Vehicle safely stopped completely off paved lanes on the shoulder. 4-way hazard flashers activated; ready for roadside assistance.';
          signalStateBadge.textContent = 'STOPPED SAFE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: PANIC BRAKING IN A SKID (FATAL 360° SPIN-OUT)
      // =========================================================================
      else if (currentMode === 3) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        counterSteerGroup.setAttribute('opacity', '0.0');
        blowoutVectorGroup.setAttribute('opacity', '0.0');
        flasherFront.style.opacity = '0.0';
        flasherRear.style.opacity = '0.0';

        // Blue Car in Lane 2 cruises far ahead at x = 74% to 80%
        const blueX = 74.0 + (t / duration) * 6.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 65 MPH (LANE 2)';

        // Yellow Traffic in Lane 1: Approaching and emergency stops before crash
        let yellowX, yellowY;
        if (t < 2.5) {{
          const progress = t / 2.5;
          yellowX = 23.0 + progress * 8.0; // 23% to 31%
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'APPROACHING: 65 MPH (LANE 1)';
        }} else {{
          // Emergency threshold brake: stops at x = 31%
          yellowX = 31.0;
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'PANIC THRESHOLD STOP! AVOIDING SPIN';
        }}
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;

        // Ego Car: Panic slams brakes -> violent 360 spin across lanes
        let egoX, egoY, yawAngle, egoSpeed;
        if (t < 1.6) {{
          // Initial skid (+18 deg)
          const progress = t / 1.6;
          egoX = 44.0 + progress * 3.0; // 44% to 47%
          egoY = getLane2Y(egoX);
          yawAngle = progress * 18.0;
          egoSpeed = 50;
          brakeLights.style.opacity = '0.0';
          skidTracksGroup.setAttribute('opacity', `${{progress * 0.6}}`);
          spinHazardGroup.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
        }} else if (t < 3.2) {{
          // Panic slams brakes! Locked wheels initiate violent spin
          const progress = (t - 1.6) / 1.6;
          egoX = 47.0 + progress * 2.0; // 47% to 49%
          egoY = getLane2Y(egoX);
          yawAngle = 18.0 + progress * 162.0; // 18 -> 180 deg
          egoSpeed = Math.round(50 * (1 - progress * 0.7)); // 50 -> 15 MPH
          brakeLights.style.opacity = '1.0'; // Hard brakes!
          skidTracksGroup.setAttribute('opacity', '1.0');
          spinHazardGroup.setAttribute('opacity', '1.0');
          hazardStar.setAttribute('transform', `translate(${{egoX * 10}}, ${{egoY * 6}})`);
          hazardBanner.style.opacity = '1.0';
        }} else {{
          // Frozen spun around backwards at 180 deg across lanes
          egoX = 49.0;
          egoY = getLane2Y(egoX);
          yawAngle = 180.0;
          egoSpeed = 0;
          brakeLights.style.opacity = '1.0';
          skidTracksGroup.setAttribute('opacity', '1.0');
          spinHazardGroup.setAttribute('opacity', '1.0');
          hazardStar.setAttribute('transform', `translate(${{egoX * 10}}, ${{egoY * 6}})`);
          hazardBanner.style.opacity = '1.0';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = `rotate(${{yawAngle.toFixed(1)}}deg)`;

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (SPUN OUT)' : `${{egoSpeed}} MPH (SPINNING)`;
        telemYaw.textContent = `${{yawAngle.toFixed(0)}}° (${{yawAngle >= 170 ? 'FACING BACKWARDS' : 'UNCONTROLLED SPIN'}})`;
        telemThrottle.textContent = 'OFF ACCELERATOR';
        telemBrake.textContent = (t >= 1.6) ? 'LOCKED BRAKES (FATAL)' : 'NONE';
        telemSteer.textContent = (t >= 1.6) ? 'ZERO STEERING AUTHORITY' : 'NORMAL';
        telemTraction.textContent = (t >= 1.6) ? 'TOTAL LOSS (100% SLIP)' : 'BREAKING LOOSE';

        pillStatusText.textContent = 'CRITICAL PANIC ERROR: SLAMMING BRAKES IN A SKID CAUSES A FATAL 360° SPIN';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: REAR SKID BREAKS OUT • DRIVER PANICS';
          hudNarrative.textContent = 'Step 1: Vehicle enters sudden skid. Driver reacts instinctively with terror instead of training.';
          signalStateBadge.textContent = 'PANIC REACTION';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: BRAKES SLAMMED! WHEELS LOCK • SPIN INITIATED';
          hudNarrative.textContent = 'Step 2: Driver slams hard on brake pedal! Locked front tires lose all lateral traction, sending vehicle into an uncontrollable high-speed spin.';
          signalStateBadge.textContent = 'LOCKED BRAKES';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: 180° REVERSE SPUN • CRITICAL HIGHWAY PILEUP RISK';
          hudNarrative.textContent = 'Step 3 & 4: Vehicle spins completely around backwards across active travel lanes. Approaching traffic forced into panic stops to avoid fatal T-bone collision.';
          signalStateBadge.textContent = 'FATAL SPIN-OUT';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L05_T14_skids_and_blowouts.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 21 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_simulation()
