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

    print("Encoding Lesson 24 assets to base64...")
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
  <title>Lesson 24: Construction & Work Zone Safety (TTC § 542.404 & § 472.022)</title>
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
      background: #F97316;
      cursor: pointer;
      border: 2px solid #7C2D12;
      box-shadow: 0 0 10px rgba(249, 115, 22, 0.7);
    }}
    .custom-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.15);
      background: #FB923C;
    }}
    @keyframes pulseOrange {{
      0%, 100% {{ opacity: 0.35; filter: drop-shadow(0 0 4px #F97316); }}
      50% {{ opacity: 0.85; filter: drop-shadow(0 0 14px #FB923C); }}
    }}
    .work-pulse {{
      animation: pulseOrange 2.0s ease-in-out infinite;
    }}
    @keyframes dangerPulse {{
      0%, 100% {{ transform: scale(1); opacity: 0.75; }}
      50% {{ transform: scale(1.15); opacity: 1.0; filter: drop-shadow(0 0 16px #EF4444); }}
    }}
    .danger-pulse {{
      animation: dangerPulse 1.2s ease-in-out infinite;
      transform-origin: center;
    }}
    @keyframes beaconBlink {{
      0%, 49% {{ opacity: 1.0; filter: drop-shadow(0 0 8px #F59E0B); }}
      50%, 100% {{ opacity: 0.2; filter: none; }}
    }}
    .beacon-flash {{
      animation: beaconBlink 0.8s infinite;
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
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-orange-500/20 text-orange-400 border border-orange-500/30 mono">2.5D VECTOR ENGINE</span>
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 24</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L05-T17: Construction & Work Zone Safety — Automatic Doubled Fines & Flaggers
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Transportation Code § 542.404 (Fine Doubling When Workers Present) & § 542.501 (Flagger Authority)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-orange-500/40 bg-orange-600 text-white shadow-md shadow-orange-900/40" data-mode="1">
          1: Lawful Work Zone Merging (45 MPH)
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: Human Flagger Control (STOP/SLOW)
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Work Zone Speeding (2x Fine)
        </button>
        <div class="h-4 w-px bg-gray-700 mx-1"></div>
        <label class="flex items-center space-x-1.5 text-xs font-medium text-gray-300 cursor-pointer pr-1">
          <input type="checkbox" id="auto-loop-toggle" checked class="rounded bg-gray-800 border-gray-700 text-orange-500 focus:ring-0">
          <span>Auto-Loop</span>
        </label>
      </div>
    </header>

    <!-- INTERACTIVE STEPPER CARDS -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <button class="step-card bg-[#121824] border border-orange-500/40 rounded-xl p-2.5 text-left transition hover:border-orange-400 group relative overflow-hidden" data-step="1">
        <div class="text-[10px] font-bold text-orange-400 mono flex items-center justify-between">
          <span>STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-orange-400"></span>
        </div>
        <div id="step-title-1" class="text-xs font-bold text-white mt-1 group-hover:text-orange-200">Advance Warning Signage</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Barrel Taper Merge (45 MPH)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Flagger & Crew Buffer Zone</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Safe Work Zone Clearance</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG VECTOR OVERLAYS (WORK ZONE CHANNELIZATION, SIGNS, BARRELS, CREW) -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <marker id="arrow-orange" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#F97316" />
          </marker>
          <marker id="arrow-danger" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#EF4444" />
          </marker>
        </defs>

        <!-- CLOSED LANE 1 STRIP OVERLAY (Spans from x = 400 to 750) -->
        <g id="work-zone-closed-lane" opacity="0.45">
          <!-- Translucent hatch/tint over closed Lane 1 -->
          <polygon points="410,480 490,260 740,110 650,330" fill="#F97316" fill-opacity="0.2" stroke="#EA580C" stroke-width="1.5" stroke-dasharray="8,6" />
        </g>

        <!-- RETROREFLECTIVE CHANNELIZING BARRELS / DRUMS (Taper from Lane 1 to Lane 2) -->
        <g id="channelizing-barrels">
          <!-- Barrel 1 (Start of Taper) -->
          <g transform="translate(390, 485)">
            <rect x="-6" y="-12" width="12" height="24" rx="3" fill="#EA580C" stroke="#7C2D12" stroke-width="0.8" />
            <rect x="-6" y="-6" width="12" height="5" fill="#FFFFFF" />
            <rect x="-6" y="3" width="12" height="5" fill="#FFFFFF" />
            <circle cx="0" cy="-14" r="3" fill="#F59E0B" class="beacon-flash" />
          </g>
          <!-- Barrel 2 -->
          <g transform="translate(425, 435)">
            <rect x="-6" y="-12" width="12" height="24" rx="3" fill="#EA580C" stroke="#7C2D12" stroke-width="0.8" />
            <rect x="-6" y="-6" width="12" height="5" fill="#FFFFFF" />
            <rect x="-6" y="3" width="12" height="5" fill="#FFFFFF" />
          </g>
          <!-- Barrel 3 -->
          <g transform="translate(460, 385)">
            <rect x="-6" y="-12" width="12" height="24" rx="3" fill="#EA580C" stroke="#7C2D12" stroke-width="0.8" />
            <rect x="-6" y="-6" width="12" height="5" fill="#FFFFFF" />
            <rect x="-6" y="3" width="12" height="5" fill="#FFFFFF" />
          </g>
          <!-- Barrel 4 (Taper pinch at Lane 2 edge) -->
          <g transform="translate(495, 335)">
            <rect x="-6" y="-12" width="12" height="24" rx="3" fill="#EA580C" stroke="#7C2D12" stroke-width="0.8" />
            <rect x="-6" y="-6" width="12" height="5" fill="#FFFFFF" />
            <rect x="-6" y="3" width="12" height="5" fill="#FFFFFF" />
            <circle cx="0" cy="-14" r="3" fill="#F59E0B" class="beacon-flash" />
          </g>
          <!-- Barrel 5 (Work area buffer) -->
          <g transform="translate(560, 275)">
            <rect x="-6" y="-12" width="12" height="24" rx="3" fill="#EA580C" stroke="#7C2D12" stroke-width="0.8" />
            <rect x="-6" y="-6" width="12" height="5" fill="#FFFFFF" />
            <rect x="-6" y="3" width="12" height="5" fill="#FFFFFF" />
          </g>
          <!-- Barrel 6 -->
          <g transform="translate(630, 210)">
            <rect x="-6" y="-12" width="12" height="24" rx="3" fill="#EA580C" stroke="#7C2D12" stroke-width="0.8" />
            <rect x="-6" y="-6" width="12" height="5" fill="#FFFFFF" />
            <rect x="-6" y="3" width="12" height="5" fill="#FFFFFF" />
          </g>
        </g>

        <!-- ACTIVE HIGHWAY ROAD CREW & WORK ZONE CALLOUTS -->
        <g id="crew-and-equipment" transform="translate(585, 315)">
          <!-- Construction Utility Truck Graphic -->
          <rect x="-24" y="-14" width="48" height="26" rx="4" fill="#F59E0B" stroke="#78350F" stroke-width="1.2" />
          <rect x="6" y="-10" width="16" height="18" rx="2" fill="#1E293B" />
          <!-- Flashing Rooftop Amber Bar -->
          <rect x="-6" y="-18" width="12" height="4" rx="2" fill="#FBBF24" class="beacon-flash" />
          
          <!-- Human Worker 1 (in hi-vis safety vest & hard hat) -->
          <g transform="translate(32, -6)">
            <circle cx="0" cy="-10" r="4.5" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8" />
            <path d="M -4,-5 L 4,-5 L 5,8 L -5,8 Z" fill="#EA580C" stroke="#C2410C" stroke-width="0.8" />
            <rect x="-3" y="-1" width="6" height="2" fill="#FFFFFF" />
          </g>

          <!-- Human Worker 2 -->
          <g transform="translate(42, 6)">
            <circle cx="0" cy="-10" r="4.5" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8" />
            <path d="M -4,-5 L 4,-5 L 5,8 L -5,8 Z" fill="#EA580C" stroke="#C2410C" stroke-width="0.8" />
            <rect x="-3" y="-1" width="6" height="2" fill="#FFFFFF" />
          </g>
        </g>

        <!-- HUMAN FLAGGER WITH ROTATABLE PADDLE (Stationed at protected taper shoulder x = 540, y = 350) -->
        <g id="human-flagger-group" transform="translate(540, 350)">
          <!-- Flagger Body in Hi-Vis Vest -->
          <circle cx="0" cy="-14" r="5" fill="#FEF08A" stroke="#CA8A04" stroke-width="1" />
          <path d="M -5,-8 L 5,-8 L 6,10 L -6,10 Z" fill="#EA580C" stroke="#C2410C" stroke-width="1" />
          <rect x="-4" y="-3" width="8" height="2.5" fill="#FFFFFF" />
          <!-- Flagger Paddle (Rotates between SLOW and STOP, held towards oncoming traffic) -->
          <g id="flagger-paddle" transform="translate(-14, -8) rotate(0)">
            <line x1="0" y1="0" x2="0" y2="24" stroke="#4B5563" stroke-width="2" />
            <circle id="paddle-circle" cx="0" cy="-5" r="9.5" fill="#EA580C" stroke="#7C2D12" stroke-width="1.2" />
            <text id="paddle-text" x="0" y="-2" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="5" font-weight="900" text-anchor="middle">SLOW</text>
          </g>
          <!-- Flagger Authority Badge (Positioned below flagger on shoulder pavement to avoid vehicle tag collisions) -->
          <g transform="translate(0, 20)">
            <rect x="-35" y="-7" width="70" height="14" rx="7" fill="#431407" stroke="#EA580C" stroke-width="1" />
            <text x="0" y="3" fill="#FDBA74" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="900" text-anchor="middle">TX-FLAGGER</text>
          </g>
        </g>

        <!-- ROADSIDE ADVANCE WARNING SIGNAGE (In grassy embankment before taper) -->
        <g id="advance-warning-signage">
          <!-- MUTCD W20-1 (Diamond: ROAD WORK AHEAD) -->
          <g transform="translate(450, 440)">
            <polygon points="0,-16 16,0 0,16 -16,0" fill="#EA580C" stroke="#7C2D12" stroke-width="1.5" />
            <rect x="-1" y="16" width="2" height="16" fill="#4B5563" />
            <text x="0" y="-4" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="4.2" font-weight="900" text-anchor="middle">ROAD</text>
            <text x="0" y="2" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="4.2" font-weight="900" text-anchor="middle">WORK</text>
            <text x="0" y="8" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="3.5" font-weight="800" text-anchor="middle">AHEAD</text>
          </g>

          <!-- Regulatory Speed Limit & Doubled Fines Sign -->
          <g transform="translate(535, 440)">
            <rect x="-42" y="-14" width="84" height="28" rx="4" fill="#FFFFFF" stroke="#000000" stroke-width="1.5" />
            <text x="0" y="-4" fill="#000000" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="900" text-anchor="middle">SPEED LIMIT 45</text>
            <rect x="-38" y="0" width="76" height="11" rx="2" fill="#EA580C" />
            <text x="0" y="8" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="900" text-anchor="middle">$ FINES DOUBLE $</text>
          </g>
        </g>

        <!-- MERGE TAPER TRAJECTORY ARROW (Lane 1 into Lane 2) -->
        <g id="merge-arrow-group" opacity="1.0">
          <path d="M 370,490 C 400,450 430,370 460,340" fill="none" stroke="#F97316" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-orange)" />
        </g>

        <!-- MODE 3: SPEEDING IMPACT HAZARD & VIOLATION CALLOUT -->
        <g id="spin-hazard-group" opacity="0.0">
          <ellipse cx="560" cy="270" rx="65" ry="32" fill="none" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="8,6" class="danger-pulse" />
          <polygon id="hazard-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- BLUE LEAD VEHICLE (LANE 2 AHEAD AT 45 MPH) -->
      <div id="veh-blue" class="absolute z-20 pointer-events-none transition-transform" style="left: 70.0%; top: 22.4%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_ne_b64}" alt="Lead Vehicle Lane 2" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          WORK FLOW: 45 MPH (LANE 2)
        </div>
      </div>

      <!-- YELLOW TRAILING VEHICLE (LANE 2 FOLLOWING AT 45 MPH) -->
      <div id="veh-yellow" class="absolute z-20 pointer-events-none transition-transform" style="left: 17.0%; top: 75.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Traffic Lane 2" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          TRAFFIC: 45 MPH (LANE 2)
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - WORK ZONE MERGE & SPEED COMPLIANCE) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none" style="left: 36.0%; top: 70.7%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_red_ne_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          <!-- Left Turn Blinker -->
          <div id="blinker-left" class="absolute w-2 h-2 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 25%; left: 75%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 35%; left: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-orange-500/40 text-[9.5px] font-bold text-orange-300 mono shadow-lg tracking-wider">
          EGO: 45 MPH • EARLY MERGE SIGNAL
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#431407]/95 border border-orange-500 text-orange-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-orange-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS WORK ZONE RULE: OBEY FLAGGERS • MERGE EARLY • FINES DOUBLE WITH WORKERS</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#431407]/90 border border-orange-500/50 text-orange-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-orange-400"></span>
        <span id="compliance-text">TTC § 542.404 WORK ZONE STATUTORY COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & WORK ZONE HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[270px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-orange-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">WORK ZONE SAFETY HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-400 border border-orange-500/30 mono">45 MPH LIMIT</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-orange-400 mono text-right" id="telem-speed">45 MPH</span>

          <span class="text-gray-400">Posted Limit:</span>
          <span class="font-bold text-white mono text-right" id="telem-limit">45 MPH (WORK ZONE)</span>

          <span class="text-gray-400">Active Workers:</span>
          <span class="font-bold text-amber-400 mono text-right" id="telem-workers">PRESENT ON SITE</span>

          <span class="text-gray-400">Penalty Status:</span>
          <span class="font-bold text-rose-400 mono text-right" id="telem-fines">2X FINES DOUBLE</span>

          <span class="text-gray-400">Flagger Command:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-flagger">SLOW / PROCEED</span>

          <span class="text-gray-400">Lane Status:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-lane">LANE 2 SECURED</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Approaching work zone. Advance signs warn of Lane 1 closure. Driver reduces speed to 45 MPH and prepares to merge.
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER (Positioned below status pill in clear air space) -->
      <div id="hazard-banner" class="absolute z-35 w-[265px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL: WORK ZONE VIOLATION</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>WORKER ENDANGERMENT (TTC § 542.404)</strong><br>
          Speeding through channelized cones endangers road crew. Moving violations result in mandatory 2X fine doubling and court appearance.
        </div>
      </div>

    </div>

    <!-- TIMELINE & PLAYBACK CONTROLS -->
    <footer class="bg-[#121824] border border-[#1E293B] rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <button id="play-pause-btn" class="w-10 h-10 rounded-xl bg-orange-600 hover:bg-orange-500 text-white flex items-center justify-center shadow-lg transition" title="Play/Pause">
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
    let currentMode = 1; // 1: Lawful Work Zone Merging, 2: Human Flagger Control, 3: Work Zone Speeding Hazard
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

    const blinkerLeft = document.getElementById('blinker-left');
    const brakeLights = document.getElementById('brake-lights');

    const flaggerPaddle = document.getElementById('flagger-paddle');
    const paddleCircle = document.getElementById('paddle-circle');
    const paddleText = document.getElementById('paddle-text');
    const mergeArrowGroup = document.getElementById('merge-arrow-group');

    const spinHazardGroup = document.getElementById('spin-hazard-group');
    const hazardStar = document.getElementById('hazard-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const telemSpeed = document.getElementById('telem-speed');
    const telemLimit = document.getElementById('telem-limit');
    const telemWorkers = document.getElementById('telem-workers');
    const telemFines = document.getElementById('telem-fines');
    const telemFlagger = document.getElementById('telem-flagger');
    const telemLane = document.getElementById('telem-lane');
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
        {{ time: 0.8, title: "Advance Warning Signage" }},
        {{ time: 2.2, title: "Barrel Taper Merge (45 MPH)" }},
        {{ time: 3.6, title: "Flagger & Crew Buffer Zone" }},
        {{ time: 5.0, title: "Safe Work Zone Clearance" }}
      ],
      2: [
        {{ time: 0.8, title: "Flagger Signals Red 'STOP'" }},
        {{ time: 2.2, title: "Ego Stops at Taper Line" }},
        {{ time: 3.6, title: "Flagger Rotates to 'SLOW'" }},
        {{ time: 5.0, title: "Proceed Past Active Crew" }}
      ],
      3: [
        {{ time: 0.8, title: "65 MPH in 45 MPH Work Zone" }},
        {{ time: 2.2, title: "Late Swerve Into Cones!" }},
        {{ time: 3.6, title: "Near Miss With Road Crew" }},
        {{ time: 5.0, title: "Doubled Fine Citation ($800)" }}
      ]
    }};

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('.mode-btn').forEach(btn => {{
        const m = parseInt(btn.dataset.mode);
        if (m === mode) {{
          if (m === 1) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-orange-500/40 bg-orange-600 text-white shadow-md shadow-orange-900/40';
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
      // MODE 1: LAWFUL WORK ZONE MERGING & 45 MPH SPEED REDUCTION (TTC § 542.404)
      // =========================================================================
      if (currentMode === 1) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-orange-500/40 text-[9.5px] font-bold text-orange-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        brakeLights.style.opacity = '0.0';
        mergeArrowGroup.setAttribute('opacity', '1.0');

        // Flagger shows SLOW paddle
        paddleCircle.setAttribute('fill', '#EA580C');
        paddleText.textContent = 'SLOW';
        telemFlagger.textContent = 'SLOW / PROCEED';
        telemFlagger.className = 'font-bold text-emerald-400 mono text-right';

        // Blue Lead Vehicle in Lane 2 ahead at 45 MPH
        const blueX = 68.0 + (t / duration) * 8.0; // 68% to 76%
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'WORK FLOW: 45 MPH (LANE 2)';

        // Yellow Trailing Vehicle in Lane 2 following at 45 MPH
        const yellowX = 16.0 + (t / duration) * 8.0; // 16% to 24%
        const yellowY = getLane2Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'TRAFFIC: 45 MPH (LANE 2)';

        // Ego Car: Approaching in Lane 1, signals, merges into Lane 2 at taper (45 MPH)
        let egoX, egoY, egoSpeed;
        if (t < 2.0) {{
          // Approach in Lane 1, slowing 55 -> 45 MPH, signaling left
          const progress = t / 2.0;
          egoX = 35.0 + progress * 7.0; // 35% to 42%
          egoY = getLane1Y(egoX);
          egoSpeed = Math.round(55 - progress * 10);
          blinkerLeft.style.opacity = blinkOn ? '1.0' : '0.0';
        }} else if (t < 3.8) {{
          // Taper diagonal merge from Lane 1 into Lane 2
          const progress = (t - 2.0) / 1.8;
          egoX = 42.0 + progress * 6.0; // 42% to 48%
          const y1 = getLane1Y(egoX);
          const y2 = getLane2Y(egoX);
          egoY = y1 + progress * (y2 - y1);
          egoSpeed = 45;
          blinkerLeft.style.opacity = blinkOn ? '1.0' : '0.0';
        }} else {{
          // Stabilized in Lane 2 cruising past crew at 45 MPH
          const progress = (t - 3.8) / 2.2;
          egoX = 48.0 + progress * 6.0; // 48% to 54%
          egoY = getLane2Y(egoX);
          egoSpeed = 45;
          blinkerLeft.style.opacity = '0.0';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';

        telemSpeed.textContent = `${{egoSpeed}} MPH`;
        telemLimit.textContent = '45 MPH (WORK ZONE)';
        telemWorkers.textContent = 'PRESENT ON SITE';
        telemFines.textContent = '2X FINES DOUBLE';
        telemLane.textContent = (t < 2.0) ? 'LANE 1 (CLOSING)' : ((t < 3.8) ? 'MERGING TO LANE 2' : 'LANE 2 SECURED');

        pillStatusText.textContent = 'TEXAS WORK ZONE RULE: OBEY FLAGGERS • MERGE EARLY • FINES DOUBLE WITH WORKERS';

        if (t < 2.0) {{
          tagVehEgo.textContent = 'EGO: 45 MPH • EARLY MERGE SIGNAL';
          hudNarrative.textContent = 'Step 1: Driver notes W20-1 "ROAD WORK AHEAD" sign. Signals left for not less than 100 ft and eases speed to 45 MPH.';
          signalStateBadge.textContent = 'EARLY MERGE SIGNAL';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-400 border border-orange-500/30 mono';
        }} else if (t < 3.8) {{
          tagVehEgo.textContent = 'EGO: MERGING AT TAPER (45 MPH)';
          hudNarrative.textContent = 'Step 2: Driver merges smoothly along retroreflective barrel taper into open Lane 2 gap without cutting off traffic.';
          signalStateBadge.textContent = 'BARREL TAPER MERGE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-400 border border-orange-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: 45 MPH • BUFFER ZONE SECURE';
          hudNarrative.textContent = 'Step 3 & 4: Ego safely clears work zone in Lane 2 with ample buffer from active road crew. Full TTC § 542.404 compliance verified.';
          signalStateBadge.textContent = 'COMPLIANCE VERIFIED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 2: HUMAN FLAGGER CONTROL (STOP / SLOW PADDLE PREEMPTION)
      // =========================================================================
      else if (currentMode === 2) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-orange-500/40 text-[9.5px] font-bold text-orange-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        mergeArrowGroup.setAttribute('opacity', '0.0');
        blinkerLeft.style.opacity = '0.0';

        // Blue Lead Vehicle far ahead
        const blueX = 72.0 + (t / duration) * 6.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'THRU FLOW: 25 MPH (LANE 2)';

        // Yellow Trailing Vehicle waiting behind Ego
        const yellowX = 18.0;
        const yellowY = getLane2Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'STOPPED BEHIND EGO (TAPER)';

        // Flagger Paddle State & Ego Motion
        let egoX, egoY, egoSpeed;
        if (t < 2.5) {{
          // Flagger holds STOP paddle (Red octagonal face)
          paddleCircle.setAttribute('fill', '#EF4444');
          paddleText.textContent = 'STOP';
          telemFlagger.textContent = 'STOP (RED PADDLE)';
          telemFlagger.className = 'font-bold text-red-400 mono text-right';

          // Ego decelerates to a complete stop at the taper line (x = 42%)
          const progress = Math.min(1.0, t / 2.0);
          egoX = 36.0 + progress * 6.0; // 36% to 42%
          egoY = getLane2Y(egoX);
          egoSpeed = Math.round(30 * (1 - progress));
          brakeLights.style.opacity = (egoSpeed > 0) ? '1.0' : '0.0';
        }} else {{
          // Flagger rotates paddle to SLOW (Orange face)
          paddleCircle.setAttribute('fill', '#EA580C');
          paddleText.textContent = 'SLOW';
          telemFlagger.textContent = 'SLOW / PROCEED';
          telemFlagger.className = 'font-bold text-emerald-400 mono text-right';

          // Ego accelerates gently to 20 MPH past the work crew
          const progress = (t - 2.5) / 3.5;
          egoX = 42.0 + progress * 10.0; // 42% to 52%
          egoY = getLane2Y(egoX);
          egoSpeed = Math.min(20, Math.round(progress * 20));
          brakeLights.style.opacity = '0.0';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (STOPPED)' : `${{egoSpeed}} MPH`;
        telemLimit.textContent = 'FLAGGER PREEMPTION';
        telemWorkers.textContent = 'PRESENT ON SITE';
        telemFines.textContent = '2X FINES DOUBLE';
        telemLane.textContent = (egoSpeed === 0) ? 'STOPPED AT TAPER' : 'PROCEEDING CAUTIOUSLY';

        pillStatusText.textContent = 'FLAGGER LAW (TTC § 542.501): HUMAN FLAGGER COMMAND OVERRULES ALL SIGNS';

        if (t < 2.5) {{
          tagVehEgo.textContent = 'EGO: STOPPED AT TAPER LINE • OBEYING FLAGGER';
          hudNarrative.textContent = 'Step 1 & 2: Human flagger holds red STOP paddle to let equipment enter. Driver comes to a complete halt at the barrel taper under § 542.501.';
          signalStateBadge.textContent = 'FLAGGER STOP';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: 20 MPH • PROCEEDING PAST CREW';
          hudNarrative.textContent = 'Step 3 & 4: Flagger rotates paddle to SLOW. Ego proceeds at 20 MPH with alert scanning past workers and equipment.';
          signalStateBadge.textContent = 'FLAGGER SLOW';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: WORK ZONE SPEEDING & WORKER ENDANGERMENT (2X FINES)
      // =========================================================================
      else if (currentMode === 3) {{
        if (t < 2.0) {{
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        }} else {{
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        }}
        blinkerLeft.style.opacity = '0.0';
        mergeArrowGroup.setAttribute('opacity', '0.0');

        // Blue Lead Vehicle far ahead in Lane 2
        const blueX = 74.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'WORK FLOW: 45 MPH (LANE 2)';

        // Yellow Vehicle following safely at 45 MPH
        const yellowX = 18.0 + (t / duration) * 4.0;
        const yellowY = getLane2Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'LAWFUL DRIVER: 45 MPH (LANE 2)';

        // Flagger waves frantic emergency warning
        paddleCircle.setAttribute('fill', '#EF4444');
        paddleText.textContent = 'STOP!';
        telemFlagger.textContent = 'WARNING: VIOLATOR!';
        telemFlagger.className = 'font-bold text-red-500 mono text-right';

        // Ego Car: Speeding at 65 MPH in Lane 1, late swerve, strikes barrels near crew
        let egoX, egoY, yawAngle, egoSpeed;
        if (t < 2.0) {{
          const progress = t / 2.0;
          egoX = 35.0 + progress * 8.0; // 35% to 43% in Lane 1
          egoY = getLane1Y(egoX);
          yawAngle = 0;
          egoSpeed = 65;
          brakeLights.style.opacity = '0.0';
          spinHazardGroup.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
        }} else if (t < 3.2) {{
          const progress = (t - 2.0) / 1.2;
          egoX = 43.0 + progress * 14.0; // 43% to 57%
          const y1 = getLane1Y(egoX);
          const y2 = getLane2Y(egoX);
          egoY = y1 + progress * (y2 - y1) - 15; // aggressive swerve into barrel zone
          yawAngle = progress * 18.0;
          egoSpeed = Math.round(65 * (1 - progress * 0.7)); // 65 -> 20 MPH
          brakeLights.style.opacity = '1.0';
          spinHazardGroup.setAttribute('opacity', '1.0');
          hazardStar.setAttribute('transform', `translate(${{egoX * 10}}, ${{egoY * 6}})`);
          hazardBanner.style.opacity = '1.0';
        }} else {{
          // Stopped after smashing barrels near work truck
          egoX = 57.0;
          egoY = getLane2Y(egoX) - 5;
          yawAngle = 18.0;
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

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (PULLED OVER)' : `${{egoSpeed}} MPH (SPEEDING)`;
        telemLimit.textContent = '45 MPH (EXCEEDED by 20+)';
        telemWorkers.textContent = 'WORKERS ENDANGERED';
        telemFines.textContent = 'AUTOMATIC 2X ($800+)';
        telemLane.textContent = (t < 2.0) ? 'SPEEDING IN CLOSED LANE' : 'BARRELS STRUCK / CITATION';

        pillStatusText.textContent = 'CRITICAL WORK ZONE ERROR: FINES AUTOMATICALLY DOUBLE WHEN WORKERS PRESENT';

        if (t < 2.0) {{
          tagVehEgo.textContent = 'EGO: 65 MPH IN 45 MPH WORK ZONE • ILLEGAL SPEED';
          hudNarrative.textContent = 'Step 1: Driver ignores W20-1 work zone signs and barrels through closed lane taper at full 65 MPH highway speed.';
          signalStateBadge.textContent = 'RECKLESS SPEED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: LATE PANIC SWERVE! CONES STRUCK NEAR ROAD CREW';
          hudNarrative.textContent = 'Step 2: Driver spots work truck too late, locks brakes, and violently swerves, sending channelizing barrels flying near workers.';
          signalStateBadge.textContent = 'CONES STRUCK';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: CITATION ISSUED • MANDATORY 2X FINE ($800+)';
          hudNarrative.textContent = 'Step 3 & 4: Police officer on site issues citation under TTC § 542.404. Speeding fine is legally doubled; no deferred disposition.';
          signalStateBadge.textContent = '2X FINE DOUBLED';
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
          card.classList.add('border-orange-500/60', 'bg-orange-950/20');
        }} else {{
          card.classList.remove('border-orange-500/60', 'bg-orange-950/20');
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L05_T17_work_zones.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 24 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_simulation()
