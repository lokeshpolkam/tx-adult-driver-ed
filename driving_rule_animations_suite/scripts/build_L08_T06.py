import os
import base64

def build_l08_t06():
    # Asset Paths
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    car_blue_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_blue_clean_ne.png"

    print("Encoding Lesson 31 assets to base64...")
    with open(car_red_path, "rb") as f:
        car_red_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_yellow_path, "rb") as f:
        car_yellow_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_blue_path, "rb") as f:
        car_blue_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(bg_img_path, "rb") as f:
        bg_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

    print("Assets successfully encoded.")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>L08-T06: Risk of Not Wearing a Safety Belt &amp; Crash Physics</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700;800&display=swap');
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
    @keyframes pulse-belt {{
      0%, 100% {{ opacity: 0.8; transform: scale(1); }}
      50% {{ opacity: 1; transform: scale(1.05); }}
    }}
    .belt-glow {{
      animation: pulse-belt 1.5s infinite ease-in-out;
    }}
    @keyframes pulse-eject {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.96); }}
      50% {{ opacity: 0.95; transform: scale(1.04); }}
    }}
    .eject-pulse {{
      animation: pulse-eject 0.8s infinite ease-in-out;
    }}
    .timeline-slider::-webkit-slider-thumb {{
      appearance: none;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #3B82F6;
      cursor: pointer;
      box-shadow: 0 0 8px rgba(59, 130, 246, 0.8);
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col items-center p-3 md:p-6 bg-[#0B0E14]">

  <div class="max-w-6xl w-full flex flex-col gap-4">

    <!-- HEADER BLOCK -->
    <header class="bg-[#121722] border border-[#232C3D] rounded-2xl p-4 md:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
      <div>
        <div class="flex items-center gap-2 mb-1.5 flex-wrap">
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">TDLR ADE-1317</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 31</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L08-T06: Risk of Not Wearing a Safety Belt &amp; Crash Physics
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          The 3 Collisions of a Crash &bull; Occupant Ejection Dynamics (5x Fatality Surge) &bull; TTC &sect; 545.413 &amp; &sect; 545.412
        </p>
      </div>

      <!-- SCENARIO MODE SELECTOR -->
      <div class="flex items-center gap-2 bg-[#0B0E14] p-1.5 rounded-xl border border-[#232C3D] flex-wrap">
        <button id="mode-1" data-mode="1" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40">
          1: The 3 Collisions of a Crash
        </button>
        <button id="mode-2" data-mode="2" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/50">
          Hazard: Unbelted Ejection (5x Fatality)
        </button>
        <button id="mode-3" data-mode="3" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/50">
          Child Passenger Safety (TTC § 545.412)
        </button>
        <label class="flex items-center gap-1.5 text-xs text-gray-300 font-medium ml-2 cursor-pointer">
          <input type="checkbox" id="auto-loop" class="rounded bg-[#121722] border-gray-600 text-blue-500 focus:ring-0" checked />
          <span>Auto-Loop</span>
        </label>
      </div>
    </header>

    <!-- STEPPER CARDS (4 STEPS) -->
    <div id="steps-container" class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
      <button class="step-card group text-left p-2.5 rounded-xl border border-blue-500/60 bg-blue-950/30 transition shadow-sm" data-step="1">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-blue-400 mono">STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-blue-400 step-dot"></span>
        </div>
        <p class="text-xs font-bold text-white mt-1 leading-snug">Pre-Impact Velocity (55 MPH)</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition" data-step="2">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Collision 1: Vehicle Impact</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition" data-step="3">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Collision 2: Occupant Restraint</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition" data-step="4">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Collision 3 &amp; Control Retained</p>
      </button>
    </div>

    <!-- MAIN SIMULATION VIEWPORT (16:9) -->
    <div class="relative w-full aspect-[16/9] bg-[#0E131F] rounded-2xl border border-[#232C3D] overflow-hidden shadow-2xl">
      
      <!-- Diorama Canvas Background Image -->
      <img src="{bg_b64}" alt="Texas Highway Corridor" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- VECTOR OVERLAY CANVAS (SVG) -->
      <svg id="vector-canvas" class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1000 562.5" preserveAspectRatio="none">
        <defs>
          <!-- Restraint Energy Dispersion Gradient -->
          <radialGradient id="energyGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.8" />
            <stop offset="50%" stop-color="#059669" stop-opacity="0.3" />
            <stop offset="100%" stop-color="#047857" stop-opacity="0.0" />
          </radialGradient>

          <!-- Impact Shockwave Gradient -->
          <radialGradient id="shockwaveGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#EF4444" stop-opacity="0.9" />
            <stop offset="70%" stop-color="#B91C1C" stop-opacity="0.4" />
            <stop offset="100%" stop-color="#7F1D1D" stop-opacity="0.0" />
          </radialGradient>
        </defs>

        <!-- Crumple Zone Impact Shockwave Circle -->
        <circle id="svg-impact-shockwave" cx="580" cy="260" r="35" fill="url(#shockwaveGrad)" style="display: none;" />

        <!-- Occupant Restraint Survival Bubble around Ego Cabin -->
        <ellipse id="svg-occupant-cushion" cx="440" cy="330" rx="42" ry="22" fill="url(#energyGrad)" stroke="#10B981" stroke-width="2" stroke-dasharray="4,2" style="display: none;" />

        <!-- Unbelted Occupant Ejection Trajectory Vector (Mode 2) -->
        <g id="svg-ejection-vector" style="display: none;">
          <path id="ejection-path" d="M 440,310 Q 480,240 540,210" fill="none" stroke="#EF4444" stroke-width="3.5" stroke-dasharray="6,4" />
          <polygon points="535,205 548,208 542,218" fill="#EF4444" />
          <circle cx="545" cy="210" r="12" fill="#EF4444" fill-opacity="0.8" class="eject-pulse" />
          <text x="565" y="215" fill="#EF4444" font-size="11" font-weight="800" font-family="'JetBrains Mono', monospace">EJECTION: 55 MPH PROJECTILE (5x FATAL!)</text>
        </g>
      </svg>

      <!-- VEHICLE 1: EGO RED VEHICLE (Lane 2 / Center Lane) -->
      <div id="veh-ego" class="absolute transition-transform duration-75 pointer-events-none" style="left: 40%; top: 52%; transform: translate(-50%, -50%);">
        <div class="relative">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-24 md:w-28 drop-shadow-[0_8px_16px_rgba(0,0,0,0.85)]" />
          <!-- Ego Badge -->
          <div id="ego-tag" class="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span id="ego-tag-text">EGO: 3-POINT HARNESS SECURED &bull; CABIN ARMED</span>
          </div>
        </div>
      </div>

      <!-- VEHICLE 2: IMPACT OBSTACLE (Yellow Vehicle / Disabled Car) -->
      <div id="veh-yellow" class="absolute transition-transform duration-75 pointer-events-none" style="left: 60%; top: 32%; transform: translate(-50%, -50%);">
        <div class="relative">
          <img src="{car_yellow_b64}" alt="Impact Obstacle" class="w-24 md:w-28 drop-shadow-[0_8px_16px_rgba(0,0,0,0.85)]" />
          <!-- Yellow Vehicle Badge -->
          <div id="yellow-tag" class="absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500/50 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5">
            <span id="yellow-dot" class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            <span id="yellow-tag-text">DISABLED OBSTACLE: CRASH CUSHION IMPACT</span>
          </div>
        </div>
      </div>

      <!-- IN-CABIN RESTRAINT STATUS WIDGET (Top-Right) -->
      <div id="restraint-widget" class="absolute top-4 right-4 z-20 w-48 md:w-52 p-2.5 rounded-xl bg-[#0F141D]/95 border border-emerald-500/60 shadow-2xl backdrop-blur-md">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span class="text-[9px] font-black text-emerald-400 mono tracking-wider uppercase">CABIN RESTRAINTS</span>
          </div>
          <span id="restraint-status-badge" class="text-[9px] font-black text-white mono bg-emerald-950/80 px-1.5 py-0.5 rounded border border-emerald-500/40">LOCKED (100%)</span>
        </div>
        
        <div class="mt-2 space-y-1.5 text-[10px] mono">
          <div class="flex justify-between items-center text-gray-300">
            <span>Pretensioner:</span>
            <span id="val-pretensioner" class="text-emerald-400 font-bold">15ms ARMED</span>
          </div>
          <div class="flex justify-between items-center text-gray-300">
            <span>Force Dissipation:</span>
            <span id="val-dissipation" class="text-blue-400 font-bold">PELVIS &amp; RIBS</span>
          </div>
          <div class="flex justify-between items-center text-gray-300">
            <span>Driver Anchored:</span>
            <span id="val-anchored" class="text-emerald-400 font-bold">YES &bull; IN WHEEL</span>
          </div>
          <div class="flex justify-between items-center text-gray-300 border-t border-gray-800 pt-1">
            <span>Ejection Probability:</span>
            <span id="val-ejection" class="text-emerald-400 font-bold">0.0% (ZERO)</span>
          </div>
        </div>
      </div>

      <!-- TOP CRITICAL HAZARD BANNER (Hidden in Mode 1, Active in Mode 2 & 3) -->
      <div id="hazard-banner" class="absolute top-4 left-1/2 -translate-x-1/2 z-20 px-4 py-2 rounded-xl bg-red-950/90 border border-red-500 text-center shadow-2xl backdrop-blur-md max-w-lg transition-all duration-300" style="display: none;">
        <div class="flex items-center justify-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span id="hazard-title" class="text-xs font-black text-red-200 uppercase tracking-wider mono">CRITICAL HAZARD: UNBELTED OCCUPANT EJECTION</span>
        </div>
        <p id="hazard-desc" class="text-[11px] text-gray-300 mt-1 leading-snug">
          Unbelted occupants continue moving forward at vehicle speed (Newton's 1st Law), resulting in windshield penetration, violent ejection, and 5x fatality rate.
        </p>
      </div>

      <!-- TELEMETRY HUD (Top Left) -->
      <div id="telemetry-hud" class="absolute top-4 left-4 z-20 w-64 md:w-72 p-3 rounded-xl bg-[#0D111A]/95 border border-[#232C3D] shadow-2xl backdrop-blur-md flex flex-col gap-2">
        <div class="flex items-center justify-between border-b border-[#1E2638] pb-1.5">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            <span class="text-xs font-black text-white tracking-wider mono">CRASH DYNAMICS HUD</span>
          </div>
          <span id="hud-status-pill" class="text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">3-POINT RESTRAINT</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1.5 text-xs mono">
          <div class="text-gray-400">Crash Phase:</div>
          <div id="hud-phase" class="font-bold text-white text-right">PRE-IMPACT (55 MPH)</div>

          <div class="text-gray-400">Vehicle Decel:</div>
          <div id="hud-decel" class="font-bold text-blue-400 text-right">0.0 G (CRUISING)</div>

          <div class="text-gray-400">Human Collision:</div>
          <div id="hud-human-col" class="font-bold text-emerald-400 text-right">BELT SPREADS FORCE</div>

          <div class="text-gray-400">Driver Control:</div>
          <div id="hud-control" class="font-bold text-emerald-400 text-right">ANCHORED IN SEAT</div>

          <div class="text-gray-400">Statutory Mandate:</div>
          <div id="hud-statute" class="font-bold text-yellow-400 text-right">TTC &sect; 545.413</div>
        </div>

        <!-- Instructional Subtext -->
        <div id="hud-subtext" class="text-[11px] text-gray-300 border-t border-[#1E2638] pt-1.5 leading-relaxed">
          Safety belts provide crucial deceleration distance, spreading impact energy across the pelvis and rib cage and preventing violent ejection through the windshield.
        </div>
      </div>

      <!-- TOP FLOATING CYCLE STATUS PILL (Mode 1 Only) -->
      <div id="cycle-pill" class="absolute top-4 left-1/2 -translate-x-1/2 z-10 px-3 py-1 rounded-full bg-[#0D111A]/90 border border-emerald-500/30 text-[10px] font-bold text-emerald-300 shadow-md mono flex items-center gap-2 backdrop-blur-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="cycle-pill-text">TEXAS MANDATE: ALL PASSENGERS IN ALL SEATS MUST BE BUCKLED (TTC &sect; 545.413)</span>
      </div>

    </div>

    <!-- PLAYBACK & TIMELINE CONTROLS -->
    <div class="bg-[#121722] border border-[#232C3D] rounded-2xl p-4 flex flex-col md:flex-row items-center gap-4 shadow-xl">
      <div class="flex items-center gap-2">
        <button id="btn-play-pause" class="w-10 h-10 rounded-xl bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center transition shadow-lg shadow-blue-900/30">
          <svg id="icon-play" class="w-5 h-5 hidden" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
          <svg id="icon-pause" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
        <button id="btn-reset" class="w-10 h-10 rounded-xl bg-[#1A2232] hover:bg-[#232D42] text-gray-300 flex items-center justify-center transition border border-[#2B374E]" title="Reset Simulation">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
        <button id="btn-step-back" class="w-10 h-10 rounded-xl bg-[#1A2232] hover:bg-[#232D42] text-gray-300 flex items-center justify-center transition border border-[#2B374E]" title="Step Back (-0.5s)">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <button id="btn-step-fwd" class="w-10 h-10 rounded-xl bg-[#1A2232] hover:bg-[#232D42] text-gray-300 flex items-center justify-center transition border border-[#2B374E]" title="Step Forward (+0.5s)">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Scrubber Timeline -->
      <div class="flex-1 w-full flex items-center gap-3">
        <span id="current-time-display" class="text-xs font-bold text-gray-300 mono w-12">0.0s</span>
        <input id="timeline-slider" type="range" min="0" max="12" step="0.05" value="0" class="timeline-slider flex-1 h-2 bg-[#1A2232] rounded-lg appearance-none cursor-pointer border border-[#28354D]" />
        <span id="total-time-display" class="text-xs font-bold text-gray-500 mono w-12">12.0s</span>
      </div>

      <!-- Speed & Law Badge -->
      <div class="hidden lg:flex items-center gap-3 text-xs mono">
        <div class="px-2.5 py-1 rounded-lg bg-[#18202F] border border-[#2B3850] text-gray-300">
          <span class="text-gray-500">MANDATE:</span> <span class="font-bold text-emerald-400">100% BUCKLED</span>
        </div>
        <div class="px-2.5 py-1 rounded-lg bg-[#18202F] border border-[#2B3850] text-gray-300">
          <span class="text-gray-500">STATUTE:</span> <span class="font-bold text-yellow-400">TTC &sect; 545.413</span>
        </div>
      </div>
    </div>

    <!-- STATUTORY & LEGAL FOOTER SUMMARY -->
    <div class="p-4 rounded-2xl bg-[#121722] border border-[#232C3D] flex flex-col md:flex-row items-center justify-between text-xs text-gray-400 gap-2 shadow-lg">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span><strong>Texas Transportation Code &sect; 545.413:</strong> All occupants (front and back seat) must wear safety belts. Fine up to $50 for adults; $100&ndash;$200 for unbelted child occupants.</span>
      </div>
      <div class="text-[11px] mono text-gray-500">
        ADE-1317 Texas Adult Driver Education Engine
      </div>
    </div>

  </div>

  <!-- SIMULATION CORE SCRIPT -->
  <script>
    // State Variables
    let currentMode = 1;
    let currentTime = 0.0;
    const duration = 12.0;
    let isPlaying = true;
    let lastTimestamp = null;

    // DOM Elements
    const timelineSlider = document.getElementById('timeline-slider');
    const currentTimeDisplay = document.getElementById('current-time-display');
    const btnPlayPause = document.getElementById('btn-play-pause');
    const iconPlay = document.getElementById('icon-play');
    const iconPause = document.getElementById('icon-pause');
    const autoLoop = document.getElementById('auto-loop');

    const vehEgo = document.getElementById('veh-ego');
    const egoTag = document.getElementById('ego-tag');
    const egoTagText = document.getElementById('ego-tag-text');

    const vehYellow = document.getElementById('veh-yellow');
    const yellowTag = document.getElementById('yellow-tag');
    const yellowTagText = document.getElementById('yellow-tag-text');
    const yellowDot = document.getElementById('yellow-dot');

    const svgImpactShockwave = document.getElementById('svg-impact-shockwave');
    const svgOccupantCushion = document.getElementById('svg-occupant-cushion');
    const svgEjectionVector = document.getElementById('svg-ejection-vector');

    const restraintWidget = document.getElementById('restraint-widget');
    const restraintStatusBadge = document.getElementById('restraint-status-badge');
    const valPretensioner = document.getElementById('val-pretensioner');
    const valDissipation = document.getElementById('val-dissipation');
    const valAnchored = document.getElementById('val-anchored');
    const valEjection = document.getElementById('val-ejection');

    const hazardBanner = document.getElementById('hazard-banner');
    const hazardTitle = document.getElementById('hazard-title');
    const hazardDesc = document.getElementById('hazard-desc');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const hudPhase = document.getElementById('hud-phase');
    const hudDecel = document.getElementById('hud-decel');
    const hudHumanCol = document.getElementById('hud-human-col');
    const hudControl = document.getElementById('hud-control');
    const hudStatute = document.getElementById('hud-statute');
    const hudSubtext = document.getElementById('hud-subtext');
    const cyclePill = document.getElementById('cycle-pill');
    const cyclePillText = document.getElementById('cycle-pill-text');

    // Highway Geometry Coordinate Calculator: y = Y0 - 1.005 * (x - 50.0)
    // Lane 2 (center): Y0 = 42.56
    function getLaneY(lane, x) {{
      const Y0 = (lane === 1) ? 56.62 : (lane === 2) ? 42.56 : 28.50;
      return Y0 - 1.005 * (x - 50.0);
    }}

    function setMode(mode) {{
      currentMode = mode;
      currentTime = 0.0;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40';
        }} else if (m === 2) {{
          btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/50';
        }} else if (m === 3) {{
          btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/50';
        }}
      }});

      updateStepCardsForMode();
      updateSimulation(currentTime);
    }}

    function updateStepCardsForMode() {{
      const cards = document.querySelectorAll('.step-card');
      if (currentMode === 1) {{
        cards[0].querySelector('p').innerText = "Pre-Impact Velocity (55 MPH)";
        cards[1].querySelector('p').innerText = "Collision 1: Vehicle Impact";
        cards[2].querySelector('p').innerText = "Collision 2: Occupant Restraint";
        cards[3].querySelector('p').innerText = "Collision 3 & Control Retained";
      }} else if (currentMode === 2) {{
        cards[0].querySelector('p').innerText = "Unbelted Occupant in Motion";
        cards[1].querySelector('p').innerText = "Impact & Forward Inertia";
        cards[2].querySelector('p').innerText = "Violent Windshield Ejection";
        cards[3].querySelector('p').innerText = "Secondary Roadway Collision";
      }} else if (currentMode === 3) {{
        cards[0].querySelector('p').innerText = "Rear-Seat Placement";
        cards[1].querySelector('p').innerText = "Booster & Harness Under 8";
        cards[2].querySelector('p').innerText = "Airbag Deployment Clearance";
        cards[3].querySelector('p').innerText = "Texas Child Restraint Law";
      }}
    }}

    function jumpToStep(step) {{
      currentTime = (step - 1) * 3.0 + 0.1;
      updateSimulation(currentTime);
    }}

    function updateSimulation(t) {{
      timelineSlider.value = t;
      currentTimeDisplay.innerText = t.toFixed(1) + 's';

      const currentStep = Math.min(4, Math.floor(t / 3.0) + 1);
      highlightStep(currentStep);

      if (currentMode === 1) {{
        renderMode1(t, currentStep);
      }} else if (currentMode === 2) {{
        renderMode2(t, currentStep);
      }} else if (currentMode === 3) {{
        renderMode3(t, currentStep);
      }}
    }}

    // ==========================================
    // MODE 1: THE 3 COLLISIONS OF A CRASH
    // ==========================================
    function renderMode1(t, step) {{
      hazardBanner.style.display = 'none';
      svgEjectionVector.style.display = 'none';
      cyclePill.style.display = 'flex';
      hudStatusPill.style.opacity = '1.0';
      restraintWidget.style.display = 'block';

      // Yellow car fixed at crash site ahead in Lane 2
      const yellX = 58.0;
      const yellY = getLaneY(2, yellX);
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';
      yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500/50 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      yellowTagText.innerText = "CRASH BARRIER / IMPACT POINT";

      if (step === 1) {{
        // Step 1: Pre-Impact Velocity (t = 0..3s)
        const prog = t / 3.0;
        const egoX = 36.0 + prog * 4.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "EGO: 55 MPH • 3-POINT HARNESS SECURED";

        svgImpactShockwave.style.display = 'none';
        svgOccupantCushion.style.display = 'block';
        svgOccupantCushion.setAttribute('cx', egoX * 10);
        svgOccupantCushion.setAttribute('cy', egoY * 5.625);

        // Restraint Widget
        restraintWidget.className = 'absolute top-4 right-4 z-20 w-48 md:w-52 p-2.5 rounded-xl bg-[#0F141D]/95 border border-emerald-500/60 shadow-2xl backdrop-blur-md';
        restraintStatusBadge.innerText = "SECURED (100%)";
        restraintStatusBadge.className = "text-[9px] font-black text-white mono bg-emerald-950/80 px-1.5 py-0.5 rounded border border-emerald-500/40";
        valPretensioner.innerText = "ARMED & READY";
        valDissipation.innerText = "PELVIS & RIBS";
        valAnchored.innerText = "YES • IN WHEEL";
        valEjection.innerText = "0.0% (ZERO)";

        // Telemetry HUD
        hudStatusPill.innerText = "3-POINT RESTRAINT";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono";
        hudPhase.innerText = "PRE-IMPACT (55 MPH)";
        hudPhase.className = "font-bold text-white text-right";
        hudDecel.innerText = "0.0 G (CRUISING)";
        hudDecel.className = "font-bold text-blue-400 text-right";
        hudHumanCol.innerText = "BELT PREPARED";
        hudHumanCol.className = "font-bold text-emerald-400 text-right";
        hudControl.innerText = "ANCHORED IN SEAT";
        hudControl.className = "font-bold text-emerald-400 text-right";
        hudStatute.innerText = "TTC § 545.413";
        hudSubtext.innerHTML = "<strong>Step 1:</strong> Pre-impact approach at 55 MPH. Texas Transportation Code &sect; 545.413 mandates all occupants in front and rear seats wear lap/shoulder belts.";

      }} else if (step === 2) {{
        // Step 2: Collision 1 - Vehicle Impact (t = 3..6s)
        const prog = (t - 3.0) / 3.0;
        const egoX = 40.0 + prog * 10.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500/50 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "COLLISION 1: CRUMPLE ZONE CRUSH (-25G)";

        svgImpactShockwave.style.display = 'block';
        svgImpactShockwave.setAttribute('cx', egoX * 10 + 40);
        svgImpactShockwave.setAttribute('cy', egoY * 5.625 - 25);
        svgOccupantCushion.style.display = 'block';
        svgOccupantCushion.setAttribute('cx', egoX * 10);
        svgOccupantCushion.setAttribute('cy', egoY * 5.625);

        // Restraint Widget
        valPretensioner.innerText = "FIRED (15ms)";
        valPretensioner.className = "text-amber-400 font-bold";
        valDissipation.innerText = "RETRACTOR TIGHTENED";
        valAnchored.innerText = "HELD IN SEAT";
        valEjection.innerText = "0.0% PROTECTED";

        // Telemetry HUD
        hudStatusPill.innerText = "COLLISION 1: CRUMPLE";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono";
        hudPhase.innerText = "CAR STOPS (0.1 SEC)";
        hudPhase.className = "font-bold text-amber-400 text-right";
        hudDecel.innerText = "-25.0 G (EXTREME)";
        hudDecel.className = "font-bold text-red-500 text-right";
        hudHumanCol.innerText = "PRE-TENSIONER LOCK";
        hudHumanCol.className = "font-bold text-amber-400 text-right";
        hudControl.innerText = "SEATED FIRMLY";
        hudControl.className = "font-bold text-emerald-400 text-right";
        hudSubtext.innerHTML = "<strong>Collision 1 (The Car Crash):</strong> Front bumper strikes barrier. The car crunches and absorbs kinetic energy, decelerating from 55 to 0 MPH in 1/10th of a second.";

      }} else if (step === 3) {{
        // Step 3: Collision 2 - Occupant Restraint (t = 6..9s)
        const egoX = 51.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-emerald-500 text-[10px] font-extrabold text-emerald-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5 belt-glow';
        egoTagText.innerText = "COLLISION 2: BELT STRETCHES & ABSORBS MOMENTUM";

        svgImpactShockwave.style.display = 'none';
        svgOccupantCushion.style.display = 'block';
        svgOccupantCushion.setAttribute('cx', egoX * 10);
        svgOccupantCushion.setAttribute('cy', egoY * 5.625);

        // Restraint Widget
        restraintWidget.className = 'absolute top-4 right-4 z-20 w-48 md:w-52 p-2.5 rounded-xl bg-[#0F141D]/95 border border-emerald-500 shadow-2xl backdrop-blur-md';
        valPretensioner.innerText = "ENERGY DISSIPATED";
        valPretensioner.className = "text-emerald-400 font-bold";
        valDissipation.innerText = "PELVIC BONES (SAFE)";
        valAnchored.innerText = "ANCHORED TO SEAT";
        valEjection.innerText = "0% (CONTAINED)";

        // Telemetry HUD
        hudStatusPill.innerText = "COLLISION 2: OCCUPANT";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono";
        hudPhase.innerText = "HUMAN DECELERATION";
        hudPhase.className = "font-bold text-emerald-400 text-right";
        hudDecel.innerText = "MOMENTUM CUSHIONED";
        hudDecel.className = "font-bold text-emerald-400 text-right";
        hudHumanCol.innerText = "PREVENTS INTERIOR HIT";
        hudHumanCol.className = "font-bold text-emerald-400 text-right";
        hudControl.innerText = "100% IN POSITION";
        hudControl.className = "font-bold text-emerald-400 text-right";
        hudSubtext.innerHTML = "<strong>Collision 2 (Human Crash):</strong> Unbelted occupants hit dashboard or windshield at 55 MPH. The safety belt stretches controlled webbing, keeping human momentum within the survival cell.";

      }} else if (step === 4) {{
        // Step 4: Collision 3 & Control Retained (t = 9..12s)
        const egoX = 51.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "SURVIVAL CELL SECURE • DRIVER REMAINS AT WHEEL";

        svgImpactShockwave.style.display = 'none';
        svgOccupantCushion.style.display = 'block';
        svgOccupantCushion.setAttribute('cx', egoX * 10);
        svgOccupantCushion.setAttribute('cy', egoY * 5.625);

        // Restraint Widget
        restraintWidget.className = 'absolute top-4 right-4 z-20 w-48 md:w-52 p-2.5 rounded-xl bg-[#0F141D]/95 border border-emerald-500/60 shadow-2xl backdrop-blur-md';
        valPretensioner.innerText = "FULL RECOVERY";
        valDissipation.innerText = "INTERNAL ORGANS PROTECTED";
        valAnchored.innerText = "READY TO STEER CLEAR";
        valEjection.innerText = "ZERO EJECTION";

        // Telemetry HUD
        hudStatusPill.innerText = "SURVIVAL COMPLETE";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono";
        hudPhase.innerText = "ORGAN DECEL BUFFER";
        hudPhase.className = "font-bold text-emerald-400 text-right";
        hudDecel.innerText = "CONTROLLED STOP";
        hudDecel.className = "font-bold text-emerald-400 text-right";
        hudHumanCol.innerText = "ZERO CABIN EJECTION";
        hudHumanCol.className = "font-bold text-emerald-400 text-right";
        hudControl.innerText = "PREVENTS SECONDARY HIT";
        hudControl.className = "font-bold text-emerald-400 text-right";
        hudSubtext.innerHTML = "<strong>Collision 3 &amp; Anchored Control:</strong> Organs slow gradually inside the body cavity. By keeping the driver planted in the seat, the driver avoids secondary collision into adjacent freeway lanes.";
      }}
    }}

    // ==========================================
    // MODE 2: HAZARD — UNBELTED OCCUPANT EJECTION
    // ==========================================
    function renderMode2(t, step) {{
      hazardBanner.style.display = 'block';
      svgImpactShockwave.style.display = 'none';
      svgOccupantCushion.style.display = 'none';
      svgEjectionVector.style.display = 'block';
      cyclePill.style.display = 'none';
      hudStatusPill.style.opacity = '0.0';

      hazardTitle.innerText = "CRITICAL HAZARD: UNBELTED OCCUPANT EJECTION (5x FATALITY)";
      hazardDesc.innerText = "Unbelted occupants continue moving forward at vehicle speed (Newton's 1st Law). Being thrown from vehicle increases fatal crash risk fivefold.";

      // Yellow car obstacle
      const yellX = 58.0;
      const yellY = getLaneY(2, yellX);
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';
      yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500/50 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      yellowTagText.innerText = "IMPACT POINT";

      // Ego at impact site
      const egoX = 44.0;
      const egoY = getLaneY(2, egoX);
      vehEgo.style.left = egoX + '%';
      vehEgo.style.top = egoY + '%';
      egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5 animate-pulse';
      egoTagText.innerText = "UNBELTED OCCUPANTS: PROJECTILES AT 55 MPH!";

      // Restraint Widget showing Failure
      restraintWidget.className = 'absolute top-4 right-4 z-20 w-48 md:w-52 p-2.5 rounded-xl bg-[#0F141D]/95 border border-red-500 shadow-2xl backdrop-blur-md';
      restraintStatusBadge.innerText = "UNBELTED (0%)";
      restraintStatusBadge.className = "text-[9px] font-black text-white mono bg-red-950 px-1.5 py-0.5 rounded border border-red-600";
      valPretensioner.innerText = "NONE (NOT BUCKLED)";
      valPretensioner.className = "text-red-400 font-bold";
      valDissipation.innerText = "WINDSHIELD & ROAD";
      valDissipation.className = "text-red-400 font-bold";
      valAnchored.innerText = "THROWN FROM SEAT";
      valAnchored.className = "text-red-400 font-bold";
      valEjection.innerText = "5x FATAL SURGE";
      valEjection.className = "text-red-500 font-bold";

      // Telemetry HUD
      hudPhase.innerText = "VIOLENT EJECTION";
      hudPhase.className = "font-bold text-red-500 text-right";
      hudDecel.innerText = "ZERO RESTRAINT CUSHION";
      hudDecel.className = "font-bold text-red-400 text-right";
      hudHumanCol.innerText = "WINDSHIELD PENETRATION";
      hudHumanCol.className = "font-bold text-red-500 text-right";
      hudControl.innerText = "DRIVER EJECTED (0 CONTROL)";
      hudControl.className = "font-bold text-red-500 text-right";
      hudStatute.innerText = "TTC § 545.413 VIOLATION";
      hudSubtext.innerHTML = "<strong>Unbelted Catastrophe:</strong> In a 55 MPH impact, an unbelted occupant strikes the glass and is launched onto the pavement. TxDOT forensic records confirm ejection carries a 5x higher fatality rate.";
    }}

    // ==========================================
    // MODE 3: CHILD PASSENGER SAFETY (TTC § 545.412)
    // ==========================================
    function renderMode3(t, step) {{
      hazardBanner.style.display = 'block';
      svgImpactShockwave.style.display = 'none';
      svgOccupantCushion.style.display = 'block';
      svgEjectionVector.style.display = 'none';
      cyclePill.style.display = 'none';
      hudStatusPill.style.opacity = '0.0';

      hazardTitle.innerText = "CHILD PASSENGER SAFETY MANDATE (TTC § 545.412)";
      hazardDesc.innerText = "Children under 8 years of age (or under 4 feet 9 inches tall) must be secured in a child safety seat system. Rear seat placement avoids airbag deployment trauma.";

      // Ego cruising safely
      const egoX = 42.0;
      const egoY = getLaneY(2, egoX);
      vehEgo.style.left = egoX + '%';
      vehEgo.style.top = egoY + '%';
      egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-emerald-500 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      egoTagText.innerText = "EGO: CHILD IN REAR SAFETY SEAT (TTC § 545.412)";

      // Yellow car at safe trailing distance
      const yellX = 66.0;
      const yellY = getLaneY(2, yellX);
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';
      yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-blue-500/50 text-[10px] font-extrabold text-blue-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      yellowTagText.innerText = "SAFE TRAILING DISTANCE (4-SEC CUSHION)";

      svgOccupantCushion.setAttribute('cx', egoX * 10);
      svgOccupantCushion.setAttribute('cy', egoY * 5.625);

      // Restraint Widget showing Child Seat
      restraintWidget.className = 'absolute top-4 right-4 z-20 w-48 md:w-52 p-2.5 rounded-xl bg-[#0F141D]/95 border border-emerald-500 shadow-2xl backdrop-blur-md';
      restraintStatusBadge.innerText = "CHILD SECURED";
      restraintStatusBadge.className = "text-[9px] font-black text-white mono bg-emerald-950 px-1.5 py-0.5 rounded border border-emerald-500";
      valPretensioner.innerText = "5-POINT HARNESS";
      valPretensioner.className = "text-emerald-400 font-bold";
      valDissipation.innerText = "REAR SEAT POSITION";
      valDissipation.className = "text-blue-400 font-bold";
      valAnchored.innerText = "LATCH SYSTEM LOCKED";
      valAnchored.className = "text-emerald-400 font-bold";
      valEjection.innerText = "0% (FULLY PROTECTED)";
      valEjection.className = "text-emerald-400 font-bold";

      // Telemetry HUD
      hudPhase.innerText = "CHILD RESTRAINT COMPLIANT";
      hudPhase.className = "font-bold text-emerald-400 text-right";
      hudDecel.innerText = "REAR AIRBAG CLEARANCE";
      hudDecel.className = "font-bold text-emerald-400 text-right";
      hudHumanCol.innerText = "5-POINT HARNESS RETENTION";
      hudHumanCol.className = "font-bold text-emerald-400 text-right";
      hudControl.innerText = "DRIVER RESPONSIBLE UNDER 17";
      hudControl.className = "font-bold text-emerald-400 text-right";
      hudStatute.innerText = "TTC § 545.412 & § 545.413";
      hudSubtext.innerHTML = "<strong>Texas Child Seat Mandate:</strong> Drivers face fines of up to $250 for failing to secure children under 8 (or under 4 feet 9 inches) in an approved booster/car seat. Drivers are strictly responsible for securing all occupants under 17.";
    }}

    function highlightStep(step) {{
      const cards = document.querySelectorAll('.step-card');
      cards.forEach((btn, idx) => {{
        const s = idx + 1;
        const dot = btn.querySelector('.step-dot');
        const num = btn.querySelector('span:first-child');
        const title = btn.querySelector('p');

        if (s === step) {{
          btn.className = 'step-card group text-left p-2.5 rounded-xl border border-blue-500/80 bg-blue-950/40 transition shadow-md shadow-blue-950/30 ring-1 ring-blue-500/30';
          dot.className = 'w-1.5 h-1.5 rounded-full bg-blue-400 step-dot animate-pulse';
          num.className = 'text-[10px] font-extrabold text-blue-400 mono';
          title.className = 'text-xs font-bold text-white mt-1 leading-snug';
        }} else {{
          btn.className = 'step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition';
          dot.className = 'w-1.5 h-1.5 rounded-full bg-transparent step-dot';
          num.className = 'text-[10px] font-extrabold text-gray-500 mono';
          title.className = 'text-xs font-bold text-gray-400 mt-1 leading-snug';
        }}
      }});
    }}

    function animate(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = (timestamp - lastTimestamp) / 1000;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += dt;
        if (currentTime >= duration) {{
          if (autoLoop.checked) {{
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

    // Event Listeners
    btnPlayPause.addEventListener('click', () => {{
      isPlaying = !isPlaying;
      lastTimestamp = null;
      updatePlayPauseButton();
    }});

    document.getElementById('btn-reset').addEventListener('click', () => {{
      currentTime = 0.0;
      updateSimulation(currentTime);
    }});

    document.getElementById('btn-step-back').addEventListener('click', () => {{
      currentTime = Math.max(0, currentTime - 0.5);
      updateSimulation(currentTime);
    }});

    document.getElementById('btn-step-fwd').addEventListener('click', () => {{
      currentTime = Math.min(duration, currentTime + 0.5);
      updateSimulation(currentTime);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      isPlaying = false;
      lastTimestamp = null;
      updatePlayPauseButton();
      updateSimulation(currentTime);
    }});

    document.querySelectorAll('.step-card').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const step = parseInt(btn.dataset.step);
        jumpToStep(step);
      }});
    }});

    document.querySelectorAll('.mode-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const mode = parseInt(btn.dataset.mode);
        setMode(mode);
      }});
    }});

    // Initialize
    updatePlayPauseButton();
    updateSimulation(0.0);
    requestAnimationFrame(animate);
  </script>
</body>
</html>
"""

    output_path = os.path.abspath("driving_rule_animations_suite/simulations/L08_T06_safety_belts.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 31 simulation built successfully at: {output_path}")

if __name__ == '__main__':
    build_l08_t06()
