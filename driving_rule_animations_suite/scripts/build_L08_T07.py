import os
import base64

def build_l08_t07():
    # Asset Paths
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    car_blue_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_blue_clean_ne.png"

    print("Encoding Lesson 32 assets to base64...")
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
  <title>L08-T07: Dangers of Driving at Night &amp; Overdriving Headlights</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700;800&display=swap');
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #070A10;
      color: #E6EDF3;
      user-select: none;
      -webkit-user-select: none;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    @keyframes pulse-beam {{
      0%, 100% {{ opacity: 0.65; }}
      50% {{ opacity: 0.95; }}
    }}
    .beam-pulse {{
      animation: pulse-beam 2.2s infinite ease-in-out;
    }}
    @keyframes pulse-danger {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.96); }}
      50% {{ opacity: 0.9; transform: scale(1.04); }}
    }}
    .danger-pulse {{
      animation: pulse-danger 0.8s infinite ease-in-out;
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
<body class="min-h-screen flex flex-col items-center p-3 md:p-6 bg-[#070A10]">

  <div class="max-w-6xl w-full flex flex-col gap-4">

    <!-- HEADER BLOCK -->
    <header class="bg-[#0E131E] border border-[#1E2638] rounded-2xl p-4 md:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
      <div>
        <div class="flex items-center gap-2 mb-1.5 flex-wrap">
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">TDLR ADE-1317</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 32</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L08-T07: Dangers of Driving at Night
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Overdriving Headlights Physics &bull; 500-FT / 300-FT Dimming Mandates &bull; Fog Line Visual Anchor (TTC &sect; 547.302 &amp; &sect; 547.333)
        </p>
      </div>

      <!-- SCENARIO MODE SELECTOR -->
      <div class="flex items-center gap-2 bg-[#070A10] p-1.5 rounded-xl border border-[#1E2638] flex-wrap">
        <button id="mode-1" data-mode="1" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40">
          1: Overdriving Headlights
        </button>
        <button id="mode-2" data-mode="2" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/50">
          Hazard: Glare &amp; 500-FT Dimming
        </button>
        <button id="mode-3" data-mode="3" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/50">
          300-FT Following Dimming
        </button>
        <label class="flex items-center gap-1.5 text-xs text-gray-300 font-medium ml-2 cursor-pointer">
          <input type="checkbox" id="auto-loop" class="rounded bg-[#0E131E] border-gray-600 text-blue-500 focus:ring-0" checked />
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
        <p class="text-xs font-bold text-white mt-1 leading-snug">Low Beam: 45 MPH Safe</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#1E2638] bg-[#0E131E] hover:border-blue-500/50 transition" data-step="2">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Speed Surge: Overdriving!</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#1E2638] bg-[#0E131E] hover:border-blue-500/50 transition" data-step="3">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Unlit Obstacle in Dark</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#1E2638] bg-[#0E131E] hover:border-blue-500/50 transition" data-step="4">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">High Beam or Slower Speed</p>
      </button>
    </div>

    <!-- MAIN SIMULATION VIEWPORT (16:9) -->
    <div class="relative w-full aspect-[16/9] bg-[#070A10] rounded-2xl border border-[#1E2638] overflow-hidden shadow-2xl">
      
      <!-- Diorama Canvas Background Image with Night Darkness Tint -->
      <img src="{bg_b64}" alt="Texas Highway Corridor" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none filter brightness-50 contrast-125" />

      <!-- Nocturnal Blue Atmosphere Scrim -->
      <div class="absolute inset-0 bg-[#060A14]/65 mix-blend-multiply pointer-events-none"></div>

      <!-- VECTOR OVERLAY CANVAS (SVG) -->
      <svg id="vector-canvas" class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1000 562.5" preserveAspectRatio="none">
        <defs>
          <!-- Low-Beam Headlight Gradient (Warm Amber-White, 180 FT) -->
          <linearGradient id="lowBeamGrad" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FEF08A" stop-opacity="0.85" />
            <stop offset="50%" stop-color="#FDE047" stop-opacity="0.45" />
            <stop offset="100%" stop-color="#EAB308" stop-opacity="0.0" />
          </linearGradient>

          <!-- High-Beam Headlight Gradient (Intense Pure White, 420 FT) -->
          <linearGradient id="highBeamGrad" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95" />
            <stop offset="60%" stop-color="#FEF08A" stop-opacity="0.55" />
            <stop offset="100%" stop-color="#FDE047" stop-opacity="0.0" />
          </linearGradient>

          <!-- Oncoming High Beam Glare Gradient -->
          <radialGradient id="glareGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1" />
            <stop offset="30%" stop-color="#60A5FA" stop-opacity="0.7" />
            <stop offset="70%" stop-color="#3B82F6" stop-opacity="0.3" />
            <stop offset="100%" stop-color="#1D4ED8" stop-opacity="0.0" />
          </radialGradient>
        </defs>

        <!-- Dynamic Headlight Cones -->
        <polygon id="svg-headlight-cone" points="390,320 540,190 600,240" fill="url(#lowBeamGrad)" class="beam-pulse" />

        <!-- Stopping Distance Vector Overlay on Road -->
        <g id="svg-stopping-vector">
          <line id="stop-dist-line" x1="390" y1="320" x2="520" y2="210" stroke="#10B981" stroke-width="4" stroke-dasharray="6,4" />
          <circle id="stop-dist-point" cx="520" cy="210" r="6" fill="#10B981" />
          <text id="stop-dist-text" x="310" y="200" fill="#10B981" font-size="11" font-weight="bold" font-family="'JetBrains Mono', monospace">
            <tspan id="stop-dist-line1" x="310" dy="0">STOPPING DISTANCE: 145 FT</tspan>
            <tspan id="stop-dist-line2" x="310" dy="14">(SAFE STOP WITHIN BEAM)</tspan>
          </text>
        </g>

        <!-- White Fog Line Gaze Anchor Line (Mode 2) -->
        <g id="svg-fog-anchor" style="display: none;">
          <line x1="390" y1="330" x2="490" y2="410" stroke="#38BDF8" stroke-width="3" stroke-dasharray="4,3" />
          <circle cx="490" cy="410" r="5" fill="#38BDF8" />
          <text x="505" y="415" fill="#38BDF8" font-size="11" font-weight="800" font-family="'JetBrains Mono', monospace">WHITE FOG LINE ANCHOR (AVOIDS GLARE)</text>
        </g>

        <!-- Oncoming Glare Halo (Mode 2) -->
        <circle id="svg-glare-halo" cx="620" cy="180" r="50" fill="url(#glareGrad)" style="display: none;" />
      </svg>

      <!-- VEHICLE 1: EGO RED VEHICLE (Lane 2 / Center Lane) -->
      <div id="veh-ego" class="absolute transition-transform duration-75 pointer-events-none" style="left: 38%; top: 54%; transform: translate(-50%, -50%);">
        <div class="relative">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-24 md:w-28 drop-shadow-[0_8px_16px_rgba(0,0,0,0.95)]" />
          <!-- Ego Badge -->
          <div id="ego-tag" class="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span id="ego-tag-text">EGO: 45 MPH &bull; LOW BEAMS (180 FT ILLUMINATION)</span>
          </div>
        </div>
      </div>

      <!-- VEHICLE 2: UNLIT ROADWAY OBSTACLE / AHEAD TRAFFIC (Yellow Car) -->
      <div id="veh-yellow" class="absolute transition-transform duration-75 pointer-events-none" style="left: 62%; top: 30%; transform: translate(-50%, -50%);">
        <div class="relative">
          <img src="{car_yellow_b64}" alt="Ahead Vehicle" class="w-24 md:w-28 drop-shadow-[0_8px_16px_rgba(0,0,0,0.95)] filter brightness-75" />
          <!-- Yellow Vehicle Badge -->
          <div id="yellow-tag" class="absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#090D16]/90 border border-amber-500/50 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5">
            <span id="yellow-dot" class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            <span id="yellow-tag-text">UNLIT ROAD OBSTACLE: 200 FT AHEAD</span>
          </div>
        </div>
      </div>

      <!-- IN-CABIN LIGHTING & TELEMETRY WIDGET (Top-Right) -->
      <div id="lighting-widget" class="absolute top-4 right-4 z-20 w-48 md:w-52 p-2.5 rounded-xl bg-[#0A0E18]/95 border border-yellow-500/60 shadow-2xl backdrop-blur-md">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-yellow-400"></span>
            <span class="text-[9px] font-black text-yellow-400 mono tracking-wider uppercase">HEADLIGHT TELEMETRY</span>
          </div>
          <span id="beam-mode-badge" class="text-[9px] font-black text-white mono bg-yellow-950/80 px-1.5 py-0.5 rounded border border-yellow-500/40">LOW BEAM</span>
        </div>
        
        <div class="mt-2 space-y-1.5 text-[10px] mono">
          <div class="flex justify-between items-center text-gray-300">
            <span>Beam Range:</span>
            <span id="val-beam-reach" class="text-yellow-300 font-bold">180 FEET</span>
          </div>
          <div class="flex justify-between items-center text-gray-300">
            <span>Stopping Dist:</span>
            <span id="val-stopping-dist" class="text-emerald-400 font-bold">145 FEET</span>
          </div>
          <div class="flex justify-between items-center text-gray-300">
            <span>Safety Margin:</span>
            <span id="val-margin" class="text-emerald-400 font-bold">+35 FT (SAFE)</span>
          </div>
          <div class="flex justify-between items-center text-gray-300 border-t border-gray-800 pt-1">
            <span>Overdriving Risk:</span>
            <span id="val-overdrive-status" class="text-emerald-400 font-bold">NONE (0%)</span>
          </div>
        </div>
      </div>

      <!-- TOP CRITICAL HAZARD BANNER (Hidden in Mode 1, Active in Mode 2 & 3) -->
      <div id="hazard-banner" class="absolute top-4 left-1/2 -translate-x-1/2 z-20 px-4 py-2 rounded-xl bg-red-950/90 border border-red-500 text-center shadow-2xl backdrop-blur-md max-w-lg transition-all duration-300" style="display: none;">
        <div class="flex items-center justify-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span id="hazard-title" class="text-xs font-black text-red-200 uppercase tracking-wider mono">CRITICAL HAZARD: ONCOMING HIGH BEAM GLARE</span>
        </div>
        <p id="hazard-desc" class="text-[11px] text-gray-300 mt-1 leading-snug">
          High beams blind approaching drivers for 3&ndash;7 seconds. Texas law mandates dimming to low beams within 500 feet of oncoming vehicles (TTC &sect; 547.333).
        </p>
      </div>

      <!-- TELEMETRY HUD (Top Left) -->
      <div id="telemetry-hud" class="absolute top-4 left-4 z-20 w-64 md:w-72 p-3 rounded-xl bg-[#0A0E18]/95 border border-[#1E2638] shadow-2xl backdrop-blur-md flex flex-col gap-2">
        <div class="flex items-center justify-between border-b border-[#1A2234] pb-1.5">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-yellow-400"></span>
            <span class="text-xs font-black text-white tracking-wider mono">NIGHT VISIBILITY HUD</span>
          </div>
          <span id="hud-status-pill" class="text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">SAFE ILLUMINATION</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1.5 text-xs mono">
          <div class="text-gray-400">Ego Speed:</div>
          <div id="hud-speed" class="font-bold text-white text-right">45 MPH (CEILING)</div>

          <div class="text-gray-400">Beam Coverage:</div>
          <div id="hud-beam" class="font-bold text-yellow-300 text-right">180 FT (LOW BEAM)</div>

          <div class="text-gray-400">Stopping Distance:</div>
          <div id="hud-stopping" class="font-bold text-emerald-400 text-right">145 FT (INSIDE BEAM)</div>

          <div class="text-gray-400">Stopping Buffer:</div>
          <div id="hud-buffer" class="font-bold text-emerald-400 text-right">+35 FT BUFFER</div>

          <div class="text-gray-400">Statutory Limit:</div>
          <div id="hud-statute" class="font-bold text-yellow-400 text-right">TTC &sect; 547.333</div>
        </div>

        <!-- Instructional Subtext -->
        <div id="hud-subtext" class="text-[11px] text-gray-300 border-t border-[#1A2234] pt-1.5 leading-relaxed">
          Overdriving headlights occurs when stopping distance exceeds illuminated headlight reach. Low beams illuminate 150&ndash;200 ft; safe speed is capped at 45 MPH.
        </div>
      </div>

      <!-- TOP FLOATING CYCLE STATUS PILL (Mode 1 Only) -->
      <div id="cycle-pill" class="absolute top-4 left-1/2 -translate-x-1/2 z-10 px-3 py-1 rounded-full bg-[#0A0E18]/90 border border-yellow-500/30 text-[10px] font-bold text-yellow-300 shadow-md mono flex items-center gap-2 backdrop-blur-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-yellow-400 animate-pulse"></span>
        <span id="cycle-pill-text">HEADLIGHT RULE: MUST BE ABLE TO STOP WITHIN VISIBLE ILLUMINATED BEAM</span>
      </div>

    </div>

    <!-- PLAYBACK & TIMELINE CONTROLS -->
    <div class="bg-[#0E131E] border border-[#1E2638] rounded-2xl p-4 flex flex-col md:flex-row items-center gap-4 shadow-xl">
      <div class="flex items-center gap-2">
        <button id="btn-play-pause" class="w-10 h-10 rounded-xl bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center transition shadow-lg shadow-blue-900/30">
          <svg id="icon-play" class="w-5 h-5 hidden" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
          <svg id="icon-pause" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
        <button id="btn-reset" class="w-10 h-10 rounded-xl bg-[#151D2C] hover:bg-[#1E283C] text-gray-300 flex items-center justify-center transition border border-[#232F46]" title="Reset Simulation">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
        <button id="btn-step-back" class="w-10 h-10 rounded-xl bg-[#151D2C] hover:bg-[#1E283C] text-gray-300 flex items-center justify-center transition border border-[#232F46]" title="Step Back (-0.5s)">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <button id="btn-step-fwd" class="w-10 h-10 rounded-xl bg-[#151D2C] hover:bg-[#1E283C] text-gray-300 flex items-center justify-center transition border border-[#232F46]" title="Step Forward (+0.5s)">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Scrubber Timeline -->
      <div class="flex-1 w-full flex items-center gap-3">
        <span id="current-time-display" class="text-xs font-bold text-gray-300 mono w-12">0.0s</span>
        <input id="timeline-slider" type="range" min="0" max="12" step="0.05" value="0" class="timeline-slider flex-1 h-2 bg-[#151D2C] rounded-lg appearance-none cursor-pointer border border-[#232F46]" />
        <span id="total-time-display" class="text-xs font-bold text-gray-500 mono w-12">12.0s</span>
      </div>

      <!-- Speed & Law Badge -->
      <div class="hidden lg:flex items-center gap-3 text-xs mono">
        <div class="px-2.5 py-1 rounded-lg bg-[#141C2B] border border-[#232F46] text-gray-300">
          <span class="text-gray-500">LOW BEAM MAX:</span> <span class="font-bold text-yellow-400">45 MPH</span>
        </div>
        <div class="px-2.5 py-1 rounded-lg bg-[#141C2B] border border-[#232F46] text-gray-300">
          <span class="text-gray-500">DIM MANDATE:</span> <span class="font-bold text-emerald-400">500 FT / 300 FT</span>
        </div>
      </div>
    </div>

    <!-- STATUTORY & LEGAL FOOTER SUMMARY -->
    <div class="p-4 rounded-2xl bg-[#0E131E] border border-[#1E2638] flex flex-col md:flex-row items-center justify-between text-xs text-gray-400 gap-2 shadow-lg">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-yellow-400"></span>
        <span><strong>Texas Transportation Code &sect; 547.333:</strong> Must dim high beams within 500 ft of oncoming vehicles and within 300 ft when following from behind.</span>
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

    const svgHeadlightCone = document.getElementById('svg-headlight-cone');
    const svgStoppingVector = document.getElementById('svg-stopping-vector');
    const stopDistLine = document.getElementById('stop-dist-line');
    const stopDistPoint = document.getElementById('stop-dist-point');
    const stopDistText = document.getElementById('stop-dist-text');
    const stopDistLine1 = document.getElementById('stop-dist-line1');
    const stopDistLine2 = document.getElementById('stop-dist-line2');
    const svgFogAnchor = document.getElementById('svg-fog-anchor');
    const svgGlareHalo = document.getElementById('svg-glare-halo');

    const lightingWidget = document.getElementById('lighting-widget');
    const beamModeBadge = document.getElementById('beam-mode-badge');
    const valBeamReach = document.getElementById('val-beam-reach');
    const valStoppingDist = document.getElementById('val-stopping-dist');
    const valMargin = document.getElementById('val-margin');
    const valOverdriveStatus = document.getElementById('val-overdrive-status');

    const hazardBanner = document.getElementById('hazard-banner');
    const hazardTitle = document.getElementById('hazard-title');
    const hazardDesc = document.getElementById('hazard-desc');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const hudSpeed = document.getElementById('hud-speed');
    const hudBeam = document.getElementById('hud-beam');
    const hudStopping = document.getElementById('hud-stopping');
    const hudBuffer = document.getElementById('hud-buffer');
    const hudStatute = document.getElementById('hud-statute');
    const hudSubtext = document.getElementById('hud-subtext');
    const cyclePill = document.getElementById('cycle-pill');
    const cyclePillText = document.getElementById('cycle-pill-text');

    // Highway Geometry Coordinate Calculator: y = Y0 - 1.005 * (x - 50.0)
    // Lane 1 (right): Y0 = 56.62
    // Lane 2 (center): Y0 = 42.56
    // Lane 3 (left passing): Y0 = 28.50
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
        cards[0].querySelector('p').innerText = "Low Beam: 45 MPH Safe";
        cards[1].querySelector('p').innerText = "Speed Surge: Overdriving!";
        cards[2].querySelector('p').innerText = "Unlit Obstacle in Dark";
        cards[3].querySelector('p').innerText = "High Beam or Slower Speed";
      }} else if (currentMode === 2) {{
        cards[0].querySelector('p').innerText = "Oncoming High Beams Approach";
        cards[1].querySelector('p').innerText = "500-FT Dimming Mandate";
        cards[2].querySelector('p').innerText = "Retinal Bleach / Glare Hazard";
        cards[3].querySelector('p').innerText = "White Fog Line Visual Anchor";
      }} else if (currentMode === 3) {{
        cards[0].querySelector('p').innerText = "Trailing Traffic at Night";
        cards[1].querySelector('p').innerText = "300-FT Distance Threshold";
        cards[2].querySelector('p').innerText = "Rearview Mirror Glare Risk";
        cards[3].querySelector('p').innerText = "Mandatory Low Beam Dimming";
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
    // MODE 1: OVERDRIVING HEADLIGHTS
    // ==========================================
    function renderMode1(t, step) {{
      hazardBanner.style.display = 'none';
      svgFogAnchor.style.display = 'none';
      svgGlareHalo.style.display = 'none';
      cyclePill.style.display = 'flex';
      hudStatusPill.style.opacity = '1.0';
      lightingWidget.style.display = 'block';

      // Unlit obstacle at 62% in Lane 2
      const yellX = 62.0;
      const yellY = getLaneY(2, yellX);
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';

      if (step === 1) {{
        // Step 1: Low Beam 45 MPH Safe (t = 0..3s)
        const prog = t / 3.0;
        const egoX = 36.0 + prog * 2.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "EGO: 45 MPH • LOW BEAMS (180 FT BEAM REACH)";

        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#090D16]/90 border border-gray-600 text-[10px] font-extrabold text-gray-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "UNLIT ROADWAY OBSTACLE: 200 FT AHEAD";

        // Low beam cone: 180 ft (~18% of screen)
        svgHeadlightCone.style.display = 'block';
        svgHeadlightCone.setAttribute('fill', 'url(#lowBeamGrad)');
        svgHeadlightCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 150}},${{egoY * 5.625 - 110}} ${{egoX * 10 + 190}},${{egoY * 5.625 - 40}}`);

        // Stopping distance line: 145 ft (< 180 ft)
        svgStoppingVector.style.display = 'block';
        stopDistLine.setAttribute('x1', egoX * 10);
        stopDistLine.setAttribute('y1', egoY * 5.625);
        stopDistLine.setAttribute('x2', egoX * 10 + 120);
        stopDistLine.setAttribute('y2', egoY * 5.625 - 85);
        stopDistLine.setAttribute('stroke', '#10B981');
        stopDistPoint.setAttribute('cx', egoX * 10 + 120);
        stopDistPoint.setAttribute('cy', egoY * 5.625 - 85);
        stopDistPoint.setAttribute('fill', '#10B981');
        const text1X = egoX * 10 - 70;
        const text1Y = egoY * 5.625 - 90;
        stopDistText.setAttribute('x', text1X);
        stopDistText.setAttribute('y', text1Y);
        stopDistText.setAttribute('fill', '#10B981');
        stopDistLine1.setAttribute('x', text1X);
        stopDistLine1.textContent = "STOPPING DISTANCE: 145 FT";
        stopDistLine2.setAttribute('x', text1X);
        stopDistLine2.textContent = "(SAFE STOP WITHIN BEAM)";

        // Widget
        beamModeBadge.innerText = "LOW BEAM (SAFE)";
        beamModeBadge.className = "text-[9px] font-black text-white mono bg-emerald-950 px-1.5 py-0.5 rounded border border-emerald-500/40";
        valBeamReach.innerText = "180 FEET";
        valStoppingDist.innerText = "145 FEET";
        valStoppingDist.className = "text-emerald-400 font-bold";
        valMargin.innerText = "+35 FT BUFFER";
        valMargin.className = "text-emerald-400 font-bold";
        valOverdriveStatus.innerText = "NONE (SAFE)";
        valOverdriveStatus.className = "text-emerald-400 font-bold";

        // HUD
        hudStatusPill.innerText = "SAFE ILLUMINATION";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono";
        hudSpeed.innerText = "45 MPH (LEGAL CEILING)";
        hudSpeed.className = "font-bold text-emerald-400 text-right";
        hudBeam.innerText = "180 FT (LOW BEAM)";
        hudStopping.innerText = "145 FT (STOPPING DIST)";
        hudStopping.className = "font-bold text-emerald-400 text-right";
        hudBuffer.innerText = "+35 FT ILLUMINATED";
        hudBuffer.className = "font-bold text-emerald-400 text-right";
        hudSubtext.innerHTML = "<strong>Step 1:</strong> At 45 MPH on low beams, stopping distance is 145 feet. Because the low-beam pattern reaches 180 feet, you can perceive and stop safely within your illuminated sightline.";

      }} else if (step === 2) {{
        // Step 2: Speed Surge: Overdriving Headlights! (t = 3..6s)
        const prog = (t - 3.0) / 3.0;
        const egoX = 38.0 + prog * 4.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5 animate-pulse';
        egoTagText.innerText = "EGO: 65 MPH ON LOW BEAMS • OVERDRIVING HEADLIGHTS!";

        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#090D16]/90 border border-amber-500 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "UNLIT ROAD OBSTACLE: 200 FT AHEAD (BEYOND BEAM!)";

        // Low beam cone: still 180 ft
        svgHeadlightCone.style.display = 'block';
        svgHeadlightCone.setAttribute('fill', 'url(#lowBeamGrad)');
        svgHeadlightCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 150}},${{egoY * 5.625 - 110}} ${{egoX * 10 + 190}},${{egoY * 5.625 - 40}}`);

        // Stopping distance line: 312 ft (EXTENDS 132 FT PAST BEAM!)
        svgStoppingVector.style.display = 'block';
        stopDistLine.setAttribute('x1', egoX * 10);
        stopDistLine.setAttribute('y1', egoY * 5.625);
        stopDistLine.setAttribute('x2', egoX * 10 + 260);
        stopDistLine.setAttribute('y2', egoY * 5.625 - 190);
        stopDistLine.setAttribute('stroke', '#EF4444');
        stopDistPoint.setAttribute('cx', egoX * 10 + 260);
        stopDistPoint.setAttribute('cy', egoY * 5.625 - 190);
        stopDistPoint.setAttribute('fill', '#EF4444');
        const text2X = egoX * 10 - 80;
        const text2Y = egoY * 5.625 - 90;
        stopDistText.setAttribute('x', text2X);
        stopDistText.setAttribute('y', text2Y);
        stopDistText.setAttribute('fill', '#EF4444');
        stopDistLine1.setAttribute('x', text2X);
        stopDistLine1.textContent = "STOPPING DISTANCE: 312 FT";
        stopDistLine2.setAttribute('x', text2X);
        stopDistLine2.textContent = "(OVERSHOOTS BEAM BY 132 FT!)";

        // Widget
        beamModeBadge.innerText = "OVERDRIVING!";
        beamModeBadge.className = "text-[9px] font-black text-white mono bg-red-950 px-1.5 py-0.5 rounded border border-red-500";
        valBeamReach.innerText = "180 FEET";
        valStoppingDist.innerText = "312 FEET";
        valStoppingDist.className = "text-red-400 font-bold";
        valMargin.innerText = "-132 FT DEFICIT";
        valMargin.className = "text-red-500 font-bold";
        valOverdriveStatus.innerText = "CRITICAL HAZARD";
        valOverdriveStatus.className = "text-red-500 font-bold";

        // HUD
        hudStatusPill.innerText = "OVERDRIVING HEADLIGHTS";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono";
        hudSpeed.innerText = "65 MPH (OVERDRIVE!)";
        hudSpeed.className = "font-bold text-red-500 text-right";
        hudBeam.innerText = "180 FT (LOW BEAM)";
        hudStopping.innerText = "312 FT (STOPPING DIST)";
        hudStopping.className = "font-bold text-red-500 text-right";
        hudBuffer.innerText = "-132 FT DEFICIT";
        hudBuffer.className = "font-bold text-red-500 text-right";
        hudSubtext.innerHTML = "<strong>Step 2 (The Overdriving Dilemma):</strong> Accelerating to 65 MPH pushes stopping distance to 312 feet. Since low beams only illuminate 180 feet, you are driving 132 feet completely blind into the dark!";

      }} else if (step === 3) {{
        // Step 3: Unlit Obstacle in Dark (t = 6..9s)
        const prog = (t - 6.0) / 3.0;
        const egoX = 42.0 + prog * 4.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5 animate-bounce';
        egoTagText.innerText = "EGO: OBSTACLE SUDDENLY VISIBLE • CANNOT STOP IN TIME!";

        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#090D16]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "UNLIT OBSTACLE: CRITICAL COLLISION COURSE!";

        // Beam reaches just to obstacle, but car cannot stop before it
        svgHeadlightCone.style.display = 'block';
        svgHeadlightCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 150}},${{egoY * 5.625 - 110}} ${{egoX * 10 + 190}},${{egoY * 5.625 - 40}}`);

        svgStoppingVector.style.display = 'block';
        stopDistLine.setAttribute('x1', egoX * 10);
        stopDistLine.setAttribute('y1', egoY * 5.625);
        stopDistLine.setAttribute('x2', egoX * 10 + 260);
        stopDistLine.setAttribute('y2', egoY * 5.625 - 190);
        stopDistLine.setAttribute('stroke', '#EF4444');
        stopDistPoint.setAttribute('cx', egoX * 10 + 260);
        stopDistPoint.setAttribute('cy', egoY * 5.625 - 190);
        stopDistPoint.setAttribute('fill', '#EF4444');
        const text3X = egoX * 10 - 90;
        const text3Y = egoY * 5.625 - 90;
        stopDistText.setAttribute('x', text3X);
        stopDistText.setAttribute('y', text3Y);
        stopDistText.setAttribute('fill', '#EF4444');
        stopDistLine1.setAttribute('x', text3X);
        stopDistLine1.textContent = "COLLISION ENVELOPE: 312 FT";
        stopDistLine2.setAttribute('x', text3X);
        stopDistLine2.textContent = "(IMPACT GUARANTEED)";

        // Widget
        beamModeBadge.innerText = "CRASH IMMINENT";
        beamModeBadge.className = "text-[9px] font-black text-white mono bg-red-950 px-1.5 py-0.5 rounded border border-red-500";
        valBeamReach.innerText = "180 FEET";
        valStoppingDist.innerText = "312 FEET";
        valMargin.innerText = "COLLISION PREDICTED";
        valMargin.className = "text-red-500 font-bold";
        valOverdriveStatus.innerText = "100% FATAL RISK";

        // HUD
        hudStatusPill.innerText = "IMPACT UNAVOIDABLE";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white border border-red-400 mono";
        hudSpeed.innerText = "65 MPH (BRAKING)";
        hudSpeed.className = "font-bold text-red-500 text-right";
        hudBuffer.innerText = "OVERSHOOT HAZARD";
        hudSubtext.innerHTML = "<strong>Step 3 (The Crash Reality):</strong> The obstacle suddenly appears in low beams only 180 feet away. Because stopping takes 312 feet, an impact is physically guaranteed before the vehicle can halt.";

      }} else if (step === 4) {{
        // Step 4: High Beam Illumination & Safe Speed (t = 9..12s)
        const egoX = 40.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';

        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "EGO: HIGH BEAMS ACTIVE (420 FT REACH) • SAFE STOP";

        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#090D16]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "OBSTACLE PERCEIVED 220 FT BEFORE STOP POINT";

        // High beam expansive cone piercing into distance
        svgHeadlightCone.style.display = 'block';
        svgHeadlightCone.setAttribute('fill', 'url(#highBeamGrad)');
        svgHeadlightCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 320}},${{egoY * 5.625 - 240}} ${{egoX * 10 + 390}},${{egoY * 5.625 - 90}}`);

        // Stopping distance: 312 ft (INSIDE 420 FT BEAM!)
        svgStoppingVector.style.display = 'block';
        stopDistLine.setAttribute('x1', egoX * 10);
        stopDistLine.setAttribute('y1', egoY * 5.625);
        stopDistLine.setAttribute('x2', egoX * 10 + 260);
        stopDistLine.setAttribute('y2', egoY * 5.625 - 190);
        stopDistLine.setAttribute('stroke', '#10B981');
        stopDistPoint.setAttribute('cx', egoX * 10 + 260);
        stopDistPoint.setAttribute('cy', egoY * 5.625 - 190);
        stopDistPoint.setAttribute('fill', '#10B981');
        const text4X = egoX * 10 - 80;
        const text4Y = egoY * 5.625 - 90;
        stopDistText.setAttribute('x', text4X);
        stopDistText.setAttribute('y', text4Y);
        stopDistText.setAttribute('fill', '#10B981');
        stopDistLine1.setAttribute('x', text4X);
        stopDistLine1.textContent = "STOPPING DISTANCE: 312 FT";
        stopDistLine2.setAttribute('x', text4X);
        stopDistLine2.textContent = "(SAFE INSIDE 420 FT HIGH BEAM)";

        // Widget
        beamModeBadge.innerText = "HIGH BEAM (COMPLIANT)";
        beamModeBadge.className = "text-[9px] font-black text-white mono bg-emerald-950 px-1.5 py-0.5 rounded border border-emerald-500/40";
        valBeamReach.innerText = "420 FEET";
        valStoppingDist.innerText = "312 FEET";
        valStoppingDist.className = "text-emerald-400 font-bold";
        valMargin.innerText = "+108 FT BUFFER";
        valMargin.className = "text-emerald-400 font-bold";
        valOverdriveStatus.innerText = "PROTECTED";
        valOverdriveStatus.className = "text-emerald-400 font-bold";

        // HUD
        hudStatusPill.innerText = "SAFE NIGHT PROFILE";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono";
        hudSpeed.innerText = "65 MPH (CONTROLLED)";
        hudSpeed.className = "font-bold text-emerald-400 text-right";
        hudBeam.innerText = "420 FT (HIGH BEAM)";
        hudStopping.innerText = "312 FT (STOPPING DIST)";
        hudStopping.className = "font-bold text-emerald-400 text-right";
        hudBuffer.innerText = "+108 FT BUFFER";
        hudBuffer.className = "font-bold text-emerald-400 text-right";
        hudSubtext.innerHTML = "<strong>Step 4:</strong> High beams extend sightline to 420 feet, providing a 108-foot safety buffer ahead of your 312-foot stopping distance. Or, if high beams cannot be used, speed must be reduced to 45 MPH.";
      }}
    }}

    // ==========================================
    // MODE 2: HAZARD — ONCOMING HIGH BEAM GLARE & 500-FT DIMMING
    // ==========================================
    function renderMode2(t, step) {{
      hazardBanner.style.display = 'block';
      svgFogAnchor.style.display = 'block';
      svgGlareHalo.style.display = 'block';
      svgStoppingVector.style.display = 'none';
      cyclePill.style.display = 'none';
      hudStatusPill.style.opacity = '0.0';

      hazardTitle.innerText = "CRITICAL HAZARD: ONCOMING HIGH BEAM GLARE (TTC § 547.333)";
      hazardDesc.innerText = "Approaching high beams blind vision for 3 to 7 full seconds. Texas law mandates dimming within 500 feet. Anchor eyes to the lower right white fog line.";

      // Ego in Lane 2
      const egoX = 40.0;
      const egoY = getLaneY(2, egoX);
      vehEgo.style.left = egoX + '%';
      vehEgo.style.top = egoY + '%';
      egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-sky-400 text-[10px] font-extrabold text-sky-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      egoTagText.innerText = "EGO: GAZE ANCHORED TO RIGHT FOG LINE • LOW BEAMS ON";

      // Oncoming high-beam car in Lane 3 (heading down-left)
      const yellX = 56.0;
      const yellY = getLaneY(3, yellX);
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';
      yellowTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5 animate-pulse';
      yellowTagText.innerText = "ONCOMING VEHICLE: HIGH BEAMS WITHIN 500 FT (VIOLATION!)";

      // Oncoming Glare Halo
      svgGlareHalo.setAttribute('cx', yellX * 10);
      svgGlareHalo.setAttribute('cy', yellY * 5.625);

      // Low beam for Ego
      svgHeadlightCone.style.display = 'block';
      svgHeadlightCone.setAttribute('fill', 'url(#lowBeamGrad)');
      svgHeadlightCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 150}},${{egoY * 5.625 - 110}} ${{egoX * 10 + 190}},${{egoY * 5.625 - 40}}`);

      // Widget showing Glare Protocol
      beamModeBadge.innerText = "GLARE DEFENSE";
      beamModeBadge.className = "text-[9px] font-black text-white mono bg-sky-950 px-1.5 py-0.5 rounded border border-sky-400";
      valBeamReach.innerText = "LOW BEAMS ON";
      valStoppingDist.innerText = "TTC § 547.333";
      valMargin.innerText = "FOG LINE ANCHOR";
      valMargin.className = "text-sky-300 font-bold";
      valOverdriveStatus.innerText = "GLARE DEFUSED";
      valOverdriveStatus.className = "text-emerald-400 font-bold";

      // HUD
      hudSpeed.innerText = "45 MPH (CONTROLLED)";
      hudSpeed.className = "font-bold text-white text-right";
      hudBeam.innerText = "LOW BEAMS (DIMMED)";
      hudStopping.innerText = "500-FT MANDATE";
      hudStopping.className = "font-bold text-yellow-400 text-right";
      hudBuffer.innerText = "WHITE LINE ANCHOR";
      hudBuffer.className = "font-bold text-sky-400 text-right";
      hudSubtext.innerHTML = "<strong>Texas Fog Line Rule:</strong> Never stare directly into oncoming high beams. Shift your eyes downward toward the white edge fog line on the right side of the road to track your lane while avoiding retinal bleaching.";
    }}

    // ==========================================
    // MODE 3: 300-FT REAR FOLLOWING DIMMING MANDATE
    // ==========================================
    function renderMode3(t, step) {{
      hazardBanner.style.display = 'block';
      svgFogAnchor.style.display = 'none';
      svgGlareHalo.style.display = 'none';
      svgStoppingVector.style.display = 'none';
      cyclePill.style.display = 'none';
      hudStatusPill.style.opacity = '0.0';

      hazardTitle.innerText = "300-FT REAR FOLLOWING DIMMING MANDATE (TTC § 547.333)";
      hazardDesc.innerText = "When following within 300 feet behind another vehicle, headlights must be dimmed to low beams. High beams reflect off rearview mirrors, blinding lead drivers.";

      // Ego following closely in Lane 2
      const egoX = 42.0;
      const egoY = getLaneY(2, egoX);
      vehEgo.style.left = egoX + '%';
      vehEgo.style.top = egoY + '%';
      egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#090D16]/90 border border-emerald-500 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      egoTagText.innerText = "EGO: 220 FT FOLLOWING • LOW BEAMS ACTIVE (TTC § 547.333)";

      // Lead vehicle in Lane 2
      const yellX = 62.0;
      const yellY = getLaneY(2, yellX);
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';
      yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#090D16]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      yellowTagText.innerText = "LEAD VEHICLE: PROTECTED FROM REARVIEW MIRROR GLARE";

      // Low beam for Ego
      svgHeadlightCone.style.display = 'block';
      svgHeadlightCone.setAttribute('fill', 'url(#lowBeamGrad)');
      svgHeadlightCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 150}},${{egoY * 5.625 - 110}} ${{egoX * 10 + 190}},${{egoY * 5.625 - 40}}`);

      // Widget
      beamModeBadge.innerText = "LOW BEAM MANDATE";
      beamModeBadge.className = "text-[9px] font-black text-white mono bg-emerald-950 px-1.5 py-0.5 rounded border border-emerald-500/40";
      valBeamReach.innerText = "180 FEET";
      valStoppingDist.innerText = "220 FT BUFFER";
      valMargin.innerText = "ZERO MIRROR GLARE";
      valMargin.className = "text-emerald-400 font-bold";
      valOverdriveStatus.innerText = "100% COMPLIANT";
      valOverdriveStatus.className = "text-emerald-400 font-bold";

      // HUD
      hudSpeed.innerText = "50 MPH (SYNCHRONIZED)";
      hudSpeed.className = "font-bold text-white text-right";
      hudBeam.innerText = "LOW BEAM (< 300 FT)";
      hudStopping.innerText = "MIRRORS SHIELDED";
      hudStopping.className = "font-bold text-emerald-400 text-right";
      hudBuffer.innerText = "TTC § 547.333";
      hudBuffer.className = "font-bold text-yellow-400 text-right";
      hudSubtext.innerHTML = "<strong>Texas 300-Foot Rear Dimming Mandate:</strong> Texas Transportation Code &sect; 547.333 strictly prohibits using high beams when following another vehicle within 300 feet. Low beams protect the forward driver's night vision.";
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
          btn.className = 'step-card group text-left p-2.5 rounded-xl border border-[#1E2638] bg-[#0E131E] hover:border-blue-500/50 transition';
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

    output_path = os.path.abspath("driving_rule_animations_suite/simulations/L08_T07_night_driving.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 32 simulation built successfully at: {output_path}")

if __name__ == '__main__':
    build_l08_t07()
