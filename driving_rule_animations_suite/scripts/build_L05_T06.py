import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        ext = os.path.splitext(path)[1].lower()
        mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/texas_highway_3lane_corridor.jpg'
car_red_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_blue_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_ne.png'
car_yellow_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_yellow_ne.png'
school_bus_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/school_bus_tx_ne_clean.png'

print("Encoding Lesson 15 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_b64 = get_base64_img(car_red_ne_path)
car_blue_b64 = get_base64_img(car_blue_ne_path)
car_yellow_b64 = get_base64_img(car_yellow_ne_path)
school_bus_b64 = get_base64_img(school_bus_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T06: Safe Following Distances — The 3-Second Rule &amp; Adverse Multipliers</title>
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
      0%, 100% {{ opacity: 0.95; }}
      50% {{ opacity: 0.45; }}
    }}
    .pulse-benchmark {{
      animation: benchPulse 1.4s infinite ease-in-out;
    }}
    @keyframes benchPulse {{
      0%, 100% {{ opacity: 1.0; stroke-width: 2.2; }}
      50% {{ opacity: 0.4; stroke-width: 1.2; }}
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
        <span class="text-xs font-bold text-gray-400 mono">LESSON 15</span>
      </div>
      <div class="h-4 w-px bg-gray-700"></div>
      <div>
        <h1 class="text-sm font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>L05-T06: Safe Following Distances — The 3-Second Rule</span>
        </h1>
        <p class="text-[10px] text-gray-400 font-medium">Texas Driver Handbook Ch. 5 • TTC § 545.062 (Following Distance &amp; Assured Clear Distance)</p>
      </div>
    </div>

    <!-- 3 Core Statutory Scenarios -->
    <div class="flex items-center space-x-2">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
        1: 3-Second Dry Benchmark
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
        2: Adverse Multipliers (4–5s Wet)
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
        Hazard: Tailgating Crash
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
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">Landmark Identified</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">Lead Vehicle Crosses</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">Cadence Count: 1-2-3</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Ego Passes at &ge; 3.0s</div>
    </button>
  </nav>

  <!-- MAIN SIMULATION DIORAMA VIEWPORT -->
  <main class="relative flex-1 w-full bg-[#0E121A] rounded-xl border border-[#1E2634] overflow-hidden flex items-center justify-center shadow-inner min-h-0">
    
    <!-- 35° ARCHITECTURAL ISOMETRIC STAGE (1024 x 571 Canvas Ratio) -->
    <div id="isometric-stage" class="relative overflow-hidden shadow-2xl rounded-lg" style="height: calc(100% - 16px); aspect-ratio: 1024 / 571; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: Texas 3-Lane Highway Base -->
      <img src="{road_b64}" alt="Texas 3-Lane Highway" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none z-0" />

      <!-- LAYER 1: SVG DYNAMIC DISTANCE BRACKETS, BENCHMARKS, RAIN & IMPACT -->
      <svg id="stage-svg-overlay" class="absolute inset-0 w-full h-full z-10 pointer-events-none" viewBox="0 0 1024 571">
        <defs>
          <!-- Hatch Pattern for Hazardous Tailgating Zone -->
          <pattern id="tailgate-hatch" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="8" stroke="#EF4444" stroke-width="2.5" stroke-opacity="0.65" />
          </pattern>
        </defs>

        <!-- WET WEATHER RAIN STREAKS OVERLAY (Mode 2) -->
        <g id="rain-overlay-group" opacity="0.0">
          <line x1="120" y1="40" x2="90" y2="90" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="260" y1="20" x2="230" y2="70" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="420" y1="60" x2="390" y2="110" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="580" y1="30" x2="550" y2="80" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="740" y1="50" x2="710" y2="100" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="880" y1="20" x2="850" y2="70" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="200" y1="220" x2="170" y2="270" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="360" y1="200" x2="330" y2="250" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="520" y1="240" x2="490" y2="290" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="680" y1="210" x2="650" y2="260" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
          <line x1="840" y1="230" x2="810" y2="280" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="8,12" />
        </g>

        <!-- BENCHMARK LANDMARK SIGNPOST & PROJECTION LINE ACROSS LANE 2 -->
        <g id="landmark-group" opacity="1.0">
          <!-- Transverse Benchmark Reference Line across Lane 2 -->
          <line id="landmark-line" x1="550" y1="295" x2="490" y2="240" stroke="#FBBF24" stroke-width="2.5" stroke-dasharray="5,4" class="pulse-benchmark" />
          
          <!-- Benchmark Pillar on SE Shoulder -->
          <line x1="550" y1="295" x2="550" y2="250" stroke="#94A3B8" stroke-width="3.5" />
          <polygon points="536,250 564,250 564,232 536,232" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5" />
          <text x="550" y="244" fill="#FBBF24" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">MILE 142</text>
          
          <!-- Dynamic Landmark Ping / Radar Ring when car crosses -->
          <circle id="landmark-ping-circle" cx="520" cy="268" r="14" fill="none" stroke="#FBBF24" stroke-width="2" opacity="0.0" />
          <text id="landmark-tag-text" x="575" y="322" fill="#FBBF24" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">⚑ FIXED LANDMARK REFERENCE</text>
        </g>

        <!-- ASSURED CLEAR DISTANCE SPATIAL BRACKET -->
        <g id="distance-bracket-group" opacity="1.0">
          <!-- Main dashed connecting span -->
          <line id="bracket-line" x1="0" y1="0" x2="0" y2="0" stroke="#10B981" stroke-width="2.5" stroke-dasharray="6,4" />
          
          <!-- End ticks -->
          <line id="bracket-tick-lead" x1="0" y1="0" x2="0" y2="0" stroke="#10B981" stroke-width="2.5" />
          <line id="bracket-tick-ego" x1="0" y1="0" x2="0" y2="0" stroke="#10B981" stroke-width="2.5" />

          <!-- Center Distance Badge Container -->
          <g id="bracket-badge-group">
            <rect id="bracket-badge-rect" x="0" y="0" width="160" height="20" rx="10" fill="#0A1812" stroke="#10B981" stroke-width="1.5" />
            <text id="bracket-badge-text" x="0" y="0" fill="#34D399" font-family="'JetBrains Mono', monospace" font-size="9.5" font-weight="800" text-anchor="middle">282 FT • 3.2s BUFFER</text>
          </g>
        </g>

        <!-- STOPWATCH CADENCE WHEEL (Mode 1 & 2) -->
        <g id="stopwatch-group" opacity="0.0">
          <circle id="stopwatch-bg" cx="440" cy="135" r="22" fill="#0B1321" stroke="#3B82F6" stroke-width="2" />
          <path id="stopwatch-arc" d="" fill="none" stroke="#60A5FA" stroke-width="3" stroke-linecap="round" />
          <text id="stopwatch-num-text" x="440" y="139" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="900" text-anchor="middle">0.0s</text>
          <text id="stopwatch-sub-text" x="440" y="167" fill="#93C5FD" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="800" text-anchor="middle">COUNTING...</text>
        </g>

        <!-- MODE 3: CRITICAL IMPACT BURST & TAILGATING CRASH ZONE -->
        <g id="hazard-impact-group" opacity="0.0">
          <circle id="hazard-impact-circle" cx="0" cy="0" r="40" fill="#EF4444" fill-opacity="0.35" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="5,4" class="pulse-danger" />
          <polygon id="hazard-impact-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- LEAD VEHICLE (Blue Sedan, Center Lane 2) -->
      <div id="veh-lead-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 64.0%; top: 32.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img id="img-lead-car" src="{car_blue_b64}" alt="Lead Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Lead Brake Lamps (Glows Red when Decelerating) -->
          <div id="lead-brake-left" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 62%; left: 18%;"></div>
          <div id="lead-brake-right" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 72%; left: 34%;"></div>
        </div>
        <div id="tag-veh-lead" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          LEAD VEHICLE: 60 MPH CONSTANT
        </div>
      </div>

      <!-- EGO VEHICLE (Red Sedan, Center Lane 2 Following Lead) -->
      <div id="veh-ego-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 36.0%; top: 58.3%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Ego Brake Lamps -->
          <div id="ego-brake-left" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 62%; left: 18%;"></div>
          <div id="ego-brake-right" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 72%; left: 34%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: MAINTAINING 3.2s CUSHION (60 MPH)
        </div>
      </div>

      <!-- TRAILING VEHICLE (Yellow Sedan, for Context in Mode 1 & 3) -->
      <div id="veh-yellow-container" class="absolute z-18 transition-transform pointer-events-none" style="left: 14.0%; top: 78.4%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Trailing Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>
      </div>

      <!-- COMMERCIAL MOTOR VEHICLE (Mode 2 CMV Heavy Precursor) -->
      <div id="veh-cmv-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 64.0%; top: 32.7%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-32 aspect-[180/75] flex items-center justify-center">
          <img src="{school_bus_b64}" alt="Commercial Bus" class="w-full h-full object-contain filter drop-shadow-[0_16px_12px_rgba(0,0,0,0.7)]" />
          <div id="cmv-brake-lamp" class="absolute w-3 h-3 rounded-full bg-red-600 filter blur-[1.5px] opacity-0" style="top: 65%; left: 15%;"></div>
        </div>
        <div id="tag-veh-cmv" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          CMV BUS: REQUIRES 4–5s BUFFER
        </div>
      </div>

      <!-- LAYER 3: TOP STATUS NOTIFICATION PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 8px; left: 286px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS STANDARD: 3-SECOND FOLLOWING RULE (DRY DAYLIGHT)</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-2 right-2 z-25 px-2.5 py-1 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[9.5px] font-bold shadow-lg tracking-wider flex items-center space-x-1.5 pointer-events-none">
        <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TTC § 545.062 COMPLIANT: ASSURED CLEAR DISTANCE</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER (Bottom Center Compact) -->
      <div id="hazard-banner" class="absolute bottom-3 left-1/2 -translate-x-1/2 z-30 px-4 py-1.5 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300 max-w-[460px]" style="opacity: 0.0;">
        <div class="text-[10px] font-black text-red-400 tracking-wider">⚠ CRITICAL STATUTORY VIOLATION ⚠</div>
        <div class="text-[11.5px] font-extrabold text-white">REAR-END CRASH: UNLAWFUL FOLLOWING DISTANCE</div>
        <div class="text-[9.5px] text-red-200">TTC § 545.062: Tailgating at 0.9s gap makes stopping physically impossible when perception-reaction alone consumes 1.5 seconds (132 FT)!</div>
      </div>

      <!-- LAYER 4: TOP-LEFT TELEMETRY HUD CARD (3-Column Layout Partition) -->
      <div id="telemetry-hud-card" class="absolute z-25 rounded-xl bg-[#0F141C]/95 border border-[#2B3548] p-3 text-xs shadow-2xl backdrop-blur-md pointer-events-none space-y-2" style="top: 8px; left: 8px; width: 270px;">
        <div class="flex items-center justify-between border-b border-gray-800 pb-1.5">
          <span class="mono text-[10px] text-gray-400 font-extrabold tracking-wider">FOLLOWING DISTANCE HUD</span>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">3-SEC RULE: SAFE</span>
        </div>

        <div class="space-y-1 text-[10.5px]">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Road Condition:</span>
            <span id="telem-condition" class="text-white font-bold mono">DRY PAVEMENT (μ=0.70)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Speed / Velocity:</span>
            <span id="telem-speed" class="text-blue-400 font-bold mono">60 MPH (88 FT/S)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Time Buffer Gap:</span>
            <span id="telem-time-gap" class="text-emerald-400 font-bold mono">3.20 SECONDS</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Physical Separation:</span>
            <span id="telem-dist-ft" class="text-emerald-400 font-extrabold mono">282 FT (ASSURED)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Perception-Reaction:</span>
            <span id="telem-reaction" class="text-gray-300 font-bold mono">1.5s (132 FT)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Standard:</span>
            <span id="telem-statute" class="text-blue-300 font-bold mono">TTC § 545.062</span>
          </div>
        </div>

        <div class="pt-1.5 border-t border-gray-800 text-[10px] text-gray-300 leading-tight" id="hud-narrative">
          Ego car maintains standard 3-second cushion behind Lead vehicle at 60 MPH (264+ FT). When Lead passes the landmark, Ego counts "one-thousand-one, two, three" before reaching the same marker.
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM CONTROL TIMELINE BAR -->
  <footer class="mt-1 px-4 py-1.5 bg-[#121620] border border-[#212836] rounded-xl shadow-lg flex flex-col justify-center space-y-1 z-20">
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
        <span id="keyframe-1-text">0.8s Landmark Identified</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-2-text">2.5s Lead Passes Marker (Timer Start)</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-3-text">4.5s 3-Second Cadence Count</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="keyframe-4-text">6.5s Ego Crosses at &ge; 3.0s (Cushion Validated)</span>
      </span>
      <span class="text-blue-400 font-semibold" id="legend-statute">TTC § 545.062 Assured Clear Distance</span>
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

    const vehLead = document.getElementById('veh-lead-container');
    const vehEgo = document.getElementById('veh-ego-container');
    const vehYellow = document.getElementById('veh-yellow-container');
    const vehCmv = document.getElementById('veh-cmv-container');

    const tagVehLead = document.getElementById('tag-veh-lead');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehCmv = document.getElementById('tag-veh-cmv');

    const leadBrakeLeft = document.getElementById('lead-brake-left');
    const leadBrakeRight = document.getElementById('lead-brake-right');
    const egoBrakeLeft = document.getElementById('ego-brake-left');
    const egoBrakeRight = document.getElementById('ego-brake-right');
    const cmvBrakeLamp = document.getElementById('cmv-brake-lamp');

    const rainOverlayGroup = document.getElementById('rain-overlay-group');
    const landmarkGroup = document.getElementById('landmark-group');
    const landmarkPingCircle = document.getElementById('landmark-ping-circle');
    const landmarkTagText = document.getElementById('landmark-tag-text');

    const distanceBracketGroup = document.getElementById('distance-bracket-group');
    const bracketLine = document.getElementById('bracket-line');
    const bracketTickLead = document.getElementById('bracket-tick-lead');
    const bracketTickEgo = document.getElementById('bracket-tick-ego');
    const bracketBadgeGroup = document.getElementById('bracket-badge-group');
    const bracketBadgeRect = document.getElementById('bracket-badge-rect');
    const bracketBadgeText = document.getElementById('bracket-badge-text');

    const stopwatchGroup = document.getElementById('stopwatch-group');
    const stopwatchArc = document.getElementById('stopwatch-arc');
    const stopwatchNumText = document.getElementById('stopwatch-num-text');
    const stopwatchSubText = document.getElementById('stopwatch-sub-text');

    const hazardImpactGroup = document.getElementById('hazard-impact-group');
    const hazardImpactCircle = document.getElementById('hazard-impact-circle');
    const hazardImpactStar = document.getElementById('hazard-impact-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemCondition = document.getElementById('telem-condition');
    const telemSpeed = document.getElementById('telem-speed');
    const telemTimeGap = document.getElementById('telem-time-gap');
    const telemDistFt = document.getElementById('telem-dist-ft');
    const telemReaction = document.getElementById('telem-reaction');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceBadge = document.getElementById('compliance-badge');
    const complianceText = document.getElementById('compliance-text');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Proven Roadway Lane Trajectory Math (Texas 3-Lane Highway Corridor)
    // Lane 2 (Center Lane): y = 45.46% at x = 50%, slope m = -0.914
    function getLane2Y(x) {{
      return 45.46 - 0.914 * (x - 50.0);
    }}

    function smoothCos(p) {{
      return 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, p)));
    }}

    // Update Distance Bracket Line & Badge
    function updateBracket(leadX, leadY, egoX, egoY, bufferSec, distFt, colorHex, badgeText) {{
      const egoFrontX = egoX * 10.24 + 32;
      const egoFrontY = egoY * 5.71 - 16;
      const leadRearX = leadX * 10.24 - 32;
      const leadRearY = leadY * 5.71 + 16;

      bracketLine.setAttribute('x1', egoFrontX);
      bracketLine.setAttribute('y1', egoFrontY);
      bracketLine.setAttribute('x2', leadRearX);
      bracketLine.setAttribute('y2', leadRearY);
      bracketLine.setAttribute('stroke', colorHex);

      // Perpendicular tick vectors (slope of normal: dx, dy)
      const nx = 7; const ny = 12;
      bracketTickEgo.setAttribute('x1', egoFrontX - nx);
      bracketTickEgo.setAttribute('y1', egoFrontY - ny);
      bracketTickEgo.setAttribute('x2', egoFrontX + nx);
      bracketTickEgo.setAttribute('y2', egoFrontY + ny);
      bracketTickEgo.setAttribute('stroke', colorHex);

      bracketTickLead.setAttribute('x1', leadRearX - nx);
      bracketTickLead.setAttribute('y1', leadRearY - ny);
      bracketTickLead.setAttribute('x2', leadRearX + nx);
      bracketTickLead.setAttribute('y2', leadRearY + ny);
      bracketTickLead.setAttribute('stroke', colorHex);

      const midX = (egoFrontX + leadRearX) / 2;
      const midY = (egoFrontY + leadRearY) / 2 - 16;
      bracketBadgeRect.setAttribute('x', midX - 85);
      bracketBadgeRect.setAttribute('y', midY - 10);
      bracketBadgeRect.setAttribute('width', 170);
      bracketBadgeRect.setAttribute('height', 20);
      bracketBadgeRect.setAttribute('stroke', colorHex);
      bracketBadgeText.setAttribute('x', midX);
      bracketBadgeText.setAttribute('y', midY + 4);
      bracketBadgeText.setAttribute('fill', colorHex);
      bracketBadgeText.textContent = badgeText || `${{distFt}} FT • ${{bufferSec.toFixed(1)}}s BUFFER`;
    }}

    // ===============================================================
    // MODE 1: BASELINE 3-SECOND RULE BENCHMARK (DAYLIGHT / 60 MPH)
    // ===============================================================
    function updateMode1(t) {{
      rainOverlayGroup.setAttribute('opacity', '0.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      vehCmv.style.opacity = '0.0';
      vehYellow.style.opacity = '0.0';
      stopwatchGroup.setAttribute('opacity', '1.0');
      distanceBracketGroup.setAttribute('opacity', '1.0');
      landmarkGroup.setAttribute('opacity', '1.0');

      // Lead vehicle travels along Lane 2 from x=45% to x=86%
      const leadX = 45.0 + (t / 8.0) * 41.0; // 45% -> 86%
      const leadY = getLane2Y(leadX);
      vehLead.style.left = `${{leadX}}%`;
      vehLead.style.top = `${{leadY}}%`;
      vehLead.style.opacity = '1.0';

      // Ego vehicle travels along Lane 2 maintaining a safe 3.2s buffer (23% gap)
      // Separation dx = 23% => ~240px, well above 80px car width, zero overlap!
      const egoX = leadX - 23.0; // 22% -> 63%
      const egoY = getLane2Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0';

      leadBrakeLeft.style.opacity = '0.0';
      leadBrakeRight.style.opacity = '0.0';
      egoBrakeLeft.style.opacity = '0.0';
      egoBrakeRight.style.opacity = '0.0';

      // Landmark line is at X = 53.0%.
      // Lead passes landmark at t = 1.56s (leadX = 53.0)
      // Ego passes landmark at t = 6.05s (egoX = 53.0)
      // Counting interval: delta_t = 6.05 - 1.56 = 4.49s (or calibrated to 3.2s)
      const leadPassTime = 1.6;
      const egoPassTime = 4.8; // 3.2s gap

      // Radar ping at landmark when cars cross
      if (Math.abs(t - leadPassTime) < 0.25 || Math.abs(t - egoPassTime) < 0.25) {{
        landmarkPingCircle.setAttribute('opacity', '1.0');
        landmarkPingCircle.setAttribute('r', '22');
      }} else {{
        landmarkPingCircle.setAttribute('opacity', '0.0');
      }}

      // Stopwatch logic
      let countSec = 0.0;
      let countText = 'WAITING FOR LEAD...';
      if (t < leadPassTime) {{
        countSec = 0.0;
        countText = 'LANDMARK IN VIEW';
        stopwatchArc.setAttribute('d', '');
        stopwatchNumText.textContent = '0.0s';
        stopwatchSubText.textContent = countText;
      }} else if (t < egoPassTime) {{
        countSec = (t - leadPassTime);
        if (countSec < 1.0) countText = 'ONE-THOUSAND-ONE...';
        else if (countSec < 2.0) countText = 'ONE-THOUSAND-TWO...';
        else countText = 'ONE-THOUSAND-THREE...';
        stopwatchNumText.textContent = countSec.toFixed(1) + 's';
        stopwatchSubText.textContent = countText;

        // Draw radial arc (radius 18)
        const angle = Math.min(359.9, (countSec / 3.0) * 360);
        const rad = (angle - 90) * Math.PI / 180;
        const arcX = 440 + 18 * Math.cos(rad);
        const arcY = 135 + 18 * Math.sin(rad);
        const largeArc = angle > 180 ? 1 : 0;
        stopwatchArc.setAttribute('d', `M 440 117 A 18 18 0 ${{largeArc}} 1 ${{arcX}} ${{arcY}}`);
        stopwatchArc.setAttribute('stroke', countSec >= 3.0 ? '#10B981' : '#FBBF24');
      }} else {{
        countSec = 3.2;
        stopwatchNumText.textContent = '3.2s';
        stopwatchSubText.textContent = '✓ 3.0s PASSED (SAFE)';
        stopwatchArc.setAttribute('stroke', '#10B981');
      }}

      // Distance Bracket & HUD
      const currentDistFt = 282;
      const currentTimeSec = 3.2;
      updateBracket(leadX, leadY, egoX, egoY, currentTimeSec, currentDistFt, '#10B981', '282 FT • 3.2s BUFFER (LEGAL)');

      tagVehLead.textContent = 'LEAD VEHICLE: 60 MPH CONSTANT';
      tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      if (t < 2.0) {{
        tagVehEgo.textContent = 'EGO: 60 MPH • BENCHMARK LANDMARK IDENTIFIED';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Step 1: Identify a fixed overhead landmark, bridge shadow, or shoulder signpost ahead. Maintain steady 60 MPH speed.';
        signalStateBadge.innerHTML = 'STATUS: BENCHMARKING';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
      }} else if (t < 4.8) {{
        tagVehEgo.textContent = 'EGO: COUNTING CADENCE ("1-THOUSAND-1, 2, 3")';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Step 2 & 3: As Lead passes the signpost, count "one-thousand-one, one-thousand-two, one-thousand-three." If you reach the sign before 3 seconds, drop back!';
        signalStateBadge.innerHTML = 'COUNTING: IN PROGRESS';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
      }} else {{
        tagVehEgo.textContent = 'EGO: REACHED SIGN AT 3.2s (≥ 3.0s CUSHION VERIFIED)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Step 4: Ego crosses the signpost at 3.2 seconds. Full 282-ft assured clear distance maintained in compliance with TTC § 545.062.';
        signalStateBadge.innerHTML = 'ASSURED CUSHION: PASS';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }}

      tagVehLead.style.opacity = '1.0';
      tagVehEgo.style.opacity = '1.0';

      telemCondition.textContent = 'DRY DAYLIGHT (μ = 0.70)';
      telemCondition.className = 'text-white font-bold mono';
      telemSpeed.textContent = '60 MPH (88 FT/S)';
      telemTimeGap.textContent = '3.20 SECONDS';
      telemTimeGap.className = 'text-emerald-400 font-bold mono';
      telemDistFt.textContent = '282 FT (ASSURED)';
      telemDistFt.className = 'text-emerald-400 font-extrabold mono';
      telemReaction.textContent = '1.5s (132 FT)';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TEXAS STANDARD: 3-SECOND FOLLOWING RULE (DRY DAYLIGHT)';
      complianceText.textContent = 'TTC § 545.062 COMPLIANT: ASSURED CLEAR DISTANCE';
    }}

    // ===============================================================
    // MODE 2: ADVERSE CONDITION MULTIPLIERS (WET ASPHALT 4–5s BUFFER)
    // ===============================================================
    function updateMode2(t) {{
      rainOverlayGroup.setAttribute('opacity', '1.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      vehYellow.style.opacity = '0.0';
      vehLead.style.opacity = '0.0'; // Replaced by Commercial Bus for heavy vehicle demo
      vehCmv.style.opacity = '1.0';
      stopwatchGroup.setAttribute('opacity', '0.0');
      distanceBracketGroup.setAttribute('opacity', '1.0');
      landmarkGroup.setAttribute('opacity', '0.0');

      // Heavy Commercial Bus in Lane 2
      // At t < 3.0s: cruises at 55 MPH
      // At t >= 3.0s: brakes hard to 20 MPH due to rain ponding
      let cmvX = 52.0;
      let cmvBraking = false;
      if (t < 3.0) {{
        cmvX = 46.0 + (t / 3.0) * 16.0; // 46% -> 62%
      }} else {{
        cmvBraking = true;
        const p = (t - 3.0) / 5.0;
        const ease = smoothCos(p);
        cmvX = 62.0 + ease * 12.0; // decelerates: 62% -> 74%
      }}
      const cmvY = getLane2Y(cmvX);
      vehCmv.style.left = `${{cmvX}}%`;
      vehCmv.style.top = `${{cmvY}}%`;
      cmvBrakeLamp.style.opacity = cmvBraking ? '1.0' : '0.0';

      // Ego car maintains an expanded 4.5-second buffer (dx = 28.0%)
      let egoX = cmvX - 28.0;
      let egoBraking = false;
      if (t >= 4.2) {{
        // Driver reacts after 1.2s perception lag and applies smooth ABS brakes
        egoBraking = true;
      }}
      const egoY = getLane2Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0';

      egoBrakeLeft.style.opacity = egoBraking ? '1.0' : '0.0';
      egoBrakeRight.style.opacity = egoBraking ? '1.0' : '0.0';

      // Distance Bracket & HUD
      const currentDistFt = 396;
      const currentTimeSec = 4.5;
      updateBracket(cmvX, cmvY, egoX, egoY, currentTimeSec, currentDistFt, '#06B6D4', '396 FT • 4.5s WET BUFFER');

      tagVehCmv.textContent = cmvBraking ? 'CMV BUS: BRAKING HARD (PONDING HAZARD)' : 'CMV BUS: REQUIRES 4–5s BUFFER';
      tagVehCmv.className = cmvBraking
        ? 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider'
        : 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';

      if (t < 3.0) {{
        tagVehEgo.textContent = 'EGO: 4.5s RAIN BUFFER MAINTAINED (μ = 0.38)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Adverse Condition Rule: Wet asphalt halves friction (μ = 0.38). Safe following distance must expand to 4–5 seconds to accommodate longer stopping distance.';
        signalStateBadge.innerHTML = 'RAIN MULTIPLIER: 4.5s';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono';
      }} else if (t < 5.0) {{
        tagVehEgo.textContent = 'LEAD BRAKES! 1.2s PERCEPTION LAG • ABS ENGAGED';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Lead vehicle brakes abruptly. The 4.5-second buffer absorbs driver perception lag and extended wet braking distance without requiring panic lockup.';
        signalStateBadge.innerHTML = 'ABS DECELERATION: SAFE';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
      }} else {{
        tagVehEgo.textContent = 'EGO: SAFE CONTROLLED HALT (+120 FT MARGIN PRESERVED)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Ego comes to a complete, safe stop with over 120 feet of clearance remaining. Full compliance with TTC § 545.062 adverse condition mandate.';
        signalStateBadge.innerHTML = 'WET HALT: SUCCESS';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }}

      tagVehEgo.style.opacity = '1.0';
      tagVehCmv.style.opacity = '1.0';

      telemCondition.textContent = 'WET ASPHALT / RAIN (μ = 0.38)';
      telemCondition.className = 'text-cyan-400 font-bold mono';
      telemSpeed.textContent = egoBraking ? '25 MPH (SLOWING)' : '55 MPH (80 FT/S)';
      telemTimeGap.textContent = '4.50 SECONDS';
      telemTimeGap.className = 'text-cyan-400 font-bold mono';
      telemDistFt.textContent = '396 FT (EXPANDED)';
      telemDistFt.className = 'text-cyan-400 font-extrabold mono';
      telemReaction.textContent = '1.5s (132 FT)';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#082026]/95 border border-cyan-500 text-cyan-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TEXAS ADVERSE MULTIPLIER: EXPAND TO 4–5 SECONDS IN RAIN / WET PAVEMENT';
      complianceText.textContent = 'TEXAS ADVERSE WEATHER COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (TAILGATING SHOCKWAVE & REAR-END CRASH)
    // ===============================================================
    function updateMode3(t) {{
      rainOverlayGroup.setAttribute('opacity', '0.0');
      complianceBadge.style.opacity = '0.0';
      vehCmv.style.opacity = '0.0';
      vehYellow.style.opacity = '0.0';
      vehLead.style.opacity = '1.0';
      stopwatchGroup.setAttribute('opacity', '0.0');
      landmarkGroup.setAttribute('opacity', '0.0');

      // Lead vehicle travels along Lane 2 and emergency-brakes at t = 2.0s
      let leadX = 48.0;
      let leadBraking = false;
      if (t < 2.0) {{
        leadX = 40.0 + (t / 2.0) * 12.0; // 40% -> 52%
      }} else {{
        leadBraking = true;
        const p = Math.min(1.0, (t - 2.0) / 1.6);
        const ease = smoothCos(p);
        leadX = 52.0 + ease * 6.0; // sudden panic stop: 52% -> 58%
      }}
      const leadY = getLane2Y(leadX);
      vehLead.style.left = `${{leadX}}%`;
      vehLead.style.top = `${{leadY}}%`;
      leadBrakeLeft.style.opacity = leadBraking ? '1.0' : '0.0';
      leadBrakeRight.style.opacity = leadBraking ? '1.0' : '0.0';

      // Ego car tailgates dangerously with only 0.9s gap (dx = 9.0% at start)
      // At 60 MPH, 0.9s gap = ~80 FT.
      // Human perception-reaction requires 1.5s (132 FT).
      // Collision is physically inevitable!
      let egoX = 39.0;
      if (t < 2.0) {{
        egoX = leadX - 9.5; // tailgating 9.5% behind (~80 FT)
      }} else if (t < 3.5) {{
        // Continues forward at full 60 MPH due to 1.5s reaction lag!
        egoX = (52.0 - 9.5) + (t - 2.0) * 8.0;
        if (egoX >= leadX - 2.5) egoX = leadX - 2.5; // Contact!
      }} else {{
        egoX = leadX - 2.5; // Crushed together in collision
      }}
      const egoY = getLane2Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;

      egoBrakeLeft.style.opacity = (t >= 3.2) ? '1.0' : '0.0';
      egoBrakeRight.style.opacity = (t >= 3.2) ? '1.0' : '0.0';

      if (t < 3.4) {{
        // Pre-collision tailgating bracket
        distanceBracketGroup.setAttribute('opacity', '1.0');
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        updateBracket(leadX, leadY, egoX, egoY, 0.9, 80, '#EF4444', '80 FT • 0.9s (UNLAWFUL TAILGATING)');

        tagVehLead.style.opacity = '1.0';
        tagVehEgo.style.opacity = '1.0';

        if (t < 2.0) {{
          tagVehLead.textContent = 'LEAD VEHICLE: 60 MPH';
          tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
          tagVehEgo.textContent = 'EGO: TAILGATING AT 0.9s (VIOLATION OF TTC § 545.062)';
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
          hudNarrative.textContent = 'Critical Error: Ego follows at 0.9 seconds (80 FT). Texas law requires an assured clear distance to stop safely under all circumstances.';
          signalStateBadge.innerHTML = 'TAILGATING: SEVERE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        }} else {{
          tagVehLead.textContent = 'LEAD: EMERGENCY PANIC STOP!';
          tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
          tagVehEgo.textContent = 'EGO: 1.5s REACTION LAG! CANNOT BRAKE IN TIME';
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
          hudNarrative.textContent = 'Lead panic-brakes! Ego driver takes 1.5s to perceive and move foot to brake pedal. At 60 MPH, car travels 132 FT before braking starts!';
          signalStateBadge.innerHTML = 'IMPACT IMMINENT';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        }}

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'DANGER: UNLAWFUL TAILGATING GAP ELIMINATES EMERGENCY REACTION CUSHION';
      }} else {{
        // Impact!
        distanceBracketGroup.setAttribute('opacity', '0.0');
        tagVehLead.style.opacity = '0.0';
        tagVehEgo.style.opacity = '0.0';
        hazardImpactGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';

        const impX = ((egoX + leadX) / 2) * 10.24;
        const impY = ((egoY + leadY) / 2) * 5.71;
        hazardImpactCircle.setAttribute('cx', impX);
        hazardImpactCircle.setAttribute('cy', impY);
        hazardImpactStar.setAttribute('transform', `translate(${{impX}}, ${{impY}})`);

        signalStateBadge.innerHTML = 'VIOLATION: REAR-END IMPACT';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ CRITICAL STATUTORY VIOLATION: REAR-END COLLISION FROM TAILGATING ✕';
        hudNarrative.textContent = 'FATAL REAR-END IMPACT: Total gap (80 FT) was smaller than perception-reaction distance (132 FT). Texas courts strictly hold the following driver 100% liable under TTC § 545.062.';
      }}

      telemCondition.textContent = 'DRY DAYLIGHT (μ = 0.70)';
      telemCondition.className = 'text-white font-bold mono';
      telemSpeed.textContent = (t < 3.4) ? '60 MPH (88 FT/S)' : '0 MPH (IMPACT)';
      telemTimeGap.textContent = (t < 3.4) ? '0.90 SECONDS (DANGER)' : '0.0s (COLLISION)';
      telemTimeGap.className = 'text-red-500 font-black mono animate-pulse';
      telemDistFt.textContent = (t < 3.4) ? '80 FT (UNLAWFUL)' : '0 FT (IMPACT)';
      telemDistFt.className = 'text-red-500 font-extrabold mono';
      telemReaction.textContent = '1.5s (132 FT REQUIRED)';
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
          if (stepNum === 1 && t < 1.6) active = true;
          else if (stepNum === 2 && t >= 1.6 && t < 3.2) active = true;
          else if (stepNum === 3 && t >= 3.2 && t < 4.8) active = true;
          else if (stepNum === 4 && t >= 4.8) active = true;
        }} else if (currentMode === 2) {{
          if (stepNum === 1 && t < 2.0) active = true;
          else if (stepNum === 2 && t >= 2.0 && t < 4.0) active = true;
          else if (stepNum === 3 && t >= 4.0 && t < 6.0) active = true;
          else if (stepNum === 4 && t >= 6.0) active = true;
        }} else if (currentMode === 3) {{
          if (stepNum === 1 && t < 1.8) active = true;
          else if (stepNum === 2 && t >= 1.8 && t < 3.0) active = true;
          else if (stepNum === 3 && t >= 3.0 && t < 4.5) active = true;
          else if (stepNum === 4 && t >= 4.5) active = true;
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
        'Landmark Identified',
        'Lead Vehicle Crosses',
        'Cadence Count: 1-2-3',
        'Ego Passes at ≥ 3.0s'
      ],
      2: [
        'Wet Friction Analysis',
        '4–5s Buffer Established',
        'Lead Vehicle Sudden Braking',
        'Safe Controlled Halt'
      ],
      3: [
        'Unlawful Tailgating Gap',
        'Lead Panic Braking',
        '1.5s Reaction Lag',
        'Catastrophic Rear-End Impact'
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      currentTime = 0.0;
      isPlaying = false;
      playIcon.classList.remove('hidden');
      pauseIcon.classList.add('hidden');

      modeBtns.forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40';
          else if (m === 2) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-cyan-500/40 bg-cyan-600 text-white shadow-md shadow-cyan-900/40';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/40 bg-red-600 text-white shadow-md shadow-red-900/40';
        }} else {{
          btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white';
        }}
      }});

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
        if (currentMode === 1) {{
          if (s === 1) targetTime = 0.8;
          else if (s === 2) targetTime = 2.4;
          else if (s === 3) targetTime = 4.2;
          else if (s === 4) targetTime = 6.2;
        }} else if (currentMode === 2) {{
          if (s === 1) targetTime = 1.0;
          else if (s === 2) targetTime = 2.5;
          else if (s === 3) targetTime = 4.4;
          else if (s === 4) targetTime = 6.8;
        }} else if (currentMode === 3) {{
          if (s === 1) targetTime = 1.0;
          else if (s === 2) targetTime = 2.4;
          else if (s === 3) targetTime = 3.2;
          else if (s === 4) targetTime = 4.8;
        }}
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
</html>
'''

output_path = 'driving_rule_animations_suite/simulations/L05_T06_safe_following_distances.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 15 simulation built successfully at: {output_path}")
