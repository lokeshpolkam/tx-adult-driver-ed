import os
import base64

def build_l08_t04():
    # Asset Paths
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    car_blue_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_blue_clean_ne.png"

    print("Encoding Lesson 30 assets to base64...")
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
  <title>L08-T04: Distractions That Affect Driving &amp; The 5-Second Blind Horizon</title>
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
    @keyframes pulse-scan {{
      0%, 100% {{ opacity: 0.18; transform: scaleY(0.96); }}
      50% {{ opacity: 0.38; transform: scaleY(1.04); }}
    }}
    .scan-cone {{
      animation: pulse-scan 2.0s infinite ease-in-out;
      transform-origin: 460px 480px;
    }}
    @keyframes pulse-blind {{
      0%, 100% {{ opacity: 0.35; }}
      50% {{ opacity: 0.85; }}
    }}
    .blind-pulse {{
      animation: pulse-blind 1.0s infinite ease-in-out;
    }}
    @keyframes pulse-danger {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.95); }}
      50% {{ opacity: 0.9; transform: scale(1.05); }}
    }}
    .danger-pulse {{
      animation: pulse-danger 0.9s infinite ease-in-out;
    }}
    @keyframes phone-vibe {{
      0%, 100% {{ transform: rotate(0deg); }}
      20% {{ transform: rotate(-3deg); }}
      40% {{ transform: rotate(3deg); }}
      60% {{ transform: rotate(-2deg); }}
      80% {{ transform: rotate(2deg); }}
    }}
    .phone-vibrating {{
      animation: phone-vibe 0.6s infinite ease-in-out;
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
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 30</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L08-T04: Distractions That Affect Driving
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          5-Second Texting Blind Horizon (Traversing Football Field Blind) &bull; TTC &sect; 545.4251 &amp; &sect; 545.425
        </p>
      </div>

      <!-- SCENARIO MODE SELECTOR -->
      <div class="flex items-center gap-2 bg-[#0B0E14] p-1.5 rounded-xl border border-[#232C3D] flex-wrap">
        <button id="mode-1" data-mode="1" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40">
          1: The 5-Sec Blind Horizon
        </button>
        <button id="mode-2" data-mode="2" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/50">
          Hazard: Distracted Drifter
        </button>
        <button id="mode-3" data-mode="3" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/50">
          Hazard: School Zone Wireless Ban
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
        <p class="text-xs font-bold text-white mt-1 leading-snug">Eyes Divert to Device</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition" data-step="2">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Halfway Blind Traversal</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition" data-step="3">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Eyes Up: 403 FT Blind</p>
      </button>

      <button class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition" data-step="4">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p class="text-xs font-bold text-gray-400 mt-1 leading-snug">Focus Mode &amp; Law Compliance</p>
      </button>
    </div>

    <!-- MAIN SIMULATION VIEWPORT (16:9) -->
    <div class="relative w-full aspect-[16/9] bg-[#0E131F] rounded-2xl border border-[#232C3D] overflow-hidden shadow-2xl">
      
      <!-- Diorama Canvas Background Image -->
      <img src="{bg_b64}" alt="Texas Highway Corridor" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- VECTOR OVERLAY CANVAS (SVG) -->
      <svg id="vector-canvas" class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1000 562.5" preserveAspectRatio="none">
        <defs>
          <!-- Green Defensive Scan Horizon Cone Gradient -->
          <linearGradient id="scanGrad" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.38" />
            <stop offset="60%" stop-color="#065F46" stop-opacity="0.16" />
            <stop offset="100%" stop-color="#047857" stop-opacity="0.0" />
          </linearGradient>

          <!-- Red Cognitive Blindness Cone Gradient -->
          <linearGradient id="blindGrad" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#EF4444" stop-opacity="0.65" />
            <stop offset="60%" stop-color="#B91C1C" stop-opacity="0.30" />
            <stop offset="100%" stop-color="#991B1B" stop-opacity="0.0" />
          </linearGradient>
        </defs>

        <!-- Dynamic Vision / Scanning Cones -->
        <polygon id="svg-scan-cone" points="400,280 680,80 780,180" fill="url(#scanGrad)" class="scan-cone" style="display: none;" />
        <polygon id="svg-blind-cone" points="400,280 530,170 580,220" fill="url(#blindGrad)" class="blind-pulse" style="display: none;" />

        <!-- Football Field Blind Traversal Ribbon (Mode 1) -->
        <g id="svg-football-ribbon" style="display: none;">
          <!-- Traversed Path Ribbon on Lane 2 -->
          <polygon id="ribbon-polygon" points="360,335 480,230 500,245 380,350" fill="#EF4444" fill-opacity="0.28" stroke="#F87171" stroke-width="2" stroke-dasharray="6,4" />
          <!-- Benchmark Yardage Markers -->
          <text id="marker-0ft" x="350" y="360" fill="#EF4444" font-size="10" font-weight="bold" font-family="'JetBrains Mono', monospace">0 FT [TEXT GLANCE START]</text>
          <text id="marker-mid" x="430" y="295" fill="#FBBF24" font-size="10" font-weight="bold" font-family="'JetBrains Mono', monospace">200 FT [1/2 FOOTBALL FIELD]</text>
          <text id="marker-goal" x="510" y="235" fill="#EF4444" font-size="10" font-weight="bold" font-family="'JetBrains Mono', monospace">403 FT [1.34 FOOTBALL FIELDS BLIND!]</text>
        </g>

        <!-- Mode 2: Unsafe Drifting Lane Trajectory Vector -->
        <g id="svg-drift-vector" style="display: none;">
          <path id="drift-path" d="M 520,330 Q 550,280 500,240" fill="none" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" />
          <polygon points="495,235 508,238 502,248" fill="#EF4444" />
          <text x="545" y="300" fill="#F87171" font-size="11" font-weight="bold" font-family="'JetBrains Mono', monospace">ERRATIC DRIFT VECTOR</text>
        </g>

        <!-- Mode 3: School Zone Crosswalk & 20 MPH Flasher Ground Markings -->
        <g id="svg-school-zone" style="display: none;">
          <line x1="560" y1="180" x2="680" y2="300" stroke="#FBBF24" stroke-width="8" stroke-dasharray="14,14" stroke-opacity="0.85" />
          <text x="590" y="200" fill="#FDE047" font-size="12" font-weight="800" font-family="'JetBrains Mono', monospace">SCHOOL ZONE &bull; 20 MPH &bull; NO WIRELESS</text>
        </g>

        <!-- Safe 360-degree Space Cushion Ring around Ego -->
        <ellipse id="svg-ego-bubble" cx="400" cy="300" rx="65" ry="32" fill="none" stroke="#10B981" stroke-width="2.5" stroke-dasharray="5,3" style="display: none;" />
      </svg>

      <!-- VEHICLE 1: EGO RED VEHICLE (Lane 2 / Center Lane) -->
      <div id="veh-ego" class="absolute transition-transform duration-75 pointer-events-none" style="left: 36%; top: 54%; transform: translate(-50%, -50%);">
        <div class="relative">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-24 md:w-28 drop-shadow-[0_8px_16px_rgba(0,0,0,0.85)]" />
          <!-- Ego Badge -->
          <div id="ego-tag" class="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500/50 text-[10px] font-extrabold text-red-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-ping"></span>
            <span id="ego-tag-text">EGO: 55 MPH &bull; LOOKING DOWN AT PHONE</span>
          </div>
        </div>
      </div>

      <!-- VEHICLE 2: LEAD VEHICLE / THREAT VEHICLE (Yellow Sedan) -->
      <div id="veh-yellow" class="absolute transition-transform duration-75 pointer-events-none" style="left: 64%; top: 28%; transform: translate(-50%, -50%);">
        <div class="relative">
          <img src="{car_yellow_b64}" alt="Yellow Vehicle" class="w-24 md:w-28 drop-shadow-[0_8px_16px_rgba(0,0,0,0.85)]" />
          <!-- Yellow Vehicle Badge -->
          <div id="yellow-tag" class="absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500/50 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5">
            <span id="yellow-dot" class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            <span id="yellow-tag-text">LEAD CAR: 50 MPH (LANE 2)</span>
          </div>
        </div>
      </div>

      <!-- VEHICLE 3: PASSING TRAFFIC (Blue Sedan - Available for optional traffic) -->
      <div id="veh-blue" class="absolute transition-transform duration-75 pointer-events-none" style="display: none; left: 74%; top: 6%; transform: translate(-50%, -50%);">
        <div class="relative">
          <img src="{car_blue_b64}" alt="Blue Vehicle" class="w-22 md:w-26 drop-shadow-[0_8px_16px_rgba(0,0,0,0.85)]" />
          <div id="blue-tag" class="absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-blue-500/50 text-[10px] font-extrabold text-blue-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
            <span id="blue-tag-text">PASSING FLOW</span>
          </div>
        </div>
      </div>

      <!-- IN-CABIN SMARTPHONE MOCKUP OVERLAY (Top-Right of Viewport) -->
      <div id="phone-widget" class="absolute top-4 right-4 z-20 w-44 md:w-48 p-2.5 rounded-xl bg-[#0F141D]/95 border border-red-500/60 shadow-2xl backdrop-blur-md">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
            <span class="text-[9px] font-black text-red-400 mono tracking-wider uppercase">IN-CABIN PHONE</span>
          </div>
          <span id="phone-timer" class="text-[10px] font-black text-white mono bg-red-950/80 px-1.5 py-0.5 rounded border border-red-600/40">4.8s SCREEN</span>
        </div>
        
        <div id="phone-body" class="mt-2 space-y-1.5">
          <div class="bg-gray-900/90 rounded-lg p-1.5 border border-gray-700">
            <div class="text-[9px] text-gray-400 flex justify-between">
              <span>Text Message</span>
              <span>Now</span>
            </div>
            <div id="phone-msg" class="text-[10px] font-bold text-white mt-0.5 leading-tight">
              "Hey, where are you guys at right now?"
            </div>
          </div>
          <div class="flex items-center justify-between text-[9px] mono pt-0.5">
            <span class="text-gray-400">TTC &sect; 545.4251:</span>
            <span id="phone-status" class="text-red-400 font-bold">ILLEGAL DEVICE USE</span>
          </div>
        </div>
      </div>

      <!-- FOOTBALL FIELD EQUIVALENCE OVERLAY BAR (Bottom Center) -->
      <div id="football-hud-bar" class="absolute bottom-2.5 left-1/2 -translate-x-1/2 z-20 w-80 md:w-96 px-3 py-1.5 rounded-xl bg-[#0D111A]/95 border border-amber-500/60 shadow-2xl backdrop-blur-md">
        <div class="flex items-center justify-between text-[9px] font-bold mono mb-1">
          <span class="text-amber-400 flex items-center gap-1">
            <span>🏈</span> <span>BLIND DISTANCE:</span>
          </span>
          <span id="football-stat-val" class="text-white bg-amber-950 px-1.5 py-0.5 rounded border border-amber-500/40 font-black">
            403 FT (1.34 FIELDS)
          </span>
        </div>
        <!-- Progress bar representing 0 to 450 ft (100 yd football field is 300 ft) -->
        <div class="w-full h-2 rounded-full bg-gray-900 border border-gray-700 overflow-hidden relative">
          <!-- 300 FT regulation field marker line at 66.6% -->
          <div class="absolute top-0 bottom-0 left-[66.6%] w-0.5 bg-yellow-400 z-10" title="1 Football Field (300 ft)"></div>
          <div id="football-fill" class="h-full bg-gradient-to-r from-amber-500 via-orange-500 to-red-600 transition-all duration-150" style="width: 89%;"></div>
        </div>
        <div class="flex justify-between text-[8px] mono text-gray-400 mt-0.5">
          <span>0 FT</span>
          <span class="text-yellow-400 font-bold">300 FT (1 FOOTBALL FIELD)</span>
          <span>450 FT</span>
        </div>
      </div>

      <!-- TOP CRITICAL HAZARD BANNER (Hidden in Mode 1, Active in Mode 2 & 3) -->
      <div id="hazard-banner" class="absolute top-4 left-1/2 -translate-x-1/2 z-20 px-4 py-2 rounded-xl bg-red-950/90 border border-red-500 text-center shadow-2xl backdrop-blur-md max-w-lg transition-all duration-300" style="display: none;">
        <div class="flex items-center justify-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span id="hazard-title" class="text-xs font-black text-red-200 uppercase tracking-wider mono">CRITICAL HAZARD: DISTRACTED LANE DRIFT</span>
        </div>
        <p id="hazard-desc" class="text-[11px] text-gray-300 mt-1 leading-snug">
          Driver on phone drifts across lane lines (TTC &sect; 545.060). Distraction impairs peripheral vision, causing failure to perceive lateral borders.
        </p>
      </div>

      <!-- TELEMETRY HUD (Top Left) -->
      <div id="telemetry-hud" class="absolute top-4 left-4 z-20 w-64 md:w-72 p-3 rounded-xl bg-[#0D111A]/95 border border-[#232C3D] shadow-2xl backdrop-blur-md flex flex-col gap-2">
        <div class="flex items-center justify-between border-b border-[#1E2638] pb-1.5">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            <span class="text-xs font-black text-white tracking-wider mono">DISTRACTION HUD</span>
          </div>
          <span id="hud-status-pill" class="text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono">BLIND TRAVERSAL</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1.5 text-xs mono">
          <div class="text-gray-400">Eyes-Off-Road:</div>
          <div id="hud-eyes-off" class="font-bold text-red-400 text-right">4.8s (CRITICAL)</div>

          <div class="text-gray-400">Blind Distance:</div>
          <div id="hud-blind-dist" class="font-bold text-amber-300 text-right">387 FT (TRAVERSED)</div>

          <div class="text-gray-400">Football Fields:</div>
          <div id="hud-fields" class="font-bold text-orange-400 text-right">1.29 FIELDS BLIND</div>

          <div class="text-gray-400">Crash Risk:</div>
          <div id="hud-crash-risk" class="font-bold text-red-500 text-right">23.0x SURGE</div>

          <div class="text-gray-400">Ego Speed:</div>
          <div id="hud-ego-speed" class="font-bold text-white text-right">55 MPH (80.7 FPS)</div>
        </div>

        <!-- Instructional Subtext -->
        <div id="hud-subtext" class="text-[11px] text-gray-300 border-t border-[#1E2638] pt-1.5 leading-relaxed">
          At 55 MPH, taking your eyes off the road for 5 seconds to send or read a text means hurtling over 400 feet&mdash;longer than a football field&mdash;completely blindfolded.
        </div>
      </div>

      <!-- TOP FLOATING CYCLE STATUS PILL (Mode 1 Only) -->
      <div id="cycle-pill" class="absolute top-4 left-1/2 -translate-x-1/2 z-10 px-3 py-1 rounded-full bg-[#0D111A]/90 border border-blue-500/30 text-[10px] font-bold text-blue-300 shadow-md mono flex items-center gap-2 backdrop-blur-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></span>
        <span id="cycle-pill-text">TEXAS WIRELESS LAW: 5-SEC TEXT = TRAVERSING ENTIRE FOOTBALL FIELD BLIND</span>
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
          <span class="text-gray-500">SPEED:</span> <span class="font-bold text-blue-400">55 MPH</span>
        </div>
        <div class="px-2.5 py-1 rounded-lg bg-[#18202F] border border-[#2B3850] text-gray-300">
          <span class="text-gray-500">STATUTE:</span> <span class="font-bold text-emerald-400">TTC &sect; 545.4251</span>
        </div>
      </div>
    </div>

    <!-- STATUTORY & LEGAL FOOTER SUMMARY -->
    <div class="p-4 rounded-2xl bg-[#121722] border border-[#232C3D] flex flex-col md:flex-row items-center justify-between text-xs text-gray-400 gap-2 shadow-lg">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span><strong>Texas Transportation Code &sect; 545.4251:</strong> Criminal misdemeanor to read, write, or send electronic messages while operating a motor vehicle.</span>
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

    const vehBlue = document.getElementById('veh-blue');
    const blueTag = document.getElementById('blue-tag');
    const blueTagText = document.getElementById('blue-tag-text');

    const svgScanCone = document.getElementById('svg-scan-cone');
    const svgBlindCone = document.getElementById('svg-blind-cone');
    const svgFootballRibbon = document.getElementById('svg-football-ribbon');
    const ribbonPolygon = document.getElementById('ribbon-polygon');
    const svgDriftVector = document.getElementById('svg-drift-vector');
    const svgSchoolZone = document.getElementById('svg-school-zone');
    const svgEgoBubble = document.getElementById('svg-ego-bubble');

    const phoneWidget = document.getElementById('phone-widget');
    const phoneTimer = document.getElementById('phone-timer');
    const phoneMsg = document.getElementById('phone-msg');
    const phoneStatus = document.getElementById('phone-status');

    const footballHudBar = document.getElementById('football-hud-bar');
    const footballStatVal = document.getElementById('football-stat-val');
    const footballFill = document.getElementById('football-fill');

    const hazardBanner = document.getElementById('hazard-banner');
    const hazardTitle = document.getElementById('hazard-title');
    const hazardDesc = document.getElementById('hazard-desc');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const hudEyesOff = document.getElementById('hud-eyes-off');
    const hudBlindDist = document.getElementById('hud-blind-dist');
    const hudFields = document.getElementById('hud-fields');
    const hudCrashRisk = document.getElementById('hud-crash-risk');
    const hudEgoSpeed = document.getElementById('hud-ego-speed');
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
        cards[0].querySelector('p').innerText = "Eyes Divert to Device";
        cards[1].querySelector('p').innerText = "Halfway Blind Traversal";
        cards[2].querySelector('p').innerText = "Eyes Up: 403 FT Blind";
        cards[3].querySelector('p').innerText = "Focus Mode & Law Compliance";
      }} else if (currentMode === 2) {{
        cards[0].querySelector('p').innerText = "Detecting Erratic Drifter";
        cards[1].querySelector('p').innerText = "Unsafe Lane Divider Drift";
        cards[2].querySelector('p').innerText = "Defensive Egress & Horn Alert";
        cards[3].querySelector('p').innerText = "Cushion Restored & Evaded";
      }} else if (currentMode === 3) {{
        cards[0].querySelector('p').innerText = "School Zone Approach";
        cards[1].querySelector('p').innerText = "Illegal Handheld Phone Use";
        cards[2].querySelector('p').innerText = "Unperceived Crossing Threat";
        cards[3].querySelector('p').innerText = "Strict Zero-Tolerance Rule";
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
    // MODE 1: THE 5-SECOND BLIND HORIZON
    // ==========================================
    function renderMode1(t, step) {{
      hazardBanner.style.display = 'none';
      svgDriftVector.style.display = 'none';
      svgSchoolZone.style.display = 'none';
      footballHudBar.style.display = 'block';
      phoneWidget.style.display = 'block';
      cyclePill.style.display = 'flex';
      hudStatusPill.style.opacity = '1.0';
      vehBlue.style.display = 'none'; // Uncluttered focused view in Mode 1

      if (step === 1) {{
        // Step 1: Glance Initiated (t = 0..3s)
        const prog = t / 3.0;
        const eyesTime = (prog * 1.5).toFixed(1);
        const distTraversed = Math.round(prog * 1.5 * 80.7);
        const fieldsBlind = (distTraversed / 300.0).toFixed(2);

        // Ego in Lane 2
        const egoX = 36.0 + prog * 2.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';
        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500/50 text-[10px] font-extrabold text-red-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "EGO: EYES DIVERTING DOWN TO PHONE (55 MPH)";

        // Lead yellow car ahead in Lane 2
        const yellX = 64.0 + prog * 1.0;
        const yellY = getLaneY(2, yellX);
        vehYellow.style.left = yellX + '%';
        vehYellow.style.top = yellY + '%';
        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500/50 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "LEAD CAR: 52 MPH (AHEAD IN LANE 2)";

        // Cones & Ribbon
        svgScanCone.style.display = 'none';
        svgBlindCone.style.display = 'block';
        svgBlindCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 90}},${{egoY * 5.625 - 60}} ${{egoX * 10 + 130}},${{egoY * 5.625 - 20}}`);
        svgFootballRibbon.style.display = 'none';
        svgEgoBubble.style.display = 'none';

        // Phone Widget
        phoneWidget.className = 'absolute top-4 right-4 z-20 w-44 md:w-48 p-2.5 rounded-xl bg-[#0F141D]/95 border border-red-500/60 shadow-2xl backdrop-blur-md phone-vibrating';
        phoneTimer.innerText = eyesTime + 's SCREEN';
        phoneTimer.className = 'text-[10px] font-black text-white mono bg-red-950/80 px-1.5 py-0.5 rounded border border-red-600/40';
        phoneStatus.innerText = "ILLEGAL DEVICE USE";
        phoneStatus.className = 'text-red-400 font-bold';

        // Football HUD
        const fillPct = Math.min(100, Math.round((distTraversed / 450.0) * 100));
        footballFill.style.width = fillPct + '%';
        footballStatVal.innerText = `${{distTraversed}} FT (${{fieldsBlind}} FIELDS)`;

        // Telemetry HUD
        hudStatusPill.innerText = "COGNITIVE BLINDNESS";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono";
        hudEyesOff.innerText = eyesTime + "s (DIVERTING)";
        hudEyesOff.className = "font-bold text-red-400 text-right";
        hudBlindDist.innerText = distTraversed + " FT (ACCUMULATING)";
        hudBlindDist.className = "font-bold text-amber-300 text-right";
        hudFields.innerText = fieldsBlind + " FIELDS";
        hudFields.className = "font-bold text-orange-400 text-right";
        hudCrashRisk.innerText = "4.0x ELEVATED";
        hudCrashRisk.className = "font-bold text-red-400 text-right";
        hudEgoSpeed.innerText = "55 MPH (80.7 FPS)";
        hudSubtext.innerHTML = "<strong>Step 1:</strong> Driver glances down at incoming mobile notification. Texas Transportation Code &sect; 545.4251 explicitly prohibits reading electronic messages in motion.";

      }} else if (step === 2) {{
        // Step 2: Halfway Traversal (t = 3..6s)
        const prog = (t - 3.0) / 3.0;
        const eyesTime = (1.5 + prog * 1.5).toFixed(1);
        const distTraversed = Math.round((1.5 + prog * 1.5) * 80.7);
        const fieldsBlind = (distTraversed / 300.0).toFixed(2);

        // Ego in Lane 2
        const egoX = 38.0 + prog * 4.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';
        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500/50 text-[10px] font-extrabold text-red-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "EGO: 2.5s BLIND • NO PERCEPTION OF HAZARD";

        // Lead yellow car slowing down abruptly in Lane 2
        const yellX = 65.0 - prog * 2.0;
        const yellY = getLaneY(2, yellX);
        vehYellow.style.left = yellX + '%';
        vehYellow.style.top = yellY + '%';
        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500/50 text-[10px] font-extrabold text-red-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "LEAD CAR: ABRUPT BRAKING FOR DEBRIS!";

        // Visual Blind Ribbon
        svgScanCone.style.display = 'none';
        svgBlindCone.style.display = 'block';
        svgBlindCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 70}},${{egoY * 5.625 - 50}} ${{egoX * 10 + 110}},${{egoY * 5.625 - 10}}`);
        svgFootballRibbon.style.display = 'block';
        ribbonPolygon.setAttribute('points', `360,335 ${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 20}},${{egoY * 5.625 + 15}} 380,350`);
        svgEgoBubble.style.display = 'none';

        // Phone Widget
        phoneWidget.className = 'absolute top-4 right-4 z-20 w-44 md:w-48 p-2.5 rounded-xl bg-[#0F141D]/95 border border-red-500/80 shadow-2xl backdrop-blur-md';
        phoneTimer.innerText = eyesTime + 's SCREEN';
        phoneStatus.innerText = "BLIND TRAVERSAL ACTIVE";

        // Football HUD
        const fillPct = Math.min(100, Math.round((distTraversed / 450.0) * 100));
        footballFill.style.width = fillPct + '%';
        footballStatVal.innerText = `${{distTraversed}} FT (${{fieldsBlind}} FIELDS)`;

        // Telemetry HUD
        hudStatusPill.innerText = "UNSEEN BRAKING HAZARD";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-400 border border-orange-500/30 mono";
        hudEyesOff.innerText = eyesTime + "s (CRITICAL)";
        hudEyesOff.className = "font-bold text-red-400 text-right";
        hudBlindDist.innerText = distTraversed + " FT BLIND";
        hudBlindDist.className = "font-bold text-amber-300 text-right";
        hudFields.innerText = fieldsBlind + " FIELDS";
        hudFields.className = "font-bold text-orange-400 text-right";
        hudCrashRisk.innerText = "12.5x SEVERE";
        hudCrashRisk.className = "font-bold text-red-500 text-right";
        hudEgoSpeed.innerText = "55 MPH (80.7 FPS)";
        hudSubtext.innerHTML = "<strong>Step 2:</strong> 2.5 seconds blind. Lead vehicle brakes hard for roadway debris. Driver's cognitive bandwidth is consumed by device; buffer distance drops by over 200 feet.";

      }} else if (step === 3) {{
        // Step 3: Eyes Return to Road (t = 6..9s)
        const prog = (t - 6.0) / 3.0;
        const eyesTime = (3.0 + prog * 2.0).toFixed(1);
        const distTraversed = Math.round(Math.min(5.0, 3.0 + prog * 2.0) * 80.7);
        const fieldsBlind = (distTraversed / 300.0).toFixed(2);

        // Ego in Lane 2 closing gap dangerously
        const egoX = 42.0 + prog * 4.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';
        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5 animate-bounce';
        egoTagText.innerText = "EGO: 403 FT TRAVERSED BLIND • PANIC BRAKE!";

        // Yellow car very close ahead in Lane 2
        const yellX = 64.0;
        const yellY = getLaneY(2, yellX);
        vehYellow.style.left = yellX + '%';
        vehYellow.style.top = yellY + '%';
        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "LEAD CAR: 25 FT AHEAD (CRITICAL NEAR-MISS!)";

        // Full Ribbon covering 403 feet
        svgScanCone.style.display = 'none';
        svgBlindCone.style.display = 'block';
        svgBlindCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 50}},${{egoY * 5.625 - 40}} ${{egoX * 10 + 80}},${{egoY * 5.625 - 10}}`);
        svgFootballRibbon.style.display = 'block';
        ribbonPolygon.setAttribute('points', `360,335 480,230 500,245 380,350`);
        svgEgoBubble.style.display = 'none';

        // Phone Widget showing full 5 seconds
        phoneWidget.className = 'absolute top-4 right-4 z-20 w-44 md:w-48 p-2.5 rounded-xl bg-[#0F141D]/95 border border-red-500 shadow-2xl backdrop-blur-md';
        phoneTimer.innerText = "5.0s SCREEN";
        phoneStatus.innerText = "403 FT TRAVERSED BLIND";

        // Football HUD showing 1.34 fields
        footballFill.style.width = '89%';
        footballStatVal.innerText = "403 FT (1.34 FIELDS BLIND)";

        // Telemetry HUD
        hudStatusPill.innerText = "PANIC NEAR-MISS";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white border border-red-400 mono";
        hudEyesOff.innerText = "5.0s (ELAPSED)";
        hudEyesOff.className = "font-bold text-red-500 text-right";
        hudBlindDist.innerText = "403 FT (FULL FIELD+)";
        hudBlindDist.className = "font-bold text-red-400 text-right";
        hudFields.innerText = "1.34 FOOTBALL FIELDS";
        hudFields.className = "font-bold text-red-400 text-right";
        hudCrashRisk.innerText = "23.0x PEAK RISK";
        hudCrashRisk.className = "font-bold text-red-500 text-right";
        hudEgoSpeed.innerText = "28 MPH (HARD DECEL)";
        hudSubtext.innerHTML = "<strong>Step 3:</strong> At 5 seconds, over 400 feet were traveled blind. Driver discovers lead vehicle mere feet ahead, forcing panic braking and near fatal pileup.";

      }} else if (step === 4) {{
        // Step 4: Focus Mode & Law Compliance (t = 9..12s)
        const prog = (t - 9.0) / 3.0;

        // Ego in Lane 2 at safe trailing distance
        const egoX = 40.0;
        const egoY = getLaneY(2, egoX);
        vehEgo.style.left = egoX + '%';
        vehEgo.style.top = egoY + '%';
        egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        egoTagText.innerText = "EGO: 100% FOCUS ON ROAD • PHONE STOWED";

        // Lead yellow car at comfortable 4-second distance
        const yellX = 66.0;
        const yellY = getLaneY(2, yellX);
        vehYellow.style.left = yellX + '%';
        vehYellow.style.top = yellY + '%';
        yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-emerald-500/50 text-[10px] font-extrabold text-emerald-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
        yellowTagText.innerText = "LEAD CAR: 250+ FT BUFFER (SAFE CUSHION)";

        // Restore Green 12-15s Scan Cone
        svgScanCone.style.display = 'block';
        svgScanCone.setAttribute('points', `${{egoX * 10}},${{egoY * 5.625}} ${{egoX * 10 + 260}},${{egoY * 5.625 - 190}} ${{egoX * 10 + 340}},${{egoY * 5.625 - 100}}`);
        svgBlindCone.style.display = 'none';
        svgFootballRibbon.style.display = 'none';
        svgEgoBubble.style.display = 'block';
        svgEgoBubble.setAttribute('cx', egoX * 10);
        svgEgoBubble.setAttribute('cy', egoY * 5.625);

        // Phone Stowed Widget
        phoneWidget.className = 'absolute top-4 right-4 z-20 w-44 md:w-48 p-2.5 rounded-xl bg-[#0F141D]/95 border border-emerald-500/60 shadow-2xl backdrop-blur-md';
        phoneTimer.innerText = "DEVICE STOWED";
        phoneTimer.className = 'text-[10px] font-black text-white mono bg-emerald-950/80 px-1.5 py-0.5 rounded border border-emerald-600/40';
        phoneStatus.innerText = "COMPLIANT WITH TTC § 545.4251";
        phoneStatus.className = 'text-emerald-400 font-bold';

        // Football HUD
        footballFill.style.width = '0%';
        footballStatVal.innerText = "0 FT BLIND (100% ROAD VISIBILITY)";

        // Telemetry HUD
        hudStatusPill.innerText = "FOCUS MODE ACTIVE";
        hudStatusPill.className = "text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono";
        hudEyesOff.innerText = "0.0s (STOWED)";
        hudEyesOff.className = "font-bold text-emerald-400 text-right";
        hudBlindDist.innerText = "0 FT (EYES FORWARD)";
        hudBlindDist.className = "font-bold text-emerald-400 text-right";
        hudFields.innerText = "0.00 FIELDS";
        hudFields.className = "font-bold text-emerald-400 text-right";
        hudCrashRisk.innerText = "BASELINE (1.0x)";
        hudCrashRisk.className = "font-bold text-emerald-400 text-right";
        hudEgoSpeed.innerText = "55 MPH (CONTROLLED)";
        hudSubtext.innerHTML = "<strong>Step 4:</strong> Phone stowed in console. Do Not Disturb While Driving active. Driver maintains continuous 12&ndash;15 second forward scan and protective 4-second following cushion.";
      }}
    }}

    // ==========================================
    // MODE 2: HAZARD — DISTRACTED LANE DRIFTER
    // ==========================================
    function renderMode2(t, step) {{
      hazardBanner.style.display = 'block';
      svgDriftVector.style.display = 'block';
      svgSchoolZone.style.display = 'none';
      footballHudBar.style.display = 'none';
      phoneWidget.style.display = 'none';
      cyclePill.style.display = 'none';
      hudStatusPill.style.opacity = '0.0';
      vehBlue.style.display = 'none';

      hazardTitle.innerText = "CRITICAL HAZARD: DISTRACTED LANE DRIFTER (TTC § 545.060)";
      hazardDesc.innerText = "Vehicle in adjacent lane drifts across lane lines while driver is on phone. Defensive drivers spot weaving cues and yield right-of-way.";

      // Ego in Lane 2
      const egoX = 40.0;
      const egoY = getLaneY(2, egoX);
      vehEgo.style.left = egoX + '%';
      vehEgo.style.top = egoY + '%';
      egoTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-blue-500/50 text-[10px] font-extrabold text-blue-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      egoTagText.innerText = "EGO: OBSERVING DRIFT • BUFFERING";

      // Distracted Yellow Car drifting from Lane 1 into Lane 2
      let yellX = 53.0;
      let yellY = getLaneY(1, 53); // Starts in Lane 1 (53.6%)
      if (step >= 2) {{
        // Drifts into Lane 2
        yellY = getLaneY(1, 53) - 10.0;
      }}
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';
      yellowTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-red-500 text-[10px] font-extrabold text-red-400 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      yellowTagText.innerText = "DISTRACTED DRIFTER: TEXTING & WEAVING";

      svgScanCone.style.display = 'none';
      svgBlindCone.style.display = 'none';
      svgFootballRibbon.style.display = 'none';
      svgEgoBubble.style.display = 'block';
      svgEgoBubble.setAttribute('cx', egoX * 10);
      svgEgoBubble.setAttribute('cy', egoY * 5.625);

      // Telemetry HUD
      hudEyesOff.innerText = "ADJACENT DRIFT";
      hudEyesOff.className = "font-bold text-red-400 text-right";
      hudBlindDist.innerText = "LATERAL INTRUSION";
      hudBlindDist.className = "font-bold text-amber-300 text-right";
      hudFields.innerText = "UNSAFE LANE CHANGE";
      hudFields.className = "font-bold text-orange-400 text-right";
      hudCrashRisk.innerText = "HIGH SIDESWIPE RISK";
      hudCrashRisk.className = "font-bold text-red-500 text-right";
      hudEgoSpeed.innerText = "48 MPH (DEFENSIVE YIELD)";
      hudSubtext.innerHTML = "<strong>Hazard Drill:</strong> Visual recognition of distracted drivers: erratic speed, weaving, and head tilted downward. Do not attempt to hold lane; ease off throttle, tap horn, and maintain lateral cushion.";
    }}

    // ==========================================
    // MODE 3: HAZARD — SCHOOL ZONE WIRELESS BAN
    // ==========================================
    function renderMode3(t, step) {{
      hazardBanner.style.display = 'block';
      svgDriftVector.style.display = 'none';
      svgSchoolZone.style.display = 'block';
      footballHudBar.style.display = 'none';
      phoneWidget.style.display = 'none';
      cyclePill.style.display = 'none';
      hudStatusPill.style.opacity = '0.0';
      vehBlue.style.display = 'none';

      hazardTitle.innerText = "CRITICAL HAZARD: SCHOOL ZONE WIRELESS BAN (TTC § 545.425)";
      hazardDesc.innerText = "Handheld wireless communication is strictly prohibited in active Texas school crossing zones. Cognitive distraction in school zones poses fatal risk to children.";

      // Ego entering school crossing area
      const egoX = 38.0;
      const egoY = getLaneY(2, egoX);
      vehEgo.style.left = egoX + '%';
      vehEgo.style.top = egoY + '%';
      egoTag.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      egoTagText.innerText = "EGO: 20 MPH SCHOOL ZONE • NO WIRELESS ALLOWED";

      // Lead vehicle stopped at crosswalk
      const yellX = 60.0;
      const yellY = getLaneY(2, yellX);
      vehYellow.style.left = yellX + '%';
      vehYellow.style.top = yellY + '%';
      yellowTag.className = 'absolute left-1/2 -translate-x-1/2 -top-7 px-2 py-0.5 rounded bg-[#10141D]/90 border border-amber-500 text-[10px] font-extrabold text-amber-300 whitespace-nowrap shadow-md mono flex items-center gap-1.5';
      yellowTagText.innerText = "STOPPED FOR SCHOOL CROSSWALK";

      svgScanCone.style.display = 'none';
      svgBlindCone.style.display = 'none';
      svgFootballRibbon.style.display = 'none';
      svgEgoBubble.style.display = 'block';
      svgEgoBubble.setAttribute('cx', egoX * 10);
      svgEgoBubble.setAttribute('cy', egoY * 5.625);

      // Telemetry HUD
      hudEyesOff.innerText = "PROHIBITED (TTC § 545.425)";
      hudEyesOff.className = "font-bold text-amber-400 text-right";
      hudBlindDist.innerText = "CROSSWALK ZONE";
      hudBlindDist.className = "font-bold text-amber-300 text-right";
      hudFields.innerText = "ZERO-TOLERANCE";
      hudFields.className = "font-bold text-orange-400 text-right";
      hudCrashRisk.innerText = "CRITICAL PEDESTRIAN RISK";
      hudCrashRisk.className = "font-bold text-red-500 text-right";
      hudEgoSpeed.innerText = "20 MPH (SCHOOL LIMIT)";
      hudSubtext.innerHTML = "<strong>Statutory Mandate:</strong> Texas law strictly forbids all handheld wireless device usage in school crossing zones unless the vehicle is fully stopped. For drivers under 18 (&sect; 545.424), all wireless device usage (including hands-free) is completely barred.";
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

    output_path = os.path.abspath("driving_rule_animations_suite/simulations/L08_T04_distractions.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 30 simulation built successfully at: {output_path}")

if __name__ == '__main__':
    build_l08_t04()
