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
    police_patrol_path = r"c:\tx_dmv\driving_rule_animations_suite\assets\vehicles\police_cruiser_tx_ne_clean.png"

    print("Encoding Lesson 20 assets to base64...")
    bg_b64 = get_base64_jpg(highway_bg_path)
    car_red_ne_b64 = get_base64_image(car_red_ne_path)
    car_blue_ne_b64 = get_base64_image(car_blue_ne_path)
    car_yellow_ne_b64 = get_base64_image(car_yellow_ne_path)
    police_patrol_b64 = get_base64_image(police_patrol_path)
    print("Assets successfully encoded.")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson 20: Managing a Vehicle Breakdown — Shoulder Safety & Warning Triangles (TTC § 545.301 & § 545.305)</title>
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
      background: #10B981;
      cursor: pointer;
      border: 2px solid #064E3B;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.7);
    }}
    .custom-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.15);
      background: #34D399;
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.35; filter: drop-shadow(0 0 4px #10B981); }}
      50% {{ opacity: 0.85; filter: drop-shadow(0 0 14px #34D399); }}
    }}
    .safe-pulse {{
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
    @keyframes triangleFlash {{
      0%, 100% {{ opacity: 0.6; filter: drop-shadow(0 0 3px #F97316); }}
      50% {{ opacity: 1.0; filter: drop-shadow(0 0 10px #EA580C); }}
    }}
    .triangle-glow {{
      animation: triangleFlash 1.5s ease-in-out infinite;
    }}
    @keyframes strobePolice {{
      0%, 48% {{ filter: drop-shadow(0 0 12px #3B82F6); }}
      50%, 100% {{ filter: drop-shadow(0 0 12px #EF4444); }}
    }}
    .strobe-bar {{
      animation: strobePolice 0.6s steps(1) infinite;
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
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 20</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L05-T13: Managing a Vehicle Breakdown — Shoulder Safety & Triangles
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Driver Handbook Ch. 5 • TTC § 545.301 (Paved Shoulder Clearance Mandate) & § 545.305 (Removal of Stalled Vehicles)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
          1: Shoulder Pulloff & Triangles
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: Left Tire Hazard & Patrol Escort
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Stopping in Travel Lane
        </button>
        <div class="h-4 w-px bg-gray-700 mx-1"></div>
        <label class="flex items-center space-x-1.5 text-xs font-medium text-gray-300 cursor-pointer pr-1">
          <input type="checkbox" id="auto-loop-toggle" checked class="rounded bg-gray-800 border-gray-700 text-emerald-500 focus:ring-0">
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
        <div id="step-title-1" class="text-xs font-bold text-white mt-1 group-hover:text-blue-200">Mechanical Failure (Coasting)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Shoulder Clearance (0 MPH)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Warning Triangles (10/100/200 FT)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Occupant Guardrail Safety</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG VECTOR OVERLAYS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <linearGradient id="safe-shoulder-glow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.10" />
            <stop offset="50%" stop-color="#10B981" stop-opacity="0.25" />
            <stop offset="100%" stop-color="#10B981" stop-opacity="0.05" />
          </linearGradient>

          <!-- Warning Triangle Symbol Template -->
          <g id="warning-triangle-sym">
            <polygon points="0,-13 11,8 -11,8" fill="#F97316" stroke="#FFFFFF" stroke-width="1.8" stroke-linejoin="round" />
            <polygon points="0,-8 6,5 -6,5" fill="#7C2D12" stroke="#EA580C" stroke-width="1.0" />
            <circle cx="0" cy="1" r="1.5" fill="#FFFFFF" />
          </g>
        </defs>

        <!-- SAFE SHOULDER PERIMETER ZONE (Mode 1 & 2) -->
        <g id="shoulder-safe-group" opacity="1.0">
          <polygon points="290,490 640,280 690,360 340,570" fill="url(#safe-shoulder-glow)" stroke="#10B981" stroke-width="1.5" stroke-dasharray="10,6" class="safe-pulse" />
          <line x1="290" y1="490" x2="640" y2="280" stroke="#FFFFFF" stroke-width="2.5" />
        </g>

        <!-- WARNING TRIANGLES DEPLOYMENT LAYER (Mode 1 Step 3 & 4) -->
        <g id="triangles-group" opacity="0.0" class="transition-opacity duration-300">
          <!-- Guide line connecting triangles -->
          <line x1="320" y1="519" x2="495" y2="414" stroke="#F97316" stroke-width="1.5" stroke-dasharray="6,4" />

          <!-- Triangle 3 (200 FT Buffer) -->
          <g transform="translate(320, 519)" class="triangle-glow">
            <use href="#warning-triangle-sym" />
            <rect x="-35" y="12" width="70" height="15" rx="7.5" fill="#1C1917" stroke="#EA580C" stroke-width="1.2" />
            <text x="0" y="22.5" fill="#FDBA74" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">200 FT BUFFER</text>
          </g>

          <!-- Triangle 2 (100 FT Midline) -->
          <g transform="translate(420, 459)" class="triangle-glow">
            <use href="#warning-triangle-sym" />
            <rect x="-35" y="12" width="70" height="15" rx="7.5" fill="#1C1917" stroke="#EA580C" stroke-width="1.2" />
            <text x="0" y="22.5" fill="#FDBA74" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">100 FT MID</text>
          </g>

          <!-- Triangle 1 (10 FT Perimeter) -->
          <g transform="translate(495, 414)" class="triangle-glow">
            <use href="#warning-triangle-sym" />
            <rect x="-32" y="12" width="64" height="15" rx="7.5" fill="#1C1917" stroke="#EA580C" stroke-width="1.2" />
            <text x="0" y="22.5" fill="#FDBA74" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">10 FT CLOSE</text>
          </g>
        </g>

        <!-- OCCUPANT SAFETY VECTOR (BEHIND GUARDRAIL ON EMBANKMENT) -->
        <g id="occupant-safety-group" opacity="0.0" class="transition-opacity duration-300">
          <!-- Green safety zone indicator along guardrail -->
          <path d="M 520,440 Q 570,410 630,380" stroke="#10B981" stroke-width="2.5" stroke-dasharray="6,4" fill="none" />
          <g transform="translate(585, 435)">
            <circle cx="0" cy="0" r="13" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
            <!-- Person icon / safety check -->
            <path d="M-4,-4 L0,-7 L4,-4 M0,-7 L0,4 M-4,0 L4,0" stroke="#34D399" stroke-width="1.5" stroke-linecap="round" fill="none" />
            <rect x="-60" y="14" width="120" height="16" rx="8" fill="#062418" stroke="#10B981" stroke-width="1.2" />
            <text x="0" y="25" fill="#6EE7B7" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="800" text-anchor="middle">SAFE BEHIND GUARDRAIL</text>
          </g>
        </g>

        <!-- MODE 2: LEFT TIRE DANGER ZONE (TRAFFIC FLANK) -->
        <g id="left-tire-danger-group" opacity="0.0" class="transition-opacity duration-300">
          <polygon points="485,385 545,348 535,335 475,372" fill="#EF4444" fill-opacity="0.35" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="6,4" class="danger-pulse" />
          <g transform="translate(510, 340)">
            <rect x="-70" y="-18" width="140" height="16" rx="8" fill="#450A0A" stroke="#EF4444" stroke-width="1.2" />
            <text x="0" y="-7" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="900" text-anchor="middle">DO NOT KNEEL IN TRAFFIC!</text>
          </g>
        </g>

        <!-- MODE 3: DEAD STOP IMPACT HAZARD CIRCLE -->
        <g id="hazard-impact-group" opacity="0.0">
          <circle id="hazard-circle" cx="0" cy="0" r="38" fill="#EF4444" fill-opacity="0.3" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="6,4" class="danger-pulse" />
          <polygon id="hazard-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- PATROL / COURTESY VEHICLE (MODE 2 ESCORT) -->
      <div id="veh-patrol" class="absolute z-19 pointer-events-none transition-transform opacity-0" style="left: 42.0%; top: 76.5%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{police_patrol_b64}" alt="TxDOT Courtesy Patrol" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
          <!-- Emergency Strobe Roof Bar -->
          <div class="absolute w-6 h-2 rounded-full bg-blue-500 filter blur-[1px] strobe-bar" style="top: 20%; left: 45%;"></div>
        </div>
        <div id="tag-veh-patrol" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/50 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          TXDOT COURTESY PATROL: SCENE SHIELDED
        </div>
      </div>

      <!-- BLUE THRU HIGHWAY VEHICLE (LANE 2 CRUISING AT 65 MPH) -->
      <div id="veh-blue" class="absolute z-20 pointer-events-none transition-transform" style="left: 65.0%; top: 27.5%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_ne_b64}" alt="Thru Highway Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          THRU FLOW: 65 MPH (LANE 2)
        </div>
      </div>

      <!-- YELLOW TRAFFIC VEHICLE (LANE 1 APPROACHING / PASSING) -->
      <div id="veh-yellow" class="absolute z-20 pointer-events-none transition-transform" style="left: 30.0%; top: 76.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Highway Traffic Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          HIGHWAY FLOW: 65 MPH (LANE 1)
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - DISABLED / COASTING TO SHOULDER) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none transition-transform" style="left: 52.0%; top: 66.5%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_ne_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          
          <!-- Hazard Flashers Front & Rear (Both blink simultaneously) -->
          <div id="flasher-front" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 25%; left: 75%;"></div>
          <div id="flasher-rear" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 35%; left: 10%;"></div>
          <div id="flasher-side" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="bottom: 25%; right: 10%;"></div>
          
          <!-- White Distress Cloth on Mirror -->
          <div id="distress-cloth" class="absolute w-2.5 h-3.5 bg-white rounded-sm shadow-md border border-gray-300 opacity-0" style="bottom: 30%; right: 28%;"></div>

          <!-- Open Hood Graphic Overlay -->
          <div id="distress-hood" class="absolute w-5 h-3 bg-red-700/80 border border-white/50 rounded-sm shadow opacity-0 transform -rotate-12" style="top: 15%; right: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: SHOULDER CLEARANCE (0 MPH) • HAZARDS ON
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TTC § 545.301 MANDATE: PULL COMPLETELY OFF PAVED TRAVEL LANES ONTO SHOULDER</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#081C15]/90 border border-emerald-500/50 text-emerald-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="compliance-text">TTC § 545.301 SHOULDER CLEARANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & BREAKDOWN PROTOCOL HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[275px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">BREAKDOWN TELEMETRY HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">SHOULDER SAFE</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-speed">0 MPH (PARKED)</span>

          <span class="text-gray-400">Lane Position:</span>
          <span class="font-bold text-emerald-300 mono text-right" id="telem-lane">IMPROVED SHOULDER</span>

          <span class="text-gray-400">Hazard Flashers:</span>
          <span class="font-bold text-yellow-400 mono text-right" id="telem-hazards">4-WAY ACTIVE [ON]</span>

          <span class="text-gray-400">Warning Devices:</span>
          <span class="font-bold text-amber-400 mono text-right" id="telem-triangles">3 TRIANGLES (200 FT)</span>

          <span class="text-gray-400">Occupant Safety:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-occupants">BEHIND GUARDRAIL</span>

          <span class="text-gray-400">TTC Compliance:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-statute">§ 545.301 PASSED</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Sudden mechanical failure in Lane 1. Driver grips steering wheel firmly, avoids slamming brakes, signals right, and coasts smoothly toward the wide right shoulder.
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER (Positioned below status pill in clear air space) -->
      <div id="hazard-banner" class="absolute z-35 w-[390px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10.5px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL HAZARD: NEVER STOP IN A TRAVEL LANE</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>UNLAWFUL STOPPING (TTC § 545.301) & TOW PREEMPTION (§ 545.305)</strong><br>
          Leaving a disabled vehicle in a travel lane creates lethal rear-end crash hazards. Always coast to shoulder. Police authorized to immediately tow vehicle.
        </div>
      </div>

    </div>

    <!-- TIMELINE & PLAYBACK CONTROLS -->
    <footer class="bg-[#121824] border border-[#1E293B] rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <button id="play-pause-btn" class="w-10 h-10 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white flex items-center justify-center shadow-lg transition" title="Play/Pause">
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
    let currentMode = 1; // 1: Safe Pulloff & Triangles, 2: Left Tire Hazard & Patrol, 3: Travel Lane Stopping Hazard
    let currentTime = 0.0;
    const duration = 6.0;
    let isPlaying = true;
    let lastTimestamp = null;

    // DOM Elements
    const vehEgo = document.getElementById('veh-ego');
    const vehBlue = document.getElementById('veh-blue');
    const vehYellow = document.getElementById('veh-yellow');
    const vehPatrol = document.getElementById('veh-patrol');

    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehBlue = document.getElementById('tag-veh-blue');
    const tagVehYellow = document.getElementById('tag-veh-yellow');
    const tagVehPatrol = document.getElementById('tag-veh-patrol');

    const flasherFront = document.getElementById('flasher-front');
    const flasherRear = document.getElementById('flasher-rear');
    const flasherSide = document.getElementById('flasher-side');
    const distressCloth = document.getElementById('distress-cloth');
    const distressHood = document.getElementById('distress-hood');

    const shoulderSafeGroup = document.getElementById('shoulder-safe-group');
    const trianglesGroup = document.getElementById('triangles-group');
    const occupantSafetyGroup = document.getElementById('occupant-safety-group');
    const leftTireDangerGroup = document.getElementById('left-tire-danger-group');

    const hazardImpactGroup = document.getElementById('hazard-impact-group');
    const hazardCircle = document.getElementById('hazard-circle');
    const hazardStar = document.getElementById('hazard-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const telemSpeed = document.getElementById('telem-speed');
    const telemLane = document.getElementById('telem-lane');
    const telemHazards = document.getElementById('telem-hazards');
    const telemTriangles = document.getElementById('telem-triangles');
    const telemOccupants = document.getElementById('telem-occupants');
    const telemStatute = document.getElementById('telem-statute');
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
    function getShoulderY(x) {{
      return 68.50 - 1.005 * (x - 50.0);
    }}

    // Step definitions for each mode
    const stepConfigs = {{
      1: [
        {{ time: 0.8, title: "Mechanical Failure (Coasting)" }},
        {{ time: 2.2, title: "Shoulder Clearance (0 MPH)" }},
        {{ time: 3.6, title: "Warning Triangles (10/100/200 FT)" }},
        {{ time: 5.0, title: "Occupant Guardrail Safety" }}
      ],
      2: [
        {{ time: 0.8, title: "Left Tire Blowout Detected" }},
        {{ time: 2.2, title: "Lethal Traffic Flank Risk" }},
        {{ time: 3.6, title: "Call Roadside Assistance (*DPS)" }},
        {{ time: 5.0, title: "TxDOT Patrol Shield Active" }}
      ],
      3: [
        {{ time: 0.8, title: "Panic Stop in Travel Lane" }},
        {{ time: 2.2, title: "Trapped in Active Flow (0 MPH)" }},
        {{ time: 3.6, title: "Emergency Highway Swerve" }},
        {{ time: 5.0, title: "Secondary Crash & Tow Mandate" }}
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40';
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

      // Hazard flasher flash tick
      const flashOn = (Math.sin(t * 10) > 0);

      // =========================================================================
      // MODE 1: PROPER SHOULDER PULLOFF & TRIANGLE PLACEMENT (TTC § 545.301)
      // =========================================================================
      if (currentMode === 1) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        leftTireDangerGroup.setAttribute('opacity', '0.0');
        vehPatrol.style.opacity = '0.0';
        shoulderSafeGroup.setAttribute('opacity', '1.0');

        // Thru Traffic:
        // Blue Car in Lane 2 at constant 65 MPH
        const blueX = 52.0 + (t / duration) * 18.0; // 52% to 70%
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 65 MPH (LANE 2)';

        // Yellow Car in Lane 1 at constant 65 MPH
        const yellowX = 20.0 + (t / duration) * 16.0; // 20% to 36%
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'HIGHWAY FLOW: 65 MPH (LANE 1)';

        // Ego Car: Coasting from Lane 1 to Shoulder, then stopped
        let egoX, egoY, egoSpeed;
        if (t < 2.0) {{
          // Coasting across fog line to shoulder
          const progress = t / 2.0;
          egoX = 36.0 + progress * 16.0; // 36% to 52%
          const yLane = getLane1Y(egoX);
          const yShld = getShoulderY(egoX);
          egoY = yLane + progress * (yShld - yLane);
          egoSpeed = Math.round(50 * (1 - progress)); // 50 -> 0 MPH
          flasherFront.style.opacity = flashOn ? '1.0' : '0.0';
          flasherRear.style.opacity = flashOn ? '1.0' : '0.0';
          flasherSide.style.opacity = flashOn ? '1.0' : '0.0';
          distressCloth.style.opacity = '0.0';
          distressHood.style.opacity = '0.0';
          trianglesGroup.setAttribute('opacity', '0.0');
          occupantSafetyGroup.setAttribute('opacity', '0.0');
        }} else {{
          // Stopped 100% on shoulder at x = 52%
          egoX = 52.0;
          egoY = getShoulderY(egoX);
          egoSpeed = 0;
          flasherFront.style.opacity = flashOn ? '1.0' : '0.0';
          flasherRear.style.opacity = flashOn ? '1.0' : '0.0';
          flasherSide.style.opacity = flashOn ? '1.0' : '0.0';

          if (t >= 3.2) {{
            trianglesGroup.setAttribute('opacity', '1.0');
          }} else {{
            trianglesGroup.setAttribute('opacity', '0.0');
          }}

          if (t >= 4.5) {{
            distressCloth.style.opacity = '1.0';
            distressHood.style.opacity = '1.0';
            occupantSafetyGroup.setAttribute('opacity', '1.0');
          }} else {{
            distressCloth.style.opacity = '0.0';
            distressHood.style.opacity = '0.0';
            occupantSafetyGroup.setAttribute('opacity', '0.0');
          }}
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (PARKED)' : `${{egoSpeed}} MPH (COASTING)`;
        telemLane.textContent = (t < 2.0) ? 'COASTING TO SHOULDER' : 'IMPROVED SHOULDER (100% CLEAR)';
        telemHazards.textContent = '4-WAY ACTIVE [ON]';
        telemTriangles.textContent = (t >= 3.2) ? '3 STAGED (10/100/200 FT)' : 'DEPLOYING...';
        telemOccupants.textContent = (t >= 4.5) ? 'BEHIND GUARDRAIL' : 'SEATED & BUCKLED';
        telemStatute.textContent = '§ 545.301 PASSED';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: MECHANICAL FAILURE • COASTING SMOOTHLY TO SHOULDER';
          pillStatusText.textContent = 'TTC § 545.301 MANDATE: PULL COMPLETELY OFF PAVED TRAVEL LANES';
          hudNarrative.textContent = 'Step 1: Sudden mechanical failure in Lane 1. Driver grips steering wheel firmly, avoids slamming brakes, signals right, and coasts smoothly toward the wide right shoulder.';
          signalStateBadge.textContent = 'COASTING';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: 100% SHOULDER CLEARANCE (0 MPH) • HAZARDS ON';
          pillStatusText.textContent = 'PAVED SHOULDER ACHIEVED: TRAVEL LANES COMPLETELY UNOBSTRUCTED';
          hudNarrative.textContent = 'Step 2: Vehicle parked 100% clear of paved travel lanes. Emergency parking brake set; 4-way hazard flashers activated immediately.';
          signalStateBadge.textContent = 'SHOULDER SAFE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else if (t < 4.5) {{
          tagVehEgo.textContent = 'EGO: MUTCD WARNING TRIANGLES STAGED (10 FT • 100 FT • 200 FT)';
          pillStatusText.textContent = 'REFLECTIVE WARNING TRIANGLES: 10 FT, 100 FT & 200 FT SPACING';
          hudNarrative.textContent = 'Step 3: Staging MUTCD emergency reflective triangles: #1 at 10 ft behind vehicle, #2 at 100 ft, and #3 at 200 ft to warn approaching 65 MPH highway traffic.';
          signalStateBadge.textContent = 'TRIANGLES ACTIVE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: OCCUPANTS BEHIND GUARDRAIL • DISTRESS HOOD RAISED';
          pillStatusText.textContent = 'OCCUPANT SAFETY: REMAIN BEHIND GUARDRAIL • NEVER STAND IN TRAFFIC';
          hudNarrative.textContent = 'Step 4: Hood raised and white cloth tied to mirror as universal distress signals. Occupants exit curbside and wait safely behind the steel guardrail on the grass embankment.';
          signalStateBadge.textContent = 'PROTOCOL COMPLETE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 2: LEFT TIRE BLOWOUT HAZARD & TXDOT COURTESY PATROL SHIELD
      // =========================================================================
      else if (currentMode === 2) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        trianglesGroup.setAttribute('opacity', '0.0');
        occupantSafetyGroup.setAttribute('opacity', '0.0');
        shoulderSafeGroup.setAttribute('opacity', '1.0');

        // Blue Thru Traffic in Lane 2
        const blueX = 54.0 + (t / duration) * 16.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 65 MPH (LANE 2)';

        // Yellow Traffic moves over from Lane 1 to Lane 2 under TTC § 545.157
        let yellowX, yellowY;
        if (t < 2.2) {{
          const progress = t / 2.2;
          yellowX = 20.0 + progress * 12.0; // 20% to 32%
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'APPROACHING: 65 MPH (LANE 1)';
        }} else if (t < 4.0) {{
          const progress = (t - 2.2) / 1.8;
          yellowX = 32.0 + progress * 16.0; // 32% to 48%
          const yL1 = getLane1Y(yellowX);
          const yL2 = getLane2Y(yellowX);
          yellowY = yL1 + progress * (yL2 - yL1);
          tagVehYellow.textContent = 'VACATING LANE 1 (MOVE OVER LAW)';
        }} else {{
          const progress = (t - 4.0) / 2.0;
          yellowX = 48.0 + progress * 14.0; // 48% to 62%
          yellowY = getLane2Y(yellowX);
          tagVehYellow.textContent = 'SAFE LANE 2 PASS (TTC § 545.157)';
        }}
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;

        // Ego Car parked on shoulder
        const egoX = 52.0;
        const egoY = getShoulderY(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        flasherFront.style.opacity = flashOn ? '1.0' : '0.0';
        flasherRear.style.opacity = flashOn ? '1.0' : '0.0';
        flasherSide.style.opacity = flashOn ? '1.0' : '0.0';
        distressCloth.style.opacity = '1.0';
        distressHood.style.opacity = '1.0';

        // Courtesy Patrol arrival in Step 4 (Parked safely back on shoulder at x = 36%)
        if (t >= 4.0) {{
          vehPatrol.style.left = '36.0%';
          vehPatrol.style.top = `${{getShoulderY(36.0)}}%`;
          vehPatrol.style.opacity = '1.0';
          tagVehPatrol.textContent = 'TXDOT COURTESY PATROL: SCENE SHIELDED';
        }} else {{
          vehPatrol.style.opacity = '0.0';
        }}

        // Left tire danger zone active in steps 1, 2, 3
        if (t < 4.0) {{
          leftTireDangerGroup.setAttribute('opacity', '1.0');
        }} else {{
          leftTireDangerGroup.setAttribute('opacity', '0.0');
        }}

        telemSpeed.textContent = '0 MPH (PARKED)';
        telemLane.textContent = 'SHOULDER (LEFT TIRE FLAT)';
        telemHazards.textContent = '4-WAY ACTIVE [ON]';
        telemTriangles.textContent = 'STANDBY FOR HERO';
        telemOccupants.textContent = 'INSIDE BUCKLED / GUARDRAIL';
        telemStatute.textContent = '§ 545.301 COMPLIANT';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: LEFT TIRE BLOWOUT • TIRE FACES 65 MPH TRAFFIC';
          pillStatusText.textContent = 'CRITICAL TIRE HAZARD: LEFT-SIDE TIRE DIRECTLY EXPOSED TO TRAFFIC';
          hudNarrative.textContent = 'Step 1: Left-side blowout occurs. Vehicle is parked on shoulder, but damaged tire sits right on the edge of the high-speed travel lane.';
          signalStateBadge.textContent = 'EXPOSURE HAZARD';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'CRITICAL RULE: NEVER KNEEL IN ACTIVE TRAVEL LANE!';
          pillStatusText.textContent = 'LETHAL PEDESTRIAN RISK: NEVER ATTEMPT TIRE CHANGE ON TRAFFIC FLANK';
          hudNarrative.textContent = 'Step 2: Crucial survival rule: Never attempt to change a left-side tire on a narrow shoulder! Kneeling in Lane 1 carries fatal pedestrian impact risks from 65+ MPH traffic.';
          signalStateBadge.textContent = 'LETHAL RISK';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        }} else if (t < 4.5) {{
          tagVehEgo.textContent = 'EGO: CALLING *DPS (TXDOT COURTESY PATROL DISPATCH)';
          pillStatusText.textContent = 'SAFETY ACTION: CALL *DPS FOR HIGHWAY COURTESY PATROL / TOW';
          hudNarrative.textContent = 'Step 3: Remain inside with seatbelt fastened or step behind guardrail. Dial *DPS (*377) on cell phone for Texas Highway Patrol or TxDOT HERO service.';
          signalStateBadge.textContent = 'ASSISTANCE CALLED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: PROTECTED BY TXDOT HERO COURTESY ESCORT';
          pillStatusText.textContent = 'SCENE SECURED: TXDOT COURTESY VEHICLE SHIELDS TIRE CHANGE';
          hudNarrative.textContent = 'Step 4: TxDOT Courtesy Patrol arrives with high-intensity warning arrow board, blocking traffic into Lane 2 and creating a secure barrier for roadside repair.';
          signalStateBadge.textContent = 'SCENE PROTECTED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: STOPPING DEAD IN TRAVEL LANE (TTC § 545.301 & § 545.305)
      // =========================================================================
      else if (currentMode === 3) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-2 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        trianglesGroup.setAttribute('opacity', '0.0');
        occupantSafetyGroup.setAttribute('opacity', '0.0');
        leftTireDangerGroup.setAttribute('opacity', '0.0');
        vehPatrol.style.opacity = '0.0';
        shoulderSafeGroup.setAttribute('opacity', '0.0');

        // Blue Car in Lane 2 cruises far ahead
        const blueX = 68.0 + (t / duration) * 8.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 65 MPH (LANE 2)';

        // Ego Car: STOPS DEAD in Lane 1 at x = 45% (Unlawful Stop!)
        const egoX = 45.0;
        const egoY = getLane1Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        flasherFront.style.opacity = flashOn ? '1.0' : '0.0';
        flasherRear.style.opacity = flashOn ? '1.0' : '0.0';
        flasherSide.style.opacity = flashOn ? '1.0' : '0.0';
        distressCloth.style.opacity = '0.0';
        distressHood.style.opacity = '0.0';

        const egoSvgX = egoX * 10;
        const egoSvgY = egoY * 6;

        // Yellow Traffic approaches in Lane 1 and must emergency-brake/swerve
        let yellowX, yellowY;
        if (t < 2.2) {{
          // Approaching in Lane 1 at 65 MPH
          const progress = t / 2.2;
          yellowX = 18.0 + progress * 14.0; // 18% to 32%
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'APPROACHING: 65 MPH (LANE 1)';
        }} else if (t < 4.0) {{
          // Emergency swerve into Lane 2
          const progress = (t - 2.2) / 1.8;
          yellowX = 32.0 + progress * 8.0; // 32% to 40%
          const yL1 = getLane1Y(yellowX);
          const yL2 = getLane2Y(yellowX);
          yellowY = yL1 + progress * (yL2 - yL1);
          tagVehYellow.textContent = 'PANIC SWERVE! AVOIDING IMPACT';
        }} else {{
          // Continues in Lane 2 past Ego
          const progress = (t - 4.0) / 2.0;
          yellowX = 40.0 + progress * 12.0; // 40% to 52%
          yellowY = getLane2Y(yellowX);
          tagVehYellow.textContent = 'SWERVE EVASION COMPLETE (LANE 2)';
        }}

        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;

        telemSpeed.textContent = '0 MPH (DEAD STOP)';
        telemLane.textContent = 'LANE 1 (ACTIVE TRAVEL LANE)';
        telemHazards.textContent = '4-WAY ACTIVE';
        telemTriangles.textContent = 'NONE (UNLAWFUL STOP)';
        telemOccupants.textContent = 'EXTREME DANGER IN LANE';
        telemStatute.textContent = '§ 545.301 VIOLATION!';

        pillStatusText.textContent = 'CRITICAL STATUTORY VIOLATION: UNLAWFUL HIGHWAY LANE STOPPING (TTC § 545.301)';

        if (t < 2.0) {{
          tagVehEgo.textContent = 'EGO: UNLAWFUL STOP IN TRAVEL LANE (0 MPH)';
          hudNarrative.textContent = 'Step 1: Driver experiences breakdown and stops dead in Lane 1 instead of coasting to the open shoulder. Violates TTC § 545.301.';
          hazardImpactGroup.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
          signalStateBadge.textContent = 'LANE BLOCKED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        }} else if (t < 3.8) {{
          tagVehEgo.textContent = 'EGO: LETHAL OBSTACLE • APPROACHING 65 MPH CAR PANIC BRAKING';
          hudNarrative.textContent = 'Step 2 & 3: Approaching 65 MPH highway traffic crests and encounters stationary vehicle! Forced into emergency threshold braking and panic swerve into Lane 2.';
          hazardImpactGroup.setAttribute('opacity', '1.0');
          hazardCircle.setAttribute('cx', egoSvgX);
          hazardCircle.setAttribute('cy', egoSvgY);
          hazardStar.setAttribute('transform', `translate(${{egoSvgX}}, ${{egoSvgY}})`);
          hazardBanner.style.opacity = '1.0';
          signalStateBadge.textContent = 'CRASH RISK';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: TTC § 545.305 TOW PREEMPTION • REMOVAL AUTHORIZED';
          hudNarrative.textContent = "Step 4: Unlawful lane blockage causes massive multi-car secondary crash risk. Under TTC § 545.305, law enforcement is authorized to immediately remove (tow) the vehicle at owner's expense.";
          hazardImpactGroup.setAttribute('opacity', '1.0');
          hazardCircle.setAttribute('cx', egoSvgX);
          hazardCircle.setAttribute('cy', egoSvgY);
          hazardStar.setAttribute('transform', `translate(${{egoSvgX}}, ${{egoSvgY}})`);
          hazardBanner.style.opacity = '1.0';
          signalStateBadge.textContent = 'TOW PREEMPTION';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L05_T13_vehicle_breakdown.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 20 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_simulation()
