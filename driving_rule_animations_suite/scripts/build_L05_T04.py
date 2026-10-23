import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        ext = os.path.splitext(path)[1].lower()
        mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/texas_suburban_2lane_corridor.jpg'
car_red_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_yellow_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_yellow_ne.png'
car_blue_sw_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_sw_clean.png'

print("Encoding Lesson 13 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_ne_b64 = get_base64_img(car_red_ne_path)
car_yellow_ne_b64 = get_base64_img(car_yellow_ne_path)
car_blue_sw_b64 = get_base64_img(car_blue_sw_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T04: Passing Maneuvers — The 200-Foot Oncoming Return Clearance Rule</title>
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
      animation: dangerPulse 1.2s infinite ease-in-out;
    }}
    @keyframes dangerPulse {{
      0%, 100% {{ transform: scale(1); opacity: 0.9; }}
      50% {{ transform: scale(1.18); opacity: 0.4; }}
    }}
    input[type=range]::-webkit-slider-thumb {{
      height: 16px;
      width: 16px;
      border-radius: 9999px;
      background: #3B82F6;
      cursor: pointer;
      border: 2px solid #FFFFFF;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.8);
    }}
  </style>
</head>
<body class="flex flex-col h-screen w-screen overflow-hidden p-2 bg-[#0B0E14] text-gray-100">

  <!-- TOP HEADER / SCENARIO SELECTOR BAR -->
  <header class="flex items-center justify-between px-3 py-1.5 bg-[#121620] border border-[#212836] rounded-xl shadow-lg mb-1 z-20">
    <div class="flex items-center space-x-3">
      <div class="flex items-center space-x-2">
        <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">TDLR ADE-1317</span>
        <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">2.5D VECTOR ENGINE</span>
        <span class="text-xs font-bold text-gray-400 mono">LESSON 13</span>
      </div>
      <div class="h-4 w-px bg-gray-700"></div>
      <div>
        <h1 class="text-sm font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>L05-T04: Passing Maneuvers — The 200-Foot Oncoming Return Clearance Rule</span>
        </h1>
        <p class="text-[10px] text-gray-400 font-medium">Texas Transportation Code § 545.054 • § 545.053 • § 545.056</p>
      </div>
    </div>

    <!-- 3 Core Statutory Scenarios -->
    <div class="flex items-center space-x-2">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
        1: Lawful Pass (≥200 FT Clearance)
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
        2: 100-Ft Bridge / Choke Point Abort
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
        Hazard: Late Return Within 200 FT
      </button>

      <div class="h-4 w-px bg-gray-700 ml-1 mr-1"></div>
      <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-gray-300 font-medium">
        <input type="checkbox" id="auto-loop-toggle" checked class="rounded bg-gray-800 border-gray-700 text-blue-500 focus:ring-0">
        <span class="text-[11px] mono">Auto-Loop</span>
      </label>
    </div>
  </header>

  <!-- CANONICAL 4-STEP STEPPER BAR -->
  <nav class="grid grid-cols-4 gap-2 mb-1 z-20">
    <button data-step="1" class="step-btn px-2.5 py-1 rounded-lg border border-blue-500/40 bg-blue-950/30 text-left transition hover:border-blue-500">
      <div class="text-[9px] mono text-blue-400 font-bold uppercase tracking-wider">STEP 1</div>
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">Sight Distance &amp; Gap Scan</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">100-Ft Signal &amp; Pullout</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">Headlights in Mirror (Apex)</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Re-entry with ≥200 FT Buffer</div>
    </button>
  </nav>

  <!-- MAIN SIMULATION VIEWPORT -->
  <main class="relative flex-1 w-full bg-[#0E121A] rounded-xl border border-[#1E2634] overflow-hidden flex items-center justify-center shadow-inner min-h-0">
    
    <!-- 35° ARCHITECTURAL ISOMETRIC STAGE -->
    <div id="isometric-stage" class="relative overflow-hidden shadow-2xl rounded-lg" style="height: calc(100% - 16px); aspect-ratio: 1024 / 667; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: Suburban 2-Lane Highway Base -->
      <img src="{road_b64}" alt="Texas 2-Lane Highway" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none z-0" />

      <!-- LAYER 1: SVG OVERLAYS, SIGHTLINE CORRIDORS & BUFFER BRACKETS -->
      <svg id="stage-svg-overlay" class="absolute inset-0 w-full h-full z-10 pointer-events-none" viewBox="0 0 1024 667">
        <defs>
          <marker id="arrow-green" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 6 3, 0 6" fill="#10B981" />
          </marker>
          <marker id="arrow-red" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 6 3, 0 6" fill="#EF4444" />
          </marker>
        </defs>

        <!-- Dynamic Oncoming Clearance Measurement Bracket -->
        <g id="clearance-bracket-group" opacity="0.0">
          <line id="bracket-line" x1="680" y1="285" x2="800" y2="165" stroke="#10B981" stroke-width="2.5" stroke-dasharray="4,4" />
          <g id="bracket-badge" transform="translate(740, 225)">
            <rect x="-95" y="-10" width="190" height="20" rx="4" fill="#0B132B" fill-opacity="0.95" stroke="#10B981" stroke-width="1.2" />
            <text id="bracket-text" x="0" y="4" fill="#34D399" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="900" text-anchor="middle">← 250 FT BUFFER (LAW: ≥ 200 FT) →</text>
          </g>
        </g>

        <!-- Mode 2: Bridge 100-Ft Prohibition Zone Regulatory Sign (Placed on NW Shoulder) -->
        <g id="bridge-zone-group" opacity="0.0" transform="translate(470, 150)">
          <rect x="-115" y="-12" width="230" height="24" rx="4" fill="#2B1505" fill-opacity="0.95" stroke="#F59E0B" stroke-width="1.2" />
          <text x="0" y="4" fill="#FBBF24" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">⚠ 100-FT BRIDGE PROHIBITION ZONE (TTC § 545.056)</text>
        </g>

        <!-- HAZARD DEMO: CRITICAL CONFLICT ZONE -->
        <g id="hazard-conflict-zone" opacity="0.0">
          <circle id="hazard-circle" cx="660" cy="186" r="38" fill="#EF4444" fill-opacity="0.3" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="5,4" class="pulse-danger" />
          <polygon id="hazard-star" points="0,-15 5,-5 16,-4 8,4 11,15 0,8 -11,15 -8,4 -16,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" transform="translate(660, 186)" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- LEAD SLOWER VEHICLE (Yellow Sedan, Lane 1 heading NE at 35 MPH) -->
      <div id="veh-lead-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 40.0%; top: 66.6%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Lead Slower Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>
        <div id="tag-veh-lead" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          LEAD VEHICLE: 35 MPH (LANE 1)
        </div>
      </div>

      <!-- EGO PASSING VEHICLE (Red Sedan, initiating pass into Lane 2 at 50 MPH) -->
      <div id="veh-ego-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 18.0%; top: 88.8%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_ne_b64}" alt="Ego Passing Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Turn Signal Blinkers -->
          <div id="blinker-left-front" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 24%; left: 74%;"></div>
          <div id="blinker-left-rear" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 18%; left: 24%;"></div>
          <div id="blinker-right-front" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="bottom: 24%; left: 74%;"></div>
          <div id="blinker-right-rear" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="bottom: 18%; left: 24%;"></div>
        </div>

        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: SCANNING SIGHTLINE
        </div>
      </div>

      <!-- ONCOMING VEHICLE (Blue Sedan, traveling SW in Lane 2 at 40 MPH) -->
      <div id="veh-oncoming-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 92.0%; top: 2.0%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_sw_b64}" alt="Oncoming Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>
        <div id="tag-veh-oncoming" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          ONCOMING (LANE 2)
        </div>
      </div>

      <!-- LAYER 3: TOP STATUS NOTIFICATION PILL (Cleanly partitioned between Card and Oncoming Lane) -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 8px; left: 286px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TTC § 545.054: COMPLETE PASS &amp; RETURN BEFORE 200 FT OF ONCOMING</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-2 right-2 z-25 px-2.5 py-1 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[9.5px] font-bold shadow-lg tracking-wider flex items-center space-x-1.5 pointer-events-none">
        <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TTC § 545.054 200-FT CLEARANCE VERIFIED</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER (Bottom Center Compact) -->
      <div id="hazard-banner" class="absolute bottom-3 left-1/2 -translate-x-1/2 z-30 px-4 py-1.5 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300 max-w-[420px]" style="opacity: 0.0;">
        <div class="text-[10.5px] font-black tracking-widest text-red-400 flex items-center justify-center space-x-1">
          <span>⚠</span>
          <span>CRITICAL STATUTORY VIOLATION</span>
          <span>⚠</span>
        </div>
        <div class="text-[10px] font-bold text-white">FAILED TO RETURN BEFORE 200 FT OF ONCOMING VEHICLE</div>
        <div class="text-[9px] text-red-300 leading-tight">
          TTC § 545.054: Remaining in opposing lane within 200 ft of approaching vehicle forces emergency evasive swerve!
        </div>
      </div>

      <!-- LAYER 4: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
      <div id="telemetry-hud-card" class="absolute top-2 left-2 z-30 max-w-[270px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-2 space-y-1 shadow-xl pointer-events-none">
        <div class="flex items-center justify-between border-b border-[#222B38] pb-1">
          <span class="text-[9.5px] font-bold text-gray-400 mono uppercase tracking-wider">Passing Clearance</span>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">
            CLEARANCE: ≥200 FT (SAFE)
          </span>
        </div>

        <div class="space-y-0.5 text-[11px] mono">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Oncoming Buffer:</span>
            <span id="telem-buffer" class="text-emerald-400 font-bold">250 FT</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Ego Speed:</span>
            <span id="telem-ego-spd" class="text-emerald-400 font-bold">50 MPH</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Lead Vehicle:</span>
            <span id="telem-lead-spd" class="text-amber-400 font-bold">35 MPH (STEADY)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Mandate:</span>
            <span id="telem-statute" class="text-emerald-300 font-bold">TTC § 545.054</span>
          </div>
        </div>

        <div class="pt-1 border-t border-[#1F2633] text-[9.5px] text-gray-300 leading-snug font-sans" id="hud-narrative">
          TTC § 545.054 requires returning to the right lane before coming within 200 feet of oncoming vehicles. Pass completed with &ge;200-ft safe buffer.
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM SCRUBBABLE TIMELINE & PLAYBACK CONTROLS -->
  <footer class="bg-[#121620] border border-[#212836] rounded-xl px-4 py-2 shadow-lg flex flex-col gap-1.5 mt-1 z-30">
    <div class="flex items-center space-x-3">
      <button id="play-pause-btn" class="w-7 h-7 rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center font-bold shadow transition">
        <svg id="play-icon" class="w-3.5 h-3.5 fill-current hidden" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        <svg id="pause-icon" class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
      </button>

      <button id="reset-btn" class="w-7 h-7 rounded-lg bg-[#1C2331] hover:bg-[#252F42] text-gray-300 flex items-center justify-center transition border border-[#2B3548]">
        <svg class="w-3.5 h-3.5 stroke-current fill-none" viewBox="0 0 24 24" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
      </button>

      <span id="time-display" class="mono text-xs text-blue-400 font-bold w-12">0.00s</span>

      <div class="flex-1 relative flex items-center">
        <input type="range" id="timeline-slider" min="0" max="8.0" step="0.01" value="0" class="w-full h-1.5 bg-[#212836] rounded-lg appearance-none cursor-pointer accent-blue-500" />
      </div>

      <span class="mono text-xs text-gray-400">8.00s</span>

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
        <span id="keyframe-1-text">0.8s Scan &amp; Verification</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-2-text">2.5s Acceleration in Lane 2</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-3-text">4.5s Apex (Headlights Visible)</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="keyframe-4-text">6.2s Return (&ge;200 FT Buffer)</span>
      </span>
      <span class="text-blue-400 font-semibold" id="legend-statute">TTC § 545.054 200-Ft Rule</span>
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

    // DOM Elements
    const playPauseBtn = document.getElementById('play-pause-btn');
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');
    const resetBtn = document.getElementById('reset-btn');
    const timeDisplay = document.getElementById('time-display');
    const timelineSlider = document.getElementById('timeline-slider');
    const autoLoopToggle = document.getElementById('auto-loop-toggle');

    const vehEgo = document.getElementById('veh-ego-container');
    const vehLead = document.getElementById('veh-lead-container');
    const vehOncoming = document.getElementById('veh-oncoming-container');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehLead = document.getElementById('tag-veh-lead');
    const tagVehOncoming = document.getElementById('tag-veh-oncoming');

    const blinkerLF = document.getElementById('blinker-left-front');
    const blinkerLR = document.getElementById('blinker-left-rear');
    const blinkerRF = document.getElementById('blinker-right-front');
    const blinkerRR = document.getElementById('blinker-right-rear');

    const clearanceBracketGroup = document.getElementById('clearance-bracket-group');
    const bracketLine = document.getElementById('bracket-line');
    const bracketBadge = document.getElementById('bracket-badge');
    const bracketText = document.getElementById('bracket-text');
    const bridgeZoneGroup = document.getElementById('bridge-zone-group');
    const hazardConflictZone = document.getElementById('hazard-conflict-zone');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemBuffer = document.getElementById('telem-buffer');
    const telemEgoSpd = document.getElementById('telem-ego-spd');
    const telemLeadSpd = document.getElementById('telem-lead-spd');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceText = document.getElementById('compliance-text');
    const complianceBadge = document.getElementById('compliance-badge');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Roadway Lane Math (Texas Suburban 2-Lane Corridor)
    // Lane 1 (South-East / Lower Lane heading NE):
    function getLane1Y(x) {{
      return 56.62 - 1.005 * (x - 50.0);
    }}
    // Lane 2 (North-West / Upper Passing Lane):
    function getLane2Y(x) {{
      return 42.56 - 1.005 * (x - 50.0);
    }}
    function smoothCos(p) {{
      return 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, p)));
    }}

    // ===============================================================
    // MODE 1: LAWFUL PASS WITH >= 200 FT ONCOMING CLEARANCE
    // ===============================================================
    function updateMode1(t) {{
      bridgeZoneGroup.setAttribute('opacity', '0.0');
      hazardConflictZone.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';

      // Lead Slower Vehicle (Yellow Sedan) in Lane 1 at 35 MPH
      // Steady progress from X = 40% to X = 60%
      const leadX = 40.0 + (t / 8.0) * 20.0;
      const leadY = getLane1Y(leadX);
      vehLead.style.left = `${{leadX}}%`;
      vehLead.style.top = `${{leadY}}%`;
      tagVehLead.textContent = 'LEAD VEHICLE: 35 MPH (LANE 1)';
      tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';

      // Oncoming Vehicle (Blue Sedan) in Lane 2 traveling SW at 35 MPH
      // Starts at X = 92% and moves to X = 76%
      const oncX = 92.0 - (t / 8.0) * 16.0;
      const oncY = getLane2Y(oncX);
      vehOncoming.style.left = `${{oncX}}%`;
      vehOncoming.style.top = `${{oncY}}%`;
      tagVehOncoming.textContent = 'ONCOMING (LANE 2)';
      tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      // Ego Passing Vehicle
      let egoX = 18.0, egoY = getLane1Y(18.0), egoSpeed = 35;
      let leftBlink = false, rightBlink = false;

      if (t < 1.2) {{
        // Stage 1: Following behind in Lane 1, scanning sightline
        const p = t / 1.2;
        egoX = 18.0 + p * (24.0 - 18.0);
        egoY = getLane1Y(egoX);
        egoSpeed = 35;
        tagVehEgo.textContent = 'EGO: SIGHTLINE VERIFIED';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else if (t < 2.2) {{
        // Stage 2: Signal 100 ft & pullout into Lane 2 (well behind lead vehicle)
        const p = (t - 1.2) / 1.0;
        const ease = smoothCos(p);
        egoX = 24.0 + p * (30.0 - 24.0);
        egoY = (1 - ease) * getLane1Y(egoX) + ease * getLane2Y(egoX);
        egoSpeed = Math.round(35 + p * 15);
        leftBlink = true;
        tagVehEgo.textContent = `EGO: 100-FT SIGNAL & PULLOUT (${{egoSpeed}} MPH)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
      }} else if (t < 4.2) {{
        // Stage 3: Brisk acceleration & passing in Lane 2 at 50 MPH
        const p = (t - 2.2) / 2.0;
        egoX = 30.0 + p * (58.0 - 30.0);
        egoY = getLane2Y(egoX);
        egoSpeed = 50;
        tagVehEgo.textContent = (t < 3.4) ? 'EGO: PASSING IN OPPOSING LANE (50 MPH)' : 'APEX: HEADLIGHTS IN REARVIEW MIRROR';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
      }} else if (t < 5.2) {{
        // Stage 4: Returning to Lane 1 with safe cushion
        const p = (t - 4.2) / 1.0;
        const ease = smoothCos(p);
        egoX = 58.0 + p * (67.0 - 58.0);
        egoY = (1 - ease) * getLane2Y(egoX) + ease * getLane1Y(egoX);
        egoSpeed = Math.round(50 - p * 5);
        rightBlink = true;
        tagVehEgo.textContent = 'EGO: RETURNING TO LANE 1 (≥200 FT BUFFER)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else {{
        // Stage 5: Pass Completed, safely cruising in Lane 1
        const p = (t - 5.2) / (8.0 - 5.2);
        egoX = 67.0 + p * (74.0 - 67.0);
        egoY = getLane1Y(egoX);
        egoSpeed = 45;
        tagVehEgo.textContent = 'EGO: PASS COMPLETED (TTC § 545.054 VERIFIED)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }}

      // Calculate Oncoming Buffer (Feet)
      let bufferFt = Math.round((oncX - egoX) * 18.5);
      if (t >= 5.2) bufferFt = Math.max(220, bufferFt);

      // Dynamic Clearance Bracket (Displayed during return phase)
      if (t >= 5.0 && t <= 7.0) {{
        clearanceBracketGroup.setAttribute('opacity', '1.0');
        tagVehOncoming.style.opacity = '0.0';
        const x1 = egoX * 10.24; const y1 = egoY * 6.67;
        const x2 = oncX * 10.24; const y2 = oncY * 6.67;
        bracketLine.setAttribute('x1', x1); bracketLine.setAttribute('y1', y1);
        bracketLine.setAttribute('x2', x2); bracketLine.setAttribute('y2', y2);
        const midX = (x1 + x2) / 2; const midY = (y1 + y2) / 2 - 30;
        bracketBadge.setAttribute('transform', `translate(${{midX}}, ${{midY}})`);
        bracketText.textContent = `← CLEARANCE: ${{bufferFt}} FT (LAW: ≥ 200 FT) →`;
      }} else {{
        clearanceBracketGroup.setAttribute('opacity', '0.0');
        tagVehOncoming.style.opacity = '1.0';
      }}

      // Blinkers Flash
      const flash = (Math.sin(t * 14) > 0);
      blinkerLF.style.opacity = (leftBlink && flash) ? '1.0' : '0.0';
      blinkerLR.style.opacity = (leftBlink && flash) ? '1.0' : '0.0';
      blinkerRF.style.opacity = (rightBlink && flash) ? '1.0' : '0.0';
      blinkerRR.style.opacity = (rightBlink && flash) ? '1.0' : '0.0';

      vehEgo.style.left = `${{egoX}}%`; vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0'; vehLead.style.opacity = '1.0'; vehOncoming.style.opacity = '1.0';
      tagVehEgo.style.opacity = '1.0'; tagVehLead.style.opacity = '1.0';

      telemBuffer.textContent = `${{bufferFt}} FT`;
      telemBuffer.className = (bufferFt >= 200) ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold';
      telemEgoSpd.textContent = `${{egoSpeed}} MPH`;
      telemLeadSpd.textContent = '35 MPH (STEADY)';

      signalStateBadge.innerHTML = 'CLEARANCE: ≥200 FT (SAFE)';
      signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TTC § 545.054: COMPLETE PASS & RETURN BEFORE 200 FT OF ONCOMING';
      hudNarrative.textContent = 'Texas Transportation Code § 545.054 requires returning to the right lane before coming within 200 feet of oncoming vehicles. Pass completed with &ge;200-ft safe buffer.';
      complianceText.textContent = 'TTC § 545.054 200-FT CLEARANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 2: STATUTORY PROHIBITION ZONE (100-FT BRIDGE / CHOKE POINT)
    // ===============================================================
    function updateMode2(t) {{
      clearanceBracketGroup.setAttribute('opacity', '0.0');
      hazardConflictZone.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      bridgeZoneGroup.setAttribute('opacity', '1.0');
      complianceBadge.style.opacity = '1.0';

      // Lead vehicle cruises steadily in Lane 1
      const leadX = 38.0 + (t / 8.0) * 18.0;
      const leadY = getLane1Y(leadX);
      vehLead.style.left = `${{leadX}}%`; vehLead.style.top = `${{leadY}}%`;
      tagVehLead.textContent = 'LEAD VEHICLE: 35 MPH';
      tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';

      // Ego vehicle recognizes 100-ft bridge zone and ABORTS pass
      const egoX = 20.0 + (t / 8.0) * 18.0;
      const egoY = getLane1Y(egoX);
      const egoSpeed = 35;

      tagVehEgo.textContent = 'EGO: 100-FT BRIDGE DETECTED → ABORT PASS';
      tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';

      // Oncoming car passes in Lane 2
      const oncX = 90.0 - (t / 8.0) * 36.0;
      const oncY = getLane2Y(oncX);
      vehOncoming.style.left = `${{oncX}}%`; vehOncoming.style.top = `${{oncY}}%`;
      tagVehOncoming.textContent = 'ONCOMING (LANE 2)';
      tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      blinkerLF.style.opacity = '0.0'; blinkerLR.style.opacity = '0.0';
      blinkerRF.style.opacity = '0.0'; blinkerRR.style.opacity = '0.0';

      vehEgo.style.left = `${{egoX}}%`; vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0'; vehLead.style.opacity = '1.0'; vehOncoming.style.opacity = '1.0';
      tagVehEgo.style.opacity = '1.0'; tagVehLead.style.opacity = '1.0';

      signalStateBadge.innerHTML = 'ZONE: NO-PASSING (BRIDGE)';
      signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';

      telemBuffer.textContent = 'N/A (LANE 1 HELD)';
      telemBuffer.className = 'text-gray-400 font-bold';
      telemEgoSpd.textContent = '35 MPH (BUFFER)';
      telemLeadSpd.textContent = '35 MPH (LANE 1)';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TTC § 545.056: NO PASSING WITHIN 100 FT OF BRIDGE / VIADUCT';
      hudNarrative.textContent = 'Texas Transportation Code § 545.056 strictly prohibits passing to the left within 100 feet of a bridge, viaduct, or tunnel. Ego vehicle complies by remaining in Lane 1.';
      complianceText.textContent = 'TTC § 545.056 PROHIBITION COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (LATE RETURN VIOLATING 200-FT RULE)
    // ===============================================================
    function updateMode3(t) {{
      clearanceBracketGroup.setAttribute('opacity', '0.0');
      bridgeZoneGroup.setAttribute('opacity', '0.0');
      complianceBadge.style.opacity = '0.0';

      // Lead car in Lane 1
      const leadX = 36.0 + (t / 8.0) * 16.0;
      const leadY = getLane1Y(leadX);
      vehLead.style.left = `${{leadX}}%`; vehLead.style.top = `${{leadY}}%`;
      tagVehLead.textContent = 'LEAD VEHICLE: 35 MPH';
      tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';

      // Ego vehicle remains in Lane 2 too long, oncoming vehicle rushes SW!
      let egoX = 20.0, egoY = getLane1Y(20.0), egoSpeed = 48;
      if (t < 1.8) {{
        const p = t / 1.8;
        egoX = 20.0 + p * (34.0 - 20.0);
        egoY = (1 - p) * getLane1Y(egoX) + p * getLane2Y(egoX);
        tagVehEgo.textContent = 'EGO: RISKY PASS INITIATION';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-red-950/90 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
      }} else if (t <= 5.0) {{
        const p = (t - 1.8) / (5.0 - 1.8);
        egoX = 34.0 + p * (62.0 - 34.0);
        egoY = getLane2Y(egoX);
        tagVehEgo.textContent = 'EGO: DELAYED RETURN → HEAD-ON HAZARD!';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-red-950/90 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
      }} else {{
        egoX = 62.0; egoY = getLane2Y(62.0);
      }}

      // Oncoming car in Lane 2 approaches rapidly to X = 70%
      let oncX = 94.0 - (t / 5.0) * 24.0;
      if (t > 5.0) oncX = 70.0;
      let oncY = getLane2Y(oncX);
      vehOncoming.style.left = `${{oncX}}%`; vehOncoming.style.top = `${{oncY}}%`;
      tagVehOncoming.textContent = 'ONCOMING (EMERGENCY BRAKE!)';
      tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-red-950/90 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';

      vehEgo.style.left = `${{egoX}}%`; vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0'; vehLead.style.opacity = '1.0'; vehOncoming.style.opacity = '1.0';

      const hazardDistance = Math.max(0, Math.round((oncX - egoX) * 18.5));

      if (t >= 3.8 && t <= 7.0) {{
        tagVehEgo.style.opacity = '0.0';
        tagVehOncoming.style.opacity = '0.0';
        tagVehLead.style.opacity = '0.0'; // clean view without background label clash
        const midX = ((egoX + oncX) / 2) * 10.24;
        const midY = ((egoY + oncY) / 2) * 6.67;
        document.getElementById('hazard-circle').setAttribute('cx', midX);
        document.getElementById('hazard-circle').setAttribute('cy', midY);
        document.getElementById('hazard-star').setAttribute('transform', `translate(${{midX}}, ${{midY}})`);
        hazardConflictZone.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';

        signalStateBadge.innerHTML = 'VIOLATION: BUFFER < 200 FT';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        telemBuffer.textContent = `${{hazardDistance}} FT (CRITICAL VIOLATION)`;
        telemBuffer.className = 'text-red-500 font-black animate-pulse';
        telemEgoSpd.textContent = 'EMERGENCY SWERVE';
        telemEgoSpd.className = 'text-red-400 font-bold';

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ CRITICAL HAZARD: RETURNED WITHIN 200 FT OF ONCOMING TRAFFIC ✕';
        hudNarrative.textContent = 'CRITICAL HAZARD: Failure to return to Lane 1 before coming within 200 feet of an oncoming vehicle violates TTC § 545.054 and forces head-on evasive action!';
        complianceText.textContent = 'CRITICAL VIOLATION: RETURNED WITHIN 200 FT OF ONCOMING TRAFFIC';
      }} else {{
        tagVehEgo.style.opacity = '1.0';
        tagVehOncoming.style.opacity = '1.0';
        tagVehLead.style.opacity = '1.0';
        hazardConflictZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'WARNING: INSUFFICIENT PASSING GAP BEFORE ONCOMING TRAFFIC';
      }}
    }}

    // ===============================================================
    // MAIN UPDATE DISPATCHER
    // ===============================================================
    function updateSimulation(t) {{
      timeDisplay.textContent = t.toFixed(2) + 's';
      timelineSlider.value = t;

      if (currentMode === 1) updateMode1(t);
      else if (currentMode === 2) updateMode2(t);
      else if (currentMode === 3) updateMode3(t);

      // Stepper Active Indicator Sync
      stepBtns.forEach(btn => {{
        const stepNum = parseInt(btn.dataset.step);
        let active = false;
        if (currentMode === 1) {{
          if (stepNum === 1 && t < 1.2) active = true;
          else if (stepNum === 2 && t >= 1.2 && t < 3.2) active = true;
          else if (stepNum === 3 && t >= 3.2 && t < 5.2) active = true;
          else if (stepNum === 4 && t >= 5.2) active = true;
        }} else if (currentMode === 2) {{
          if (stepNum === 1 && t < 2.0) active = true;
          else if (stepNum === 2 && t >= 2.0 && t < 4.0) active = true;
          else if (stepNum === 3 && t >= 4.0 && t < 6.0) active = true;
          else if (stepNum === 4 && t >= 6.0) active = true;
        }} else if (currentMode === 3) {{
          if (stepNum === 1 && t < 1.8) active = true;
          else if (stepNum === 2 && t >= 1.8 && t < 3.8) active = true;
          else if (stepNum === 3 && t >= 3.8 && t < 5.8) active = true;
          else if (stepNum === 4 && t >= 5.8) active = true;
        }}

        if (active) {{
          btn.className = 'step-btn px-2.5 py-1 rounded-lg border border-blue-500/60 bg-blue-950/40 text-left transition shadow-md shadow-blue-900/30';
          btn.querySelector('.mono').className = 'text-[9px] mono text-blue-400 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-white truncate';
        }} else {{
          btn.className = 'step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600';
          btn.querySelector('.mono').className = 'text-[9px] mono text-gray-500 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-gray-300 truncate';
        }}
      }});
    }}

    // Animation Loop
    function animate(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += dt * playbackSpeed;
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

      requestAnimationFrame(animate);
    }}

    // Step labels per mode
    const stepLabels = {{
      1: [
        'Sight Distance & Gap Scan',
        '100-Ft Signal & Pullout',
        'Headlights in Mirror (Apex)',
        'Re-entry with ≥200 FT Buffer'
      ],
      2: [
        '100-Ft Bridge Approach',
        'Prohibition Zone Detected',
        'Abort Pass & Lane 1 Cushion',
        'TTC § 545.056 Compliance'
      ],
      3: [
        'Risky Overtake Initiation',
        'Oncoming Distance Shrinking',
        'Breach of 200-Ft Buffer',
        'Emergency Evasive Swerve'
      ]
    }};

    // Mode Switching
    function setMode(mode) {{
      currentMode = mode;
      currentTime = 0.0;
      isPlaying = true;
      playIcon.classList.add('hidden');
      pauseIcon.classList.remove('hidden');

      modeBtns.forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40';
          else if (m === 2) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/40 bg-red-600 text-white shadow-md shadow-red-900/40';
        }} else {{
          btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white';
        }}
      }});

      // Update Stepper labels
      for (let i = 1; i <= 4; i++) {{
        document.getElementById(`step-label-${{i}}`).textContent = stepLabels[mode][i - 1];
      }}

      updateSimulation(0.0);
    }}

    // Event Listeners
    playPauseBtn.addEventListener('click', () => {{
      isPlaying = !isPlaying;
      playIcon.classList.toggle('hidden', isPlaying);
      pauseIcon.classList.toggle('hidden', !isPlaying);
      lastTimestamp = null;
    }});

    resetBtn.addEventListener('click', () => {{
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    autoLoopToggle.addEventListener('change', (e) => {{
      autoLoop = e.target.checked;
    }});

    stepBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        const s = parseInt(btn.dataset.step);
        let targetTime = 0.8;
        if (s === 1) targetTime = 0.8;
        else if (s === 2) targetTime = 2.5;
        else if (s === 3) targetTime = 4.5;
        else if (s === 4) targetTime = 6.2;
        currentTime = targetTime;
        updateSimulation(currentTime);
      }});
    }});

    speedBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        playbackSpeed = parseFloat(btn.dataset.speed);
        speedBtns.forEach(b => {{
          if (b === btn) {{
            b.className = 'speed-btn px-2 py-0.5 rounded bg-blue-600 text-white font-bold';
          }} else {{
            b.className = 'speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white';
          }}
        }});
      }});
    }});

    modeBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        setMode(parseInt(btn.dataset.mode));
      }});
    }});

    // Initialize
    updateSimulation(0.0);
    requestAnimationFrame(animate);
  </script>
</body>
</html>'''

out_path = 'driving_rule_animations_suite/simulations/L05_T04_passing_turning_parking.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 13 simulation rebuilt successfully at: {out_path}")
