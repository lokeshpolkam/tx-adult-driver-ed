import os
import base64

def build_l07_t12():
    # 1. Asset Paths
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"
    truck_clean_path = r"C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\semi_truck_ne_clean.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"

    print("Encoding Lesson 28 assets to base64...")
    with open(truck_clean_path, "rb") as f:
        truck_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_yellow_path, "rb") as f:
        car_yellow_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_red_path, "rb") as f:
        car_red_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(bg_img_path, "rb") as f:
        bg_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

    print("Assets successfully encoded.")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>L07-T12: Operating Near Oversize Vehicles & Wide Convoys</title>
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
    @keyframes strobe-amber {{
      0%, 100% {{ opacity: 0.25; transform: scale(0.9); }}
      50% {{ opacity: 1.0; transform: scale(1.2); filter: drop-shadow(0 0 10px #F59E0B); }}
    }}
    .amber-strobe {{
      animation: strobe-amber 0.35s infinite ease-in-out;
    }}
    @keyframes pulse-danger {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.95); }}
      50% {{ opacity: 0.9; transform: scale(1.05); }}
    }}
    .danger-pulse {{
      animation: pulse-danger 1.0s infinite ease-in-out;
    }}
    @keyframes sweep-corridor {{
      0% {{ stroke-dashoffset: 40; }}
      100% {{ stroke-dashoffset: 0; }}
    }}
    .corridor-flow {{
      stroke-dasharray: 8, 6;
      animation: sweep-corridor 1.2s linear infinite;
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
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 28</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L07-T12: Operating Near Oversize Vehicles &amp; Wide Convoys
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          TxDMV Permitted Oversize Loads &bull; TTC &sect; 623.001 &amp; &sect; 545.062 (Buffer &amp; Safe Passing Rules)
        </p>
      </div>

      <!-- SCENARIO MODE SELECTOR -->
      <div class="flex items-center gap-2 bg-[#0B0E14] p-1.5 rounded-xl border border-[#232C3D] flex-wrap">
        <button id="mode-1" data-mode="1" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40">
          1: Lawful Convoy Trailing &amp; Pass
        </button>
        <button id="mode-2" data-mode="2" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60">
          Hazard: Narrow Bridge Pinch
        </button>
        <button id="mode-3" data-mode="3" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/60">
          Hazard: Premature Cut-In Crush
        </button>
        <label class="flex items-center gap-1.5 ml-2 text-xs text-gray-400 cursor-pointer mono">
          <input type="checkbox" id="auto-loop" checked class="rounded border-gray-700 bg-gray-900 text-blue-500 focus:ring-0">
          Auto-Loop
        </label>
      </div>
    </header>

    <!-- STEPPER NAVIGATION (MODE 1: 4 PEDAGOGICAL STEPS) -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
      <button data-step="1" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-blue-400 mono">STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-blue-400 step-dot"></span>
        </div>
        <p id="step-title-1" class="text-xs font-bold text-gray-200 mt-1 leading-snug">Detect Pilot Strobes &amp; Wide Deck</p>
      </button>

      <button data-step="2" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p id="step-title-2" class="text-xs font-bold text-gray-400 mt-1 leading-snug">Respect Convoy Buffer &amp; Straddle</p>
      </button>

      <button data-step="3" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p id="step-title-3" class="text-xs font-bold text-gray-400 mt-1 leading-snug">Pass Briskly in Passing Lane 3</p>
      </button>

      <button data-step="4" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p id="step-title-4" class="text-xs font-bold text-gray-400 mt-1 leading-snug">Mirror Check Headlights Return</p>
      </button>
    </div>

    <!-- MAIN SIMULATION CANVAS VIEWPORT -->
    <div id="simulation-container" class="relative w-full aspect-[16/10.5] max-h-[640px] bg-[#0E131E] rounded-2xl border border-[#232C3D] overflow-hidden shadow-2xl">

      <!-- ISOMETRIC 3-LANE TEXAS HIGHWAY BASE LAYER -->
      <img src="{bg_b64}" alt="Texas Highway 3-Lane Corridor" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none" />

      <!-- LAYER 1: SVG SPATIAL OVERLAYS (BUFFER BRACKETS, OVERHANG ENVELOPE, SIGHTLINES, HAZARDS) -->
      <svg id="sim-svg-layer" viewBox="0 0 1280 840" class="absolute inset-0 w-full h-full pointer-events-none select-none z-10">
        <defs>
          <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#3B82F6" />
          </marker>
          <marker id="arrow-emerald" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#10B981" />
          </marker>
          <marker id="arrow-danger" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#EF4444" />
          </marker>
          <!-- Radial gradient for amber hazard pinch -->
          <radialGradient id="grad-pinch" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#EF4444" stop-opacity="0.8" />
            <stop offset="60%" stop-color="#EF4444" stop-opacity="0.2" />
            <stop offset="100%" stop-color="#EF4444" stop-opacity="0.0" />
          </radialGradient>
        </defs>

        <!-- OVERSIZE CONVOY OVERHANG SAFETY ENVELOPE (14-FT WIDE LOAD FOOTPRINT) -->
        <g id="overhang-safety-group" opacity="1.0">
          <!-- Lateral Overhang Zone spanning into Lane 2 -->
          <polygon id="overhang-poly" points="490,440 680,310 740,360 550,490" fill="#F59E0B" fill-opacity="0.14" stroke="#F59E0B" stroke-width="1.8" stroke-dasharray="6,4" />
          <text id="overhang-badge-txt" x="610" y="445" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="800" text-anchor="middle" letter-spacing="1">
            ⚠ 14-FT WIDE LOAD • 3-FT LATERAL OVERHANG INTO LANE 2
          </text>
        </g>

        <!-- 200+ FT TRAILING REAR BUFFER BRACKET -->
        <g id="rear-buffer-bracket-group" opacity="1.0">
          <path id="rear-buffer-bracket" d="M 360,540 L 520,430" fill="none" stroke="#3B82F6" stroke-width="2.5" stroke-dasharray="5,4" />
          <g id="buffer-badge" transform="translate(440, 480)">
            <rect x="-85" y="-10" width="170" height="20" rx="10" fill="#0B132B" stroke="#3B82F6" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#93C5FD" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="800" text-anchor="middle">
              SAFE 200+ FT CONVOY BUFFER
            </text>
          </g>
        </g>

        <!-- SAFE PASSING CORRIDOR IN LANE 3 -->
        <g id="passing-corridor-group" opacity="0.0">
          <path id="corridor-path" d="M 380,520 L 780,240" fill="none" stroke="#10B981" stroke-width="3" class="corridor-flow" marker-end="url(#arrow-emerald)" />
          <g id="corridor-badge" transform="translate(580, 240)">
            <rect x="-105" y="-10" width="210" height="20" rx="10" fill="#064E3B" stroke="#10B981" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#A7F3D0" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="800" text-anchor="middle">
              LANE 3: UNIMPEDED PASSING CORRIDOR
            </text>
          </g>
        </g>

        <!-- REARVIEW MIRROR SIGHTLINE CONE (STEP 4) -->
        <g id="mirror-cone-group" opacity="0.0">
          <!-- Cone extending from Ego's rearview mirror back to Lead Pilot headlights -->
          <polygon id="mirror-cone-poly" points="1010,210 880,310 930,345" fill="#3B82F6" fill-opacity="0.18" stroke="#60A5FA" stroke-width="1.2" stroke-dasharray="4,3" />
          <line x1="1010" y1="210" x2="895" y2="315" stroke="#60A5FA" stroke-width="1.5" stroke-dasharray="4,2" />
          <line x1="1010" y1="210" x2="925" y2="335" stroke="#60A5FA" stroke-width="1.5" stroke-dasharray="4,2" />
          <g id="mirror-badge" transform="translate(945, 260)">
            <rect x="-95" y="-9" width="190" height="18" rx="9" fill="#1E293B" stroke="#60A5FA" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#BFDBFE" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" text-anchor="middle">
              ✓ BOTH PILOT HEADLIGHTS IN REARVIEW
            </text>
          </g>
        </g>

        <!-- MODE 2 HAZARD: NARROW BRIDGE / BOTTLENECK PINCH -->
        <g id="bridge-pinch-hazard-group" opacity="0.0">
          <circle cx="690" cy="380" r="45" fill="url(#grad-pinch)" class="danger-pulse" />
          <line x1="650" y1="410" x2="730" y2="350" stroke="#EF4444" stroke-width="3" stroke-dasharray="5,4" />
          <g transform="translate(690, 380)">
            <polygon points="0,-16 5,-5 16,-5 8,4 11,16 0,9 -11,16 -8,4 -16,-5 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
          </g>
          <g id="pinch-callout" transform="translate(690, 440)">
            <rect x="-105" y="-12" width="210" height="24" rx="12" fill="#450A0A" stroke="#EF4444" stroke-width="1.5" />
            <text x="0" y="3.5" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="900" text-anchor="middle">
              💥 LATERAL PINCH: 0 ROOM IN BOTTLENECK!
            </text>
          </g>
        </g>

        <!-- MODE 3 HAZARD: PREMATURE CUT-IN 400+ FT STOPPING HAZARD -->
        <g id="cut-in-hazard-group" opacity="0.0">
          <!-- 400+ FT Stopping Distance Requirement Bracket -->
          <path d="M 640,430 L 800,320" fill="none" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" />
          <circle cx="730" cy="370" r="42" fill="url(#grad-pinch)" class="danger-pulse" />
          <g id="cut-in-callout" transform="translate(730, 420)">
            <rect x="-110" y="-12" width="220" height="24" rx="12" fill="#450A0A" stroke="#EF4444" stroke-width="1.5" />
            <text x="0" y="3.5" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">
              💥 400+ FT STOPPING DEFICIT: REAR OVERRIDE
            </text>
          </g>
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- LEAD PILOT ESCORT VEHICLE (YELLOW SEDAN WITH AMBER STROBE ROOF BAR & OVERSIZE BANNER) -->
      <div id="veh-pilot" class="absolute z-20 pointer-events-none transition-transform" style="left: 70.0%; top: 36.5%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[215/153] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Lead Pilot Escort Car" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
          
          <!-- Roof-Mounted High-Intensity Amber Lightbar -->
          <div class="absolute -top-1.5 left-1/2 -translate-x-1/2 flex items-center gap-1 bg-[#1A1A1A] px-1 py-0.5 rounded border border-amber-500/80 shadow-md">
            <span class="w-2 h-2 rounded-full bg-amber-400 amber-strobe"></span>
            <span class="text-[6.5px] font-black text-amber-300 mono whitespace-nowrap tracking-tighter">PILOT</span>
            <span class="w-2 h-2 rounded-full bg-amber-400 amber-strobe"></span>
          </div>

          <!-- Rooftop OVERSIZE LOAD Banner Sign -->
          <div class="absolute -top-5 left-1/2 -translate-x-1/2 bg-amber-400 text-black px-1.5 py-0.2 rounded-sm border border-amber-600 font-black text-[6px] tracking-tight whitespace-nowrap shadow-md">
            OVERSIZE LOAD
          </div>
        </div>

        <div id="tag-veh-pilot" class="absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/95 border border-amber-500/50 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          LEAD PILOT: 50 MPH (AMBER STROBES)
        </div>
      </div>

      <!-- OVERSIZE LOAD COMMERCIAL RIG (CLASS 8 TRACTOR WITH 14-FT WIDE DECK) -->
      <div id="veh-truck" class="absolute z-19 pointer-events-none transition-transform" style="left: 48.0%; top: 58.6%; transform: translate(-50%, -50%);">
        <div id="veh-truck-sprite" class="relative w-48 aspect-[1264/768] flex items-center justify-center">
          <img src="{truck_b64}" alt="Oversize Commercial Transport Rig" class="w-full h-full object-contain filter drop-shadow-[0_16px_16px_rgba(0,0,0,0.85)]" />
          
          <!-- Cab Rooftop Amber Flashing Beacon -->
          <div class="absolute top-[28%] right-[18%] w-3 h-3 rounded-full bg-amber-400 amber-strobe filter blur-[0.5px]"></div>
          
          <!-- Red Wide-Load Corner Warning Flags -->
          <!-- Rear-Left Flag -->
          <div class="absolute top-[52%] left-[3%] w-2 h-2 bg-red-600 rounded-xs border border-red-300 shadow"></div>
          <!-- Rear-Right Flag -->
          <div class="absolute top-[75%] left-[16%] w-2 h-2 bg-red-600 rounded-xs border border-red-300 shadow"></div>
          <!-- Front-Left Wide Overhang Flag -->
          <div class="absolute top-[20%] right-[32%] w-2 h-2 bg-red-600 rounded-xs border border-red-300 shadow"></div>

          <!-- Rear Bumper OVERSIZE LOAD Warning Banner -->
          <div class="absolute top-[68%] left-[4%] bg-amber-400 text-black px-1 py-0.2 rounded-xs border border-amber-700 font-black text-[5.5px] tracking-tighter whitespace-nowrap shadow">
            OVERSIZE LOAD
          </div>
        </div>

        <div id="tag-veh-truck" class="absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#0F141E]/95 border border-blue-500/50 text-[9.5px] font-bold text-blue-300 mono shadow-xl tracking-wider">
          OVERSIZE RIG: 50 MPH • 14-FT WIDE LOAD
        </div>
      </div>

      <!-- EGO VEHICLE (RED/ORANGE DEFENSIVE SEDAN) -->
      <div id="veh-ego" class="absolute z-21 pointer-events-none transition-transform" style="left: 28.0%; top: 64.6%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[215/153] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Ego Defensive Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
          
          <!-- Turn Signal Indicator (Left) -->
          <div id="blinker-left" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 28%; right: 28%;"></div>
          <!-- Turn Signal Indicator (Right) -->
          <div id="blinker-right" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 58%; right: 12%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-3.5 h-1.5 rounded bg-red-500 filter blur-[1px] opacity-0" style="top: 65%; left: 8%;"></div>
        </div>

        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: 55 MPH • 200+ FT TRAILING BUFFER
        </div>
      </div>

      <!-- LAYER 3: TELEMETRY HUD & CONTROL OVERLAYS -->

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute top-4 left-72 z-30 pointer-events-none flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#0E131E]/90 border border-blue-500/40 backdrop-blur-md shadow-lg">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
        <span id="pill-status-text" class="text-xs font-bold text-blue-300 mono">
          CONVOY IDENTIFICATION: RESPECT OVERSIZE PILOT STROBES &amp; 14-FT FOOTPRINT
        </span>
      </div>

      <!-- TELEMETRY HUD CARD (LEFT OVERLAY) -->
      <div id="telemetry-hud-card" class="absolute top-4 left-4 z-30 w-[270px] bg-[#0E131E]/95 border border-[#232C3D] rounded-xl p-3.5 backdrop-blur-md shadow-2xl flex flex-col gap-2.5">
        <div class="flex items-center justify-between border-b border-gray-800 pb-2">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-500"></span>
            <span class="text-xs font-extrabold text-white tracking-wider mono uppercase">CONVOY RADAR HUD</span>
          </div>
          <span id="compliance-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">
            MONITORING
          </span>
        </div>

        <div class="space-y-1.5 text-xs">
          <div class="flex justify-between items-center text-gray-400">
            <span>Ego Speed:</span>
            <span id="telem-speed" class="font-bold text-white mono">55 MPH (CRUISING)</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Convoy Buffer:</span>
            <span id="telem-buffer" class="font-bold text-emerald-400 mono">220 FT (> 4.0s)</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Load Width:</span>
            <span id="telem-width" class="font-bold text-amber-400 mono">14 FT (OVERHANG)</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Escort Warning:</span>
            <span id="telem-escort" class="font-bold text-amber-400 mono">AMBER STROBES ACTIVE</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Mirror Sightline:</span>
            <span id="telem-mirror" class="font-bold text-gray-300 mono">BEHIND CONVOY</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Legal Status:</span>
            <span id="telem-legal" class="font-bold text-emerald-400 mono">TTC § 623.001 LAWFUL</span>
          </div>
        </div>

        <div class="border-t border-gray-800 pt-2">
          <p id="hud-narrative" class="text-[11px] text-gray-300 leading-relaxed">
            Step 1: Motorist observes amber strobe beacons and "OVERSIZE LOAD" signs. Drops speed to match convoy flow and establishes a 200+ foot following cushion outside the truck's rear blind zone.
          </p>
        </div>
      </div>

      <!-- CRITICAL HAZARD CALLOUT BANNER -->
      <div id="hazard-banner" class="absolute top-4 left-1/2 -translate-x-1/2 z-30 max-w-md w-full px-4 py-2.5 rounded-xl bg-red-950/90 border border-red-500 text-center shadow-2xl transition-opacity duration-300 opacity-0 pointer-events-none">
        <div id="hazard-banner-title" class="text-xs font-black text-red-400 mono tracking-wider uppercase">
          CRITICAL HAZARD: NARROW BRIDGE PINCH
        </div>
        <div id="hazard-banner-body" class="text-[11px] text-gray-200 mt-0.5 leading-snug">
          Attempting to squeeze alongside a 14-foot wide transport deck at a bridge chokepoint violates TTC § 623.001 and causes an unavoidable lateral crush.
        </div>
      </div>

    </div>

    <!-- SCRUBBER TIMELINE CONTROLS -->
    <div class="bg-[#121722] border border-[#232C3D] rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="flex items-center gap-3 w-full md:w-auto">
        <button id="btn-play-pause" class="w-10 h-10 rounded-xl bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center shadow-lg transition">
          <svg id="icon-play" class="w-5 h-5 hidden" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
          <svg id="icon-pause" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>

        <button id="btn-reset" class="px-3 py-2 rounded-xl bg-[#1A2232] hover:bg-[#232C3D] text-xs font-bold text-gray-300 mono transition">
          Reset (0s)
        </button>

        <div class="flex items-center gap-2">
          <button id="btn-step-back" class="p-2 rounded-lg bg-[#1A2232] hover:bg-[#232C3D] text-gray-300 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <button id="btn-step-fwd" class="p-2 rounded-lg bg-[#1A2232] hover:bg-[#232C3D] text-gray-300 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </button>
        </div>

        <span id="time-display" class="text-sm font-black text-white mono ml-2">0.00s</span>
      </div>

      <div class="w-full flex-1 flex items-center gap-3">
        <span class="text-xs text-gray-500 mono">0.0s</span>
        <input type="range" id="timeline-slider" min="0" max="5.0" step="0.05" value="0.0" class="timeline-slider w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer" />
        <span class="text-xs text-gray-500 mono">5.0s</span>
      </div>
    </div>

  </div>

  <!-- EMBEDDED KINEMATIC & ANIMATION ENGINE -->
  <script>
    // State management
    let currentMode = 1;
    let currentTime = 0.0;
    const duration = 5.0;
    let isPlaying = true;
    let lastTimestamp = null;

    // DOM Elements
    const timeDisplay = document.getElementById('time-display');
    const timelineSlider = document.getElementById('timeline-slider');
    const btnPlayPause = document.getElementById('btn-play-pause');
    const iconPlay = document.getElementById('icon-play');
    const iconPause = document.getElementById('icon-pause');
    const autoLoop = document.getElementById('auto-loop');
    const pillStatusText = document.getElementById('pill-status-text');
    const complianceBadge = document.getElementById('compliance-badge');
    const hazardBanner = document.getElementById('hazard-banner');
    const hazardBannerTitle = document.getElementById('hazard-banner-title');
    const hazardBannerBody = document.getElementById('hazard-banner-body');

    // Telemetry fields
    const telemSpeed = document.getElementById('telem-speed');
    const telemBuffer = document.getElementById('telem-buffer');
    const telemWidth = document.getElementById('telem-width');
    const telemEscort = document.getElementById('telem-escort');
    const telemMirror = document.getElementById('telem-mirror');
    const telemLegal = document.getElementById('telem-legal');
    const hudNarrative = document.getElementById('hud-narrative');

    // Vehicles
    const vehPilot = document.getElementById('veh-pilot');
    const tagVehPilot = document.getElementById('tag-veh-pilot');

    const vehTruck = document.getElementById('veh-truck');
    const tagVehTruck = document.getElementById('tag-veh-truck');

    const vehEgo = document.getElementById('veh-ego');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const blinkerLeft = document.getElementById('blinker-left');
    const blinkerRight = document.getElementById('blinker-right');
    const brakeLights = document.getElementById('brake-lights');

    // SVG Overlays
    const overhangGroup = document.getElementById('overhang-safety-group');
    const rearBufferGroup = document.getElementById('rear-buffer-bracket-group');
    const passingCorridorGroup = document.getElementById('passing-corridor-group');
    const mirrorConeGroup = document.getElementById('mirror-cone-group');
    const bridgePinchGroup = document.getElementById('bridge-pinch-hazard-group');
    const cutInHazardGroup = document.getElementById('cut-in-hazard-group');

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
        {{ time: 0.8, title: "Detect Pilot Strobes & Wide Deck" }},
        {{ time: 2.2, title: "Respect Convoy Buffer & Straddle" }},
        {{ time: 3.6, title: "Pass Briskly in Passing Lane 3" }},
        {{ time: 5.0, title: "Mirror Check Headlights Return" }}
      ],
      2: [
        {{ time: 0.8, title: "Convoy Enters Bridge Corridor" }},
        {{ time: 2.2, title: "Ego Squeezes Alongside Deck" }},
        {{ time: 3.6, title: "14-FT Deck Pinches Guardrail" }},
        {{ time: 5.0, title: "Catastrophic Barrier Crush" }}
      ],
      3: [
        {{ time: 0.8, title: "Ego Passes Oversize Rig" }},
        {{ time: 2.2, title: "Abrupt Cut-In Front of Truck" }},
        {{ time: 3.6, title: "80,000 LB Braking Deficit" }},
        {{ time: 5.0, title: "Fatal Underride Rear Impact" }}
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40';
          else if (m === 2) btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500 bg-red-600 text-white shadow-md shadow-red-900/40';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500 bg-amber-600 text-white shadow-md shadow-amber-900/40';
        }} else {{
          if (m === 2) btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60';
          else if (m === 3) btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/60';
          else btn.className = 'mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-[#232C3D] bg-[#0B0E14] text-gray-400 hover:text-white';
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

      // Convoy kinematics in Lane 1
      const convoySpeed = 50.0;
      // Convoy moves steadily SW to NE
      const truckX = 46.0 + (t / duration) * 8.0; // 46% to 54%
      const truckY = getLane1Y(truckX);
      vehTruck.style.left = `${{truckX}}%`;
      vehTruck.style.top = `${{truckY}}%`;

      const pilotX = truckX + 26.0; // 72% to 80% in Lane 1
      const pilotY = getLane1Y(pilotX);
      vehPilot.style.left = `${{pilotX}}%`;
      vehPilot.style.top = `${{pilotY}}%`;

      // Update Overhang Polygon coordinates to follow truck
      // Screen points approximate: truck center at (truckX * 12.8, truckY * 8.4)
      const cx = truckX * 12.8;
      const cy = truckY * 8.4;
      // Overhang points:
      const p1 = `${{cx - 120}},${{cy - 10}}`;
      const p2 = `${{cx + 70}},${{cy - 130}}`;
      const p3 = `${{cx + 140}},${{cy - 80}}`;
      const p4 = `${{cx - 50}},${{cy + 40}}`;
      document.getElementById('overhang-poly').setAttribute('points', `${{p1}} ${{p2}} ${{p3}} ${{p4}}`);
      const txtElem = document.getElementById('overhang-badge-txt');
      txtElem.setAttribute('x', `${{cx - 30}}`);
      txtElem.setAttribute('y', `${{cy - 100}}`);

      // =========================================================================
      // MODE 1: LAWFUL CONVOY TRAILING & SAFE MULTI-LANE PASS (THE APPROVED STANDARD)
      // =========================================================================
      if (currentMode === 1) {{
        bridgePinchGroup.setAttribute('opacity', '0.0');
        cutInHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        document.getElementById('hud-status-pill').style.opacity = '1.0';
        brakeLights.style.opacity = '0.0';
        overhangGroup.setAttribute('opacity', '1.0');

        let egoX, egoY, egoSpeed;

        if (t < 1.6) {{
          // Step 1: Detect Pilot Strobes & 14-FT Wide Deck
          const p = t / 1.6;
          egoX = 26.0 + p * 3.0; // 26% to 29% in Lane 2
          egoY = getLane2Y(egoX);
          egoSpeed = 55;

          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = '0.0';
          rearBufferGroup.setAttribute('opacity', '1.0');
          passingCorridorGroup.setAttribute('opacity', '0.0');
          mirrorConeGroup.setAttribute('opacity', '0.0');

          // Rear Buffer Bracket connects Ego front to Truck rear
          const egoCx = egoX * 12.8 + 40;
          const egoCy = egoY * 8.4;
          const trkCx = truckX * 12.8 - 90;
          const trkCy = truckY * 8.4 + 20;
          document.getElementById('rear-buffer-bracket').setAttribute('d', `M ${{egoCx}},${{egoCy}} L ${{trkCx}},${{trkCy}}`);
          document.getElementById('buffer-badge').setAttribute('transform', `translate(${{(egoCx + trkCx)/2}}, ${{(egoCy + trkCy)/2 - 28}})`);

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: 55 MPH • DETECTS OVERSIZE ESCORT';

          telemSpeed.textContent = '55 MPH (DECELERATING)';
          telemBuffer.textContent = '220 FT (> 4.0s)';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemWidth.textContent = '14 FT (3-FT OVERHANG)';
          telemEscort.textContent = 'AMBER STROBES DETECTED';
          telemMirror.textContent = 'BEHIND CONVOY';
          telemLegal.textContent = 'TTC § 623.001 LAWFUL';

          complianceBadge.textContent = 'MONITORING';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 1: Driver observes lead pilot amber strobes and wide transport banners. Drops speed to 55 mph and holds a protective 200+ foot following cushion.';
        }} else if (t < 3.0) {{
          // Step 2: Respect Convoy Buffer & Lane Straddle
          const p = (t - 1.6) / 1.4;
          egoX = 29.0 + p * 3.0; // 29% to 32% in Lane 2
          egoY = getLane2Y(egoX);
          egoSpeed = 52;

          blinkerLeft.style.opacity = blinkOn ? '1.0' : '0.0'; // begins signaling left
          blinkerRight.style.opacity = '0.0';
          rearBufferGroup.setAttribute('opacity', '1.0');
          passingCorridorGroup.setAttribute('opacity', '0.0');
          mirrorConeGroup.setAttribute('opacity', '0.0');

          const egoCx = egoX * 12.8 + 40;
          const egoCy = egoY * 8.4;
          const trkCx = truckX * 12.8 - 90;
          const trkCy = truckY * 8.4 + 20;
          document.getElementById('rear-buffer-bracket').setAttribute('d', `M ${{egoCx}},${{egoCy}} L ${{trkCx}},${{trkCy}}`);
          document.getElementById('buffer-badge').setAttribute('transform', `translate(${{(egoCx + trkCx)/2}}, ${{(egoCy + trkCy)/2 - 28}})`);

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: SIGNALS LEFT • PREPARES PASS';

          telemSpeed.textContent = '52 MPH (CHECKING MIRRORS)';
          telemBuffer.textContent = '210 FT (SAFE)';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemWidth.textContent = '14 FT (LANE 2 OVERHANG)';
          telemEscort.textContent = 'LEAD & TRUCK WARNINGS';
          telemMirror.textContent = 'CHECKING BLIND SPOT';
          telemLegal.textContent = 'TTC § 545.104 COMPLIANT';

          complianceBadge.textContent = 'SIGNALING';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 2: Respect convoy integrity. Because the 14-ft deck overhangs into Lane 2, driver activates left signal 100 ft prior and plans pass via outer Lane 3.';
        }} else if (t < 4.4) {{
          // Step 3: Pass Briskly in Passing Lane 3
          const p = (t - 3.0) / 1.4;
          egoX = 32.0 + p * 24.0; // 32% to 56% in Lane 3
          // Lane transition from Lane 2 to Lane 3 during first 0.4s
          const laneP = Math.min(1.0, p * 2.5);
          const y2 = getLane2Y(egoX);
          const y3 = getLane3Y(egoX);
          egoY = y2 + laneP * (y3 - y2);
          egoSpeed = 65;

          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = '0.0';
          rearBufferGroup.setAttribute('opacity', '0.0');
          passingCorridorGroup.setAttribute('opacity', '1.0');
          mirrorConeGroup.setAttribute('opacity', '0.0');

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: 65 MPH • PASSING IN LANE 3';

          telemSpeed.textContent = '65 MPH (BRISK PASS)';
          telemBuffer.textContent = 'LATERAL SEPARATION > 10 FT';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemWidth.textContent = 'CLEARED OVERHANG';
          telemEscort.textContent = 'PASSING PILOT VEHICLE';
          telemMirror.textContent = 'ALONGSIDE CONVOY';
          telemLegal.textContent = 'TTC § 545.053 COMPLIANT';

          complianceBadge.textContent = 'PASSING';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
          hudNarrative.textContent = 'Step 3: Accelerate briskly in Lane 3. Never linger alongside wide trailer wheels or cargo overhang. Ensure generous lateral clearance across the white dividing line.';
        }} else {{
          // Step 4: Mirror Check Headlights Return
          const p = (t - 4.4) / 0.6;
          egoX = 58.0 + p * 10.0; // 58% to 68% in Lane 3
          const y3 = getLane3Y(egoX);
          const y2 = getLane2Y(egoX);
          egoY = y3 + p * 0.4 * (y2 - y3); // beginning smooth return
          egoSpeed = 65;

          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          rearBufferGroup.setAttribute('opacity', '0.0');
          passingCorridorGroup.setAttribute('opacity', '0.0');
          mirrorConeGroup.setAttribute('opacity', '1.0');

          // Update Mirror Cone points
          const egoMirrorX = egoX * 12.8 - 10;
          const egoMirrorY = egoY * 8.4 + 5;
          const pilotFrontX = pilotX * 12.8 - 40;
          const pilotFrontY = pilotY * 8.4 - 15;
          document.getElementById('mirror-cone-poly').setAttribute('points', `${{egoMirrorX}},${{egoMirrorY}} ${{pilotFrontX - 25}},${{pilotFrontY + 20}} ${{pilotFrontX + 25}},${{pilotFrontY + 50}}`);
          document.getElementById('mirror-badge').setAttribute('transform', `translate(${{(egoMirrorX + pilotFrontX)/2 - 10}}, ${{(egoMirrorY + pilotFrontY)/2 - 10}})`);

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: CONFIRMED PILOT IN REARVIEW MIRROR';

          telemSpeed.textContent = '65 MPH (SAFE MERGE)';
          telemBuffer.textContent = 'CLEAR (> 180 FT AHEAD)';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemWidth.textContent = 'ENTIRE CONVOY CLEARED';
          telemEscort.textContent = 'BOTH HEADLIGHTS VISIBLE';
          telemMirror.textContent = 'VERIFIED IN MIRROR';
          telemLegal.textContent = 'TTC § 545.053 LAWFUL RETURN';

          complianceBadge.textContent = 'MIRROR VERIFIED';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500 text-black mono';
          hudNarrative.textContent = 'Step 4: Return to travel lane only when both headlights of the lead escort car are clearly visible in the interior rearview mirror. Signal right and merge safely.';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        pillStatusText.textContent = 'LAWFUL: HOLD 200+ FT BUFFER • PASS ON LEFT • CONFIRM HEADLIGHTS IN MIRROR';
      }}

      // =========================================================================
      // MODE 2: CRITICAL HAZARD: NARROW BRIDGE / BOTTLENECK PINCH
      // =========================================================================
      else if (currentMode === 2) {{
        overhangGroup.setAttribute('opacity', '1.0');
        rearBufferGroup.setAttribute('opacity', '0.0');
        passingCorridorGroup.setAttribute('opacity', '0.0');
        mirrorConeGroup.setAttribute('opacity', '0.0');
        bridgePinchGroup.setAttribute('opacity', '1.0');
        cutInHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '1.0';
        document.getElementById('hud-status-pill').style.opacity = '0.0';
        blinkerLeft.style.opacity = '0.0';
        blinkerRight.style.opacity = '0.0';
        brakeLights.style.opacity = '1.0';

        hazardBannerTitle.textContent = 'CRITICAL HAZARD: NARROW BRIDGE PINCH';
        hazardBannerBody.innerHTML = '<strong>ILLEGAL ATTEMPT TO PASS OVERSIZE DECK AT CHOKEPOINT</strong><br>A 14-foot wide deck straddles travel lanes. Squeezing alongside at bridges or bottlenecks pinches vehicles into concrete barriers.';

        // Ego attempts to squeeze alongside in Lane 2 right at the truck
        const egoX = truckX + 2.0; // side-by-side at x ≈ 52%
        const egoY = getLane2Y(egoX) + 2.5; // forced towards pinch
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
        tagVehEgo.textContent = 'EGO: PINCHED AGAINST BRIDGE BARRIER!';

        telemSpeed.textContent = '0 MPH (IMPACT)';
        telemBuffer.textContent = '0 FT (LATERAL CRUSH)';
        telemBuffer.className = 'font-bold text-red-500 mono text-right';
        telemWidth.textContent = '14 FT DECK OCCUPIES LANE 2';
        telemEscort.textContent = 'IGNORED PILOT CHOKEPOINT WARNING';
        telemMirror.textContent = 'BLIND CRUSH ZONE';
        telemLegal.textContent = 'TTC § 623.001 VIOLATION';
        telemLegal.className = 'font-bold text-red-500 mono text-right';

        complianceBadge.textContent = 'CRITICAL CRASH';
        complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
        pillStatusText.textContent = 'CRITICAL ERROR: NEVER PASS AN OVERSIZE CONVOY AT BRIDGES OR ROADWAY RESTRICTIONS!';
        hudNarrative.textContent = 'Catastrophic Error: Driver attempts to overtake an oversize load approaching a narrow bridge structure. The wide deck leaves zero lateral clearance, crushing the vehicle into the concrete barrier.';
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: PREMATURE CUT-IN FRONT OF 80,000 LB CMV
      // =========================================================================
      else if (currentMode === 3) {{
        overhangGroup.setAttribute('opacity', '0.0');
        rearBufferGroup.setAttribute('opacity', '0.0');
        passingCorridorGroup.setAttribute('opacity', '0.0');
        mirrorConeGroup.setAttribute('opacity', '0.0');
        bridgePinchGroup.setAttribute('opacity', '0.0');
        cutInHazardGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';
        document.getElementById('hud-status-pill').style.opacity = '0.0';
        blinkerLeft.style.opacity = '0.0';
        blinkerRight.style.opacity = '0.0';
        brakeLights.style.opacity = '1.0';

        hazardBannerTitle.textContent = 'CRITICAL HAZARD: PREMATURE CUT-IN FRONT NO-ZONE';
        hazardBannerBody.innerHTML = "<strong>INSUFFICIENT BUFFER FOR 80,000-LB COMMERCIAL RIG</strong><br>Cutting back into the lane &lt; 150 ft in front removes the truck's 400+ foot stopping distance, causing an override rear-end crash.";

        // Ego cuts directly in front of the truck in Lane 1
        const egoX = truckX + 4.5; // only 4.5% (< 18 ft) ahead of heavy truck
        const egoY = getLane1Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        const cutCx = egoX * 12.8;
        const cutCy = egoY * 8.4;
        document.getElementById('cut-in-callout').setAttribute('transform', `translate(${{cutCx - 30}}, ${{cutCy - 65}})`);

        tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
        tagVehEgo.textContent = 'EGO: ABRUPT CUT-IN (< 20 FT FRONT BUFFER)!';

        telemSpeed.textContent = '0 MPH (IMPACT)';
        telemBuffer.textContent = '< 20 FT (400 FT DEFICIT)';
        telemBuffer.className = 'font-bold text-red-500 mono text-right';
        telemWidth.textContent = '80,000 LB GROSS WEIGHT';
        telemEscort.textContent = 'CMV AIR BRAKES LOCKED';
        telemMirror.textContent = 'NO MIRROR VERIFICATION';
        telemLegal.textContent = 'TTC § 545.053 VIOLATION';
        telemLegal.className = 'font-bold text-red-500 mono text-right';

        complianceBadge.textContent = 'FATAL OVERRIDE';
        complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
        pillStatusText.textContent = 'CRITICAL ERROR: NEVER CUT IN FRONT OF HEAVY RIG UNTIL HEADLIGHTS ARE VISIBLE IN MIRROR!';
        hudNarrative.textContent = 'Fatal Error: Driver passes truck but cuts sharply in front without verifying mirror sightlines. A loaded commercial rig requires over 400 feet to stop from highway speeds, resulting in a fatal override.';
      }}

      // Step cards highlight
      const steps = stepConfigs[currentMode];
      steps.forEach((cfg, idx) => {{
        const btn = document.querySelector(`.step-card[data-step='${{idx + 1}}']`);
        const dot = btn.querySelector('.step-dot');
        const num = btn.querySelector('span:first-child');
        const title = btn.querySelector('p');

        const isCurrent = (t >= cfg.time - 0.7 && t <= cfg.time + 0.7);
        if (isCurrent) {{
          btn.className = 'step-card group text-left p-2.5 rounded-xl border border-blue-500 bg-[#162032] shadow-md shadow-blue-900/20 transition';
          dot.className = 'w-1.5 h-1.5 rounded-full bg-blue-400 step-dot';
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

    output_path = os.path.abspath("driving_rule_animations_suite/simulations/L07_T12_oversize_vehicles.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 28 simulation built successfully at: {output_path}")

if __name__ == '__main__':
    build_l07_t12()
