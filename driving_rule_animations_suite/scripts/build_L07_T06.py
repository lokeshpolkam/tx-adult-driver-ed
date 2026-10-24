import os
import base64

def build_l07_t06():
    police_clean_path = r"C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\police_cruiser_tx_ne_clean.png"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"

    print("Encoding Lesson 26 assets to base64...")
    with open(police_clean_path, "rb") as f:
        police_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_red_path, "rb") as f:
        car_red_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_yellow_path, "rb") as f:
        car_yellow_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(bg_img_path, "rb") as f:
        bg_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

    print("Assets successfully encoded.")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L07-T06: Responsibilities If Stopped by Law Enforcement</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
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
    .custom-slider {{
      -webkit-appearance: none;
      appearance: none;
      height: 6px;
      border-radius: 3px;
      background: #252E40;
      outline: none;
    }}
    .custom-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #3B82F6;
      cursor: pointer;
      border: 2px solid #FFFFFF;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.6);
      transition: transform 0.1s;
    }}
    .custom-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.2);
    }}
    @keyframes police-strobe-red {{
      0%, 49% {{ opacity: 1; filter: drop-shadow(0 0 10px #EF4444); }}
      50%, 100% {{ opacity: 0.1; }}
    }}
    @keyframes police-strobe-blue {{
      0%, 49% {{ opacity: 0.1; }}
      50%, 100% {{ opacity: 1; filter: drop-shadow(0 0 10px #3B82F6); }}
    }}
    .strobe-red {{
      animation: police-strobe-red 0.3s steps(1) infinite;
    }}
    .strobe-blue {{
      animation: police-strobe-blue 0.3s steps(1) infinite;
    }}
    @keyframes blink-amber {{
      0%, 100% {{ opacity: 1; filter: drop-shadow(0 0 8px #F59E0B); }}
      50% {{ opacity: 0.1; }}
    }}
    .blinker-active {{
      animation: blink-amber 0.6s step-end infinite;
    }}
    @keyframes pulse-danger {{
      0%, 100% {{ opacity: 0.85; transform: scale(1); }}
      50% {{ opacity: 0.35; transform: scale(1.05); }}
    }}
    .danger-pulse {{
      animation: pulse-danger 1.4s ease-in-out infinite;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-3 md:p-6 bg-[#0B0E14]">

  <!-- TOP APP BAR / NAVIGATION HEADER -->
  <main class="max-w-7xl w-full mx-auto space-y-3">
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-[#121824] border border-[#1E293B] rounded-2xl p-4 shadow-xl">
      <div>
        <div class="flex items-center space-x-2 mb-1">
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">TDLR ADE-1317</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 26</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L07-T06: Responsibilities If Stopped by Law Enforcement
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Community Safety Education Act (Senate Bill 30) &bull; TTC § 545.421 (Duty to Stop) & § 543.005 (Notice to Appear)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40" data-mode="1">
          1: Lawful Traffic Stop Protocol (SB 30)
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: Citation Signing ("Promise to Appear")
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Active Lane Halt & Furtive Moves
        </button>
        <div class="h-4 w-px bg-gray-700 mx-1"></div>
        <label class="flex items-center space-x-1.5 text-xs font-medium text-gray-300 cursor-pointer pr-1">
          <input type="checkbox" id="auto-loop-toggle" checked class="rounded bg-gray-800 border-gray-700 text-blue-500 focus:ring-0">
          <span>Auto-Loop</span>
        </label>
      </div>
    </header>

    <!-- INTERACTIVE STEPPER CARDS -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <button class="step-card bg-[#121824] border border-blue-500/60 bg-blue-950/20 rounded-xl p-2.5 text-left transition hover:border-blue-400 group relative overflow-hidden" data-step="1">
        <div class="text-[10px] font-bold text-blue-400 mono flex items-center justify-between">
          <span>STEP 1</span>
          <span class="step-dot w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        </div>
        <div id="step-title-1" class="text-xs font-bold text-blue-200 mt-1">Acknowledge & Signal Right</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="step-dot w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1">Pull to Right Shoulder & Park</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="step-dot w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1">Dome Light & Hands at 10 & 2</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="step-dot w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1">Verbal Notice Before Documents</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG DYNAMIC OVERLAYS (TACTICAL OFFSET, SAFETY CONE, CREDENTIAL CALLOUT) -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#3B82F6" />
          </marker>
          <marker id="arrow-danger" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#EF4444" />
          </marker>
        </defs>

        <!-- TACTICAL FENDER OFFSET & SAFETY CORRIDOR -->
        <g id="tactical-safety-corridor" opacity="1.0">
          <!-- Offset alignment corridor protecting officer on shoulder -->
          <polygon id="safety-corridor-poly" points="460,430 490,400 660,315 630,345" fill="#3B82F6" fill-opacity="0.14" stroke="#60A5FA" stroke-width="1.2" stroke-dasharray="6,4" />
          <g id="badge-tactical-offset" transform="translate(520, 340)">
            <rect x="-65" y="-8" width="130" height="16" rx="8" fill="#0F172A" stroke="#3B82F6" stroke-width="1" />
            <text x="0" y="3" fill="#93C5FD" font-family="'JetBrains Mono', monospace" font-size="5.8" font-weight="900" text-anchor="middle">DPS TACTICAL OFFSET (2 FT)</text>
          </g>
        </g>

        <!-- HUMAN TROOPER / OFFICER SPRITE WALKING TO PASSENGER/DRIVER SIDE -->
        <g id="officer-group" transform="translate(530, 390)" opacity="0.0">
          <circle cx="0" cy="-12" r="4.5" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8" />
          <!-- Trooper Uniform in Tan & Blue with DPS Hat -->
          <path d="M -4,-6 L 4,-6 L 5,6 L -5,6 Z" fill="#1E3A8A" stroke="#172554" stroke-width="0.8" />
          <ellipse cx="0" cy="-15" rx="6" ry="2" fill="#D97706" />
          <!-- Officer Badge (Placed below feet) -->
          <g transform="translate(0, 14)">
            <rect x="-30" y="-5" width="60" height="10" rx="5" fill="#0F172A" stroke="#3B82F6" stroke-width="0.8" />
            <text x="0" y="2.5" fill="#93C5FD" font-family="'JetBrains Mono', monospace" font-size="4.8" font-weight="900" text-anchor="middle">TX TROOPER</text>
          </g>
        </g>

        <!-- MODE 2: STATUTORY CITATION / PROMISE TO APPEAR CALLOUT -->
        <g id="citation-callout-group" opacity="0.0">
          <g transform="translate(640, 240)">
            <rect x="-95" y="-22" width="190" height="44" rx="8" fill="#0F172A" stroke="#3B82F6" stroke-width="1.5" />
            <text x="0" y="-8" fill="#60A5FA" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">TTC § 543.005 PROMISE TO APPEAR</text>
            <text x="0" y="2" fill="#E2E8F0" font-family="'Inter', sans-serif" font-size="5" font-weight="600" text-anchor="middle">Signature is NOT an admission of guilt.</text>
            <text x="0" y="11" fill="#E2E8F0" font-family="'Inter', sans-serif" font-size="5" font-weight="600" text-anchor="middle">Refusal to sign = mandatory physical arrest.</text>
            <line x1="0" y1="22" x2="0" y2="45" stroke="#3B82F6" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arrow-blue)" />
          </g>
        </g>

        <!-- MODE 3: HAZARD CALLOUT (ABRUPT TRAVEL LANE HALT) -->
        <g id="hazard-lane-stop-group" opacity="0.0">
          <ellipse id="hazard-ellipse" cx="560" cy="220" rx="60" ry="26" fill="none" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="6,4" class="danger-pulse" />
          <polygon id="hazard-star" points="0,-14 4,-4 15,-4 7,4 10,14 0,8 -10,14 -7,4 -15,-4 -4,-4" fill="#FBBF24" stroke="#B45309" stroke-width="1.2" transform="translate(560, 220)" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- TEXAS DPS HIGHWAY PATROL POLICE INTERCEPTOR (SUV WITH RED/BLUE STROBES) -->
      <div id="veh-police" class="absolute z-20 pointer-events-none transition-transform" style="left: 48.0%; top: 69.0%; transform: translate(-50%, -50%);">
        <div id="veh-police-sprite" class="relative w-24 aspect-[785/514] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{police_b64}" alt="Texas DPS Patrol Cruiser" class="w-full h-full object-contain filter drop-shadow-[0_14px_14px_rgba(0,0,0,0.8)]" />
          <!-- Rooftop Emergency Lightbar Strobes -->
          <div id="strobe-red" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] strobe-red" style="top: 20%; left: 42%;"></div>
          <div id="strobe-blue" class="absolute w-2.5 h-2.5 rounded-full bg-blue-500 filter blur-[1px] strobe-blue" style="top: 22%; left: 56%;"></div>
        </div>
        <div id="tag-veh-police" class="absolute left-1/2 -translate-x-1/2 top-full mt-2 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#0A101D]/95 border border-blue-500/50 text-[9px] font-bold text-blue-300 mono shadow-xl tracking-wider">
          TX HIGHWAY PATROL: EMERGENCY LIGHTS
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - BEING STOPPED) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none" style="left: 64.0%; top: 54.4%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          <!-- Right Turn Signal (Acknowledges Officer) -->
          <div id="blinker-right" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 55%; left: 88%;"></div>
          <!-- Interior Dome Light (Illuminates Cabin at Night) -->
          <div id="dome-light" class="absolute w-5 h-4 rounded-full bg-yellow-200/40 filter blur-[2px] opacity-0" style="top: 30%; left: 45%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 35%; left: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: SAFELY PARKED ON SHOULDER • HANDS AT 10 & 2
        </div>
      </div>

      <!-- YELLOW HIGHWAY VEHICLE (COMPLYING WITH MOVE OVER & SLOW DOWN LAW) -->
      <div id="veh-yellow" class="absolute z-19 pointer-events-none transition-transform" style="left: 60.0%; top: 18.4%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Passing Highway Traffic" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 top-full mt-2 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          THRU FLOW: VACATED LANE 1 (MOVE OVER LAW)
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#0F172A]/95 border border-blue-500 text-blue-300 mono text-[9px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse shrink-0"></span>
        <span id="pill-status-text">SENATE BILL 30: PULL RIGHT • PARK • HANDS VISIBLE ON WHEEL</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#0F172A]/90 border border-blue-500/50 text-blue-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        <span id="compliance-text">TTC § 545.421 & SB 30 TRAFFIC STOP COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & TRAFFIC STOP HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[270px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">TRAFFIC STOP SAFETY HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">SB 30 COMPLIANT</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-blue-400 mono text-right" id="telem-speed">0 MPH (STOPPED)</span>

          <span class="text-gray-400">Gear & Brake:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-gear">PARK (P) • SET</span>

          <span class="text-gray-400">Driver Hands:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-hands">ON WHEEL (10 & 2)</span>

          <span class="text-gray-400">Cabin / Dome Light:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-cabin">WINDOW DOWN • LIT</span>

          <span class="text-gray-400">Patrol Position:</span>
          <span class="font-bold text-blue-400 mono text-right" id="telem-patrol">TACTICAL OFFSET</span>

          <span class="text-gray-400">Citation Status:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-citation">PROMISE TO APPEAR</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Driver acknowledges emergency lights by activating right turn signal, slowing down smoothly, and scanning for a safe right shoulder.
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER -->
      <div id="hazard-banner" class="absolute z-35 w-[265px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL HAZARD: UNSAFE STOP</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>ABRUPT TRAVEL LANE HALT & FURTIVE MOVES</strong><br>
          Stopping in an active highway lane causes rear-end pileups. Reaching under seats endangers officer safety. Always pull right and show hands.
        </div>
      </div>

    </div>

    <!-- TIMELINE & PLAYBACK CONTROLS -->
    <footer class="bg-[#121824] border border-[#1E293B] rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <button id="play-pause-btn" class="w-10 h-10 rounded-xl bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center shadow-lg transition" title="Play/Pause">
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
    // State Variables
    let currentMode = 1;
    let currentTime = 0.0;
    const duration = 6.0;
    let isPlaying = true;
    let lastTimestamp = null;

    // DOM Elements
    const playPauseBtn = document.getElementById('play-pause-btn');
    const iconPlay = document.getElementById('icon-play');
    const iconPause = document.getElementById('icon-pause');
    const resetBtn = document.getElementById('reset-btn');
    const timelineSlider = document.getElementById('timeline-slider');
    const timeDisplay = document.getElementById('time-display');
    const autoLoopToggle = document.getElementById('auto-loop-toggle');

    // Telemetry Elements
    const telemSpeed = document.getElementById('telem-speed');
    const telemGear = document.getElementById('telem-gear');
    const telemHands = document.getElementById('telem-hands');
    const telemCabin = document.getElementById('telem-cabin');
    const telemPatrol = document.getElementById('telem-patrol');
    const telemCitation = document.getElementById('telem-citation');
    const hudNarrative = document.getElementById('hud-narrative');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const pillStatusText = document.getElementById('pill-status-text');
    const complianceText = document.getElementById('compliance-text');
    const hazardBanner = document.getElementById('hazard-banner');

    // Vehicles & Tags
    const vehPolice = document.getElementById('veh-police');
    const vehPoliceSprite = document.getElementById('veh-police-sprite');
    const tagVehPolice = document.getElementById('tag-veh-police');

    const vehEgo = document.getElementById('veh-ego');
    const vehEgoSprite = document.getElementById('veh-ego-sprite');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const blinkerRight = document.getElementById('blinker-right');
    const domeLight = document.getElementById('dome-light');
    const brakeLights = document.getElementById('brake-lights');

    const vehYellow = document.getElementById('veh-yellow');
    const tagVehYellow = document.getElementById('tag-veh-yellow');

    // SVG Groups
    const tacticalSafetyCorridor = document.getElementById('tactical-safety-corridor');
    const officerGroup = document.getElementById('officer-group');
    const citationCalloutGroup = document.getElementById('citation-callout-group');
    const hazardLaneStopGroup = document.getElementById('hazard-lane-stop-group');
    const hazardStar = document.getElementById('hazard-star');
    const hazardEllipse = document.getElementById('hazard-ellipse');

    // Highway Geometry Equations: y = Y0 - 1.005 * (x - 50.0)
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
        {{ time: 0.8, title: "Acknowledge & Signal Right" }},
        {{ time: 2.2, title: "Pull to Right Shoulder & Park" }},
        {{ time: 3.6, title: "Dome Light & Hands at 10 & 2" }},
        {{ time: 5.0, title: "Verbal Notice Before Documents" }}
      ],
      2: [
        {{ time: 0.8, title: "Officer Issues Citation" }},
        {{ time: 2.2, title: "Notice to Appear (TTC § 543.005)" }},
        {{ time: 3.6, title: "Signature Is NOT Guilt Admission" }},
        {{ time: 5.0, title: "Court Appearance Compliance" }}
      ],
      3: [
        {{ time: 0.8, title: "Abrupt Stop in Active Travel Lane" }},
        {{ time: 2.2, title: "Traffic Platoon Emergency Swerve" }},
        {{ time: 3.6, title: "Reaching Furtively Under Seats" }},
        {{ time: 5.0, title: "High-Risk Officer Safety Crisis" }}
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40';
          else if (m === 2) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-cyan-500/40 bg-cyan-600 text-white shadow-md shadow-cyan-900/40';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500 bg-red-600 text-white shadow-md shadow-red-900/40';
        }} else {{
          if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60';
          else btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white';
        }}
      }});

      const steps = stepConfigs[mode];
      steps.forEach((cfg, idx) => {{
        const titleElem = document.getElementById(`step-title-${{idx + 1}}`);
        if (titleElem) titleElem.textContent = cfg.title;
      }});

      currentTime = 0.0;
      updateSimulation(currentTime);
    }}

    function jumpToStep(stepIdx) {{
      isPlaying = false;
      lastTimestamp = null;
      updatePlayPauseButton();
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

      const blinkOn = (Math.sin(t * 10) > 0);

      // =========================================================================
      // MODE 1: LAWFUL POLICE TRAFFIC STOP PROTOCOL (SB 30 & TTC § 545.421)
      // =========================================================================
      if (currentMode === 1) {{
        tacticalSafetyCorridor.setAttribute('opacity', '1.0');
        citationCalloutGroup.setAttribute('opacity', '0.0');
        hazardLaneStopGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        // Yellow car complying with Move Over Law in Lane 3
        const yellowX = 54.0 + (t / duration) * 16.0;
        const yellowY = getLane3Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'THRU FLOW: VACATED LANE 1 (MOVE OVER LAW)';

        let egoX, egoY, egoSpeed, policeX, policeY;

        if (t < 1.6) {{
          // Step 1: Ego in Lane 2 acknowledges lights with right turn signal, slows 55 -> 35
          const progress = t / 1.6;
          egoX = 44.0 + progress * 8.0; // 44% to 52%
          egoY = getLane2Y(egoX);
          egoSpeed = Math.round(55 - progress * 20);
          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          brakeLights.style.opacity = '0.0';
          domeLight.style.opacity = '0.0';

          policeX = 28.0 + progress * 8.0; // 28% to 36%
          policeY = getLane2Y(policeX);

          officerGroup.setAttribute('opacity', '0.0');
        }} else if (t < 3.2) {{
          // Step 2: Ego crosses Lane 1 onto right emergency shoulder and stops
          const progress = (t - 1.6) / 1.6;
          egoX = 52.0 + progress * 12.0; // 52% to 64%
          const y2 = getLane2Y(egoX);
          const yS = getShoulderY(egoX);
          egoY = y2 + progress * (yS - y2);
          egoSpeed = Math.round(35 * (1 - progress));
          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          brakeLights.style.opacity = (egoSpeed > 0) ? '1.0' : '0.0';
          domeLight.style.opacity = '0.0';

          // Police cruiser follows to shoulder in tactical offset (offset left by 1.5%)
          policeX = 36.0 + progress * 12.0; // 36% to 48%
          const pY2 = getLane2Y(policeX);
          const pYS = getShoulderY(policeX) - 1.5; // offset left
          policeY = pY2 + progress * (pYS - pY2);

          officerGroup.setAttribute('opacity', '0.0');
        }} else if (t < 4.6) {{
          // Step 3: Ego fully stopped in PARK, parking brake set, dome light ON, hands at 10 & 2
          egoX = 64.0;
          egoY = getShoulderY(egoX);
          egoSpeed = 0;
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          domeLight.style.opacity = '1.0';

          policeX = 48.0;
          policeY = getShoulderY(policeX) - 1.5;

          // Officer exits patrol cruiser and begins approach
          officerGroup.setAttribute('opacity', '1.0');
          const officerProgress = (t - 3.2) / 1.4;
          const offX = 490 + officerProgress * 70; // 490 to 560
          const offY = 415 - officerProgress * 25;
          officerGroup.setAttribute('transform', `translate(${{offX}}, ${{offY}})`);
        }} else {{
          // Step 4: Officer at passenger side / driver window; driver verbally communicates
          egoX = 64.0;
          egoY = getShoulderY(egoX);
          egoSpeed = 0;
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          domeLight.style.opacity = '1.0';

          policeX = 48.0;
          policeY = getShoulderY(policeX) - 1.5;

          officerGroup.setAttribute('opacity', '1.0');
          officerGroup.setAttribute('transform', 'translate(580, 380)');
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';

        vehPolice.style.left = `${{policeX}}%`;
        vehPolice.style.top = `${{policeY}}%`;
        vehPolice.style.transform = 'translate(-50%, -50%)';
        vehPoliceSprite.style.transform = 'rotate(0deg)';

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (STOPPED)' : `${{egoSpeed}} MPH`;
        telemGear.textContent = (egoSpeed === 0) ? 'PARK (P) • SET' : 'DRIVE (DECEL)';
        telemGear.className = (egoSpeed === 0) ? 'font-bold text-emerald-400 mono text-right' : 'font-bold text-blue-400 mono text-right';
        telemHands.textContent = (t < 3.2) ? 'STEERING TO SHOULDER' : 'ON WHEEL (10 & 2)';
        telemCabin.textContent = (t < 3.2) ? 'PREPARING' : 'WINDOW DOWN • DOME ON';
        telemPatrol.textContent = (t < 3.2) ? 'FOLLOWING' : 'TACTICAL OFFSET (2 FT)';
        telemCitation.textContent = 'STANDARD TRAFFIC STOP';

        pillStatusText.textContent = 'SENATE BILL 30: PULL RIGHT • PARK • HANDS VISIBLE ON WHEEL';
        complianceText.textContent = 'TTC § 545.421 & SB 30 TRAFFIC STOP COMPLIANCE VERIFIED';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: RIGHT SIGNAL ACTIVE • EASING SPEED';
          signalStateBadge.textContent = 'ACKNOWLEDGING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 1: Driver acknowledges emergency lights by activating right turn signal, slowing down smoothly, and scanning for a safe right shoulder.';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: CROSSING TO RIGHT EMERGENCY SHOULDER';
          signalStateBadge.textContent = 'SHOULDER EGRESS';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 2: Never pull to the left median on highways. Guide vehicle smoothly to the right emergency shoulder out of live traffic lanes.';
        }} else if (t < 4.6) {{
          tagVehEgo.textContent = 'EGO: PARK ENGAGED • DOME LIGHT ON • HANDS AT 10 & 2';
          signalStateBadge.textContent = 'CABIN SECURED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
          hudNarrative.textContent = 'Step 3: Put transmission in PARK, set emergency parking brake, turn off engine, roll down window, turn on dome light at night, and keep both hands visible on the wheel.';
        }} else {{
          tagVehEgo.textContent = 'EGO: VERBAL NOTICE GIVEN BEFORE REACHING FOR LICENSE';
          signalStateBadge.textContent = 'CREDENTIAL PROTOCOL';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
          hudNarrative.textContent = 'Step 4: When officer asks for driver license and insurance, verbally inform the officer where they are located before reaching into glove compartment or pockets.';
        }}
      }}

      // =========================================================================
      // MODE 2: SIGNING THE CITATION — "PROMISE TO APPEAR" (TTC § 543.005)
      // =========================================================================
      else if (currentMode === 2) {{
        tacticalSafetyCorridor.setAttribute('opacity', '1.0');
        citationCalloutGroup.setAttribute('opacity', '1.0');
        hazardLaneStopGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        blinkerRight.style.opacity = '0.0';
        brakeLights.style.opacity = '0.0';
        domeLight.style.opacity = '1.0';

        // Yellow car traveling in Lane 3
        const yellowX = 60.0;
        const yellowY = getLane3Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'THRU TRAFFIC: 50 MPH (LANE 3)';

        // Both vehicles parked on right shoulder
        const egoX = 64.0;
        const egoY = getShoulderY(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';
        tagVehEgo.textContent = 'EGO: SIGNING NOTICE TO APPEAR (TTC § 543.005)';

        const policeX = 48.0;
        const policeY = getShoulderY(policeX) - 1.5;
        vehPolice.style.left = `${{policeX}}%`;
        vehPolice.style.top = `${{policeY}}%`;
        vehPolice.style.transform = 'translate(-50%, -50%)';
        vehPoliceSprite.style.transform = 'rotate(0deg)';
        tagVehPolice.textContent = 'TX HIGHWAY PATROL: ISSUING CITATION';

        officerGroup.setAttribute('opacity', '1.0');
        officerGroup.setAttribute('transform', 'translate(580, 380)');

        telemSpeed.textContent = '0 MPH (PARKED)';
        telemGear.textContent = 'PARK (P) • SET';
        telemGear.className = 'font-bold text-emerald-400 mono text-right';
        telemHands.textContent = 'SIGNING CITATION';
        telemCabin.textContent = 'WINDOW DOWN';
        telemPatrol.textContent = 'OFFICER AT WINDOW';
        telemCitation.textContent = 'PROMISE TO APPEAR (NOT GUILT)';
        telemCitation.className = 'font-bold text-emerald-400 mono text-right';

        pillStatusText.textContent = 'LEGAL RULE (TTC § 543.005): SIGNATURE IS A PROMISE TO APPEAR, NOT ADMISSION OF GUILT';
        complianceText.textContent = 'TTC § 543.005 CITATION COMPLIANCE VERIFIED';

        hudNarrative.textContent = 'TTC § 543.005: Signing a citation is strictly a written promise to appear in court or contact the court; it is NOT an admission of guilt. Refusal to sign requires officer to make an immediate physical arrest.';
        signalStateBadge.textContent = 'NOTICE TO APPEAR';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: ABRUPT ACTIVE LANE STOP & FURTIVE MOVEMENTS
      // =========================================================================
      else if (currentMode === 3) {{
        tacticalSafetyCorridor.setAttribute('opacity', '0.0');
        citationCalloutGroup.setAttribute('opacity', '0.0');
        hazardLaneStopGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';
        blinkerRight.style.opacity = '0.0';
        domeLight.style.opacity = '0.0';

        // Ego abruptly halts in live travel Lane 2 at x = 56%
        const egoX = 56.0;
        const egoY = getLane2Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';
        brakeLights.style.opacity = '1.0';
        tagVehEgo.textContent = 'EGO: ABRUPT HALT IN TRAVEL LANE 2 • REACHING DOWN!';

        // Police stopped behind in Lane 2 at x = 40%
        const policeX = 40.0;
        const policeY = getLane2Y(policeX);
        vehPolice.style.left = `${{policeX}}%`;
        vehPolice.style.top = `${{policeY}}%`;
        vehPolice.style.transform = 'translate(-50%, -50%)';
        vehPoliceSprite.style.transform = 'rotate(0deg)';
        tagVehPolice.textContent = 'TX HIGHWAY PATROL: TRAVEL LANE STOP HAZARD!';

        // Yellow car approaches in Lane 3 ahead, warning traffic
        const yellowX = 72.0 + (t / duration) * 8.0;
        const yellowY = getLane3Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'TRAFFIC: PANIC EMERGENCY SWERVE!';

        officerGroup.setAttribute('opacity', '0.0');

        // Position hazard star & ellipse over Ego in Lane 2 (SVG coordinates)
        const svgEgoX = 560;
        const svgEgoY = Math.round(getLane2Y(56.0) * 6.0); // 36.53% of 600 = ~219
        hazardStar.setAttribute('transform', `translate(${{svgEgoX}}, ${{svgEgoY}})`);
        hazardEllipse.setAttribute('cx', `${{svgEgoX}}`);
        hazardEllipse.setAttribute('cy', `${{svgEgoY}}`);

        telemSpeed.textContent = '0 MPH (BLOCKED LANE)';
        telemGear.textContent = 'DRIVE (NOT IN PARK)';
        telemGear.className = 'font-bold text-red-500 mono text-right';
        telemHands.textContent = 'REACHING UNDER SEAT (DANGER)';
        telemHands.className = 'font-bold text-red-500 mono text-right';
        telemCabin.textContent = 'WINDOW UP • DARK CABIN';
        telemPatrol.textContent = 'TRAPPED IN TRAFFIC LANE';
        telemCitation.textContent = 'ENDANGERING PUBLIC SAFETY';
        telemCitation.className = 'font-bold text-red-500 mono text-right';

        pillStatusText.textContent = 'CRITICAL ERROR: NEVER STOP IN AN ACTIVE HIGHWAY LANE OR REACH UNDER SEATS!';
        complianceText.textContent = 'CRITICAL SAFETY VIOLATION DETECTED';

        if (t < 2.5) {{
          signalStateBadge.textContent = 'LANE BLOCKED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
          hudNarrative.textContent = 'Step 1 & 2: Driver slams on brakes and stops directly in active highway Lane 2. Approaching highway platoon must violently swerve to prevent a rear-end pileup!';
        }} else {{
          signalStateBadge.textContent = 'FURTIVE MOVEMENT';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
          hudNarrative.textContent = 'Step 3 & 4: Driver makes sudden furtive movements searching under passenger seats. Officers cannot see driver hands, triggering an immediate high-risk felony stop posture.';
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

      document.querySelectorAll('.step-card').forEach(card => {{
        const step = parseInt(card.dataset.step);
        const dot = card.querySelector('.step-dot');
        const titleElem = card.querySelector(`[id^="step-title-"]`);
        if (step === currentStepIdx) {{
          card.classList.remove('border-[#1E293B]', 'bg-[#121824]');
          card.classList.add('border-blue-500/60', 'bg-blue-950/20');
          if (dot) {{
            dot.classList.remove('bg-transparent');
            dot.classList.add('bg-blue-400');
          }}
          if (titleElem) {{
            titleElem.classList.remove('text-gray-300');
            titleElem.classList.add('text-blue-200');
          }}
        }} else {{
          card.classList.remove('border-blue-500/60', 'bg-blue-950/20');
          card.classList.add('border-[#1E293B]', 'bg-[#121824]');
          if (dot) {{
            dot.classList.remove('bg-blue-400');
            dot.classList.add('bg-transparent');
          }}
          if (titleElem) {{
            titleElem.classList.remove('text-blue-200');
            titleElem.classList.add('text-gray-300');
          }}
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
      isPlaying = false;
      lastTimestamp = null;
      updatePlayPauseButton();
      currentTime = 0.0;
      updateSimulation(currentTime);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      isPlaying = false;
      lastTimestamp = null;
      updatePlayPauseButton();
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L07_T06_police_traffic_stop.html"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 26 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_l07_t06()
