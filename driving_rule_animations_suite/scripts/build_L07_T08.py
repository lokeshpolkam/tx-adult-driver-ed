import os
import base64

def build_l07_t08():
    car_blue_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_blue_clean_ne.png"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"

    print("Encoding Lesson 27 assets to base64...")
    with open(car_blue_path, "rb") as f:
        car_blue_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
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
  <title>L07-T08: Aggressive Driving & Road Rage Avoidance</title>
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
    @keyframes blink-amber {{
      0%, 100% {{ opacity: 1; filter: drop-shadow(0 0 8px #F59E0B); }}
      50% {{ opacity: 0.1; }}
    }}
    .blinker-active {{
      animation: blink-amber 0.6s step-end infinite;
    }}
    @keyframes strobe-highbeam {{
      0%, 20%, 40%, 100% {{ opacity: 0.15; }}
      10%, 30% {{ opacity: 0.95; filter: drop-shadow(0 0 12px #FFFFFF); }}
    }}
    .highbeam-flashing {{
      animation: strobe-highbeam 0.8s infinite;
    }}
    @keyframes pulse-danger {{
      0%, 100% {{ opacity: 0.85; transform: scale(1); }}
      50% {{ opacity: 0.35; transform: scale(1.06); }}
    }}
    .danger-pulse {{
      animation: pulse-danger 1.2s ease-in-out infinite;
    }}
    @keyframes pulse-cushion {{
      0%, 100% {{ opacity: 0.6; }}
      50% {{ opacity: 0.25; }}
    }}
    .cushion-pulse {{
      animation: pulse-cushion 2s ease-in-out infinite;
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
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 27</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L07-T08: Aggressive Driving & Road Rage Avoidance
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Defensive De-escalation &bull; TTC § 545.401 (Reckless Driving) & § 545.062 (Tailgating Distance)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40" data-mode="1">
          1: Defensive De-escalation & Yielding
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="2">
          Hazard: "Brake-Checking" Retaliation
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/60" data-mode="3">
          Hazard: Competitive Speed Duel
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
        <div id="step-title-1" class="text-xs font-bold text-blue-200 mt-1">Recognize Tailgating Hazard</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="step-dot w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1">Signal & Yield Passing Lane</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="step-dot w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1">Avoid Eye Contact & Gestures</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="step-dot w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1">Restore Safe Space Cushion</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG DYNAMIC OVERLAYS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <marker id="arrow-green" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#10B981" />
          </marker>
          <marker id="arrow-red" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#EF4444" />
          </marker>
        </defs>

        <!-- DANGEROUS TAILGATING BRACKET (< 0.5s / 15 FT) -->
        <g id="tailgate-bracket-group" opacity="1.0">
          <line id="tailgate-line" x1="440" y1="285" x2="510" y2="250" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="4,4" />
          <g id="tailgate-badge" transform="translate(420, 230)">
            <rect x="-65" y="-9" width="130" height="18" rx="9" fill="#0F172A" stroke="#EF4444" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="900" text-anchor="middle">TAILGATING: < 0.5s (15 FT)</text>
          </g>
        </g>

        <!-- SAFE 3-4 SECOND SPACE CUSHION BRACKET -->
        <g id="cushion-bracket-group" opacity="0.0">
          <polygon id="cushion-zone" points="640,255 760,195 790,220 670,280" fill="#10B981" fill-opacity="0.14" stroke="#34D399" stroke-width="1.5" stroke-dasharray="6,4" class="cushion-pulse" />
          <g id="cushion-badge" transform="translate(720, 230)">
            <rect x="-70" y="-9" width="140" height="18" rx="9" fill="#0F172A" stroke="#10B981" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#6EE7B7" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="900" text-anchor="middle">SAFE 4-SECOND CUSHION (250 FT)</text>
          </g>
        </g>

        <!-- MODE 2 HAZARD: BRAKE-CHECK COLLISION STAR & SKID MARKS -->
        <g id="brake-check-hazard-group" opacity="0.0">
          <!-- Skid Marks in Lane 2 -->
          <line x1="470" y1="275" x2="530" y2="245" stroke="#1E293B" stroke-width="4.5" stroke-linecap="round" opacity="0.8" />
          <line x1="485" y1="285" x2="545" y2="255" stroke="#1E293B" stroke-width="4.5" stroke-linecap="round" opacity="0.8" />
          <!-- Impact Burst Star -->
          <polygon id="impact-star" points="0,-16 5,-5 16,-5 8,4 11,16 0,9 -11,16 -8,4 -16,-5 -5,-5" fill="#EF4444" stroke="#F59E0B" stroke-width="1.5" transform="translate(505, 252)" />
        </g>

        <!-- MODE 3 HAZARD: COMPETITIVE DUEL WARNING -->
        <g id="duel-hazard-group" opacity="0.0">
          <ellipse cx="540" cy="205" rx="75" ry="32" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-dasharray="6,4" class="danger-pulse" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- AGGRESSIVE VEHICLE (BLUE SEDAN - TAILGATING / PASSING) -->
      <div id="veh-blue" class="absolute z-20 pointer-events-none transition-transform" style="left: 44.0%; top: 48.6%; transform: translate(-50%, -50%);">
        <div id="veh-blue-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_blue_b64}" alt="Aggressive Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          <!-- Flashing High-Beams -->
          <div id="highbeam-l" class="absolute w-2 h-2 rounded-full bg-white filter blur-[1px] highbeam-flashing" style="top: 25%; left: 88%;"></div>
          <div id="highbeam-r" class="absolute w-2 h-2 rounded-full bg-white filter blur-[1px] highbeam-flashing" style="top: 45%; left: 94%;"></div>
        </div>
        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider">
          AGGRESSIVE DRIVER: 75 MPH • TAILGATING
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - BEING TAILGATED) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none" style="left: 52.0%; top: 40.6%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          <!-- Right Turn Signal (Signal to Yield) -->
          <div id="blinker-right" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 55%; left: 88%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 35%; left: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: MAINTAINING CALM • PREPARING TO YIELD
        </div>
      </div>

      <!-- YELLOW HIGHWAY VEHICLE (NEUTRAL THRU TRAFFIC IN LANE 3) -->
      <div id="veh-yellow" class="absolute z-19 pointer-events-none transition-transform" style="left: 46.0%; top: 32.5%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Passing Highway Traffic" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          LANE 3: 65 MPH
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#0F172A]/95 border border-blue-500 text-blue-300 mono text-[9px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse shrink-0"></span>
        <span id="pill-status-text">DE-ESCALATION: SIGNAL RIGHT • YIELD PASSING LANE • AVOID CONFRONTATION</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#0F172A]/90 border border-blue-500/50 text-blue-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        <span id="compliance-text">DEFENSIVE ROAD RAGE DE-ESCALATION VERIFIED</span>
      </div>

      <!-- TELEMETRY & DEFENSIVE DE-ESCALATION HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[270px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">DEFENSIVE TACTICS HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">DE-ESCALATING</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-blue-400 mono text-right" id="telem-speed">65 MPH (STEADY)</span>

          <span class="text-gray-400">Following Buffer:</span>
          <span class="font-bold text-red-400 mono text-right" id="telem-buffer">&lt; 0.5s (15 FT)</span>

          <span class="text-gray-400">Ego Demeanor:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-demeanor">CALM • EYES AHEAD</span>

          <span class="text-gray-400">Ego Signal:</span>
          <span class="font-bold text-gray-300 mono text-right" id="telem-signal">OFF</span>

          <span class="text-gray-400">Aggressor Action:</span>
          <span class="font-bold text-red-400 mono text-right" id="telem-aggressor">TAILGATING / FLASH</span>

          <span class="text-gray-400">Legal Posture:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-legal">YIELDING SAFELY</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Driver detects aggressive tailgating in rearview mirror. Avoids anger, resists urge to brake check or speed up, and maintains steady control.
        </div>
      </aside>

      <!-- CRITICAL HAZARD BANNER -->
      <div id="hazard-banner" class="absolute z-35 w-[265px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span id="hazard-banner-title">CRITICAL HAZARD: BRAKE-CHECK</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug" id="hazard-banner-body">
          <strong>WILLFUL RECKLESS DRIVING (TTC § 545.401)</strong><br>
          Slamming brakes in front of a tailgater causes high-speed rear-end pileups. Both drivers face criminal penalties and severe liability.
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
    const telemBuffer = document.getElementById('telem-buffer');
    const telemDemeanor = document.getElementById('telem-demeanor');
    const telemSignal = document.getElementById('telem-signal');
    const telemAggressor = document.getElementById('telem-aggressor');
    const telemLegal = document.getElementById('telem-legal');
    const hudNarrative = document.getElementById('hud-narrative');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const pillStatusText = document.getElementById('pill-status-text');
    const complianceText = document.getElementById('compliance-text');
    const hazardBanner = document.getElementById('hazard-banner');
    const hazardBannerTitle = document.getElementById('hazard-banner-title');
    const hazardBannerBody = document.getElementById('hazard-banner-body');

    // Vehicles & Tags
    const vehBlue = document.getElementById('veh-blue');
    const vehBlueSprite = document.getElementById('veh-blue-sprite');
    const tagVehBlue = document.getElementById('tag-veh-blue');
    const highbeamL = document.getElementById('highbeam-l');
    const highbeamR = document.getElementById('highbeam-r');

    const vehEgo = document.getElementById('veh-ego');
    const vehEgoSprite = document.getElementById('veh-ego-sprite');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const blinkerRight = document.getElementById('blinker-right');
    const brakeLights = document.getElementById('brake-lights');

    const vehYellow = document.getElementById('veh-yellow');
    const tagVehYellow = document.getElementById('tag-veh-yellow');

    // SVG Overlays
    const tailgateBracketGroup = document.getElementById('tailgate-bracket-group');
    const cushionBracketGroup = document.getElementById('cushion-bracket-group');
    const brakeCheckHazardGroup = document.getElementById('brake-check-hazard-group');
    const duelHazardGroup = document.getElementById('duel-hazard-group');

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

    // Step definitions for each mode
    const stepConfigs = {{
      1: [
        {{ time: 0.8, title: "Recognize Tailgating Hazard" }},
        {{ time: 2.2, title: "Signal & Yield Passing Lane" }},
        {{ time: 3.6, title: "Avoid Eye Contact & Gestures" }},
        {{ time: 5.0, title: "Restore Safe Space Cushion" }}
      ],
      2: [
        {{ time: 0.8, title: "Aggressive Tailgating at 70 MPH" }},
        {{ time: 2.2, title: "Retaliatory Sudden Brake-Check" }},
        {{ time: 3.6, title: "Zero Reaction Cushion Crash" }},
        {{ time: 5.0, title: "Severe Pileup & Criminal Charge" }}
      ],
      3: [
        {{ time: 0.8, title: "Aggressor Attempts Lane 3 Pass" }},
        {{ time: 2.2, title: "Ego Accelerates to Block Pass" }},
        {{ time: 3.6, title: "Side-by-Side Competitive Duel" }},
        {{ time: 5.0, title: "Fatal Road Rage Crash Crisis" }}
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40';
          else if (m === 2) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500 bg-red-600 text-white shadow-md shadow-red-900/40';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-amber-500 bg-amber-600 text-white shadow-md shadow-amber-900/40';
        }} else {{
          if (m === 2) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/60';
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

      // Yellow car in Lane 3 cruises neutrally
      const yellowX = 29.0 + (t / duration) * 4.0;
      const yellowY = getLane3Y(yellowX);
      vehYellow.style.left = `${{yellowX}}%`;
      vehYellow.style.top = `${{yellowY}}%`;

      // =========================================================================
      // MODE 1: DEFENSIVE DE-ESCALATION & YIELDING PASSING LANE
      // =========================================================================
      if (currentMode === 1) {{
        brakeCheckHazardGroup.setAttribute('opacity', '0.0');
        duelHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        brakeLights.style.opacity = '0.0';

        let egoX, egoY, egoSpeed, blueX, blueY, blueSpeed;

        if (t < 1.6) {{
          // Step 1: Ego in Lane 2 recognizes aggressive tailgater behind (< 15 ft)
          const p = t / 1.6;
          egoX = 52.0 + p * 4.0; // 52% to 56%
          egoY = getLane2Y(egoX);
          egoSpeed = 65;

          blueX = egoX - 9.0; // tailgating right behind at 43% to 47%
          blueY = getLane2Y(blueX);
          blueSpeed = 65;

          blinkerRight.style.opacity = '0.0';
          tailgateBracketGroup.setAttribute('opacity', '1.0');
          cushionBracketGroup.setAttribute('opacity', '0.0');

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
          tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";

          telemSpeed.textContent = '65 MPH (STEADY)';
          telemBuffer.textContent = '< 0.5s (15 FT)';
          telemBuffer.className = 'font-bold text-red-400 mono text-right';
          telemDemeanor.textContent = 'CALM • EYES AHEAD';
          telemSignal.textContent = 'OFF';
          telemAggressor.textContent = 'TAILGATING / FLASH';
          telemLegal.textContent = 'HOLDING COURSE';

          tagVehEgo.textContent = 'EGO: CALM • PREPARING TO YIELD';
          tagVehBlue.textContent = 'AGGRESSIVE: 65 MPH • TAILGATING & FLASHING';
          signalStateBadge.textContent = 'MONITORING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 1: Driver detects aggressive tailgating in rearview mirror. Avoids anger, resists urge to brake check or speed up, and maintains steady control.';
        }} else if (t < 3.2) {{
          // Step 2: Ego signals right 100 ft in advance and merges from Lane 2 to Lane 1
          const p = (t - 1.6) / 1.6;
          egoX = 56.0 + p * 8.0; // 56% to 64%
          const y2 = getLane2Y(egoX);
          const y1 = getLane1Y(egoX);
          egoY = y2 + p * (y1 - y2); // smooth diagonal lane change
          egoSpeed = 63;

          blueX = 47.0 + p * 7.0; // 47% to 54% in Lane 2
          blueY = getLane2Y(blueX);
          blueSpeed = 68;

          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          tailgateBracketGroup.setAttribute('opacity', '0.0');
          cushionBracketGroup.setAttribute('opacity', '0.0');

          tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
          tagVehEgo.className = "absolute left-1/2 -translate-x-1/4 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";

          telemSpeed.textContent = '63 MPH (LANE 1 MERGE)';
          telemBuffer.textContent = 'EXPANDING';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemDemeanor.textContent = 'SIGNALING RIGHT';
          telemSignal.textContent = 'RIGHT (100+ FT)';
          telemAggressor.textContent = 'PREPARING TO PASS';
          telemLegal.textContent = 'TTC § 545.104 COMPLIANT';

          tagVehEgo.textContent = 'EGO: RIGHT SIGNAL (TTC § 545.104)';
          tagVehBlue.textContent = 'AGGRESSIVE: LANE 2 OPENING';
          signalStateBadge.textContent = 'LANE EGRESS';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 2: Signal intention at least 100 ft in advance (TTC § 545.104). Check right mirrors and blind spot, then smoothly yield the passing lane to the aggressive driver.';
        }} else if (t < 4.6) {{
          // Step 3: Ego settles in Lane 1; Blue accelerates through Lane 2 to 78 MPH
          const p = (t - 3.2) / 1.4;
          egoX = 64.0;
          egoY = getLane1Y(egoX);
          egoSpeed = 60;

          blueX = 54.0 + p * 22.0; // passes from 54% to 76%
          blueY = getLane2Y(blueX);
          blueSpeed = 78;

          blinkerRight.style.opacity = '0.0';
          tailgateBracketGroup.setAttribute('opacity', '0.0');
          cushionBracketGroup.setAttribute('opacity', '0.0');

          tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";

          telemSpeed.textContent = '60 MPH (LANE 1)';
          telemBuffer.textContent = 'PASSING OCCURRING';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemDemeanor.textContent = '0 ENGAGEMENT / NO LOOK';
          telemSignal.textContent = 'OFF';
          telemAggressor.textContent = 'PASSING AT 78 MPH';
          telemLegal.textContent = 'COURTEOUS YIELD';

          tagVehEgo.textContent = 'EGO: NO EYE CONTACT • HANDS ON WHEEL';
          tagVehBlue.textContent = 'AGGRESSIVE: 78 MPH PASS';
          signalStateBadge.textContent = 'UNIMPEDED PASS';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
          hudNarrative.textContent = 'Step 3: Allow aggressive driver to pass cleanly. Never make eye contact, mouth words, or make obscene gestures. Keep both hands on wheel and look ahead.';
        }} else {{
          // Step 4: Blue is far ahead; Ego maintains safe 4-second cushion
          egoX = 64.0;
          egoY = getLane1Y(egoX);
          egoSpeed = 60;

          blueX = 76.0;
          blueY = getLane2Y(blueX);
          blueSpeed = 80;

          blinkerRight.style.opacity = '0.0';
          tailgateBracketGroup.setAttribute('opacity', '0.0');
          cushionBracketGroup.setAttribute('opacity', '1.0');

          tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";

          telemSpeed.textContent = '60 MPH (CRUISING)';
          telemBuffer.textContent = 'SAFE 4-SEC CUSHION';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemDemeanor.textContent = 'RELAXED & DEFENSIVE';
          telemSignal.textContent = 'OFF';
          telemAggressor.textContent = 'SEPARATED (> 250 FT)';
          telemLegal.textContent = 'SAFE SPATIAL BUFFER';

          tagVehEgo.textContent = 'EGO: SAFE 4-SEC CUSHION RESTORED';
          tagVehBlue.textContent = 'AGGRESSIVE: DISTANT (> 250 FT)';
          signalStateBadge.textContent = 'BUFFER RESTORED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
          hudNarrative.textContent = 'Step 4: Safe spatial cushion restored. If aggressive driving poses an ongoing threat to others, have a passenger dial 9-1-1 or pull over to report license plate and location.';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';

        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        vehBlue.style.transform = 'translate(-50%, -50%)';

        pillStatusText.textContent = 'DE-ESCALATION: SIGNAL RIGHT • YIELD PASSING LANE • AVOID CONFRONTATION';
        complianceText.textContent = 'DEFENSIVE ROAD RAGE DE-ESCALATION VERIFIED';
      }}

      // =========================================================================
      // MODE 2: CATASTROPHIC HAZARD: BRAKE-CHECKING RETALIATION (TTC § 545.401)
      // =========================================================================
      else if (currentMode === 2) {{
        tailgateBracketGroup.setAttribute('opacity', '0.0');
        cushionBracketGroup.setAttribute('opacity', '0.0');
        duelHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '1.0';
        blinkerRight.style.opacity = '0.0';

        hazardBannerTitle.textContent = 'CRITICAL HAZARD: BRAKE-CHECK RETALIATION';
        hazardBannerBody.innerHTML = '<strong>WILLFUL RECKLESS DRIVING (TTC § 545.401)</strong><br>Slamming brakes in front of a tailgater causes high-speed rear-end pileups. Both drivers face criminal charges and civil liability.';

        // Ego abruptly slams brakes in Lane 2 at x = 54%
        const egoX = 54.0;
        const egoY = getLane2Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        brakeLights.style.opacity = '1.0';
        tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
        tagVehEgo.textContent = 'EGO: SLAMS BRAKES ("BRAKE-CHECK") IN LIVE LANE!';

        // Blue tailgating right behind at x = 47% cannot stop in time!
        const blueX = 47.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
        tagVehBlue.textContent = 'AGGRESSIVE: 0 STOPPING DISTANCE • REAR-END IMPACT!';

        brakeCheckHazardGroup.setAttribute('opacity', '1.0');

        telemSpeed.textContent = '0 MPH (IMPACT)';
        telemBuffer.textContent = 'COLLISION (0 FT)';
        telemBuffer.className = 'font-bold text-red-500 mono text-right';
        telemDemeanor.textContent = 'RETALIATORY / ENRAGED';
        telemDemeanor.className = 'font-bold text-red-500 mono text-right';
        telemSignal.textContent = 'NONE';
        telemAggressor.textContent = 'REAR-END COLLISION';
        telemAggressor.className = 'font-bold text-red-500 mono text-right';
        telemLegal.textContent = 'RECKLESS DRIVING (§ 545.401)';
        telemLegal.className = 'font-bold text-red-500 mono text-right';

        pillStatusText.textContent = 'CRITICAL ERROR: NEVER BRAKE-CHECK A TAILGATER! WILLFUL RECKLESS DRIVING OFFENSE';
        complianceText.textContent = 'CRITICAL RECKLESS DRIVING VIOLATION DETECTED';

        signalStateBadge.textContent = 'COLLISION IMPACT';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
        hudNarrative.textContent = 'Catastrophic Error: Driver retaliates by brake-checking the tailgater. At 65 MPH with under 15 ft buffer, physics guarantees an unavoidable rear-end impact, vehicle spin-out, and highway pileup.';
      }}

      // =========================================================================
      // MODE 3: COMPETITIVE SPEED DUEL & BLOCKING HAZARD
      // =========================================================================
      else if (currentMode === 3) {{
        tailgateBracketGroup.setAttribute('opacity', '0.0');
        cushionBracketGroup.setAttribute('opacity', '0.0');
        brakeCheckHazardGroup.setAttribute('opacity', '0.0');
        duelHazardGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';
        blinkerRight.style.opacity = '0.0';
        brakeLights.style.opacity = '0.0';

        hazardBannerTitle.textContent = 'HAZARD: COMPETITIVE SPEED DUEL';
        hazardBannerBody.innerHTML = '<strong>DEADLY ROAD RAGE ESCALATION</strong><br>Accelerating to block passing vehicles transforms traffic into a high-speed duel, risking multi-car pileups and felony charges.';

        // Both vehicles side-by-side at high speed (85 MPH)
        const p = Math.min(1.0, t / 5.0);
        const egoX = 50.0 + p * 15.0; // 50% to 65% in Lane 2
        const egoY = getLane2Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
        tagVehEgo.textContent = 'EGO: ACCELERATES TO 85 MPH TO BLOCK PASS!';

        const blueX = egoX - 1.0; // side-by-side in Lane 3!
        const blueY = getLane3Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
        tagVehBlue.textContent = 'AGGRESSIVE: RACING SIDE-BY-SIDE IN LANE 3!';

        telemSpeed.textContent = '85 MPH (EXCESSIVE)';
        telemSpeed.className = 'font-bold text-red-500 mono text-right';
        telemBuffer.textContent = '0 LATERAL BUFFER';
        telemBuffer.className = 'font-bold text-red-500 mono text-right';
        telemDemeanor.textContent = 'COMPETITIVE / AGGRESSIVE';
        telemDemeanor.className = 'font-bold text-red-500 mono text-right';
        telemSignal.textContent = 'NONE';
        telemAggressor.textContent = 'HIGH SPEED BLOCKADE';
        telemLegal.textContent = 'RACING ON HIGHWAY (§ 545.420)';
        telemLegal.className = 'font-bold text-red-500 mono text-right';

        pillStatusText.textContent = 'CRITICAL ERROR: NEVER COMPETE OR ACCELERATE TO PREVENT ANOTHER VEHICLE FROM PASSING!';
        complianceText.textContent = 'ILLEGAL HIGHWAY RACING VIOLATION DETECTED';

        signalStateBadge.textContent = 'HIGHWAY DUEL';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500 text-black mono font-black';
        hudNarrative.textContent = 'Critical Error: Ego accelerates to match aggressor speed and block passing. Engaging in highway duels violates TTC § 545.420 (Racing on Highway) and can escalate to deadly physical violence.';
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L07_T08_aggressive_driving_avoidance.html"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 27 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_l07_t08()
