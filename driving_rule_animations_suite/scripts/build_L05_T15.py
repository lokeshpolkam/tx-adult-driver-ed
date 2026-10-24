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

    print("Encoding Lesson 22 assets to base64...")
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
  <title>Lesson 22: Winter Driving Hazards — Bridge Icing, Black Ice & Skid Prevention (TTC § 545.351 & § 545.401)</title>
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
      background: #06B6D4;
      cursor: pointer;
      border: 2px solid #083344;
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.7);
    }}
    .custom-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.15);
      background: #22D3EE;
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.35; filter: drop-shadow(0 0 4px #06B6D4); }}
      50% {{ opacity: 0.85; filter: drop-shadow(0 0 14px #22D3EE); }}
    }}
    .ice-pulse {{
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
    @keyframes frostSheen {{
      0% {{ opacity: 0.35; }}
      50% {{ opacity: 0.65; }}
      100% {{ opacity: 0.35; }}
    }}
    .frost-shimmer {{
      animation: frostSheen 3.0s ease-in-out infinite;
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
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 22</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L05-T15: Winter Driving Hazards — Bridge Icing, Black Ice & Skid Prevention
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Driver Handbook Ch. 5 • TTC § 545.351 (Basic Speed & Road Condition Law) & § 545.401 (Reckless Driving Prevention)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-cyan-500/40 bg-cyan-600 text-white shadow-md shadow-cyan-900/40" data-mode="1">
          1: Safe Bridge Crossing (Coasting & 35 MPH)
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: Black Ice Skid & Counter-Steer
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Cruise Control & Panic Brake
        </button>
        <div class="h-4 w-px bg-gray-700 mx-1"></div>
        <label class="flex items-center space-x-1.5 text-xs font-medium text-gray-300 cursor-pointer pr-1">
          <input type="checkbox" id="auto-loop-toggle" checked class="rounded bg-gray-800 border-gray-700 text-cyan-500 focus:ring-0">
          <span>Auto-Loop</span>
        </label>
      </div>
    </header>

    <!-- INTERACTIVE STEPPER CARDS -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <button class="step-card bg-[#121824] border border-cyan-500/40 rounded-xl p-2.5 text-left transition hover:border-cyan-400 group relative overflow-hidden" data-step="1">
        <div class="text-[10px] font-bold text-cyan-400 mono flex items-center justify-between">
          <span>STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
        </div>
        <div id="step-title-1" class="text-xs font-bold text-white mt-1 group-hover:text-cyan-200">Pre-Bridge Deceleration</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Neutral Throttle on Deck</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Smooth Span Tracking</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Safe Ground Road Exit</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Viaduct Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG VECTOR OVERLAYS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <!-- Counter-Steer Marker -->
          <marker id="arrow-counter" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#06B6D4" />
          </marker>
          <marker id="arrow-danger" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#EF4444" />
          </marker>

          <!-- Ice Glaze Linear Gradient -->
          <linearGradient id="ice-glaze-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#E0F2FE" stop-opacity="0.15" />
            <stop offset="40%" stop-color="#BAE6FD" stop-opacity="0.45" />
            <stop offset="70%" stop-color="#38BDF8" stop-opacity="0.35" />
            <stop offset="100%" stop-color="#E0F2FE" stop-opacity="0.10" />
          </linearGradient>
        </defs>

        <!-- ICY BRIDGE DECK HIGHLIGHT REGION (Spans x = 380 to 650) -->
        <g id="bridge-ice-zone" opacity="0.85">
          <!-- Translucent Ice Sheet over elevated viaduct -->
          <polygon points="370,420 440,190 680,80 620,310" fill="url(#ice-glaze-grad)" class="frost-shimmer" />
          <!-- Bridge Expansion Joint Entrance (at x=370) -->
          <line x1="365" y1="425" x2="435" y2="195" stroke="#93C5FD" stroke-width="2.5" stroke-dasharray="6,4" opacity="0.8" />
          <!-- Bridge Expansion Joint Exit (at x=620) -->
          <line x1="615" y1="315" x2="675" y2="85" stroke="#93C5FD" stroke-width="2.5" stroke-dasharray="6,4" opacity="0.8" />
        </g>

        <!-- THERMAL ADVECTION VECTOR INDICATORS (Cold air blowing above & below) -->
        <g id="thermal-advection-callout">
          <!-- Cold air above bridge -->
          <path d="M 450,140 C 490,130 530,120 570,110" fill="none" stroke="#38BDF8" stroke-width="2" stroke-dasharray="5,3" opacity="0.75" />
          <!-- Cold air below bridge viaduct pillars -->
          <path d="M 480,480 C 530,470 580,460 630,450" fill="none" stroke="#38BDF8" stroke-width="2" stroke-dasharray="5,3" opacity="0.75" />
          
          <!-- Roadside MUTCD W8-13 Warning Sign (Diamond: WATCH FOR ICE ON BRIDGE) -->
          <g transform="translate(450, 430)">
            <polygon points="0,-16 16,0 0,16 -16,0" fill="#F59E0B" stroke="#78350F" stroke-width="1.5" />
            <rect x="-1" y="16" width="2" height="16" fill="#4B5563" />
            <text x="0" y="-4" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="4.2" font-weight="900" text-anchor="middle">ICE ON</text>
            <text x="0" y="2" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="4.2" font-weight="900" text-anchor="middle">BRIDGE</text>
            <text x="0" y="8" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="3.5" font-weight="800" text-anchor="middle">AHEAD</text>
          </g>

          <!-- Roadway Temperature Sensor Callout Badge -->
          <g transform="translate(535, 430)">
            <rect x="-55" y="-12" width="110" height="20" rx="6" fill="#082F49" stroke="#38BDF8" stroke-width="1.2" />
            <text x="0" y="2" fill="#BAE6FD" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" text-anchor="middle">DECK: 29°F (FREEZING)</text>
          </g>
        </g>

        <!-- COUNTER-STEER VECTOR CALLOUT (Mode 2 Step 3) -->
        <g id="counter-steer-group" opacity="0.0" class="transition-opacity duration-300">
          <path id="steer-vector-arc" d="M 490,290 C 520,295 550,285 570,265" stroke="#06B6D4" stroke-width="3" stroke-dasharray="6,4" fill="none" marker-end="url(#arrow-counter)" />
          <g transform="translate(555, 305)">
            <rect x="-65" y="-12" width="130" height="18" rx="9" fill="#042F2E" stroke="#06B6D4" stroke-width="1.2" />
            <text x="0" y="0" fill="#67E8F9" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">STEER INTO SKID →</text>
          </g>
        </g>

        <!-- MODE 3: SPIN-OUT DANGER HALO & CRITICAL HAZARD -->
        <g id="spin-hazard-group" opacity="0.0">
          <ellipse cx="480" cy="270" rx="60" ry="32" fill="none" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="8,6" class="danger-pulse" />
          <polygon id="hazard-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- BLUE THRU HIGHWAY VEHICLE (LANE 2 AHEAD AT 65 MPH / 35 MPH IN WINTER) -->
      <div id="veh-blue" class="absolute z-20 pointer-events-none transition-transform" style="left: 72.0%; top: 20.4%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_ne_b64}" alt="Thru Vehicle Lane 2" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          LEAD VEHICLE: 35 MPH (LANE 2)
        </div>
      </div>

      <!-- YELLOW TRAFFIC VEHICLE (LANE 1 TRAILING AT 65 MPH / 35 MPH) -->
      <div id="veh-yellow" class="absolute z-20 pointer-events-none transition-transform" style="left: 26.0%; top: 80.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Highway Traffic Lane 1" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          FOLLOWING CUSHION: 8 SECONDS
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - WINTER DYNAMICS & YAW SIMULATION) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none" style="left: 46.0%; top: 46.6%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_red_ne_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 35%; left: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider">
          EGO: NEUTRAL THROTTLE ON ICED BRIDGE
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#082F49]/95 border border-cyan-500 text-cyan-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS WINTER RULE: BRIDGES FREEZE FIRST • DISENGAGE CRUISE • NO PANIC BRAKING</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#082F49]/90 border border-cyan-500/50 text-cyan-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
        <span id="compliance-text">TTC § 545.351 SPECIAL ROAD HAZARD COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & WINTER DYNAMICS HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[275px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">WINTER DYNAMICS HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono">SAFE COASTING</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-cyan-400 mono text-right" id="telem-speed">35 MPH</span>

          <span class="text-gray-400">Deck Temp:</span>
          <span class="font-bold text-cyan-300 mono text-right" id="telem-temp">29°F (FROZEN)</span>

          <span class="text-gray-400">Friction Coeff:</span>
          <span class="font-bold text-amber-400 mono text-right" id="telem-friction">μ = 0.08 (BLACK ICE)</span>

          <span class="text-gray-400">Cruise Control:</span>
          <span class="font-bold text-cyan-400 mono text-right" id="telem-cruise">DISENGAGED (SAFE)</span>

          <span class="text-gray-400">Throttle Input:</span>
          <span class="font-bold text-cyan-400 mono text-right" id="telem-throttle">NEUTRAL COAST</span>

          <span class="text-gray-400">Braking Action:</span>
          <span class="font-bold text-cyan-400 mono text-right" id="telem-brake">NO BRAKES (SAFE)</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Driver notes W8-13 sign & decelerates smoothly to 35 MPH prior to bridge joint. Cruise control disengaged.
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER (Positioned below status pill in clear air space) -->
      <div id="hazard-banner" class="absolute z-35 w-[350px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10.5px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL HAZARD: CRUISE CONTROL & BRAKING ON ICE</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>TOTAL CONTROL LOSS (TTC § 545.351 & § 545.401)</strong><br>
          Automated cruise control surge combined with sudden panic braking causes complete wheel lockup, triggering an unrecoverable 360° bridge-rail pileup.
        </div>
      </div>

    </div>

    <!-- TIMELINE & PLAYBACK CONTROLS -->
    <footer class="bg-[#121824] border border-[#1E293B] rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <button id="play-pause-btn" class="w-10 h-10 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white flex items-center justify-center shadow-lg transition" title="Play/Pause">
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
    let currentMode = 1; // 1: Safe Bridge Crossing, 2: Black Ice Skid Recovery, 3: Cruise Control & Panic Brake
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

    const brakeLights = document.getElementById('brake-lights');
    const counterSteerGroup = document.getElementById('counter-steer-group');
    const spinHazardGroup = document.getElementById('spin-hazard-group');
    const hazardStar = document.getElementById('hazard-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const telemSpeed = document.getElementById('telem-speed');
    const telemTemp = document.getElementById('telem-temp');
    const telemFriction = document.getElementById('telem-friction');
    const telemCruise = document.getElementById('telem-cruise');
    const telemThrottle = document.getElementById('telem-throttle');
    const telemBrake = document.getElementById('telem-brake');
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

    // Step definitions for each mode
    const stepConfigs = {{
      1: [
        {{ time: 0.8, title: "Pre-Bridge Deceleration" }},
        {{ time: 2.2, title: "Neutral Throttle on Deck" }},
        {{ time: 3.6, title: "Smooth Span Tracking" }},
        {{ time: 5.0, title: "Safe Ground Road Exit" }}
      ],
      2: [
        {{ time: 0.8, title: "Black Ice Yaw (+16°)" }},
        {{ time: 2.2, title: "Throttle Lift (No Brakes!)" }},
        {{ time: 3.6, title: "Counter-Steer into Skid" }},
        {{ time: 5.0, title: "Straighten & Regain Grip" }}
      ],
      3: [
        {{ time: 0.8, title: "65 MPH Cruise on Bridge" }},
        {{ time: 2.2, title: "Wheel Spin & Panic Brake!" }},
        {{ time: 3.6, title: "Fatal 360° Barrier Crash" }},
        {{ time: 5.0, title: "Multi-Car Pileup Hazard" }}
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-cyan-500/40 bg-cyan-600 text-white shadow-md shadow-cyan-900/40';
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

      // =========================================================================
      // MODE 1: SAFE WINTER BRIDGE CROSSING (COASTING AT 35 MPH, NO CRUISE)
      // =========================================================================
      if (currentMode === 1) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        counterSteerGroup.setAttribute('opacity', '0.0');
        brakeLights.style.opacity = '0.0';

        // Blue Lead Vehicle ahead in Lane 2 at 35 MPH
        const blueX = 68.0 + (t / duration) * 8.0; // 68% to 76%
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'LEAD VEHICLE: 35 MPH (LANE 2)';

        // Yellow Trailing Vehicle in Lane 1 trailing at 35 MPH
        const yellowX = 26.0 + (t / duration) * 8.0; // 26% to 34%
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'TRAILING BUFFER: 8 SECONDS';

        // Ego Car: Decelerates smoothly to 35 MPH before bridge, then neutral coast across deck
        let egoX, egoY, yawAngle, egoSpeed, deckTemp, frictionVal;
        if (t < 1.6) {{
          // Pre-bridge approach on ground roadbed
          const progress = t / 1.6;
          egoX = 43.0 + progress * 3.5; // 43% to 46.5%
          egoY = getLane2Y(egoX);
          yawAngle = 0;
          egoSpeed = Math.round(50 - progress * 15); // 50 -> 35 MPH
          deckTemp = '34°F (WET ROAD)';
          frictionVal = 'μ = 0.55 (WET)';
        }} else if (t < 3.0) {{
          // Entering elevated bridge deck (neutral coast)
          const progress = (t - 1.6) / 1.4;
          egoX = 46.5 + progress * 3.5; // 46.5% to 50%
          egoY = getLane2Y(egoX);
          yawAngle = 0;
          egoSpeed = 35;
          deckTemp = '29°F (BLACK ICE)';
          frictionVal = 'μ = 0.08 (ICE)';
        }} else if (t < 4.4) {{
          // Tracking smoothly across iced viaduct span
          const progress = (t - 3.0) / 1.4;
          egoX = 50.0 + progress * 3.5; // 50% to 53.5%
          egoY = getLane2Y(egoX);
          yawAngle = 0;
          egoSpeed = 35;
          deckTemp = '29°F (BLACK ICE)';
          frictionVal = 'μ = 0.08 (ICE)';
        }} else {{
          // Exiting bridge span back onto ground asphalt
          const progress = (t - 4.4) / 1.6;
          egoX = 53.5 + progress * 3.5; // 53.5% to 57%
          egoY = getLane2Y(egoX);
          yawAngle = 0;
          egoSpeed = 38;
          deckTemp = '33°F (SALTED ROAD)';
          frictionVal = 'μ = 0.60 (RESTORED)';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = `rotate(${{yawAngle.toFixed(1)}}deg)`;

        telemSpeed.textContent = `${{egoSpeed}} MPH`;
        telemTemp.textContent = deckTemp;
        telemFriction.textContent = frictionVal;
        telemCruise.textContent = 'DISENGAGED (SAFE)';
        telemThrottle.textContent = (t < 1.6) ? 'EASING OFF THROTTLE' : ((t < 4.4) ? 'STEADY NEUTRAL COAST' : 'GENTLE ACCELERATION');
        telemBrake.textContent = 'NO BRAKES (CORRECT)';

        pillStatusText.textContent = 'TEXAS WINTER RULE: BRIDGES FREEZE FIRST • DISENGAGE CRUISE • NO PANIC BRAKING';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: PRE-BRIDGE DECEL (35 MPH) • CRUISE OFF';
          hudNarrative.textContent = 'Step 1: Driver spots W8-13 sign & eases speed to 35 MPH BEFORE the bridge expansion joint. Cruise control manually cancelled.';
          signalStateBadge.textContent = 'APPROACH SLOWDOWN';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        }} else if (t < 3.0) {{
          tagVehEgo.textContent = 'EGO: NEUTRAL THROTTLE ON ICED BRIDGE DECK';
          hudNarrative.textContent = 'Step 2: Entering elevated span where air circulates above & below. Driver maintains neutral throttle without tapping brakes or shifting gears.';
          signalStateBadge.textContent = 'NEUTRAL COAST';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono';
        }} else if (t < 4.4) {{
          tagVehEgo.textContent = 'EGO: SMOOTH WHEEL TRACKING ACROSS BLACK ICE';
          hudNarrative.textContent = 'Step 3: Maintaining straight wheel alignment across transparent black ice sheet. Zero sudden steering inputs prevents lateral breakaway.';
          signalStateBadge.textContent = 'ICE TRACKING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: CLEARED BRIDGE SPAN • TRACTION RESTORED';
          hudNarrative.textContent = 'Step 4: Crossing off elevated bridge onto ground-insulated roadbed. Tire grip restored; safe winter travel speed maintained.';
          signalStateBadge.textContent = 'SAFE CROSSING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 2: BLACK ICE SKID & COUNTER-STEER RECOVERY ON BRIDGE
      // =========================================================================
      else if (currentMode === 2) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        brakeLights.style.opacity = '0.0';

        // Blue Lead Vehicle ahead in Lane 2
        const blueX = 68.0 + (t / duration) * 8.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'LEAD VEHICLE: 35 MPH (LANE 2)';

        // Yellow Trailing Vehicle in Lane 1
        const yellowX = 26.0 + (t / duration) * 8.0;
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'TRAILING BUFFER: 8 SECONDS';

        // Ego Car: Skid breaks loose on ice deck, counter-steers, regains grip
        let egoX, egoY, yawAngle, egoSpeed;
        if (t < 1.6) {{
          // Skid yaw develops on black ice
          const progress = t / 1.6;
          egoX = 43.0 + progress * 3.0; // 43% to 46%
          egoY = getLane2Y(egoX);
          yawAngle = progress * 16.0; // 0 -> +16 deg
          egoSpeed = Math.round(42 - progress * 4); // 42 -> 38 MPH
          counterSteerGroup.setAttribute('opacity', '0.0');
        }} else if (t < 3.0) {{
          // Peak yaw (+18 deg), lifting off accelerator, zero brake touch
          const progress = (t - 1.6) / 1.4;
          egoX = 46.0 + progress * 3.0; // 46% to 49%
          egoY = getLane2Y(egoX);
          yawAngle = 16.0 + progress * 2.0; // 16 -> 18 deg
          egoSpeed = Math.round(38 - progress * 3); // 38 -> 35 MPH
          counterSteerGroup.setAttribute('opacity', '0.0');
        }} else if (t < 4.4) {{
          // Counter-steering into direction of skid
          const progress = (t - 3.0) / 1.4;
          egoX = 49.0 + progress * 3.0; // 49% to 52%
          egoY = getLane2Y(egoX);
          yawAngle = 18.0 - progress * 14.0; // 18 -> 4 deg
          egoSpeed = Math.round(35 - progress * 3); // 35 -> 32 MPH
          counterSteerGroup.setAttribute('opacity', '1.0');
        }} else {{
          // Full alignment restored as wheels clear bridge
          const progress = (t - 4.4) / 1.6;
          egoX = 52.0 + progress * 3.5; // 52% to 55.5%
          egoY = getLane2Y(egoX);
          yawAngle = Math.max(0, 4.0 - progress * 4.0); // 4 -> 0 deg
          egoSpeed = 32;
          counterSteerGroup.setAttribute('opacity', '0.0');
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = `rotate(${{yawAngle.toFixed(1)}}deg)`;

        telemSpeed.textContent = `${{egoSpeed}} MPH`;
        telemTemp.textContent = '29°F (BLACK ICE)';
        telemFriction.textContent = (t >= 4.4) ? 'μ = 0.55 (REGAINED)' : 'μ = 0.08 (SLIPPING)';
        telemCruise.textContent = 'DISENGAGED (SAFE)';
        telemThrottle.textContent = (t < 1.6) ? 'EASING OFF GAS' : 'OFF ACCELERATOR';
        telemBrake.textContent = 'NO BRAKES (CORRECT)';

        pillStatusText.textContent = 'BLACK ICE SKID: DO NOT BRAKE • COUNTER-STEER GENTLY INTO SKID';

        if (t < 1.6) {{
          tagVehEgo.textContent = `EGO: BLACK ICE SLIP (+${{yawAngle.toFixed(0)}}°) • DO NOT HIT BRAKES`;
          hudNarrative.textContent = 'Step 1: Sudden black ice glaze on bridge deck causes rear tires to lose lateral grip. Rear end steps out (+16° yaw).';
          signalStateBadge.textContent = 'ICE SKID INITIATED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.0) {{
          tagVehEgo.textContent = 'EGO: THROTTLE LIFTED • ZERO BRAKE PEDAL PRESSURE';
          hudNarrative.textContent = 'Step 2: Driver immediately lifts foot from accelerator. Does NOT touch brakes! Weight transfers forward smoothly to re-establish tire contact.';
          signalStateBadge.textContent = 'OFF ACCELERATOR';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        }} else if (t < 4.4) {{
          tagVehEgo.textContent = 'EGO: COUNTER-STEERING SMOOTHLY INTO SKID';
          hudNarrative.textContent = 'Step 3: Driver turns front wheels gently in the direction the rear is sliding. Front tires track with vehicle momentum, arresting rotation.';
          signalStateBadge.textContent = 'COUNTER-STEERING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: WHEELS STRAIGHTENED • FULL STABILITY RESTORED';
          hudNarrative.textContent = 'Step 4: As rear tires grip pavement beyond bridge joint, driver straightens wheels cleanly. Full directional control restored without spinning.';
          signalStateBadge.textContent = 'CONTROL RESTORED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: CRUISE CONTROL SURGE & PANIC BRAKING ON ICE
      // =========================================================================
      else if (currentMode === 3) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        counterSteerGroup.setAttribute('opacity', '0.0');

        // Blue Lead Vehicle far ahead in Lane 2
        const blueX = 74.0 + (t / duration) * 6.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 35 MPH (LANE 2)';

        // Yellow Trailing Traffic in Lane 1: Approaching and emergency stops
        let yellowX, yellowY;
        if (t < 2.5) {{
          const progress = t / 2.5;
          yellowX = 23.0 + progress * 8.0; // 23% to 31%
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'APPROACHING: 45 MPH (LANE 1)';
        }} else {{
          yellowX = 31.0;
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'PANIC STOP! AVOIDING BRIDGE CRASH';
        }}
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;

        // Ego Car: 65 MPH cruise control hits ice -> wheel spin -> driver slams brakes -> violent 360 spin
        let egoX, egoY, yawAngle, egoSpeed;
        if (t < 1.6) {{
          // High speed approach with cruise active
          const progress = t / 1.6;
          egoX = 42.0 + progress * 4.0; // 42% to 46%
          egoY = getLane2Y(egoX);
          yawAngle = (Math.sin(t * 12) * 3.0); // wheel torque instability
          egoSpeed = 65;
          brakeLights.style.opacity = '0.0';
          spinHazardGroup.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
        }} else if (t < 3.2) {{
          // Drive wheels spin out, cruise surges, driver panic slams brakes!
          const progress = (t - 1.6) / 1.6;
          egoX = 46.0 + progress * 3.0; // 46% to 49%
          egoY = getLane2Y(egoX);
          yawAngle = progress * 180.0; // 0 -> 180 deg violent spin
          egoSpeed = Math.round(65 * (1 - progress * 0.7)); // 65 -> 20 MPH
          brakeLights.style.opacity = '1.0'; // Hard brakes!
          spinHazardGroup.setAttribute('opacity', '1.0');
          hazardStar.setAttribute('transform', `translate(${{egoX * 10}}, ${{egoY * 6}})`);
          hazardBanner.style.opacity = '1.0';
        }} else {{
          // Spun around backwards at 180 deg into bridge railing
          egoX = 49.0;
          egoY = getLane2Y(egoX);
          yawAngle = 180.0;
          egoSpeed = 0;
          brakeLights.style.opacity = '1.0';
          spinHazardGroup.setAttribute('opacity', '1.0');
          hazardStar.setAttribute('transform', `translate(${{egoX * 10}}, ${{egoY * 6}})`);
          hazardBanner.style.opacity = '1.0';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = `rotate(${{yawAngle.toFixed(1)}}deg)`;

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (CRASHED)' : `${{egoSpeed}} MPH`;
        telemTemp.textContent = '29°F (BLACK ICE)';
        telemFriction.textContent = 'μ = 0.05 (ZERO GRIP)';
        telemCruise.textContent = (t < 1.6) ? 'ACTIVE @ 65 MPH (ILLEGAL)' : 'SURGE DISRUPTED';
        telemThrottle.textContent = (t < 1.6) ? 'CRUISE THROTTLE PULSE' : 'OFF ACCELERATOR';
        telemBrake.textContent = (t >= 1.6) ? 'LOCKED BRAKES (FATAL)' : 'NONE';

        pillStatusText.textContent = 'CRITICAL PANIC ERROR: NEVER USE CRUISE CONTROL OR SLAM BRAKES ON ICY BRIDGES';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: 65 MPH CRUISE ACTIVE • HITTING BLACK ICE SPAN';
          hudNarrative.textContent = 'Step 1: Driver leaves automated cruise control engaged across sub-freezing bridge. Wheels hit black ice at highway speed.';
          signalStateBadge.textContent = 'CRUISE DANGER';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: CRUISE SURGE! BRAKES SLAMMED • VIOLENT SPIN';
          hudNarrative.textContent = 'Step 2: Drive wheels spin freely; cruise attempts to accelerate. Driver panics and slams brakes, locking wheels and causing total spin-out.';
          signalStateBadge.textContent = 'LOCKED BRAKES';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: 180° REVERSE SPUN • BRIDGE RAILING IMPACT';
          hudNarrative.textContent = 'Step 3 & 4: Vehicle spins 180° backwards, striking the viaduct guardrail. Approaching traffic forced into panic threshold stops.';
          signalStateBadge.textContent = 'FATAL CRASH';
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
          card.classList.add('border-cyan-500/60', 'bg-cyan-950/20');
        }} else {{
          card.classList.remove('border-cyan-500/60', 'bg-cyan-950/20');
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L05_T15_winter_driving.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 22 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_simulation()
