import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/uncontrolled_intersection_final.png'
car_red_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_red_nw_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_nw.png'
car_blue_sw_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_sw_clean.png'

print("Encoding assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_ne_b64 = get_base64_img(car_red_ne_path)
car_red_nw_b64 = get_base64_img(car_red_nw_path)
car_blue_sw_b64 = get_base64_img(car_blue_sw_path)
print("Assets encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en" class="h-full bg-[#0B0E11] text-[#ECEFF1] antialiased">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Lesson L04-T02: Responding to Traffic Control Devices — Flashing Yellow Arrow (TTC § 544.007)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
    
    .timeline-slider {{
      -webkit-appearance: none;
      appearance: none;
      height: 6px;
      border-radius: 3px;
      background: #232B36;
      outline: none;
      transition: background .15s ease-in-out;
    }}
    .timeline-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #10B981;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.7);
      border: 2px solid #FFFFFF;
      transition: transform 0.1s ease;
    }}
    .timeline-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.2);
    }}

    .step-btn.active {{
      background-color: #2563EB;
      color: #FFFFFF;
      border-color: #3B82F6;
      box-shadow: 0 0 12px rgba(37, 99, 235, 0.4);
    }}

    @keyframes pulseSlow {{
      0%, 100% {{ transform: scale(1); opacity: 0.9; }}
      50% {{ transform: scale(1.08); opacity: 1; }}
    }}
    .pulse-danger {{
      animation: pulseSlow 1.4s infinite ease-in-out;
    }}

    @keyframes flashAmber {{
      0%, 100% {{ opacity: 1.0; filter: drop-shadow(0 0 6px #F59E0B); }}
      50% {{ opacity: 0.15; filter: none; }}
    }}
    .flash-yellow-arrow {{
      animation: flashAmber 1.0s infinite ease-in-out;
    }}

    @keyframes yieldPulse {{
      0%, 100% {{ stroke-opacity: 0.8; stroke-width: 2.5; }}
      50% {{ stroke-opacity: 0.3; stroke-width: 1.5; }}
    }}
    .yield-line-anim {{
      animation: yieldPulse 1.2s infinite ease-in-out;
    }}
  </style>
</head>
<body class="flex flex-col h-screen w-screen overflow-hidden bg-[#0A0D12]">

  <!-- TOP HEADER -->
  <header class="bg-[#12161F] border-b border-[#212734] px-6 py-2 flex items-center justify-between z-30 shrink-0 shadow-md">
    <div class="flex items-center space-x-3">
      <div class="flex items-center space-x-2">
        <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 mono">TDLR ADE-1317</span>
        <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">2.5D VECTOR ENGINE</span>
      </div>
      <div class="h-4 w-px bg-gray-700"></div>
      <div>
        <h1 class="text-xs md:text-sm font-extrabold text-white tracking-wide flex items-center space-x-2">
          <span>TEXAS DRIVING–RULE ANIMATION SYSTEM</span>
        </h1>
        <p class="text-[11px] text-gray-400">Lesson L04–T02: Traffic Control Devices — Flashing Yellow Arrow (Permissive) vs. Green Arrow (Texas Transportation Code § 544.007)</p>
      </div>
    </div>

    <!-- TRI-SCENARIO MODE TOGGLE -->
    <div class="flex items-center space-x-3">
      <div class="flex items-center rounded-lg bg-[#19202B] p-0.5 border border-[#2B3545]">
        <button id="scenario-btn-fya" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-amber-500 text-black shadow">
          <span>1: Flashing Yellow (Permissive)</span>
        </button>
        <button id="scenario-btn-green" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1">
          <span>2: Green Arrow (Protected)</span>
        </button>
        <button id="scenario-btn-hazard" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1">
          <span>Hazard: FYA Failure to Yield</span>
        </button>
      </div>

      <div class="h-4 w-px bg-gray-700"></div>

      <div class="flex items-center space-x-2 bg-[#1C222C] px-3 py-1 rounded-lg border border-[#2D3644] text-xs">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-gray-300 font-medium mono text-[11px]">Deterministic 60 FPS</span>
      </div>
      
      <label class="flex items-center cursor-pointer space-x-1.5 text-xs text-gray-300">
        <input type="checkbox" id="chk-autoloop" checked class="rounded border-gray-700 bg-gray-800 text-emerald-500 focus:ring-0">
        <span class="text-[11px] font-medium text-gray-300">Auto-Loop</span>
      </label>
    </div>
  </header>

  <!-- STEP CONTROLLER BAR (4 Canonical Stepper States) -->
  <nav class="bg-[#161B24] border-b border-[#232B38] px-6 py-1.5 flex items-center justify-between z-20 shrink-0">
    <div class="flex items-center space-x-2" id="step-btn-container">
      <button class="step-btn px-3 py-1 rounded-md text-xs font-semibold bg-[#212732] border border-[#2F3746] text-gray-300 hover:text-white hover:bg-[#2B3342] transition active" data-step="1" data-time="0.5">
        Step 1: Signal Identification &amp; Approach
      </button>
      <button class="step-btn px-3 py-1 rounded-md text-xs font-semibold bg-[#212732] border border-[#2F3746] text-gray-300 hover:text-white hover:bg-[#2B3342] transition" data-step="2" data-time="2.5">
        Step 2: Oncoming Traffic Yield Hold
      </button>
      <button class="step-btn px-3 py-1 rounded-md text-xs font-semibold bg-[#212732] border border-[#2F3746] text-gray-300 hover:text-white hover:bg-[#2B3342] transition" data-step="3" data-time="4.5">
        Step 3: Gap Verification &amp; Clearance
      </button>
      <button class="step-btn px-3 py-1 rounded-md text-xs font-semibold bg-[#212732] border border-[#2F3746] text-gray-300 hover:text-white hover:bg-[#2B3342] transition" data-step="4" data-time="6.8">
        Step 4: Lawful Permissive Execution
      </button>
    </div>

    <!-- Stepper Navigation (Previous / Next) -->
    <div class="flex items-center space-x-2">
      <button id="btn-prev-step" class="px-2.5 py-1 rounded-md bg-[#212732] hover:bg-[#2B3342] border border-[#2F3746] text-xs font-semibold text-gray-300 hover:text-white transition flex items-center space-x-1">
        <span>&lsaquo; Prev</span>
      </button>
      <span id="step-indicator" class="text-xs font-bold text-amber-400 mono px-2">Step 1 of 4</span>
      <button id="btn-next-step" class="px-2.5 py-1 rounded-md bg-[#212732] hover:bg-[#2B3342] border border-[#2F3746] text-xs font-semibold text-gray-300 hover:text-white transition flex items-center space-x-1">
        <span>Next &rsaquo;</span>
      </button>
    </div>
  </nav>

  <!-- MAIN SIMULATION WORKSPACE -->
  <main class="flex-1 flex overflow-hidden relative">

    <!-- VIEWPORT CONTAINER -->
    <div id="viewport-container" class="flex-1 relative overflow-hidden flex items-center justify-center p-2 bg-[#0B0E11]">

      <!-- STAGE WRAPPER (Definite responsive sizing based on viewport height and 1024/667 aspect ratio) -->
      <div id="stage-wrapper" class="relative rounded-2xl overflow-hidden shadow-2xl border border-[#262F3D] bg-[#000000]" style="width: min(calc((100vh - 180px) * 1024 / 667), 960px); max-width: calc(100% - 16px); aspect-ratio: 1024 / 667;">
        
        <!-- LAYER 0: CLEAN VECTOR ISOMETRIC INTERSECTION BASE -->
        <img src="{road_b64}" alt="Texas Signalized Intersection Diorama" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

        <!-- LAYER 1: DYNAMIC SVG OVERLAYS (Traffic Lights, Left Turn Arc, Conflict Zone) -->
        <svg id="stage-svg" viewBox="0 0 1024 667" class="absolute inset-0 w-full h-full pointer-events-none z-10">
          <defs>
            <!-- Glowing Amber Filter -->
            <filter id="glow-amber" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <!-- Glowing Green Filter -->
            <filter id="glow-green" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <!-- Glowing Red Filter -->
            <filter id="glow-red" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <!-- ADVANCE STOP LINE & LEFT TURN BAY ACCENTUATIONS -->
          <!-- SW Left Turn Yield Line (Vehicle A) -->
          <line x1="355" y1="485" x2="415" y2="450" stroke="#F59E0B" stroke-width="4" stroke-dasharray="8,5" stroke-linecap="round" class="yield-line-anim" id="sw-yield-line" />
          <!-- NE Oncoming Stop Line (Vehicle B) -->
          <line x1="525" y1="218" x2="578" y2="248" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.9" />

          <!-- PERMISSIVE LEFT-TURN TRAJECTORY PATH GUIDE -->
          <path id="left-turn-guide" d="M 389 465 Q 450 400, 440 360 T 266 280" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="6,4" opacity="0.75" />

          <!-- YIELD / CONFLICT CROSSING ZONE AT INTERSECTION APEX (440, 360) -->
          <circle id="conflict-yield-zone" cx="440" cy="360" r="42" fill="#F59E0B" fill-opacity="0.15" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6,4" opacity="0.8" />

          <!-- =============================================================== -->
          <!-- 4-SECTION TEXAS LEFT-TURN SIGNAL MAST (Controls Vehicle A)      -->
          <!-- Positioned at SW corner curb: translate(306, 470)               -->
          <!-- Sections from top to bottom:                                    -->
          <!-- 1. Red Ball (Top)                                               -->
          <!-- 2. Steady Yellow Arrow                                          -->
          <!-- 3. Flashing Yellow Arrow (FYA)                                  -->
          <!-- 4. Steady Green Arrow (Bottom)                                  -->
          <!-- =============================================================== -->
          <g id="signal-mast-sw" transform="translate(306, 470)">
            <!-- Signal Mast Pole -->
            <line x1="0" y1="25" x2="0" y2="45" stroke="#4B5563" stroke-width="3.5" />
            
            <!-- Mast Housing (4-Section vertical body with backplate) -->
            <rect x="-10" y="-38" width="20" height="62" rx="4" fill="#111827" stroke="#374151" stroke-width="1.5" />
            
            <!-- Lens 1: Red Ball (cy = -29) -->
            <circle id="sw-lens-red" cx="0" cy="-29" r="4.5" fill="#374151" opacity="0.3" />
            
            <!-- Lens 2: Steady Yellow Arrow (cy = -15) -->
            <circle id="sw-lens-yellow-arrow" cx="0" cy="-15" r="4.5" fill="#374151" opacity="0.3" />
            
            <!-- Lens 3: Flashing Yellow Arrow (cy = -1) -->
            <g id="sw-lens-fya-group" class="flash-yellow-arrow">
              <circle id="sw-lens-fya-bg" cx="0" cy="-1" r="5" fill="#F59E0B" filter="url(#glow-amber)" />
              <!-- Left Arrow Glyph -->
              <path d="M 2 -1 L -2 -1 M -0.5 -3 L -2.5 -1 L -0.5 1" stroke="#111827" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
            </g>

            <!-- Lens 4: Steady Green Arrow (cy = 13) -->
            <g id="sw-lens-green-arrow-group" opacity="0.2">
              <circle id="sw-lens-green-arrow-bg" cx="0" cy="13" r="5" fill="#10B981" filter="url(#glow-green)" />
              <path d="M 2 13 L -2 13 M -0.5 11 L -2.5 13 L -0.5 15" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
            </g>
          </g>

          <!-- =============================================================== -->
          <!-- ONCOMING OPPOSING SIGNAL (Controls Vehicle B)                   -->
          <!-- Positioned at NE approach: translate(590, 215)                  -->
          <!-- =============================================================== -->
          <g id="signal-mast-ne" transform="translate(590, 215)">
            <rect x="-8" y="-20" width="16" height="40" rx="3" fill="#111827" stroke="#374151" stroke-width="1.2" />
            <!-- Red Lens (Top) -->
            <circle id="ne-lens-red" cx="0" cy="-11" r="4" fill="#EF4444" filter="url(#glow-red)" opacity="0.2" />
            <!-- Green Lens (Bottom) -->
            <circle id="ne-lens-green" cx="0" cy="9" r="4" fill="#10B981" filter="url(#glow-green)" opacity="1.0" />
          </g>

          <!-- HAZARD DEMO: CRITICAL COLLISION IMPACT ZONE AT APEX (450, 294) -->
          <g id="hazard-collision-zone" opacity="0.0">
            <circle cx="450" cy="294" r="55" fill="#EF4444" fill-opacity="0.25" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" class="pulse-danger" />
            <circle cx="450" cy="294" r="30" fill="#DC2626" fill-opacity="0.45" stroke="#FCA5A5" stroke-width="2" />
            <line x1="390" y1="294" x2="510" y2="294" stroke="#EF4444" stroke-width="2.5" />
            <line x1="450" y1="234" x2="450" y2="354" stroke="#EF4444" stroke-width="2.5" />
            <polygon points="450,270 460,288 480,285 465,300 475,320 450,308 425,320 435,300 420,285 440,288" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
          </g>
        </svg>

        <!-- LAYER 2: VEHICLE SPRITES & DYNAMIC METADATA BADGES -->
        
        <!-- VEHICLE A (Turning Sedan - Starts NE, turns NW) -->
        <div id="veh-a-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 38.0%; top: 69.7%; transform: translate(-50%, -50%);">
          <!-- Dual Heading Sprites (NE vs NW) -->
          <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
            <!-- Sprite 1: Facing NE -->
            <img id="veh-a-sprite-ne" src="{car_red_ne_b64}" alt="Vehicle A NE" class="absolute inset-0 w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" style="opacity: 1;" />
            <!-- Sprite 2: Facing NW -->
            <img id="veh-a-sprite-nw" src="{car_red_nw_b64}" alt="Vehicle A NW" class="absolute inset-0 w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" style="opacity: 0;" />
            
            <!-- Glowing Brake Taillights -->
            <div id="veh-a-brake-left" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-100" style="bottom: 18%; left: 16%;"></div>
            <div id="veh-a-brake-right" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-100" style="bottom: 27%; left: 30%;"></div>
          </div>

          <!-- Non-overlapping Identification Badge below vehicle -->
          <div id="tag-veh-a" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider">
            VEHICLE A (YIELDING ON FLASHING ARROW)
          </div>
        </div>

        <!-- VEHICLE B (Oncoming Priority Traffic - Blue Sedan Heading SW) -->
        <div id="veh-b-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 64.5%; top: 24.0%; transform: translate(-50%, -50%);">
          <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
            <img src="{car_blue_sw_b64}" alt="Vehicle B Oncoming" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          </div>

          <!-- Non-overlapping Identification Badge above vehicle -->
          <div id="tag-veh-b" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/50 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider">
            VEHICLE B (ONCOMING THROUGH FLOW)
          </div>
        </div>
          <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
            <img src="{car_blue_sw_b64}" alt="Vehicle B Oncoming" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          </div>

          <!-- Non-overlapping Identification Badge above vehicle -->
          <div id="tag-veh-b" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/50 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider">
            VEHICLE B (ONCOMING THROUGH FLOW)
          </div>
        </div>

        <!-- SIGNAL TELEMETRY INSET PILL (Top-Right corner of stage, zero overlap) -->
        <div id="hud-signal-pill" class="absolute z-25 px-3 py-1.5 rounded-xl bg-[#1F1905]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 10px; right: 10px;">
          <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
          <span id="pill-signal-text">FLASHING YELLOW ARROW: PERMISSIVE TURN // YIELD ONCOMING</span>
        </div>

        <!-- HAZARD DEMO VIOLATION BANNER -->
        <div id="hazard-banner" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-30 px-5 py-2 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-1 pointer-events-none transition-opacity duration-300" style="opacity: 0.0;">
          <div class="text-xs font-black tracking-widest text-red-400 flex items-center justify-center space-x-1.5">
            <span>✕ CRITICAL HAZARD: FAILURE TO YIELD ON FLASHING YELLOW ARROW ✕</span>
          </div>
          <div class="text-[11px] font-semibold text-gray-200">
            TTC § 544.007 Mandate: Flashing Yellow Arrow is PERMISSIVE ONLY! You must yield right-of-way to oncoming traffic!
          </div>
        </div>

        <!-- LAYER 3: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
        <div id="telemetry-hud-card" class="absolute top-2.5 left-2.5 z-30 max-w-[340px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-3 space-y-2 shadow-xl pointer-events-none">
          <div class="flex items-center justify-between border-b border-[#222B38] pb-1.5">
            <span class="text-[10px] font-bold text-gray-400 mono uppercase tracking-wider">Telemetry &amp; Signal Phasing</span>
            <span id="signal-state-badge" class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono">
              SIGNAL: FLASHING YELLOW
            </span>
          </div>

          <div class="space-y-1 text-xs mono">
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Vehicle A (Turning):</span>
              <span id="telem-veh-a" class="text-amber-400 font-bold">0 MPH (HOLDING AT YIELD BAR)</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Vehicle B (Oncoming):</span>
              <span id="telem-veh-b" class="text-blue-400 font-bold">35 MPH (THROUGH PRIORITY)</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Turn Authorization:</span>
              <span id="telem-turn-auth" class="text-amber-300 font-bold">PERMISSIVE (MUST YIELD)</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Statutory Mandate:</span>
              <span id="telem-statute" class="text-amber-300 font-bold">TTC § 544.007 PERMISSIVE RULE</span>
            </div>
          </div>

          <div class="pt-1.5 border-t border-[#1F2633] text-[11px] text-gray-300 leading-relaxed font-sans" id="hud-narrative">
            Facing a Flashing Yellow Arrow, Vehicle A may turn left only after yielding right-of-way to oncoming through traffic. Vehicle A holds position until Vehicle B clears.
          </div>
        </div>

        <!-- ON-STAGE STATUTORY BADGE (Bottom-Right) -->
        <div class="absolute bottom-2.5 right-2.5 z-30 flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-[#0F131A]/90 border border-[#2B3545] text-[10px] mono text-amber-400 font-semibold shadow-lg pointer-events-none">
          <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
          <span id="compliance-text">TTC § 544.007 PERMISSIVE TURN COMPLIANCE VERIFIED</span>
        </div>

      </div>
    </div>
  </main>

  <!-- BOTTOM SCRUBBER & TIMELINE CONTROLLER BAR -->
  <footer class="bg-[#12161F] border-t border-[#212734] px-6 py-2 z-30 shrink-0">
    <div class="flex items-center space-x-4 mb-1.5">
      <!-- Play/Pause Button -->
      <button id="btn-play-pause" class="w-8 h-8 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold flex items-center justify-center transition shadow-lg shrink-0">
        <span id="play-icon">▶</span>
      </button>

      <!-- Reset Button -->
      <button id="btn-reset" class="w-8 h-8 rounded-lg bg-[#212732] hover:bg-[#2B3342] border border-[#2F3746] text-gray-300 hover:text-white flex items-center justify-center transition shrink-0" title="Reset Timeline">
        <span>↺</span>
      </button>

      <!-- Timeline Scrubber Track -->
      <div class="flex-1 flex items-center space-x-3">
        <span id="time-display" class="text-xs font-bold text-emerald-400 mono w-12 text-right">0.00s</span>
        <input type="range" id="timeline-scrubber" min="0" max="8.0" step="0.01" value="0" class="timeline-slider flex-1 cursor-pointer">
        <span class="text-xs font-medium text-gray-400 mono">8.00s</span>
      </div>

      <!-- Playback Speed Multipliers -->
      <div class="flex items-center rounded-lg bg-[#19202B] p-0.5 border border-[#2B3545] text-xs mono shrink-0">
        <button class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white" data-speed="0.5">0.5x</button>
        <button class="speed-btn px-2 py-0.5 rounded bg-emerald-500 text-black font-bold" data-speed="1.0">1.0x</button>
        <button class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white" data-speed="1.5">1.5x</button>
      </div>
    </div>

    <!-- Center: Key Event Chronology & Status -->
    <div class="flex items-center justify-between text-xs text-gray-400 mono pt-1 border-t border-[#1C2330]">
      <div class="flex items-center space-x-4 text-[10px]">
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-amber-400"></span><span>0.5s Flashing Yellow Arrow</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-blue-400"></span><span>1.5s–3.8s Oncoming Flow Priority</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-cyan-400"></span><span>4.5s Safe Turn Gap Cleared</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400"></span><span>5.0s–7.0s Permissive Left Turn</span></span>
      </div>
      <div class="text-[10px] text-gray-400">
        TDLR ADE-1317: Traffic Control Phasing Protocol (TTC § 544.007)
      </div>
    </div>
  </footer>

  <!-- ================= DETERMINISTIC SIMULATION SCRIPT ================= -->
  <script>
    // State Management
    let isPlaying = false;
    let currentTime = 0.0;
    const maxTime = 8.0;
    const holdTimeAtEnd = 1.2;
    let endHoldAccumulator = 0.0;
    let playbackSpeed = 1.0;
    let lastTimestamp = null;
    let animFrameId = null;

    // Modes: 'fya' (permissive turn), 'green' (protected turn), 'hazard' (FYA blind turn crash)
    let simulationMode = 'fya';

    // DOM References
    const scrubber = document.getElementById('timeline-scrubber');
    const timeDisplay = document.getElementById('time-display');
    const btnPlayPause = document.getElementById('btn-play-pause');
    const playIcon = document.getElementById('play-icon');
    const btnReset = document.getElementById('btn-reset');
    const chkAutoLoop = document.getElementById('chk-autoloop');
    const speedBtns = document.querySelectorAll('.speed-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const stepIndicator = document.getElementById('step-indicator');
    const btnPrevStep = document.getElementById('btn-prev-step');
    const btnNextStep = document.getElementById('btn-next-step');

    // Scenario Toggle Buttons
    const btnFYA = document.getElementById('scenario-btn-fya');
    const btnGreen = document.getElementById('scenario-btn-green');
    const btnHazard = document.getElementById('scenario-btn-hazard');

    // Sprites & Tags
    const vehA = document.getElementById('veh-a-container');
    const vehB = document.getElementById('veh-b-container');
    const spriteANE = document.getElementById('veh-a-sprite-ne');
    const spriteANW = document.getElementById('veh-a-sprite-nw');
    const tagVehA = document.getElementById('tag-veh-a');
    const tagVehB = document.getElementById('tag-veh-b');
    const brakeA1 = document.getElementById('veh-a-brake-left');
    const brakeA2 = document.getElementById('veh-a-brake-right');

    // SVG elements
    const swLensRed = document.getElementById('sw-lens-red');
    const swLensYellowArrow = document.getElementById('sw-lens-yellow-arrow');
    const swLensFYAGroup = document.getElementById('sw-lens-fya-group');
    const swLensGreenArrowGroup = document.getElementById('sw-lens-green-arrow-group');

    const neLensRed = document.getElementById('ne-lens-red');
    const neLensGreen = document.getElementById('ne-lens-green');

    const leftTurnGuide = document.getElementById('left-turn-guide');
    const conflictYieldZone = document.getElementById('conflict-yield-zone');
    const hazardCollisionZone = document.getElementById('hazard-collision-zone');
    const hazardBanner = document.getElementById('hazard-banner');
    const hudSignalPill = document.getElementById('hud-signal-pill');
    const pillSignalText = document.getElementById('pill-signal-text');

    // Telemetry HUD
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemVehA = document.getElementById('telem-veh-a');
    const telemVehB = document.getElementById('telem-veh-b');
    const telemTurnAuth = document.getElementById('telem-turn-auth');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceText = document.getElementById('compliance-text');

    // Canonical Stepper timestamps
    const stepTimes = [0.5, 2.5, 4.5, 6.8];
    let currentStepIdx = 0;

    // Helper: Quadratic easing
    function easeInOutQuad(t) {{
      return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }}

    // =========================================================================
    // UPDATE SIMULATION STATE DETERMINISTICALLY FOR TIME t
    // =========================================================================
    function updateSimulation(t) {{
      scrubber.value = t;
      timeDisplay.textContent = t.toFixed(2) + 's';

      // Update Active Stepper Button
      let activeStep = 0;
      for (let i = 0; i < stepTimes.length; i++) {{
        if (t >= stepTimes[i] - 0.2) activeStep = i;
      }}
      currentStepIdx = activeStep;
      stepBtns.forEach((btn, idx) => {{
        if (idx === activeStep) btn.classList.add('active');
        else btn.classList.remove('active');
      }});
      stepIndicator.textContent = `Step ${{activeStep + 1}} of 4`;

      if (simulationMode === 'fya') {{
        // =====================================================================
        // MODE 1: FLASHING YELLOW ARROW (PERMISSIVE TURN // YIELD TO ONCOMING)
        // =====================================================================
        // Signals
        swLensRed.setAttribute('opacity', '0.2');
        swLensYellowArrow.setAttribute('opacity', '0.2');
        swLensFYAGroup.style.display = 'block';
        swLensGreenArrowGroup.setAttribute('opacity', '0.15');
        neLensRed.setAttribute('opacity', '0.15');
        neLensGreen.setAttribute('opacity', '1.0');

        hudSignalPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#1F1905]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillSignalText.textContent = 'FLASHING YELLOW ARROW: PERMISSIVE TURN // YIELD ONCOMING';
        signalStateBadge.innerHTML = 'SIGNAL: FLASHING YELLOW';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';

        leftTurnGuide.setAttribute('opacity', '0.75');
        conflictYieldZone.setAttribute('opacity', '0.8');
        hazardCollisionZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        // Vehicle B (Oncoming Priority Traffic: NE to SW along Lane 2)
        // Enters at t = 0.6s (64.5%, 24.0%), apex crossing (38.0%, 50.0%) at t = 2.4s, exits (15.6%, 72.0%) at t = 4.0s
        // Lane 2 Equation: bY = 24.0 + 0.982 * (64.5 - bX)
        let bX = 64.5, bY = 24.0, bOpacity = 0.0, bSpeed = 0;
        if (t >= 0.6 && t <= 4.0) {{
          bSpeed = 35;
          const p = (t - 0.6) / (4.0 - 0.6);
          bX = 64.5 - p * (64.5 - 15.6);
          bY = 24.0 + 0.982 * (64.5 - bX);
          if (t < 0.9) bOpacity = (t - 0.6) / 0.3;
          else if (t > 3.7) bOpacity = (4.0 - t) / 0.3;
          else bOpacity = 1.0;
        }} else if (t > 4.0) {{
          bOpacity = 0.0;
          bX = 15.6; bY = 72.0; bSpeed = 0;
        }}
        vehB.style.left = `${{bX}}%`;
        vehB.style.top = `${{bY}}%`;
        vehB.style.opacity = bOpacity;
        tagVehB.textContent = 'VEHICLE B (ONCOMING THROUGH FLOW)';
        tagVehB.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/50 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        tagVehB.style.opacity = (bOpacity > 0.1) ? '1.0' : '0.0';

        // Vehicle A (Turning Vehicle):
        // Approaches and holds at stop/yield line (38.0%, 69.7%) in Lane 1 while Vehicle B passes
        // Resumes turn at t = 4.6s, reaches apex (44.0%, 54.0%) at t = 5.8s (switches to NW), exits at (26.0%, 42.0%) at t = 7.4s
        let aX = 38.0, aY = 69.7, aSpeed = 0, brakeGlow = 1.0;
        let isNW = false;

        if (t <= 4.6) {{
          // Holding behind yield/stop bar while Vehicle B passes and confirming gap
          aX = 38.0; aY = 69.7; aSpeed = 0; brakeGlow = 1.0;
          isNW = false;
          tagVehA.textContent = (t < 4.0) ? 'VEHICLE A (YIELDING ON FLASHING ARROW)' : 'VEHICLE A (GAP CONFIRMED - PREPARING TURN)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        }} else if (t <= 5.8) {{
          // Accelerating into turn pocket towards apex
          const p = easeInOutQuad((t - 4.6) / (5.8 - 4.6));
          aX = 38.0 + p * (44.0 - 38.0);
          aY = 69.7 - p * (69.7 - 54.0);
          aSpeed = Math.round(p * 14);
          brakeGlow = 0.0;
          isNW = (p > 0.65);
          tagVehA.textContent = 'VEHICLE A (EXECUTING PERMISSIVE TURN)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }} else {{
          // Completing left turn into NW roadway (ending at 26%, 42% comfortably below HUD card)
          const p = easeInOutQuad((t - 5.8) / (7.4 - 5.8));
          aX = 44.0 - p * (44.0 - 26.0);
          aY = 54.0 - p * (54.0 - 42.0);
          aSpeed = Math.round(14 + p * 6);
          brakeGlow = 0.0;
          isNW = true;
          tagVehA.textContent = 'VEHICLE A (PERMISSIVE TURN COMPLETE)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }}

        tagVehA.style.opacity = '1.0';
        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;
        brakeA1.style.opacity = brakeGlow;
        brakeA2.style.opacity = brakeGlow;

        spriteANE.style.opacity = isNW ? '0' : '1';
        spriteANW.style.opacity = isNW ? '1' : '0';

        // Telemetry Narrative & Fields
        telemVehA.innerHTML = `${{aSpeed}} MPH (${{aSpeed === 0 ? 'HOLDING AT YIELD BAR' : 'TURNING PERMISSIVE'}})`;
        telemVehA.className = aSpeed === 0 ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold';

        if (bOpacity > 0.1) {{
          telemVehB.innerHTML = `${{bSpeed}} MPH (ONCOMING PRIORITY FLOW)`;
          telemVehB.className = 'text-blue-400 font-bold';
        }} else {{
          telemVehB.innerHTML = 'CLEARED SW ROADWAY';
          telemVehB.className = 'text-gray-500 font-bold';
        }}

        telemTurnAuth.innerHTML = 'PERMISSIVE (YIELD ONCOMING)';
        telemTurnAuth.className = 'text-amber-300 font-bold';
        telemStatute.innerHTML = 'TTC § 544.007(c) PERMISSIVE YIELD';
        telemStatute.className = 'text-amber-300 font-bold';
        complianceText.textContent = 'TTC § 544.007 PERMISSIVE TURN COMPLIANCE VERIFIED';

        if (t < 2.0) {{
          hudNarrative.textContent = 'Facing Flashing Yellow Arrow, Vehicle A must yield to oncoming traffic. Driver scans approaching traffic on NE approach.';
        }} else if (t < 4.4) {{
          hudNarrative.textContent = 'Oncoming Vehicle B traverses through intersection with statutory right-of-way in Lane 2. Vehicle A holds safely behind stop bar.';
        }} else if (t < 6.0) {{
          hudNarrative.textContent = 'Oncoming traffic clears. With an adequate gap verified under TTC § 544.007, Vehicle A executes permissive left turn.';
        }} else {{
          hudNarrative.textContent = 'Vehicle A lawfully completes permissive left turn into NW roadway without conflict. Right-of-way successfully honored.';
        }}

      }} else if (simulationMode === 'green') {{
        // =====================================================================
        // MODE 2: GREEN ARROW (PROTECTED TURN // ONCOMING HELD BY RED)
        // =====================================================================
        // Signals
        swLensRed.setAttribute('opacity', '0.2');
        swLensYellowArrow.setAttribute('opacity', '0.2');
        swLensFYAGroup.style.display = 'none';
        swLensGreenArrowGroup.setAttribute('opacity', '1.0');
        neLensRed.setAttribute('opacity', '1.0');
        neLensGreen.setAttribute('opacity', '0.2');

        hudSignalPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#051F14]/95 border border-emerald-400 text-emerald-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillSignalText.textContent = 'STEADY GREEN ARROW: PROTECTED TURN // ONCOMING STOPPED';
        signalStateBadge.innerHTML = 'SIGNAL: PROTECTED GREEN ARROW';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';

        leftTurnGuide.setAttribute('opacity', '0.9');
        conflictYieldZone.setAttribute('opacity', '0.0');
        hazardCollisionZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        // Vehicle B is HELD at NE stop line in Lane 2 by steady red signal
        vehB.style.left = '54.0%';
        vehB.style.top = '34.3%';
        vehB.style.opacity = '1.0';
        tagVehB.textContent = 'VEHICLE B (STOPPED AT RED LIGHT)';
        tagVehB.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';
        tagVehB.style.opacity = '1.0';

        // Vehicle A turns smoothly without stopping under protected right-of-way
        let aX = 38.0, aY = 69.7, aSpeed = 0;
        let isNW = false;

        if (t <= 1.0) {{
          aX = 38.0; aY = 69.7; aSpeed = 0;
          isNW = false;
        }} else if (t <= 4.0) {{
          const p = easeInOutQuad((t - 1.0) / (4.0 - 1.0));
          aX = 38.0 + p * (44.0 - 38.0);
          aY = 69.7 - p * (69.7 - 54.0);
          aSpeed = Math.round(p * 18);
          isNW = (p > 0.65);
        }} else {{
          const p = easeInOutQuad((t - 4.0) / (6.8 - 4.0));
          aX = 44.0 - p * (44.0 - 26.0);
          aY = 54.0 - p * (54.0 - 42.0);
          aSpeed = Math.round(18 + p * 4);
          isNW = true;
        }}

        tagVehA.style.opacity = '1.0';
        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;
        brakeA1.style.opacity = (t <= 1.0) ? '1.0' : '0.0';
        brakeA2.style.opacity = (t <= 1.0) ? '1.0' : '0.0';

        spriteANE.style.opacity = isNW ? '0' : '1';
        spriteANW.style.opacity = isNW ? '1' : '0';

        tagVehA.textContent = 'VEHICLE A (PROTECTED RIGHT-OF-WAY)';
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';

        telemVehA.innerHTML = `${{aSpeed}} MPH (PROTECTED LEFT TURN)`;
        telemVehA.className = 'text-emerald-400 font-bold';
        telemVehB.innerHTML = '0 MPH (HELD BY RED SIGNAL)';
        telemVehB.className = 'text-red-400 font-bold';
        telemTurnAuth.innerHTML = 'PROTECTED (EXCLUSIVE ROW)';
        telemTurnAuth.className = 'text-emerald-300 font-bold';
        telemStatute.innerHTML = 'TTC § 544.007(b) PROTECTED TURN';
        telemStatute.className = 'text-emerald-300 font-bold';
        complianceText.textContent = 'TTC § 544.007 PROTECTED TURN COMPLIANCE VERIFIED';

        hudNarrative.textContent = 'Under a steady Green Arrow (TTC § 544.007b), Vehicle A has protected right-of-way. Oncoming traffic faces steady red and is held stationary.';

      }} else {{
        // =====================================================================
        // MODE 3: HAZARD DEMO (FYA FAILURE TO YIELD // BLIND TURN COLLISION)
        // =====================================================================
        swLensRed.setAttribute('opacity', '0.2');
        swLensYellowArrow.setAttribute('opacity', '0.2');
        swLensFYAGroup.style.display = 'block';
        swLensGreenArrowGroup.setAttribute('opacity', '0.15');
        neLensRed.setAttribute('opacity', '0.15');
        neLensGreen.setAttribute('opacity', '1.0');

        hudSignalPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillSignalText.textContent = '✕ HAZARD: FYA FAILURE TO YIELD ONCOMING FLOW ✕';
        signalStateBadge.innerHTML = 'SIGNAL: FYA VIOLATION';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        // Vehicle B arrives fast from NE down Lane 2
        // Collision occurs in Lane 2 at apex (44.0%, 44.1%) at t = 3.4s
        let bX = 64.5, bY = 24.0, bOpacity = 1.0;
        if (t <= 3.4) {{
          const p = t / 3.4;
          bX = 64.5 - p * (64.5 - 44.0);
          bY = 24.0 + 0.982 * (64.5 - bX);
        }} else {{
          bX = 44.0; bY = 44.1; // Impact stop position in Lane 2
        }}
        vehB.style.left = `${{bX}}%`;
        vehB.style.top = `${{bY}}%`;
        vehB.style.opacity = bOpacity;
        tagVehB.textContent = 'VEHICLE B (ONCOMING THROUGH FLOW)';
        tagVehB.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/50 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        tagVehB.style.opacity = (bOpacity > 0.1) ? '1.0' : '0.0';

        // Vehicle A launches immediately on FYA without yielding!
        // Moves from (38.0%, 69.7%) directly into Lane 2 at (44.0%, 44.1%) at t = 3.4s
        let aX = 38.0, aY = 69.7, aSpeed = 0;
        let isNW = false;

        if (t <= 1.0) {{
          aX = 38.0; aY = 69.7; aSpeed = 0;
        }} else if (t <= 3.4) {{
          const p = easeInOutQuad((t - 1.0) / (3.4 - 1.0));
          aX = 38.0 + p * (44.0 - 38.0);
          aY = 69.7 - p * (69.7 - 44.1);
          aSpeed = Math.round(p * 22);
          isNW = (p > 0.6);
        }} else {{
          aX = 44.0; aY = 44.1; aSpeed = 0; // Impact stop
          isNW = true;
        }}

        tagVehA.style.opacity = '1.0';
        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;
        brakeA1.style.opacity = (t <= 1.0 || t >= 3.4) ? '1.0' : '0.0';
        brakeA2.style.opacity = (t <= 1.0 || t >= 3.4) ? '1.0' : '0.0';

        spriteANE.style.opacity = isNW ? '0' : '1';
        spriteANW.style.opacity = isNW ? '1' : '0';

        if (t >= 3.2 && t <= 5.8) {{
          tagVehA.style.opacity = '0.0'; // Hide vehicle tags during impact so hazard banner is 100% clean
          tagVehB.style.opacity = '0.0';
          hazardCollisionZone.setAttribute('opacity', '1.0');
          hazardBanner.style.opacity = '1.0';
          telemVehA.innerHTML = 'COLLISION WITH ONCOMING TRAFFIC';
          telemVehA.className = 'text-red-400 font-black animate-pulse';
          tagVehA.innerHTML = '✕ CRITICAL FYA FAILURE TO YIELD';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';

          telemVehB.innerHTML = '35 MPH (T-BONE IMPACT)';
          telemVehB.className = 'text-red-400 font-black';

          telemTurnAuth.innerHTML = 'ILLEGAL TURN (UNYIELDED)';
          telemTurnAuth.className = 'text-red-400 font-black';
          telemStatute.innerHTML = 'TTC § 544.007 VIOLATION';
          telemStatute.className = 'text-red-500 font-black';

          hudNarrative.textContent = 'CRITICAL HAZARD: Driver treated Flashing Yellow Arrow as a protected turn, cutting directly across oncoming 35 MPH traffic! Devastating collision.';
          complianceText.textContent = 'CRITICAL VIOLATION: FAILURE TO YIELD BEFORE PERMISSIVE TURN';
        }} else {{
          hazardCollisionZone.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';

          if (t < 3.2) {{
            telemVehA.innerHTML = `${{aSpeed}} MPH (BLIND LEFT TURN)`;
            telemVehA.className = 'text-amber-400 font-bold';
            tagVehA.textContent = 'VEHICLE A (BLIND TURN ON FYA)';
            tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-amber-950/90 border border-amber-500 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
            telemVehB.innerHTML = '35 MPH (APPROACHING FAST)';
            hudNarrative.textContent = 'Vehicle A accelerates into left turn without verifying gap in oncoming flow. Oncoming Vehicle B has legal right-of-way!';
          }}
        }}
      }}
    }}

    // =========================================================================
    // DETERMINISTIC ANIMATION LOOP
    // =========================================================================
    function animationLoop(timestamp) {{
      if (!isPlaying) {{
        lastTimestamp = null;
        return;
      }}

      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      currentTime += dt * playbackSpeed;

      if (currentTime >= maxTime) {{
        if (chkAutoLoop.checked) {{
          endHoldAccumulator += dt;
          if (endHoldAccumulator >= holdTimeAtEnd) {{
            currentTime = 0.0;
            endHoldAccumulator = 0.0;
          }} else {{
            currentTime = maxTime;
          }}
        }} else {{
          currentTime = maxTime;
          pauseSimulation();
        }}
      }} else {{
        endHoldAccumulator = 0.0;
      }}

      updateSimulation(currentTime);
      animFrameId = requestAnimationFrame(animationLoop);
    }}

    function playSimulation() {{
      if (isPlaying) return;
      isPlaying = true;
      playIcon.textContent = '⏸';
      btnPlayPause.classList.replace('bg-emerald-500', 'bg-amber-500');
      btnPlayPause.classList.replace('hover:bg-emerald-400', 'hover:bg-amber-400');
      lastTimestamp = null;
      animFrameId = requestAnimationFrame(animationLoop);
    }}

    function pauseSimulation() {{
      isPlaying = false;
      playIcon.textContent = '▶';
      btnPlayPause.classList.replace('bg-amber-500', 'bg-emerald-500');
      btnPlayPause.classList.replace('hover:bg-amber-400', 'hover:bg-emerald-400');
      if (animFrameId) {{
        cancelAnimationFrame(animFrameId);
        animFrameId = null;
      }}
    }}

    // Event Listeners
    btnPlayPause.addEventListener('click', () => {{
      if (isPlaying) pauseSimulation();
      else playSimulation();
    }});

    btnReset.addEventListener('click', () => {{
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    scrubber.addEventListener('input', (e) => {{
      pauseSimulation();
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    speedBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        speedBtns.forEach(b => {{
          b.className = 'speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white';
        }});
        btn.className = 'speed-btn px-2 py-0.5 rounded bg-emerald-500 text-black font-bold';
        playbackSpeed = parseFloat(btn.dataset.speed);
      }});
    }});

    stepBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        pauseSimulation();
        const targetTime = parseFloat(btn.dataset.time);
        currentTime = targetTime;
        updateSimulation(currentTime);
      }});
    }});

    btnPrevStep.addEventListener('click', () => {{
      if (currentStepIdx > 0) {{
        currentStepIdx--;
        pauseSimulation();
        currentTime = stepTimes[currentStepIdx];
        updateSimulation(currentTime);
      }}
    }});

    btnNextStep.addEventListener('click', () => {{
      if (currentStepIdx < stepTimes.length - 1) {{
        currentStepIdx++;
        pauseSimulation();
        currentTime = stepTimes[currentStepIdx];
        updateSimulation(currentTime);
      }}
    }});

    // Stepper Labels per Scenario Mode
    const stepLabelsByMode = {{
      fya: [
        'Step 1: Signal Identification & Approach',
        'Step 2: Oncoming Traffic Yield Hold',
        'Step 3: Gap Verification & Clearance',
        'Step 4: Lawful Permissive Execution'
      ],
      green: [
        'Step 1: Protected Arrow Display',
        'Step 2: Oncoming Traffic Stopped on Red',
        'Step 3: Continuous Left-Turn Apex',
        'Step 4: Protected Corridor Complete'
      ],
      hazard: [
        'Step 1: FYA Display & Blind Launch',
        'Step 2: Collision Trajectory with Oncoming Flow',
        'Step 3: Severe Angular Impact & Crash',
        'Step 4: Failure to Yield Citation (§ 544.007)'
      ]
    }};

    function updateStepButtonLabels() {{
      const labels = stepLabelsByMode[simulationMode];
      stepBtns.forEach((btn, idx) => {{
        if (labels && labels[idx]) {{
          btn.textContent = labels[idx];
        }}
      }});
    }}

    // Mode Toggles
    btnFYA.addEventListener('click', () => {{
      simulationMode = 'fya';
      btnFYA.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-amber-500 text-black shadow';
      btnGreen.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    btnGreen.addEventListener('click', () => {{
      simulationMode = 'green';
      btnFYA.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnGreen.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-emerald-500 text-black shadow';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    btnHazard.addEventListener('click', () => {{
      simulationMode = 'hazard';
      btnFYA.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnGreen.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-red-600 text-white shadow';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    // Initial render
    updateStepButtonLabels();
    updateSimulation(0.0);
  </script>
</body>
</html>
'''

output_path = 'C:/tx_dmv/driving_rule_animations_suite/simulations/L04_T02_flashing_yellow_arrow.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Lesson 8 simulation built successfully!")
