import os
import base64

def build_l07_t03():
    # 1. Load and base64-encode image assets
    truck_clean_path = r"C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\semi_truck_ne_clean.png"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"

    print("Encoding Lesson 25 assets to base64...")
    with open(truck_clean_path, "rb") as f:
        truck_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
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
  <title>L07-T03: Laws for Sharing the Road — Commercial Motor Vehicles & The 4 No-Zones</title>
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
    @keyframes pulse-danger {{
      0%, 100% {{ opacity: 0.85; transform: scale(1); }}
      50% {{ opacity: 0.35; transform: scale(1.05); }}
    }}
    .danger-pulse {{
      animation: pulse-danger 1.4s ease-in-out infinite;
    }}
    @keyframes blink-amber {{
      0%, 100% {{ opacity: 1; filter: drop-shadow(0 0 8px #F59E0B); }}
      50% {{ opacity: 0.1; }}
    }}
    .blinker-active {{
      animation: blink-amber 0.6s step-end infinite;
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
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-amber-500/20 text-amber-400 border border-amber-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 25</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L07-T03: Laws for Sharing the Road — Commercial Trucks & The 4 No-Zones
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Driver Handbook Chapter 7 &bull; Texas Transportation Code § 545.062 (Stopping Distance) & § 545.054 (Passing Clearance)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40" data-mode="1">
          1: CMV 4 No-Zones & Safe Passing
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: Stopping Distance Physics (400 FT)
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Wide Right-Turn Squeeze
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
      <button class="step-card bg-[#121824] border border-blue-500/40 rounded-xl p-2.5 text-left transition hover:border-blue-400 group relative overflow-hidden" data-step="1">
        <div class="text-[10px] font-bold text-blue-400 mono flex items-center justify-between">
          <span>STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        </div>
        <div id="step-title-1" class="text-xs font-bold text-white mt-1 group-hover:text-blue-200">Identify 4 CMV No-Zones</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Lane 3 Passing Acceleration</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Rearview Mirror Cab Check</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Safe 200-Ft Forward Re-Entry</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG DYNAMIC NO-ZONES, SIGHTLINE RAYS & BRAKING BRACKETS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <pattern id="no-zone-hatch-red" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="10" stroke="#EF4444" stroke-width="2.5" opacity="0.45" />
          </pattern>
          <pattern id="no-zone-hatch-amber" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="10" stroke="#F59E0B" stroke-width="2.5" opacity="0.4" />
          </pattern>
          <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#3B82F6" />
          </marker>
          <marker id="arrow-danger" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#EF4444" />
          </marker>
        </defs>

        <!-- MODE 1 & 2: THE 4 COMMERCIAL MOTOR VEHICLE (CMV) NO-ZONES -->
        <g id="cmv-no-zones-group" opacity="1.0">
          <!-- 1. Front No-Zone (20 ft ahead of cab) -->
          <polygon id="zone-front" points="0,0 0,0 0,0 0,0" fill="url(#no-zone-hatch-red)" stroke="#EF4444" stroke-width="1.5" />
          <g id="badge-front-nozone" transform="translate(0, 0)">
            <rect x="-55" y="-7" width="110" height="14" rx="7" fill="#450A0A" stroke="#EF4444" stroke-width="1" />
            <text x="0" y="3" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="900" text-anchor="middle">FRONT NO-ZONE (20 FT)</text>
          </g>

          <!-- 2. Rear No-Zone (200 ft behind trailer) -->
          <polygon id="zone-rear" points="0,0 0,0 0,0 0,0" fill="url(#no-zone-hatch-amber)" stroke="#F59E0B" stroke-width="1.5" />
          <g id="badge-rear-nozone" transform="translate(0, 0)">
            <rect x="-85" y="-8" width="170" height="16" rx="8" fill="#451A03" stroke="#F59E0B" stroke-width="1" />
            <text x="0" y="3" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="900" text-anchor="middle">REAR NO-ZONE (200 FT BLIND)</text>
          </g>

          <!-- 3. Left Side No-Zone (1 lane wide beside cab) -->
          <polygon id="zone-left" points="0,0 0,0 0,0 0,0" fill="url(#no-zone-hatch-amber)" stroke="#F59E0B" stroke-width="1.5" />
          <g id="badge-left-nozone" transform="translate(0, 0)">
            <rect x="-42" y="-7" width="84" height="14" rx="7" fill="#451A03" stroke="#F59E0B" stroke-width="1" />
            <text x="0" y="3" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="900" text-anchor="middle">LEFT NO-ZONE</text>
          </g>

          <!-- 4. Right Side No-Zone (TREACHEROUS: 2 lanes wide across Lane 1) -->
          <polygon id="zone-right" points="0,0 0,0 0,0 0,0" fill="url(#no-zone-hatch-red)" stroke="#EF4444" stroke-width="2" />
          <g id="badge-right-nozone" transform="translate(0, 0)">
            <rect x="-80" y="-9" width="160" height="18" rx="9" fill="#450A0A" stroke="#EF4444" stroke-width="1.2" />
            <text x="0" y="3" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">RIGHT NO-ZONE (2 LANES WIDE)</text>
          </g>
        </g>

        <!-- SIGHTLINE RAYS FROM TRUCK CAB SIDE MIRRORS -->
        <g id="mirror-sightlines" opacity="1.0">
          <line id="sightline-left" x1="0" y1="0" x2="0" y2="0" stroke="#60A5FA" stroke-width="1.5" stroke-dasharray="4,3" />
          <line id="sightline-right" x1="0" y1="0" x2="0" y2="0" stroke="#F87171" stroke-width="1.5" stroke-dasharray="4,3" />
        </g>

        <!-- MODE 2: BRAKING DISTANCE PHYSICS COMPARISON BRACKETS -->
        <g id="braking-brackets-group" opacity="0.0">
          <!-- Passenger Car 190 ft Braking Bracket -->
          <path id="car-brake-bracket" d="M 0,0 L 0,0" stroke="#34D399" stroke-width="3" fill="none" />
          <g id="car-brake-badge" transform="translate(0, 0)">
            <rect x="-65" y="-9" width="130" height="18" rx="9" fill="#064E3B" stroke="#34D399" stroke-width="1" />
            <text x="0" y="3.5" fill="#A7F3D0" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">CAR: 190 FT STOPPING</text>
          </g>

          <!-- Semi Truck 400+ ft Braking Bracket -->
          <path id="truck-brake-bracket" d="M 0,0 L 0,0" stroke="#F87171" stroke-width="3" fill="none" />
          <g id="truck-brake-badge" transform="translate(0, 0)">
            <rect x="-80" y="-9" width="160" height="18" rx="9" fill="#450A0A" stroke="#EF4444" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">TRUCK: 400+ FT STOPPING (80K LBS)</text>
          </g>
        </g>

        <!-- MODE 3: RIGHT TURN SQUEEZE TRAJECTORY & PINCH CALLOUT -->
        <g id="squeeze-hazard-group" opacity="0.0">
          <!-- Truck Wide Swing Left trajectory -->
          <path id="truck-swing-path" d="M 460,350 C 490,300 520,270 560,250" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-dasharray="5,4" marker-end="url(#arrow-blue)" />
          <!-- Trailer Inward Off-Tracking Arc -->
          <path id="trailer-offtrack-path" d="M 430,380 C 470,360 520,350 550,380" fill="none" stroke="#EF4444" stroke-width="3.5" stroke-dasharray="6,4" marker-end="url(#arrow-danger)" />
          <!-- Squeeze Pinch Point Hazard Indicator -->
          <circle id="squeeze-pinch-point" cx="540" cy="360" r="14" fill="none" stroke="#EF4444" stroke-width="2.5" class="danger-pulse" />
          <polygon id="squeeze-hazard-star" points="0,-14 4,-4 15,-4 7,4 10,14 0,8 -10,14 -7,4 -15,-4 -4,-4" fill="#FBBF24" stroke="#B45309" stroke-width="1.2" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- COMMERCIAL MOTOR VEHICLE (CLASS 8 BLUE CAB + 53-FT WHITE BOX TRAILER) -->
      <div id="veh-truck" class="absolute z-19 pointer-events-none transition-transform" style="left: 50.0%; top: 42.56%; transform: translate(-50%, -50%);">
        <div id="veh-truck-sprite" class="relative w-48 aspect-[1264/768] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{truck_b64}" alt="Class 8 Semi-Truck" class="w-full h-full object-contain filter drop-shadow-[0_16px_16px_rgba(0,0,0,0.8)]" />
          <!-- Right Turn Blinker at Rear of Trailer -->
          <div id="truck-blinker-right" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 72%; left: 16%;"></div>
        </div>
        <div id="tag-veh-truck" class="absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#0F141E]/95 border border-blue-500/50 text-[9.5px] font-bold text-blue-300 mono shadow-xl tracking-wider">
          COMMERCIAL VEHICLE: 55 MPH (80,000 LBS)
        </div>
      </div>

      <!-- YELLOW AMBIENT VEHICLE (LANE 2 FOLLOWING BEHIND TRUCK AT 250+ FT BUFFER) -->
      <div id="veh-yellow" class="absolute z-20 pointer-events-none transition-transform" style="left: 18.0%; top: 74.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Traffic Lane 2" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          LAWFUL BUFFER: 250+ FT BEHIND CMV
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - PASSING MANEUVER / FOLLOWING DEFENSE) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none" style="left: 28.0%; top: 50.6%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          <!-- Left Turn Blinker -->
          <div id="blinker-left" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 25%; left: 75%;"></div>
          <!-- Right Turn Blinker -->
          <div id="blinker-right" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 55%; left: 88%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 35%; left: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: PASSING IN LANE 3 (65 MPH)
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#0F172A]/95 border border-blue-500 text-blue-300 mono text-[9px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse shrink-0"></span>
        <span id="pill-status-text">TEXAS CMV RULE: STAY OUT OF 4 NO-ZONES • NO RIGHT-SIDE SQUEEZE</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#0F172A]/90 border border-blue-500/50 text-blue-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        <span id="compliance-text">TTC § 545.062 & CH. 7 CMV STATUTORY COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & SHARING THE ROAD HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[270px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">CMV SHARING ROAD HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">4 NO-ZONES ACTIVE</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-blue-400 mono text-right" id="telem-ego-speed">65 MPH</span>

          <span class="text-gray-400">CMV Weight/Speed:</span>
          <span class="font-bold text-gray-200 mono text-right" id="telem-cmv-speed">55 MPH / 80K LBS</span>

          <span class="text-gray-400">Blind Spot Status:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-zone-status">CLEAR OF NO-ZONES</span>

          <span class="text-gray-400">Truck Mirrors:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-mirrors">DRIVER VISIBLE</span>

          <span class="text-gray-400">Following Buffer:</span>
          <span class="font-bold text-blue-400 mono text-right" id="telem-buffer">250+ FT (4.0 SEC)</span>

          <span class="text-gray-400">Passing Clearance:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-pass-status">CAB IN REARVIEW</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Identifying the 4 commercial No-Zones: Front (20 ft), Rear (200 ft), Left side (1 lane), and Right side (2 lanes wide).
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER (Positioned below status pill in clear air space) -->
      <div id="hazard-banner" class="absolute z-35 w-[265px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL HAZARD: RIGHT-TURN SQUEEZE</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>TRAILER OFF-TRACKING (TTC § 545.101)</strong><br>
          Trucks must swing wide left to clear curbs. Squeezing into the open right gap traps your car as the trailer cuts sharply inward!
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
    const telemEgoSpeed = document.getElementById('telem-ego-speed');
    const telemCmvSpeed = document.getElementById('telem-cmv-speed');
    const telemZoneStatus = document.getElementById('telem-zone-status');
    const telemMirrors = document.getElementById('telem-mirrors');
    const telemBuffer = document.getElementById('telem-buffer');
    const telemPassStatus = document.getElementById('telem-pass-status');
    const hudNarrative = document.getElementById('hud-narrative');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const pillStatusText = document.getElementById('pill-status-text');
    const complianceText = document.getElementById('compliance-text');
    const hazardBanner = document.getElementById('hazard-banner');

    // Vehicles & Tags
    const vehTruck = document.getElementById('veh-truck');
    const vehTruckSprite = document.getElementById('veh-truck-sprite');
    const tagVehTruck = document.getElementById('tag-veh-truck');
    const truckBlinkerRight = document.getElementById('truck-blinker-right');

    const vehYellow = document.getElementById('veh-yellow');
    const tagVehYellow = document.getElementById('tag-veh-yellow');

    const vehEgo = document.getElementById('veh-ego');
    const vehEgoSprite = document.getElementById('veh-ego-sprite');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const blinkerLeft = document.getElementById('blinker-left');
    const blinkerRight = document.getElementById('blinker-right');
    const brakeLights = document.getElementById('brake-lights');

    // SVG Groups & Elements
    const cmvNoZonesGroup = document.getElementById('cmv-no-zones-group');
    const zoneFront = document.getElementById('zone-front');
    const badgeFrontNozone = document.getElementById('badge-front-nozone');
    const zoneRear = document.getElementById('zone-rear');
    const badgeRearNozone = document.getElementById('badge-rear-nozone');
    const zoneLeft = document.getElementById('zone-left');
    const badgeLeftNozone = document.getElementById('badge-left-nozone');
    const zoneRight = document.getElementById('zone-right');
    const badgeRightNozone = document.getElementById('badge-right-nozone');

    const mirrorSightlines = document.getElementById('mirror-sightlines');
    const sightlineLeft = document.getElementById('sightline-left');
    const sightlineRight = document.getElementById('sightline-right');

    const brakingBracketsGroup = document.getElementById('braking-brackets-group');
    const carBrakeBracket = document.getElementById('car-brake-bracket');
    const carBrakeBadge = document.getElementById('car-brake-badge');
    const truckBrakeBracket = document.getElementById('truck-brake-bracket');
    const truckBrakeBadge = document.getElementById('truck-brake-badge');

    const squeezeHazardGroup = document.getElementById('squeeze-hazard-group');
    const squeezePinchPoint = document.getElementById('squeeze-pinch-point');
    const squeezeHazardStar = document.getElementById('squeeze-hazard-star');

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
        {{ time: 0.8, title: "Identify 4 CMV No-Zones" }},
        {{ time: 2.2, title: "Lane 3 Passing Acceleration" }},
        {{ time: 3.6, title: "Rearview Mirror Cab Check" }},
        {{ time: 5.0, title: "Safe 200-Ft Forward Re-Entry" }}
      ],
      2: [
        {{ time: 0.8, title: "Braking Physics Disparity (80K vs 3.5K Lbs)" }},
        {{ time: 2.2, title: "Car Stopping Distance: 190 FT" }},
        {{ time: 3.6, title: "Truck Stopping Distance: 400+ FT" }},
        {{ time: 5.0, title: "Mandatory 4-Second Following Buffer" }}
      ],
      3: [
        {{ time: 0.8, title: "Truck Signals Right & Swings Wide" }},
        {{ time: 2.2, title: "Ego Squeezes Into Open Right Gap" }},
        {{ time: 3.6, title: "Trailer Cuts Inward (Off-Tracking)" }},
        {{ time: 5.0, title: "Critical Underride & Squeeze Crash" }}
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

    // Helper: update SVG No-Zone polygons anchored to CMV center
    function updateNoZones(truckSvgX, truckSvgY) {{
      // Truck dimensions at width=192, height=116:
      // Front cab bumper: (truckSvgX + 88, truckSvgY - 22)
      // Rear trailer doors: (truckSvgX - 74, truckSvgY + 44)
      const cabX = truckSvgX + 88;
      const cabY = truckSvgY - 22;
      const rearX = truckSvgX - 74;
      const rearY = truckSvgY + 44;

      // 1. Front No-Zone (20 ft ahead of cab in Lane 2)
      // Extends NE by 50px
      const f1x = cabX + 5, f1y = cabY - 10;
      const f2x = cabX + 55, f2y = cabY - 45;
      const f3x = cabX + 75, f3y = cabY - 25;
      const f4x = cabX + 25, f4y = cabY + 10;
      zoneFront.setAttribute('points', `${{f1x}},${{f1y}} ${{f2x}},${{f2y}} ${{f3x}},${{f3y}} ${{f4x}},${{f4y}}`);
      badgeFrontNozone.setAttribute('transform', `translate(${{cabX + 40}}, ${{cabY - 30}})`);

      // 2. Rear No-Zone (200 ft behind trailer in Lane 2)
      // Extends SW by 120px
      const r1x = rearX - 5, r1y = rearY - 12;
      const r2x = rearX - 110, r2y = rearY + 65;
      const r3x = rearX - 85, r3y = rearY + 95;
      const r4x = rearX + 15, r4y = rearY + 15;
      zoneRear.setAttribute('points', `${{r1x}},${{r1y}} ${{r2x}},${{r2y}} ${{r3x}},${{r3y}} ${{r4x}},${{r4y}}`);
      badgeRearNozone.setAttribute('transform', `translate(${{rearX - 55}}, ${{rearY + 48}})`);

      // 3. Left Side No-Zone (1 lane wide NW into Lane 3 beside cab/trailer)
      const l1x = rearX + 15, l1y = rearY - 25;
      const l2x = rearX - 25, l2y = rearY - 55;
      const l3x = cabX - 10, l3y = cabY - 45;
      const l4x = cabX + 15, l4y = cabY - 15;
      zoneLeft.setAttribute('points', `${{l1x}},${{l1y}} ${{l2x}},${{l2y}} ${{l3x}},${{l3y}} ${{l4x}},${{l4y}}`);
      badgeLeftNozone.setAttribute('transform', `translate(${{(cabX + rearX) / 2 - 45}}, ${{(cabY + rearY) / 2 - 55}})`);

      // 4. Right Side No-Zone (TREACHEROUS: 2 lanes wide SE across Lane 1)
      const rt1x = rearX + 30, rt1y = rearY + 15;
      const rt2x = cabX - 10, rt2y = cabY + 15;
      const rt3x = cabX + 45, rt3y = cabY + 65;
      const rt4x = rearX - 10, rt4y = rearY + 95;
      zoneRight.setAttribute('points', `${{rt1x}},${{rt1y}} ${{rt2x}},${{rt2y}} ${{rt3x}},${{rt3y}} ${{rt4x}},${{rt4y}}`);
      badgeRightNozone.setAttribute('transform', `translate(${{(cabX + rearX) / 2 + 55}}, ${{(cabY + rearY) / 2 + 82}})`);

      // Sightline rays from truck mirrors
      sightlineLeft.setAttribute('x1', cabX - 15);
      sightlineLeft.setAttribute('y1', cabY - 18);
      sightlineLeft.setAttribute('x2', cabX - 90);
      sightlineLeft.setAttribute('y2', cabY - 70);

      sightlineRight.setAttribute('x1', cabX + 5);
      sightlineRight.setAttribute('y1', cabY + 10);
      sightlineRight.setAttribute('x2', cabX + 65);
      sightlineRight.setAttribute('y2', cabY + 70);
    }}

    function updateSimulation(t) {{
      timeDisplay.textContent = `${{t.toFixed(2)}}s`;
      timelineSlider.value = t.toFixed(2);

      const blinkOn = (Math.sin(t * 10) > 0);

      // =========================================================================
      // MODE 1: THE 4 COMMERCIAL NO-ZONES & LAWFUL PASSING (TTC § 545.054)
      // =========================================================================
      if (currentMode === 1) {{
        tagVehTruck.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#0F141E]/95 border border-blue-500/50 text-[9.5px] font-bold text-blue-300 mono shadow-xl tracking-wider';
        cmvNoZonesGroup.setAttribute('opacity', '1.0');
        mirrorSightlines.setAttribute('opacity', '1.0');
        brakingBracketsGroup.setAttribute('opacity', '0.0');
        squeezeHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        truckBlinkerRight.style.opacity = '0.0';

        // CMV cruising steadily in Lane 2 at 55 MPH
        const truckX = 48.0 + (t / duration) * 8.0; // 48% to 56%
        const truckY = getLane2Y(truckX);
        vehTruck.style.left = `${{truckX}}%`;
        vehTruck.style.top = `${{truckY}}%`;
        vehTruck.style.transform = 'translate(-50%, -50%)';
        vehTruckSprite.style.transform = 'rotate(0deg)';
        tagVehTruck.textContent = 'COMMERCIAL MOTOR VEHICLE: 55 MPH (LANE 2)';

        // Yellow Trailing Vehicle in Lane 2 maintaining 250+ ft following buffer
        const yellowX = 17.0 + (t / duration) * 8.0;
        const yellowY = getLane2Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'TRAFFIC: 250+ FT BUFFER BEHIND CMV';

        // Update dynamic 4 No-Zones around CMV
        updateNoZones(truckX * 10, truckY * 6);

        // Ego Vehicle (Red Sedan): Overtakes CMV in Lane 3 at 65 MPH, verifies mirror, returns to Lane 2
        let egoX, egoY, egoSpeed;
        if (t < 1.6) {{
          // Step 1: In Lane 3 approaching from behind, scanning blind spots
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
          const progress = t / 1.6;
          egoX = 30.0 + progress * 10.0; // 30% to 40%
          egoY = getLane3Y(egoX);
          egoSpeed = 65;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
        }} else if (t < 3.2) {{
          // Step 2: Passing briskly alongside CMV in Lane 3 (clear of Left No-Zone)
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
          const progress = (t - 1.6) / 1.6;
          egoX = 40.0 + progress * 18.0; // 40% to 58%
          egoY = getLane3Y(egoX);
          egoSpeed = 65;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
        }} else if (t < 4.6) {{
          // Step 3: Ahead of cab in Lane 3, checks inside rearview mirror, signals right
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
          const progress = (t - 3.2) / 1.4;
          egoX = 58.0 + progress * 10.0; // 58% to 68%
          egoY = getLane3Y(egoX);
          egoSpeed = 65;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';
          brakeLights.style.opacity = '0.0';
        }} else {{
          // Step 4: Merging back to Lane 2 with safe 200+ ft forward cushion ahead of truck
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
          const progress = (t - 4.6) / 1.4;
          egoX = 66.0 + progress * 6.0; // 66% to 72%
          const y3 = getLane3Y(egoX);
          const y2 = getLane2Y(egoX);
          egoY = y3 + progress * (y2 - y3);
          egoSpeed = 65;
          blinkerLeft.style.opacity = '0.0';
          blinkerRight.style.opacity = (progress < 0.6 && blinkOn) ? '1.0' : '0.0';
          brakeLights.style.opacity = '0.0';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';

        telemEgoSpeed.textContent = `${{egoSpeed}} MPH`;
        telemCmvSpeed.textContent = '55 MPH / 80K LBS';
        telemBuffer.textContent = (t < 3.2) ? 'PASSING IN LANE 3' : '200+ FT FORWARD BUFFER';

        pillStatusText.textContent = 'TEXAS CMV RULE: STAY OUT OF THE 4 NO-ZONES • NEVER SQUEEZE ON THE RIGHT';
        complianceText.textContent = 'TTC § 545.054 CMV PASSING & CLEARANCE VERIFIED';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: 65 MPH • SCANNING CMV NO-ZONES';
          telemZoneStatus.textContent = 'CLEAR OF NO-ZONES';
          telemZoneStatus.className = 'font-bold text-emerald-400 mono text-right';
          telemMirrors.textContent = 'DRIVER VISIBLE';
          telemPassStatus.textContent = 'APPROACHING IN LANE 3';
          signalStateBadge.textContent = 'SCANNING BLIND SPOTS';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 1: Identifying the 4 commercial No-Zones: Front (20 ft), Rear (200 ft), Left side (1 lane), and Right side (2 lanes wide). Ego enters passing lane.';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: PASSING BRISKLY • DO NOT LINGER';
          telemZoneStatus.textContent = 'LEFT NO-ZONE TRANSIT';
          telemZoneStatus.className = 'font-bold text-amber-400 mono text-right';
          telemMirrors.textContent = 'PASSING CAB WINDOW';
          telemPassStatus.textContent = 'OVERTAKING AT 65 MPH';
          signalStateBadge.textContent = 'BRISK PASSING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
          hudNarrative.textContent = 'Step 2: Never linger alongside a commercial truck. Pass swiftly in Lane 3 so the driver does not lose you in their side blind spot.';
        }} else if (t < 4.6) {{
          tagVehEgo.textContent = 'EGO: ENTIRE CAB IN REARVIEW • SIGNALING RIGHT';
          telemZoneStatus.textContent = 'CLEAR OF NO-ZONES';
          telemZoneStatus.className = 'font-bold text-emerald-400 mono text-right';
          telemMirrors.textContent = 'CAB VISIBLE IN REARVIEW';
          telemPassStatus.textContent = 'SAFE TO RETURN';
          signalStateBadge.textContent = 'REARVIEW CONFIRMED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
          hudNarrative.textContent = 'Step 3: Under TTC § 545.054, do NOT return to Lane 2 until you can see the entire front cab and headlights of the truck in your inside rearview mirror.';
        }} else {{
          tagVehEgo.textContent = 'EGO: 200+ FT BUFFER • SAFE RE-ENTRY';
          telemZoneStatus.textContent = 'SAFE SPACE CUSHION';
          telemZoneStatus.className = 'font-bold text-emerald-400 mono text-right';
          telemMirrors.textContent = '200 FT AHEAD';
          telemPassStatus.textContent = 'RETURN COMPLETE';
          signalStateBadge.textContent = 'COMPLIANCE VERIFIED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
          hudNarrative.textContent = 'Step 4: Re-entry complete with ample 200-ft cushion. Never cut directly in front of an 80,000 lb truck; doing so robs the trucker of their stopping distance.';
        }}
      }}

      // =========================================================================
      // MODE 2: STOPPING DISTANCE PHYSICS (400 FT VS 190 FT - TTC § 545.062)
      // =========================================================================
      else if (currentMode === 2) {{
        tagVehTruck.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#0F141E]/95 border border-blue-500/50 text-[9.5px] font-bold text-blue-300 mono shadow-xl tracking-wider';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        cmvNoZonesGroup.setAttribute('opacity', '0.35');
        mirrorSightlines.setAttribute('opacity', '0.0');
        brakingBracketsGroup.setAttribute('opacity', '1.0');
        squeezeHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        blinkerLeft.style.opacity = '0.0';
        blinkerRight.style.opacity = '0.0';
        truckBlinkerRight.style.opacity = '0.0';

        // CMV cruising steadily in Lane 2
        const truckX = 52.0;
        const truckY = getLane2Y(truckX);
        vehTruck.style.left = `${{truckX}}%`;
        vehTruck.style.top = `${{truckY}}%`;
        vehTruck.style.transform = 'translate(-50%, -50%)';
        vehTruckSprite.style.transform = 'rotate(0deg)';
        tagVehTruck.textContent = 'SEMI-TRUCK: 80,000 LBS • 400+ FT STOPPING DISTANCE';

        // Yellow Car in Lane 1
        const yellowX = 22.0;
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'PASSENGER CAR: 3,500 LBS (190 FT STOP)';

        // Ego Car following behind Truck in Lane 2 at 250+ ft (4 seconds)
        const egoX = 26.0;
        const egoY = getLane2Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';
        brakeLights.style.opacity = '0.0';
        tagVehEgo.textContent = 'EGO: 4-SECOND FOLLOWING BUFFER (250+ FT)';

        // Update No-Zones lightly
        updateNoZones(truckX * 10, truckY * 6);

        // Update Braking Comparison Brackets in SVG
        // Car Bracket: starting from Ego front bumper (cx + 25, cy - 12) extending forward 65px NE
        const cx = 260, cy = egoY * 6;
        const carFrontX = cx + 25, carFrontY = cy - 12;
        carBrakeBracket.setAttribute('d', `M ${{carFrontX}},${{carFrontY}} L ${{carFrontX + 70}},${{carFrontY - 65}}`);
        carBrakeBadge.setAttribute('transform', `translate(${{carFrontX + 35}}, ${{carFrontY - 35}})`);

        // Truck Bracket: starting from Truck cab bumper (cabX, cabY) extending forward 125px NE
        const cabX = truckX * 10 + 88, cabY = truckY * 6 - 22;
        truckBrakeBracket.setAttribute('d', `M ${{cabX}},${{cabY}} L ${{cabX + 115}},${{cabY - 105}}`);
        truckBrakeBadge.setAttribute('transform', `translate(${{cabX + 60}}, ${{cabY - 55}})`);

        telemEgoSpeed.textContent = '55 MPH (3,500 LBS)';
        telemCmvSpeed.textContent = '55 MPH (80,000 LBS)';
        telemZoneStatus.textContent = 'OUT OF REAR NO-ZONE';
        telemZoneStatus.className = 'font-bold text-emerald-400 mono text-right';
        telemMirrors.textContent = 'BOTH SIDE MIRRORS VISIBLE';
        telemBuffer.textContent = '250 FT (4.0 SEC BUFFER)';
        telemPassStatus.textContent = 'SAFE FOLLOWING DISTANCE';

        pillStatusText.textContent = 'PHYSICS RULE (TTC § 545.062): 80,000 LB SEMI-TRUCK TAKES 2X+ LONGER TO STOP';
        complianceText.textContent = 'TTC § 545.062 CMV FOLLOWING DISTANCE COMPLIANT';

        tagVehEgo.textContent = 'EGO: 4-SEC BUFFER (250+ FT) • MIRRORS VISIBLE';
        tagVehTruck.textContent = 'SEMI-TRUCK: 80,000 LBS • 400+ FT STOP';
        hudNarrative.textContent = 'Physics Comparison: A loaded semi weighs up to 80,000 lbs (over 20x a sedan). Air-brake lag and kinetic momentum require 400+ ft to stop at 55 mph vs 190 ft for cars. Maintain at least 4 seconds buffer.';
        signalStateBadge.textContent = '4-SEC BUFFER VERIFIED';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: THE "RIGHT-TURN SQUEEZE" & OFF-TRACKING (TTC § 545.101)
      // =========================================================================
      else if (currentMode === 3) {{
        tagVehTruck.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#0F141E]/95 border border-blue-500/50 text-[9.5px] font-bold text-blue-300 mono shadow-xl tracking-wider';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        cmvNoZonesGroup.setAttribute('opacity', '0.0');
        mirrorSightlines.setAttribute('opacity', '0.0');
        brakingBracketsGroup.setAttribute('opacity', '0.0');
        squeezeHazardGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';
        blinkerLeft.style.opacity = '0.0';
        blinkerRight.style.opacity = '0.0';
        truckBlinkerRight.style.opacity = blinkOn ? '1.0' : '0.0';

        // Yellow car safely held back behind truck in Lane 2
        const yellowX = 18.0;
        const yellowY = getLane2Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'DEFENSIVE DRIVER: WAITING BEHIND TRUCK';

        // Semi-Truck in Lane 2 preparing for wide right turn onto off-ramp / cross street
        // Truck swings cab left into Lane 3 while trailer cuts right
        let truckX, truckY, truckAngle;
        let egoX, egoY, egoAngle, egoSpeed;

        if (t < 2.0) {{
          // Step 1: Truck signals right, cab swings wide left into Lane 3 to clear curb
          const progress = t / 2.0;
          truckX = 46.0 + progress * 4.0; // 46% to 50%
          truckY = getLane2Y(truckX) - progress * 10; // swings left toward Lane 3
          truckAngle = -progress * 8.0; // cab angles left
          
          // Ego approaches in Lane 1, sees the gap on right, accelerates into the trap
          egoX = 35.0 + progress * 8.0; // 35% to 43%
          egoY = getLane1Y(egoX);
          egoAngle = 0;
          egoSpeed = 45;
          brakeLights.style.opacity = '0.0';
          squeezeHazardStar.setAttribute('transform', `translate(540, 360) scale(0)`);
        }} else if (t < 3.8) {{
          // Step 2 & 3: Truck cab cuts sharply right into turn. Trailer tracks inward across Lane 1!
          const progress = (t - 2.0) / 1.8;
          truckX = 50.0 + progress * 6.0; // 50% to 56%
          truckY = getLane2Y(truckX) - 10 + progress * 15;
          truckAngle = -8.0 + progress * 24.0; // turns hard right

          // Ego is caught between trailer rear tandem wheels and curb/guardrail!
          egoX = 43.0 + progress * 8.0; // 43% to 51%
          egoY = getLane1Y(egoX) + progress * 5; // pushed toward guardrail
          egoAngle = progress * 14.0; // angled/pinched
          egoSpeed = Math.round(45 * (1 - progress * 0.8));
          brakeLights.style.opacity = '1.0';
          squeezeHazardStar.setAttribute('transform', `translate(525, 365) scale(1)`);
        }} else {{
          // Step 4: Full pinch and entrapment against curb / guardrail
          truckX = 56.0;
          truckY = getLane2Y(truckX) + 5;
          truckAngle = 16.0;

          egoX = 51.0;
          egoY = getLane1Y(egoX) + 5;
          egoAngle = 14.0;
          egoSpeed = 0;
          brakeLights.style.opacity = '1.0';
          squeezeHazardStar.setAttribute('transform', `translate(525, 365) scale(1.2)`);
        }}

        vehTruck.style.left = `${{truckX}}%`;
        vehTruck.style.top = `${{truckY}}%`;
        vehTruck.style.transform = 'translate(-50%, -50%)';
        vehTruckSprite.style.transform = `rotate(${{truckAngle.toFixed(1)}}deg)`;
        tagVehTruck.textContent = 'TURNING TRUCK: SWINGING WIDE RIGHT';

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = `rotate(${{egoAngle.toFixed(1)}}deg)`;

        telemEgoSpeed.textContent = (egoSpeed === 0) ? '0 MPH (CRUSHED)' : `${{egoSpeed}} MPH`;
        telemCmvSpeed.textContent = '15 MPH (TURNING)';
        telemZoneStatus.textContent = 'RIGHT NO-ZONE PINCH';
        telemZoneStatus.className = 'font-bold text-red-500 mono text-right';
        telemMirrors.textContent = 'BLIND TO TRUCKER';
        telemBuffer.textContent = '0 FT (SQUEEZE TRAP)';
        telemPassStatus.textContent = 'ILLEGAL RIGHT PASS';

        pillStatusText.textContent = 'CRITICAL ERROR: NEVER SQUEEZE BETWEEN A TURNING TRUCK AND THE CURB!';
        complianceText.textContent = 'TTC § 545.101 RIGHT-TURN SQUEEZE VIOLATION DETECTED';

        if (t < 2.0) {{
          tagVehEgo.textContent = 'EGO: SQUEEZING INTO OPEN RIGHT GAP (DANGER!)';
          signalStateBadge.textContent = 'UNLAWFUL PASS';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
          hudNarrative.textContent = 'Step 1 & 2: Semi-truck signals right and swings wide left to clear the curb corner. Driver mistakenly assumes truck is turning left and enters right gap!';
        }} else if (t < 3.8) {{
          tagVehEgo.textContent = 'EGO: TRAPPED! TRAILER CUTTING INWARD AT CURB';
          signalStateBadge.textContent = 'OFF-TRACK PINCH';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
          hudNarrative.textContent = 'Step 3: Off-tracking occurs: trailer wheels cut a tight radius inward across Lane 1. Ego is trapped in the blind spot with zero escape path!';
        }} else {{
          tagVehEgo.textContent = 'EGO: SQUEEZE COLLISION! CRUSHED AGAINST GUARDRAIL';
          signalStateBadge.textContent = 'UNDERRIDE CRASH';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
          hudNarrative.textContent = 'Step 4: Severe right-turn squeeze collision. The rear trailer wheels crush Ego against the curb/guardrail. Rule: ALWAYS wait behind turning trucks!';
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
        if (step === currentStepIdx) {{
          card.classList.remove('border-[#1E293B]');
          card.classList.add('border-blue-500/60', 'bg-blue-950/20');
        }} else {{
          card.classList.remove('border-blue-500/60', 'bg-blue-950/20');
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L07_T03_commercial_vehicles.html"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 25 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_l07_t03()
