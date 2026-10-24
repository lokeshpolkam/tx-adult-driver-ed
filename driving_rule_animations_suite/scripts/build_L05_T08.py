import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.svg':
            mime = 'image/svg+xml'
        elif ext in ['.jpg', '.jpeg']:
            mime = 'image/jpeg'
        else:
            mime = 'image/png'
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/texas_suburban_2lane_corridor.jpg'
car_red_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_red_nw_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_nw.png'
barricade_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/traffic_control/barricade_type3_closed.svg'

print("Encoding Lesson 17 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_ne_b64 = get_base64_img(car_red_ne_path)
car_red_nw_b64 = get_base64_img(car_red_nw_path)
barricade_b64 = get_base64_img(barricade_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T08: Adverse Conditions &amp; Flash Floods — Hydroplaning &amp; Barricade Law</title>
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
    .water-flow {{
      animation: waterFlowAnim 1.6s infinite linear;
    }}
    @keyframes waterFlowAnim {{
      0% {{ stroke-dashoffset: 0; }}
      100% {{ stroke-dashoffset: -32; }}
    }}
    .spray-pulse {{
      animation: sprayAnim 0.8s infinite ease-in-out;
    }}
    @keyframes sprayAnim {{
      0%, 100% {{ opacity: 0.8; transform: scale(1); }}
      50% {{ opacity: 0.3; transform: scale(1.15); }}
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
        <span class="text-xs font-bold text-gray-400 mono">LESSON 17</span>
      </div>
      <div class="h-4 w-px bg-gray-700"></div>
      <div>
        <h1 class="text-sm font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>L05-T08: Adverse Conditions &amp; Flash Floods</span>
        </h1>
        <p class="text-[10px] text-gray-400 font-medium">Texas Driver Handbook Ch. 5 • TTC § 472.022 (Warning Signs &amp; Flood Barricade Law)</p>
      </div>
    </div>

    <!-- 3 Core Statutory Scenarios -->
    <div class="flex items-center space-x-2">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
        1: Hydroplaning &amp; Throttle-Lift
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
        2: Barricades &amp; "Turn Around, Don't Drown"
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
        Hazard: Swept Away in Flood
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
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">Standing Water Encountered</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">Water Wedge Lifts Tires (0% Grip)</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">Smooth Throttle Lift (No Brake)</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Speed &lt; 35 MPH: Grip Restored</div>
    </button>
  </nav>

  <!-- MAIN SIMULATION DIORAMA VIEWPORT -->
  <main class="relative flex-1 w-full bg-[#0E121A] rounded-xl border border-[#1E2634] overflow-hidden flex items-center justify-center shadow-inner min-h-0">
    
    <!-- 35° ARCHITECTURAL ISOMETRIC STAGE (1024 x 571 Canvas Ratio) -->
    <div id="isometric-stage" class="relative overflow-hidden shadow-2xl rounded-lg" style="height: calc(100% - 16px); aspect-ratio: 1024 / 571; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: Texas Suburban 2-Lane Roadway Base -->
      <img src="{road_b64}" alt="Texas 2-Lane Roadway" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none z-0" />

      <!-- LAYER 1: SVG DYNAMIC WATER SHEETS, DEPTH GAUGES, SPRAY & TORRENT -->
      <svg id="stage-svg-overlay" class="absolute inset-0 w-full h-full z-10 pointer-events-none" viewBox="0 0 1024 571">
        
        <!-- RAIN PRECIPITATION OVERLAY (All Modes) -->
        <g id="rain-group" opacity="0.6">
          <line x1="80" y1="30" x2="60" y2="80" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="220" y1="20" x2="200" y2="70" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="380" y1="50" x2="360" y2="100" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="540" y1="20" x2="520" y2="70" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="700" y1="40" x2="680" y2="90" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="860" y1="30" x2="840" y2="80" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="160" y1="240" x2="140" y2="290" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="320" y1="220" x2="300" y2="270" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="480" y1="250" x2="460" y2="300" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="640" y1="230" x2="620" y2="280" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
          <line x1="800" y1="240" x2="780" y2="290" stroke="#93C5FD" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="6,12" />
        </g>

        <!-- WATER POOLING / HYDROPLANING SHEET IN LANE 1 (Mode 1) -->
        <g id="hydroplane-pool-group" opacity="1.0">
          <!-- Pooling sheet polygon across Lane 1 from x=45% to x=68% -->
          <polygon id="water-sheet-poly" points="460,340 700,100 760,160 520,400" fill="#0284C7" fill-opacity="0.32" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="8,4" />
          
          <!-- Ripple contour lines -->
          <line x1="480" y1="350" x2="560" y2="270" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="12,8" class="water-flow" />
          <line x1="540" y1="360" x2="640" y2="260" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="12,8" class="water-flow" />
          <line x1="620" y1="330" x2="720" y2="230" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="12,8" class="water-flow" />

          <!-- Pool zone label placed on SE shoulder -->
          <rect x="540" y="402" width="190" height="20" rx="10" fill="#08202A" stroke="#38BDF8" stroke-width="1.5" />
          <text x="635" y="416" fill="#7DD3FC" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="800" text-anchor="middle">⚠ STANDING WATER: HYDROPLANING RISK</text>
        </g>

        <!-- WHEEL SPRAY VECTORS UNDER CAR (Mode 1 & 3) -->
        <g id="tire-spray-group" opacity="0.0">
          <ellipse id="spray-front" cx="0" cy="0" rx="20" ry="8" fill="#BAE6FD" fill-opacity="0.55" class="spray-pulse" />
          <ellipse id="spray-rear" cx="0" cy="0" rx="28" ry="10" fill="#BAE6FD" fill-opacity="0.65" class="spray-pulse" />
        </g>

        <!-- FLASH FLOOD LOW-WATER CROSSING & DEPTH GAUGE (Mode 2 & 3) -->
        <g id="flood-crossing-group" opacity="0.0">
          <!-- Massive flood torrent across both lanes from x=48% to x=78% -->
          <polygon points="460,380 760,80 880,200 580,500" fill="#075985" fill-opacity="0.5" stroke="#0284C7" stroke-width="2" />
          
          <!-- Rapid current flow lines -->
          <line x1="500" y1="390" x2="680" y2="210" stroke="#E0F2FE" stroke-width="2.5" stroke-dasharray="16,8" class="water-flow" />
          <line x1="580" y1="410" x2="780" y2="210" stroke="#E0F2FE" stroke-width="2.5" stroke-dasharray="16,8" class="water-flow" />
          <line x1="660" y1="410" x2="840" y2="230" stroke="#E0F2FE" stroke-width="2.5" stroke-dasharray="16,8" class="water-flow" />

          <!-- Texas Depth Gauge Post on Right Shoulder (x=470, y=360) -->
          <g id="depth-gauge-post" transform="translate(470, 310)">
            <rect x="0" y="0" width="10" height="90" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.5" />
            <!-- 6 inch mark (ankle deep) -->
            <line x1="0" y1="65" x2="10" y2="65" stroke="#EF4444" stroke-width="2" />
            <text x="16" y="68" fill="#EF4444" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900">6" (STALL)</text>
            <!-- 12 inch mark (floats cars) -->
            <line x1="0" y1="42" x2="10" y2="42" stroke="#EF4444" stroke-width="2" />
            <text x="16" y="45" fill="#EF4444" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900">12" (FLOATS CARS)</text>
            <!-- 24 inch mark (sweeps trucks) -->
            <line x1="0" y1="18" x2="10" y2="18" stroke="#DC2626" stroke-width="2" />
            <text x="16" y="21" fill="#DC2626" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900">24" (SWEEPS TRUCKS)</text>
          </g>

          <!-- Water Depth Callout Badge -->
          <rect x="600" y="446" width="225" height="22" rx="11" fill="#032030" stroke="#0284C7" stroke-width="1.5" />
          <text id="depth-badge-text" x="712" y="461" fill="#38BDF8" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="800" text-anchor="middle">RUSHING TORRENT: 18–24 INCHES DEEP</text>
        </g>

        <!-- MODE 3: CRITICAL WATER RESCUE / VEHICLE SWEEP-AWAY ALERT -->
        <g id="hazard-impact-group" opacity="0.0">
          <circle id="hazard-impact-circle" cx="0" cy="0" r="46" fill="#EF4444" fill-opacity="0.3" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="6,4" class="pulse-danger" />
          <polygon id="hazard-impact-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: TYPE 3 BARRICADES & ROAD CLOSED SIGN (Mode 2 & 3) -->
      <div id="barricade-lane1" class="absolute z-19 pointer-events-none transition-opacity duration-300" style="left: 45.0%; top: 56.0%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-24 aspect-[200/140]">
          <img src="{barricade_b64}" alt="MUTCD Type 3 Barricade" class="w-full h-full object-contain filter drop-shadow-[0_8px_8px_rgba(0,0,0,0.6)]" />
        </div>
        <div class="absolute left-1/2 -translate-x-1/2 -top-6 whitespace-nowrap px-2 py-0.5 rounded bg-amber-950/95 border border-amber-400 text-[8.5px] font-black text-amber-300 mono shadow-lg">
          ROAD CLOSED • HIGH WATER
        </div>
      </div>

      <div id="barricade-lane2" class="absolute z-19 pointer-events-none transition-opacity duration-300" style="left: 36.0%; top: 48.0%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-24 aspect-[200/140]">
          <img src="{barricade_b64}" alt="MUTCD Type 3 Barricade" class="w-full h-full object-contain filter drop-shadow-[0_8px_8px_rgba(0,0,0,0.6)]" />
        </div>
        <div class="absolute left-1/2 -translate-x-1/2 -top-6 whitespace-nowrap px-2 py-0.5 rounded bg-amber-950/95 border border-amber-400 text-[8.5px] font-black text-amber-300 mono shadow-lg">
          TTC § 472.022 MANDATE
        </div>
      </div>

      <!-- LAYER 2: EGO VEHICLE SPRITES -->
      <div id="veh-ego-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 18.0%; top: 88.8%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img id="img-ego-ne" src="{car_red_ne_b64}" alt="Ego Vehicle NE" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          <img id="img-ego-nw" src="{car_red_nw_b64}" alt="Ego Vehicle NW" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)] hidden" />
          
          <!-- Turn Signal Blinkers -->
          <div id="blinker-right" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 70%; left: 74%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: 52 MPH • WET HIGHWAY CRUISE
        </div>
      </div>

      <!-- LAYER 3: TOP STATUS NOTIFICATION PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 8px; left: 286px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS HYDROPLANING RULE: EASE OFF ACCELERATOR • DO NOT PANIC BRAKE</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-2 right-2 z-25 px-2.5 py-1 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[9.5px] font-bold shadow-lg tracking-wider flex items-center space-x-1.5 pointer-events-none">
        <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TEXAS ADVERSE CONDITIONS COMPLIANCE VERIFIED</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER (Bottom Center Compact) -->
      <div id="hazard-banner" class="absolute bottom-3 left-1/2 -translate-x-1/2 z-30 px-4 py-1.5 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300 max-w-[460px]" style="opacity: 0.0;">
        <div class="text-[10px] font-black text-red-400 tracking-wider">⚠ CRITICAL CRIMINAL STATUTORY VIOLATION ⚠</div>
        <div class="text-[11.5px] font-extrabold text-white">SWEPT AWAY: DISREGARDING FLASH FLOOD BARRICADE</div>
        <div class="text-[9.5px] text-red-200">TTC § 472.022: Class B Misdemeanor ($2,000 fine + 180 days jail). Moving water 18–24 inches deep exerts over 1,500 lbs of buoyant force, sweeping vehicles into fatal torrents!</div>
      </div>

      <!-- LAYER 4: TOP-LEFT TELEMETRY HUD CARD (3-Column Layout Partition) -->
      <div id="telemetry-hud-card" class="absolute z-25 rounded-xl bg-[#0F141C]/95 border border-[#2B3548] p-3 text-xs shadow-2xl backdrop-blur-md pointer-events-none space-y-2" style="top: 8px; left: 8px; width: 270px;">
        <div class="flex items-center justify-between border-b border-gray-800 pb-1.5">
          <span class="mono text-[10px] text-gray-400 font-extrabold tracking-wider">WEATHER HYDRODYNAMICS HUD</span>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">STATUS: 52 MPH</span>
        </div>

        <div class="space-y-1 text-[10.5px]">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Road Surface:</span>
            <span id="telem-surface" class="text-white font-bold mono">WET ASPHALT / POOLING</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Vehicle Speed:</span>
            <span id="telem-speed" class="text-cyan-400 font-bold mono">52 MPH (76 FT/S)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Tire Friction (μ):</span>
            <span id="telem-friction" class="text-emerald-400 font-bold mono">0.38 (WET GRIP)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Water Depth:</span>
            <span id="telem-depth" class="text-blue-300 font-bold mono">0.25 INCHES (POOL)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Steering Control:</span>
            <span id="telem-steering" class="text-emerald-400 font-bold mono">100% RESPONSIVE</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Texas Statute:</span>
            <span id="telem-statute" class="text-blue-300 font-bold mono">TX Handbook Ch. 5</span>
          </div>
        </div>

        <div class="pt-1.5 border-t border-gray-800 text-[10px] text-gray-300 leading-tight" id="hud-narrative">
          Ego vehicle approaches standing water sheet at 52 MPH. At speeds over 35 MPH, tire grooves may fail to channel water, creating a hydrodynamic wedge that lifts tires off the road.
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
        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
        <span id="keyframe-1-text">0.8s Standing Water Encountered</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-red-400"></span>
        <span id="keyframe-2-text">2.5s Hydroplaning (0% Tire Friction)</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-3-text">4.5s Throttle-Lift (No Panic Braking)</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="keyframe-4-text">6.5s Speed &lt; 35 MPH (Traction Restored)</span>
      </span>
      <span class="text-blue-400 font-semibold" id="legend-statute">TX Handbook Ch. 5 • TTC § 472.022</span>
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
    const imgEgoNe = document.getElementById('img-ego-ne');
    const imgEgoNw = document.getElementById('img-ego-nw');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const blinkerRight = document.getElementById('blinker-right');

    const barricadeLane1 = document.getElementById('barricade-lane1');
    const barricadeLane2 = document.getElementById('barricade-lane2');

    const hydroplanePoolGroup = document.getElementById('hydroplane-pool-group');
    const tireSprayGroup = document.getElementById('tire-spray-group');
    const sprayFront = document.getElementById('spray-front');
    const sprayRear = document.getElementById('spray-rear');

    const floodCrossingGroup = document.getElementById('flood-crossing-group');
    const depthBadgeText = document.getElementById('depth-badge-text');

    const hazardImpactGroup = document.getElementById('hazard-impact-group');
    const hazardImpactCircle = document.getElementById('hazard-impact-circle');
    const hazardImpactStar = document.getElementById('hazard-impact-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemSurface = document.getElementById('telem-surface');
    const telemSpeed = document.getElementById('telem-speed');
    const telemFriction = document.getElementById('telem-friction');
    const telemDepth = document.getElementById('telem-depth');
    const telemSteering = document.getElementById('telem-steering');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceBadge = document.getElementById('compliance-badge');
    const complianceText = document.getElementById('compliance-text');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Roadway Lane Math (Texas Suburban 2-Lane Corridor)
    // Lane 1 (South-East / Lower Lane heading NE):
    function getLane1Y(x) {{
      return 56.62 - 1.005 * (x - 50.0);
    }}
    // Lane 2 (North-West / Upper Opposing Lane):
    function getLane2Y(x) {{
      return 42.56 - 1.005 * (x - 50.0);
    }}

    function smoothCos(p) {{
      return 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, p)));
    }}

    // ===============================================================
    // MODE 1: HYDROPLANING HYDRODYNAMICS & CONTROLLED THROTTLE LIFT
    // ===============================================================
    function updateMode1(t) {{
      barricadeLane1.style.opacity = '0.0';
      barricadeLane2.style.opacity = '0.0';
      floodCrossingGroup.setAttribute('opacity', '0.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      hydroplanePoolGroup.setAttribute('opacity', '1.0');
      imgEgoNe.classList.remove('hidden');
      imgEgoNw.classList.add('hidden');
      blinkerRight.style.opacity = '0.0';
      vehEgo.style.transform = 'translate(-50%, -50%) rotate(0deg)';

      // Water pool spans x = 45% to x = 68%
      // Ego enters at x = 18%, moves to x = 82%
      // At t in [0.0, 2.0]: 52 MPH (x: 18 -> 45)
      // At t in [2.0, 4.5]: Hydroplaning in pool! Speed drops 52 -> 38 MPH (throttle lift)
      // At t in [4.5, 6.0]: Speed drops below 35 MPH (traction regained) (x: 62 -> 72)
      // At t in [6.0, 8.0]: Controlled cruising at 32 MPH (x: 72 -> 84)
      let egoX = 18.0;
      let currentSpeed = 52;
      let isHydroplaning = false;

      if (t < 2.0) {{
        egoX = 18.0 + (t / 2.0) * (45.0 - 18.0);
        currentSpeed = 52;
      }} else if (t < 4.5) {{
        isHydroplaning = true;
        const p = (t - 2.0) / 2.5;
        egoX = 45.0 + p * (62.0 - 45.0);
        currentSpeed = Math.round(52 - p * 14); // 52 -> 38 MPH
      }} else if (t < 6.0) {{
        const p = (t - 4.5) / 1.5;
        egoX = 62.0 + p * (72.0 - 62.0);
        currentSpeed = Math.round(38 - p * 6); // 38 -> 32 MPH
      }} else {{
        const p = (t - 6.0) / 2.0;
        egoX = 72.0 + p * (84.0 - 72.0);
        currentSpeed = 32;
      }}

      const egoY = getLane1Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0';

      // Spray vectors when in water pool
      if (isHydroplaning) {{
        tireSprayGroup.setAttribute('opacity', '1.0');
        const cx = egoX * 10.24; const cy = egoY * 5.71;
        sprayFront.setAttribute('cx', cx + 24);
        sprayFront.setAttribute('cy', cy - 8);
        sprayRear.setAttribute('cx', cx - 22);
        sprayRear.setAttribute('cy', cy + 12);
      }} else {{
        tireSprayGroup.setAttribute('opacity', '0.0');
      }}

      // Dynamic Tags & Telemetry
      if (t < 2.0) {{
        tagVehEgo.textContent = 'EGO: 52 MPH • WET HIGHWAY (STANDING WATER AHEAD)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Step 1: Approaching standing water at 52 MPH. At highway speeds, water depth as thin as 1/12 inch can cause complete loss of tire-road contact.';
        signalStateBadge.innerHTML = 'SURFACE: WET POOL';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        telemFriction.textContent = '0.38 (WET GRIP)';
        telemFriction.className = 'text-emerald-400 font-bold mono';
        telemSteering.textContent = '100% RESPONSIVE';
        telemSteering.className = 'text-emerald-400 font-bold mono';
      }} else if (t < 4.5) {{
        tagVehEgo.textContent = `HYDROPLANING! (${{currentSpeed}} MPH) • THROTTLE LIFT (DO NOT BRAKE!)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider animate-pulse';
        hudNarrative.textContent = 'Step 2 & 3: Hydrodynamic water wedge lifts tires completely off asphalt (0% grip!). Driver smoothly lifts off the throttle; maintains straight wheel grip without panic braking.';
        signalStateBadge.innerHTML = 'HYDROPLANING: ACTIVE';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        telemFriction.textContent = '0.05 (WATER FILM)';
        telemFriction.className = 'text-red-500 font-black mono animate-pulse';
        telemSteering.textContent = '0% (NO TRACTION)';
        telemSteering.className = 'text-red-500 font-bold mono';
      }} else {{
        tagVehEgo.textContent = `SPEED DROPPED TO ${{currentSpeed}} MPH • TIRES CUT WATER • TRACTION RESTORED`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Step 4: Speed drops below 35 MPH. Tire tread channels successfully evacuate water, settling tires back onto asphalt with full steering control restored.';
        signalStateBadge.innerHTML = 'TRACTION: REGAINED';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        telemFriction.textContent = '0.42 (RESTORED)';
        telemFriction.className = 'text-emerald-400 font-bold mono';
        telemSteering.textContent = '100% RESTORED';
        telemSteering.className = 'text-emerald-400 font-bold mono';
      }}

      telemSurface.textContent = isHydroplaning ? 'HYDROPLANING WATER FILM' : 'WET ASPHALT';
      telemSpeed.textContent = `${{currentSpeed}} MPH (${{Math.round(currentSpeed * 1.467)}} FT/S)`;
      telemDepth.textContent = isHydroplaning ? '0.35 INCHES (WEDGED)' : '0.10 INCHES';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TEXAS HYDROPLANING RULE: EASE OFF ACCELERATOR • DO NOT PANIC BRAKE';
      complianceText.textContent = 'TEXAS ADVERSE CONDITIONS COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 2: BARRICADES & "TURN AROUND, DON'T DROWN" (TTC § 472.022)
    // ===============================================================
    function updateMode2(t) {{
      hydroplanePoolGroup.setAttribute('opacity', '0.0');
      tireSprayGroup.setAttribute('opacity', '0.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';

      barricadeLane1.style.opacity = '1.0';
      barricadeLane2.style.opacity = '1.0';
      floodCrossingGroup.setAttribute('opacity', '1.0');
      depthBadgeText.textContent = 'RUSHING FLOODWATER: 20 INCHES DEEP (HIGH DANGER)';

      // Ego approaches the closed barricades at x = 45%
      // t in [0.0, 2.5]: Approaches from x = 18% to x = 38%, decelerating 35 -> 0 MPH
      // t in [2.5, 4.5]: Halts at x = 38% before barricade, assesses flood depth gauge
      // t in [4.5, 7.5]: Executes safe 3-point turnaround / reverse detour!
      let egoX = 18.0;
      let egoY = getLane1Y(18.0);
      let heading = 'NE';

      if (t < 2.5) {{
        const p = t / 2.5;
        const ease = 1 - Math.pow(1 - p, 2);
        egoX = 18.0 + ease * (38.0 - 18.0);
        egoY = getLane1Y(egoX);
        heading = 'NE';
        blinkerRight.style.opacity = '0.0';
      }} else if (t < 4.5) {{
        egoX = 38.0;
        egoY = getLane1Y(egoX);
        heading = 'NE';
        blinkerRight.style.opacity = (Math.sin(t * 12) > 0) ? '1.0' : '0.0';
      }} else {{
        // Safe Turnaround Detour: rotates smoothly towards NW
        const p = (t - 4.5) / 3.0;
        egoX = 38.0 - p * 12.0; // reverses back to x = 26%
        egoY = getLane1Y(egoX) - p * 6.0;
        heading = 'NW';
        blinkerRight.style.opacity = '0.0';
      }}

      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0';

      if (heading === 'NE') {{
        imgEgoNe.classList.remove('hidden');
        imgEgoNw.classList.add('hidden');
        vehEgo.style.transform = 'translate(-50%, -50%) rotate(0deg)';
      }} else {{
        imgEgoNe.classList.add('hidden');
        imgEgoNw.classList.remove('hidden');
        vehEgo.style.transform = 'translate(-50%, -50%) rotate(0deg)';
      }}

      if (t < 2.5) {{
        tagVehEgo.textContent = 'EGO: DECELERATING FOR CLOSED ROAD BARRICADE (TTC § 472.022)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Step 1: Driver spots official Type 3 HIGH WATER barricades blocking roadway. TTC § 472.022 mandates immediate halt before warning barricades.';
        signalStateBadge.innerHTML = 'BARRICADE: IDENTIFIED';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
      }} else if (t < 4.5) {{
        tagVehEgo.textContent = 'DEPTH GAUGE: 20 INCHES! (12" FLOATS CARS, 24" SWEEPS TRUCKS)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Step 2: Roadside depth gauge reads 20 inches of rushing current! Just 12 inches can float a car; 24 inches sweeps heavy trucks away into fatal torrents.';
        signalStateBadge.innerHTML = 'DEPTH: EXTREME DANGER';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
      }} else {{
        tagVehEgo.textContent = "EGO: \\\"TURN AROUND, DON'T DROWN\\\" • SAFE REVERSE DETOUR";
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = "Step 3 & 4: Driver executes Texas standard \\\"Turn Around, Don't Drown.\\\" Vehicle detours safely to higher ground, avoiding water rescue and severe criminal charges.";
        signalStateBadge.innerHTML = 'SAFE DETOUR: PASS';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }}

      telemSurface.textContent = 'LOW-WATER CROSSING DIP';
      telemSpeed.textContent = (t < 2.5) ? '15 MPH (STOPPING)' : (t < 4.5 ? '0 MPH (HALTED)' : '10 MPH (DETOUR)');
      telemFriction.textContent = 'BARRICADE COMPLIANT';
      telemDepth.textContent = '20 INCHES (LETHAL FLOW)';
      telemSteering.textContent = 'DETOURING SAFELY';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = "TEXAS FLOOD LAW: OBEY ALL BARRICADES (TTC § 472.022) • TURN AROUND, DON'T DROWN";
      complianceText.textContent = 'TTC § 472.022 BARRICADE COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (BARRICADE BYPASS & SWEEP-AWAY)
    // ===============================================================
    function updateMode3(t) {{
      hydroplanePoolGroup.setAttribute('opacity', '0.0');
      tireSprayGroup.setAttribute('opacity', '0.0');
      complianceBadge.style.opacity = '0.0';
      blinkerRight.style.opacity = '0.0';

      barricadeLane1.style.opacity = '1.0';
      barricadeLane2.style.opacity = '1.0';
      floodCrossingGroup.setAttribute('opacity', '1.0');
      imgEgoNe.classList.remove('hidden');
      imgEgoNw.classList.add('hidden');

      // Ego driver bypasses the barricades at x = 45%
      // Drives around barricade into rushing torrent at x = 54%
      // At t >= 3.0s: water sweeps car laterally off roadway into creek bed!
      let egoX = 18.0;
      let egoY = getLane1Y(18.0);
      let rotDeg = 0;

      if (t < 1.8) {{
        egoX = 18.0 + (t / 1.8) * (42.0 - 18.0);
        egoY = getLane1Y(egoX);
      }} else if (t < 3.0) {{
        // Swerves unlawfully around the barricade edge
        const p = (t - 1.8) / 1.2;
        egoX = 42.0 + p * (56.0 - 42.0);
        egoY = getLane1Y(egoX) + Math.sin(p * Math.PI) * 12.0; // sidetracks around post
      }} else {{
        // Caught in 20-inch torrent! Floated & swept off roadway into shoulder dip
        const p = (t - 3.0) / 2.5;
        const ease = smoothCos(Math.min(1.0, p));
        egoX = 56.0 + ease * 14.0;
        egoY = getLane1Y(egoX) + ease * 28.0; // washed down-right into flood channel
        rotDeg = ease * 55.0; // spins out of control
      }}

      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.transform = `translate(-50%, -50%) rotate(${{rotDeg}}deg)`;
      vehEgo.style.opacity = '1.0';

      if (t < 3.0) {{
        tagVehEgo.style.opacity = '1.0';
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        if (t < 1.8) {{
          tagVehEgo.textContent = 'EGO: DRIVING TOWARD CLOSED BARRICADE...';
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
          hudNarrative.textContent = 'Criminal Error in Progress: Driver approaches official TTC § 472.022 warning barricades without slowing.';
          signalStateBadge.innerHTML = 'WARNING: APPROACHING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'CRITICAL VIOLATION: SWERVING AROUND BARRICADE INTO FLOODWATER!';
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider animate-pulse';
          hudNarrative.textContent = 'Unlawful Action: Vehicle deliberately bypasses closed road barricade and plunges into 20-inch rushing floodwater torrent.';
          signalStateBadge.innerHTML = 'UNLAWFUL BYPASS';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        }}

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'DANGER: DISREGARDING OFFICIAL HIGH WATER BARRICADE VIOLATES TTC § 472.022';
      }} else {{
        // Swept away!
        tagVehEgo.style.opacity = '0.0';
        hazardImpactGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';

        const impX = egoX * 10.24;
        const impY = egoY * 5.71;
        hazardImpactCircle.setAttribute('cx', impX);
        hazardImpactCircle.setAttribute('cy', impY);
        hazardImpactStar.setAttribute('transform', `translate(${{impX}}, ${{impY}})`);

        signalStateBadge.innerHTML = 'CLASS B MISDEMEANOR';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ CRITICAL CRIMINAL STATUTORY VIOLATION: VEHICLE SWEPT AWAY IN FLOOD ✕';
        hudNarrative.textContent = 'CATASTROPHIC FLOOD SWEEP: Buoyant force lifted tires; moving water swept vehicle into creek bed. Violating TTC § 472.022 is a Class B Misdemeanor ($2,000 fine + 180 days jail) plus emergency water rescue costs.';
      }}

      telemSurface.textContent = 'RUSHING FLOOD CURRENT';
      telemSpeed.textContent = (t < 3.0) ? '25 MPH (IN WATER)' : 'SWEPT AWAY (0 GRIP)';
      telemFriction.textContent = '0.00 (BUOYANT FLOAT)';
      telemDepth.textContent = '20 INCHES (LETHAL FLOOD)';
      telemSteering.textContent = (t < 3.0) ? 'LOSING GRIP' : '0% (ROTATING IN TORRENT)';
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
          if (stepNum === 1 && t < 2.0) active = true;
          else if (stepNum === 2 && t >= 2.0 && t < 3.5) active = true;
          else if (stepNum === 3 && t >= 3.5 && t < 5.5) active = true;
          else if (stepNum === 4 && t >= 5.5) active = true;
        }} else if (currentMode === 2) {{
          if (stepNum === 1 && t < 2.5) active = true;
          else if (stepNum === 2 && t >= 2.5 && t < 4.5) active = true;
          else if (stepNum === 3 && t >= 4.5 && t < 6.5) active = true;
          else if (stepNum === 4 && t >= 6.5) active = true;
        }} else if (currentMode === 3) {{
          if (stepNum === 1 && t < 1.8) active = true;
          else if (stepNum === 2 && t >= 1.8 && t < 3.0) active = true;
          else if (stepNum === 3 && t >= 3.0 && t < 5.0) active = true;
          else if (stepNum === 4 && t >= 5.0) active = true;
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
        'Standing Water Encountered',
        'Water Wedge Lifts Tires (0% Grip)',
        'Smooth Throttle Lift (No Brake)',
        'Speed < 35 MPH: Grip Restored'
      ],
      2: [
        'Flood Barricades Identified',
        'Depth Gauge: 12" Floats Cars',
        '"Turn Around, Don\\'t Drown"',
        'Safe Detour to High Ground'
      ],
      3: [
        'Unlawful Barricade Bypass',
        'Entering 20" Rushing Torrent',
        'Buoyancy Lift & Loss of Control',
        'Swept Away (Class B Misdemeanor)'
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
          else if (m === 2) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40';
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
          else if (s === 2) targetTime = 2.8;
          else if (s === 3) targetTime = 4.8;
          else if (s === 4) targetTime = 6.8;
        }} else if (currentMode === 2) {{
          if (s === 1) targetTime = 1.2;
          else if (s === 2) targetTime = 3.2;
          else if (s === 3) targetTime = 5.2;
          else if (s === 4) targetTime = 7.0;
        }} else if (currentMode === 3) {{
          if (s === 1) targetTime = 1.0;
          else if (s === 2) targetTime = 2.4;
          else if (s === 3) targetTime = 3.6;
          else if (s === 4) targetTime = 5.2;
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

output_path = 'driving_rule_animations_suite/simulations/L05_T08_poor_conditions_flash_floods.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 17 simulation built successfully at: {output_path}")
