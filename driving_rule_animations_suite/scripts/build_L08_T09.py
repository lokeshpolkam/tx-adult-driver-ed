import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        ext = os.path.splitext(path)[1].lower()
        mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/texas_highway_3lane_corridor.jpg'
car_red_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_yellow_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_yellow_ne.png'
car_blue_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_ne.png'
police_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/police_cruiser_tx_ne_clean.png'

print("Encoding Lesson 33 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_b64 = get_base64_img(car_red_ne_path)
car_yellow_b64 = get_base64_img(car_yellow_ne_path)
car_blue_b64 = get_base64_img(car_blue_ne_path)
police_b64 = get_base64_img(police_ne_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en" class="h-full bg-[#0B0E11] text-[#ECEFF1] antialiased">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Lesson L08-T09: Safe Driving Practices — Steer It, Clear It Law (TTC § 550.022)</title>
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

    @keyframes blinkerPulse {{
      0%, 100% {{ opacity: 1.0; filter: drop-shadow(0 0 8px #F59E0B); }}
      50% {{ opacity: 0.1; filter: none; }}
    }}
    .hazard-blinking {{
      animation: blinkerPulse 0.6s infinite ease-in-out;
    }}

    @keyframes policeLightbar {{
      0%, 48% {{ filter: drop-shadow(0 0 12px #3B82F6); }}
      50%, 98% {{ filter: drop-shadow(0 0 12px #EF4444); }}
    }}
    .police-flashing {{
      animation: policeLightbar 0.4s infinite ease-in-out;
    }}

    @keyframes impactRipple {{
      0% {{ r: 10px; opacity: 1; stroke-width: 4px; }}
      100% {{ r: 85px; opacity: 0; stroke-width: 1px; }}
    }}
    .impact-ripple-effect {{
      animation: impactRipple 0.8s infinite ease-out;
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
          <span>TEXAS DRIVING—RULE ANIMATION SYSTEM</span>
        </h1>
        <p class="text-[11px] text-gray-400">Lesson L08—T09: Safe Driving Practices — Post-Collision "Steer It, Clear It" Freeway Law (Texas Transportation Code § 550.022 &amp; § 550.023)</p>
      </div>
    </div>

    <!-- TRI-SCENARIO MODE TOGGLE -->
    <div class="flex items-center space-x-3">
      <div class="flex items-center rounded-lg bg-[#19202B] p-0.5 border border-[#2B3545]">
        <button id="scenario-btn-legal" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-emerald-500 text-black shadow">
          <span>1: Legal "Steer It Clear It" (TTC § 550.022)</span>
        </button>
        <button id="scenario-btn-blocked" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1">
          <span>2: Unlawful Lane Blockage (Standing in Lane)</span>
        </button>
        <button id="scenario-btn-hazard" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1">
          <span>Hazard: Secondary Freeway Collision</span>
        </button>
      </div>

      <div class="h-4 w-px bg-gray-700"></div>

      <!-- Auto Loop Toggle -->
      <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-gray-300 mono">
        <input type="checkbox" id="chk-autoloop" checked class="rounded bg-[#1C2330] border-gray-600 text-emerald-500 focus:ring-0">
        <span>Auto-Loop</span>
      </label>
    </div>
  </header>

  <!-- SECONDARY ACTION BAR: CANONICAL 4-STEP STEPPER -->
  <nav class="bg-[#161B26] border-b border-[#212734] px-6 py-1.5 flex items-center justify-between z-20 shrink-0">
    <div class="flex items-center space-x-2">
      <div class="grid grid-cols-4 gap-1.5" id="stepper-container">
        <button data-step="1" data-time="0.5" class="step-btn active px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition">
          Step 1: Minor Collision &amp; Rapid Triage
        </button>
        <button data-step="2" data-time="2.5" class="step-btn px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition">
          Step 2: 4-Way Hazards &amp; Shoulder Egress
        </button>
        <button data-step="3" data-time="4.8" class="step-btn px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition">
          Step 3: Complete Highway Mainlane Clearance
        </button>
        <button data-step="4" data-time="6.8" class="step-btn px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition">
          Step 4: Driver Exchange &amp; CR-3 Reporting
        </button>
      </div>
    </div>

    <!-- Step Navigation Buttons -->
    <div class="flex items-center space-x-2">
      <button id="btn-prev-step" class="px-2.5 py-0.5 rounded bg-[#212732] hover:bg-[#2B3342] text-xs font-bold text-gray-300 transition">
        &lsaquo; Prev
      </button>
      <span id="step-indicator" class="text-xs font-mono font-bold text-emerald-400 px-2">Step 1 of 4</span>
      <button id="btn-next-step" class="px-2.5 py-0.5 rounded bg-[#212732] hover:bg-[#2B3342] text-xs font-bold text-gray-300 transition">
        Next &rsaquo;
      </button>
    </div>
  </nav>

  <!-- MAIN SIMULATION STAGE (CANVAS DIORAMA CONTAINER) -->
  <main class="flex-1 relative overflow-hidden flex items-center justify-center p-3 bg-[#080A0F]">
    <div class="relative w-full h-full max-w-[1376px] max-h-[768px] aspect-[1376/768] rounded-xl overflow-hidden shadow-2xl border border-[#1E2633] bg-[#151921] select-none">
      
      <!-- LAYER 0: BASE HIGH-RESOLUTION 2.5D TEXAS FREEWAY CORRIDOR -->
      <img src="{road_b64}" alt="Texas 3-Lane Highway Corridor" class="absolute inset-0 w-full h-full object-cover pointer-events-none" />

      <!-- LAYER 1: SVG DYNAMIC TRAJECTORY & STATUTORY MARKINGS -->
      <svg id="stage-svg-overlay" viewBox="0 0 1376 768" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <filter id="glow-emerald" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="3.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="glow-red" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="4.0" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <!-- EMERGENCY SHOULDER SAFE REFUGE CORRIDOR (GREEN GLOW POLYGON) -->
        <polygon id="shoulder-safe-zone" points="475,765 1255,285 1335,335 565,815" fill="#10B981" fill-opacity="0.12" stroke="#10B981" stroke-width="2" stroke-dasharray="8,6" opacity="0.9" />

        <!-- SHOULDER TEXT MARKER -->
        <g id="shoulder-marker-group" transform="translate(930, 475) rotate(-31.5)" opacity="0.95">
          <rect x="-10" y="-12" width="260" height="22" rx="4" fill="#064E3B" fill-opacity="0.85" stroke="#10B981" stroke-width="1.5" />
          <text x="0" y="3" fill="#6EE7B7" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="800" letter-spacing="1">PAVED EMERGENCY SHOULDER REFUGE</text>
        </g>

        <!-- CLEARANCE TRAJECTORY PATH ARROWS (MODE 1) -->
        <!-- Vehicle A Shoulder Steering Path -->
        <path id="traj-veh-a" d="M 552 411 C 630 380, 710 410, 822 245" fill="none" stroke="#34D399" stroke-width="3" stroke-dasharray="6,4" opacity="0.0" filter="url(#glow-emerald)" />
        <!-- Vehicle B Shoulder Steering Path -->
        <path id="traj-veh-b" d="M 462 466 C 530 435, 600 460, 680 332" fill="none" stroke="#FBBF24" stroke-width="3" stroke-dasharray="6,4" opacity="0.0" />

        <!-- MODE 2 & 3: ACTIVE FREEWAY HAZARD ZONE (LANE 2 OBSTRUCTION) -->
        <g id="hazard-lane-zone" opacity="0.0">
          <ellipse cx="505" cy="440" rx="145" ry="60" fill="#EF4444" fill-opacity="0.22" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="8,6" class="pulse-danger" />
          <!-- Clean hazard marker placed safely away from vehicle tags -->
          <rect x="220" y="270" width="280" height="22" rx="4" fill="#111827" fill-opacity="0.9" stroke="#EF4444" stroke-width="1.2" />
          <text x="235" y="285" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800" letter-spacing="1">CRITICAL HAZARD: BLOCKED TRAVEL LANE</text>
        </g>

        <!-- MODE 3: HIGH SPEED SECONDARY COLLISION SHOCKWAVE -->
        <g id="hazard-impact-group" opacity="0.0">
          <circle id="impact-ring" cx="462" cy="466" r="30" fill="none" stroke="#EF4444" stroke-width="4" class="impact-ripple-effect" />
          <circle cx="462" cy="466" r="16" fill="#FBBF24" fill-opacity="0.85" />
          <polygon points="462,425 474,452 502,448 480,470 492,498 462,482 432,498 444,470 422,448 450,452" fill="#EF4444" stroke="#7F1D1D" stroke-width="2" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES & DYNAMIC METADATA BADGES -->

      <!-- VEHICLE A (Red Lead Sedan) -->
      <div id="veh-a-container" class="absolute z-25 transition-transform pointer-events-none" style="left: 40.1%; top: 53.5%; transform: translate(-50%, -50%);">
        <div class="relative w-28 md:w-30 aspect-[120/68] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Vehicle A" class="w-full h-full object-contain filter drop-shadow-[0_10px_8px_rgba(0,0,0,0.65)]" />
          
          <!-- Hazard Blinker Lights -->
          <div id="veh-a-hazard-fl" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="top: 20%; right: 18%;"></div>
          <div id="veh-a-hazard-rl" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 22%; left: 16%;"></div>
          <div id="veh-a-hazard-fr" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 16%; right: 14%;"></div>
          <div id="veh-a-hazard-rr" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 12%; left: 30%;"></div>

          <!-- Vehicle A Tag Badge -->
          <div id="tag-veh-a" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider">
            VEH A (RED SEDAN)
          </div>
        </div>
      </div>

      <!-- VEHICLE B (Yellow Trailing Sedan) -->
      <div id="veh-b-container" class="absolute z-24 transition-transform pointer-events-none" style="left: 33.6%; top: 60.7%; transform: translate(-50%, -50%);">
        <div class="relative w-28 md:w-30 aspect-[120/68] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Vehicle B" class="w-full h-full object-contain filter drop-shadow-[0_10px_8px_rgba(0,0,0,0.65)]" />
          
          <!-- Hazard Blinker Lights -->
          <div id="veh-b-hazard-fl" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="top: 20%; right: 18%;"></div>
          <div id="veh-b-hazard-rl" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 22%; left: 16%;"></div>
          <div id="veh-b-hazard-fr" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 16%; right: 14%;"></div>
          <div id="veh-b-hazard-rr" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 12%; left: 30%;"></div>

          <!-- Vehicle B Tag Badge -->
          <div id="tag-veh-b" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider">
            VEH B (YELLOW SEDAN)
          </div>
        </div>
      </div>

      <!-- VEHICLE C (Blue Through-Traffic / Secondary Impact Sedan) -->
      <div id="veh-c-container" class="absolute z-22 transition-transform pointer-events-none" style="left: 20.0%; top: 68.0%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-28 md:w-30 aspect-[120/68] flex items-center justify-center">
          <img src="{car_blue_b64}" alt="Vehicle C" class="w-full h-full object-contain filter drop-shadow-[0_10px_8px_rgba(0,0,0,0.65)]" />

          <!-- Vehicle C Tag Badge -->
          <div id="tag-veh-c" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-sky-500/50 text-[10px] font-bold text-sky-300 mono shadow-lg tracking-wider">
            VEH C (THROUGH TRAFFIC: 65 MPH)
          </div>
        </div>
      </div>

      <!-- DPS TROOPER CRUISER (Arrives on Shoulder in Step 4) -->
      <div id="veh-police-container" class="absolute z-23 transition-transform pointer-events-none" style="left: 38.5%; top: 73.5%; width: 130px; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-full aspect-[785/514] flex items-center justify-center">
          <img src="{police_b64}" alt="DPS Highway Patrol" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.7)]" />
          
          <!-- Flashing Police Lightbar -->
          <div id="police-lightbar-glow" class="absolute top-[28%] left-[45%] w-5 h-2 rounded bg-cyan-400 opacity-90 police-flashing"></div>

          <!-- Police Tag Badge -->
          <div id="tag-veh-police" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/60 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider">
            TEXAS DPS TROOPER (SCENE DOCUMENTATION)
          </div>
        </div>
      </div>

      <!-- DYNAMIC STATUS PILL (TOP-LEFT OF STAGE) -->
      <div class="absolute top-4 left-4 z-30 pointer-events-none">
        <div id="stage-status-pill" class="px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-emerald-500/40 text-emerald-400 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span id="stage-status-text">STEP 1: MINOR BUMPER IMPACT — 0 INJURIES CONFIRMED</span>
        </div>
      </div>

      <!-- DYNAMIC STATUTORY BANNER (BOTTOM-RIGHT OF STAGE) -->
      <div class="absolute bottom-4 right-4 z-30 pointer-events-none">
        <div id="statute-callout-pill" class="px-3.5 py-2 rounded-lg bg-[#0E131C]/95 border border-[#2B3545] text-gray-300 font-mono text-xs shadow-2xl backdrop-blur-md max-w-md">
          <div class="flex items-center space-x-1.5 text-emerald-400 font-bold mb-0.5">
            <span class="text-sm">§</span>
            <span id="statute-title">TEXAS TRANSPORTATION CODE § 550.022</span>
          </div>
          <p id="statute-desc" class="text-[11px] text-gray-400 leading-tight">
            Accident Involving Damage to Vehicle ("Steer It Clear It"): If an accident occurs on a freeway main lane and vehicles are drivable with no injuries, drivers MUST move to the nearest shoulder.
          </p>
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM CONTROL DECK & TIMELINE SLIDER -->
  <footer class="bg-[#12161F] border-t border-[#212734] px-6 py-2.5 z-30 shrink-0">
    <div class="max-w-[1376px] mx-auto flex flex-col space-y-2">
      
      <!-- TIMELINE SCRUBBER & TIME READOUT -->
      <div class="flex items-center space-x-4">
        <button id="btn-play-pause" class="w-8 h-8 rounded-full bg-emerald-500 hover:bg-emerald-400 text-black flex items-center justify-center font-bold text-sm shadow transition">
          <span id="play-icon">▶</span>
        </button>

        <button id="btn-reset" class="w-8 h-8 rounded-full bg-[#202735] hover:bg-[#2B3545] text-gray-300 hover:text-white flex items-center justify-center font-bold text-xs transition" title="Reset Timeline">
          ↺
        </button>

        <span id="time-display" class="font-mono text-xs font-bold text-gray-300 w-12 text-center">0.0s</span>

        <input type="range" id="timeline-scrubber" min="0" max="8.0" step="0.05" value="0" class="timeline-slider flex-1">

        <span class="font-mono text-xs text-gray-400 w-12 text-center">8.0s</span>

        <!-- SPEED MULTIPLIER BUTTONS -->
        <div class="flex items-center rounded bg-[#1B222E] p-0.5 border border-[#2B3545] text-xs mono">
          <button data-speed="0.5" class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white">0.5x</button>
          <button data-speed="1.0" class="speed-btn px-2 py-0.5 rounded bg-emerald-500 text-black font-bold">1.0x</button>
          <button data-speed="2.0" class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white">2.0x</button>
        </div>
      </div>

      <!-- INSTRUCTIONAL STATUS BAR & TELEMETRY -->
      <div class="flex items-center justify-between text-xs text-gray-400 border-t border-[#1C2330] pt-2">
        <div class="flex items-center space-x-4">
          <span class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            <span id="telemetry-speed-a">Veh A Speed: 0 mph</span>
          </span>
          <span class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            <span id="telemetry-speed-b">Veh B Speed: 0 mph</span>
          </span>
          <span class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span id="telemetry-clearance">Mainlane Status: Clear Corridor</span>
          </span>
        </div>

        <div class="mono text-[11px] text-gray-400">
          Statutory Compliance: <span id="telemetry-compliance" class="text-emerald-400 font-bold">100% Fully Compliant (TTC § 550.022)</span>
        </div>
      </div>

    </div>
  </footer>

  <!-- CORE 60 FPS JAVASCRIPT ANIMATION & LOGIC ENGINE -->
  <script>
    // Elements
    const btnPlayPause = document.getElementById('btn-play-pause');
    const playIcon = document.getElementById('play-icon');
    const btnReset = document.getElementById('btn-reset');
    const scrubber = document.getElementById('timeline-scrubber');
    const timeDisplay = document.getElementById('time-display');
    const chkAutoLoop = document.getElementById('chk-autoloop');

    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');
    const btnPrevStep = document.getElementById('btn-prev-step');
    const btnNextStep = document.getElementById('btn-next-step');
    const stepIndicator = document.getElementById('step-indicator');

    // Scenarios
    const btnLegal = document.getElementById('scenario-btn-legal');
    const btnBlocked = document.getElementById('scenario-btn-blocked');
    const btnHazard = document.getElementById('scenario-btn-hazard');

    // Vehicles & Tags
    const vehA = document.getElementById('veh-a-container');
    const vehB = document.getElementById('veh-b-container');
    const vehC = document.getElementById('veh-c-container');
    const vehPolice = document.getElementById('veh-police-container');

    const tagVehA = document.getElementById('tag-veh-a');
    const tagVehB = document.getElementById('tag-veh-b');
    const tagVehC = document.getElementById('tag-veh-c');
    const tagVehPolice = document.getElementById('tag-veh-police');

    // SVG Overlays
    const trajVehA = document.getElementById('traj-veh-a');
    const trajVehB = document.getElementById('traj-veh-b');
    const hazardLaneZone = document.getElementById('hazard-lane-zone');
    const hazardImpactGroup = document.getElementById('hazard-impact-group');

    // UI Pills
    const stageStatusPill = document.getElementById('stage-status-pill');
    const stageStatusText = document.getElementById('stage-status-text');
    const statuteTitle = document.getElementById('statute-title');
    const statuteDesc = document.getElementById('statute-desc');

    const telemetrySpeedA = document.getElementById('telemetry-speed-a');
    const telemetrySpeedB = document.getElementById('telemetry-speed-b');
    const telemetryClearance = document.getElementById('telemetry-clearance');
    const telemetryCompliance = document.getElementById('telemetry-compliance');

    // Simulation State
    let isPlaying = false;
    let currentTime = 0.0;
    const maxDuration = 8.0;
    let playbackSpeed = 1.0;
    let simulationMode = 'legal'; // 'legal', 'blocked', 'hazard'
    let lastTimestamp = null;
    let animFrameId = null;

    const stepTimes = [0.5, 2.5, 4.8, 6.8];
    let currentStepIdx = 0;

    // Roadway Coordinate Transformation (1376 x 768 Canvas)
    // Lane 2 Center Line: start at (200, 627), delta: dx = 750, dy = -460
    // Lane offsets from Lane 2:
    // Lane 3 (left fast lane): -80px
    // Lane 2 (middle lane): 0px
    // Lane 1 (right lane): +80px
    // Paved Emergency Shoulder: +135px
    function getHighwayPos(laneOffsetX, progressT) {{
      const xPx = 200 + progressT * 750 + laneOffsetX;
      const yPx = 627 + progressT * (-460);
      return {{
        xPct: (xPx / 1376) * 100,
        yPct: (yPx / 768) * 100,
        xPx: xPx,
        yPx: yPx
      }};
    }}

    // Cubic Smoothstep Interpolator
    function smoothStep(t, minT, maxT) {{
      if (t <= minT) return 0.0;
      if (t >= maxT) return 1.0;
      const p = (t - minT) / (maxT - minT);
      return p * p * (3 - 2 * p);
    }}

    function updateSimulation(t) {{
      // Update scrubber & readout
      scrubber.value = t.toFixed(2);
      timeDisplay.textContent = `${{t.toFixed(1)}}s`;

      // Active Step Detection
      let step = 0;
      if (t < 2.0) step = 0;
      else if (t < 4.0) step = 1;
      else if (t < 6.0) step = 2;
      else step = 3;

      if (step !== currentStepIdx) {{
        currentStepIdx = step;
        stepBtns.forEach((btn, idx) => {{
          if (idx === currentStepIdx) {{
            btn.className = 'step-btn active px-3 py-1 rounded text-xs font-semibold border border-[#3B82F6] bg-[#2563EB] text-white transition';
          }} else {{
            btn.className = 'step-btn px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition';
          }}
        }});
        stepIndicator.textContent = `Step ${{currentStepIdx + 1}} of 4`;
      }}

      // Set Hazard Blinkers Helper
      function setHazards(on) {{
        const elIds = ['veh-a-hazard-fl', 'veh-a-hazard-rl', 'veh-a-hazard-fr', 'veh-a-hazard-rr',
                       'veh-b-hazard-fl', 'veh-b-hazard-rl', 'veh-b-hazard-fr', 'veh-b-hazard-rr'];
        elIds.forEach(id => {{
          const el = document.getElementById(id);
          if (el) {{
            if (on) {{
              el.className = 'absolute w-2 h-2 rounded-full bg-amber-400 hazard-blinking';
              el.style.opacity = '1.0';
            }} else {{
              el.className = 'absolute w-2 h-2 rounded-full bg-amber-400 opacity-0';
              el.style.opacity = '0.0';
            }}
          }}
        }});
      }}

      // SCENARIO MODE 1: LEGAL COMPLIANCE ("STEER IT, CLEAR IT")
      if (simulationMode === 'legal') {{
        hazardLaneZone.style.opacity = '0.0';
        hazardImpactGroup.style.opacity = '0.0';

        // Trajectory visibility
        trajVehA.style.opacity = (t >= 1.5 && t <= 5.0) ? '0.85' : '0.0';
        trajVehB.style.opacity = (t >= 1.8 && t <= 5.2) ? '0.85' : '0.0';

        // Vehicle A Motion:
        // t < 1.4: stopped in Lane 2 at progress 0.48
        // t 1.4 - 4.2: steering from Lane 2 (offset 0) to Shoulder (offset 135), advancing to progress 0.66
        // t >= 4.2: parked safely on shoulder
        let progA = 0.48, offsetA = 0;
        let speedA = 0;
        if (t < 1.4) {{
          progA = 0.48;
          offsetA = 0;
          speedA = 0;
        }} else if (t < 4.2) {{
          const p = smoothStep(t, 1.4, 4.2);
          progA = 0.48 + p * (0.66 - 0.48);
          offsetA = p * 135;
          speedA = Math.round(15 * Math.sin(p * Math.PI));
        }} else {{
          progA = 0.66;
          offsetA = 135;
          speedA = 0;
        }}
        const posA = getHighwayPos(offsetA, progA);
        vehA.style.left = `${{posA.xPct}}%`;
        vehA.style.top = `${{posA.yPct}}%`;

        // Vehicle B Motion:
        // t < 2.0: stopped in Lane 2 at progress 0.35
        // t 2.0 - 4.8: steering from Lane 2 to Shoulder, advancing to progress 0.46
        // t >= 4.8: parked on shoulder behind Vehicle A
        let progB = 0.35, offsetB = 0;
        let speedB = 0;
        if (t < 2.0) {{
          progB = 0.35;
          offsetB = 0;
          speedB = 0;
        }} else if (t < 4.8) {{
          const p = smoothStep(t, 2.0, 4.8);
          progB = 0.35 + p * (0.46 - 0.35);
          offsetB = p * 135;
          speedB = Math.round(15 * Math.sin(p * Math.PI));
        }} else {{
          progB = 0.46;
          offsetB = 135;
          speedB = 0;
        }}
        const posB = getHighwayPos(offsetB, progB);
        vehB.style.left = `${{posB.xPct}}%`;
        vehB.style.top = `${{posB.yPct}}%`;

        // Hazards on when t >= 1.2
        setHazards(t >= 1.2);

        // Through traffic Vehicle C: cruises past in Lane 3 (offset -80) at 65 mph (progression between 0.18 and 0.95)
        vehC.style.opacity = '1.0';
        let progC = 0.18 + ((t * 0.22) % 0.77);
        const posC = getHighwayPos(-80, progC);
        vehC.style.left = `${{posC.xPct}}%`;
        vehC.style.top = `${{posC.yPct}}%`;
        tagVehC.textContent = 'VEH C (THROUGH TRAFFIC: 65 MPH)';
        tagVehC.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-sky-500/50 text-[10px] font-bold text-sky-300 mono shadow-lg tracking-wider';

        // Police Cruiser arrives on shoulder behind Vehicle B when t >= 4.8
        if (t >= 4.8) {{
          vehPolice.style.opacity = '1.0';
          const pCop = smoothStep(t, 4.8, 6.8);
          const progCop = 0.12 + pCop * (0.26 - 0.12);
          const posCop = getHighwayPos(135, progCop);
          vehPolice.style.left = `${{posCop.xPct}}%`;
          vehPolice.style.top = `${{posCop.yPct}}%`;
        }} else {{
          vehPolice.style.opacity = '0.0';
        }}

        // Dynamic Status & Badges
        if (t < 1.6) {{
          stageStatusPill.className = 'px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-amber-500/40 text-amber-300 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm';
          stageStatusText.textContent = 'STEP 1: MINOR BUMPER IMPACT — 0 INJURIES CONFIRMED';
          tagVehA.textContent = 'VEH A: TRIAGE 0 INJURIES';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';
          tagVehB.textContent = 'VEH B: DRIVABLE VEHICLE';
          tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
          telemetryClearance.textContent = 'Mainlane Status: Lane 2 Blocked (Triage Phase)';
          telemetryCompliance.textContent = 'Executing TTC § 550.022 Protocol';
          telemetryCompliance.className = 'text-amber-400 font-bold';
        }} else if (t < 4.5) {{
          stageStatusPill.className = 'px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-blue-500/40 text-blue-300 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm';
          stageStatusText.textContent = 'STEP 2: 4-WAY HAZARDS ON — STEERING SAFELY TO SHOULDER';
          tagVehA.textContent = 'VEH A: CLEARING TO SHOULDER';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
          tagVehB.textContent = 'VEH B: FOLLOWING OUT OF TRAFFIC';
          tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
          telemetryClearance.textContent = 'Mainlane Status: Vacating Travel Lanes';
          telemetryCompliance.textContent = 'In Transit to Safety Shoulder';
          telemetryCompliance.className = 'text-blue-400 font-bold';
        }} else if (t < 6.0) {{
          stageStatusPill.className = 'px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-emerald-500/40 text-emerald-300 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm';
          stageStatusText.textContent = 'STEP 3: MAINLANES 100% CLEAR — FREEWAY FLOW RESTORED';
          tagVehA.textContent = 'VEH A: PARKED SAFELY ON SHOULDER';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
          tagVehB.textContent = 'VEH B: PARKED SAFELY ON SHOULDER';
          tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
          telemetryClearance.textContent = 'Mainlane Status: Corridor 100% Free';
          telemetryCompliance.textContent = 'Fully Compliant (§ 550.022)';
          telemetryCompliance.className = 'text-emerald-400 font-bold';
        }} else {{
          stageStatusPill.className = 'px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-emerald-500/40 text-emerald-300 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm';
          stageStatusText.textContent = 'STEP 4: DRIVERS EXCHANGING CREDENTIALS BEHIND GUARDRAIL (§ 550.023)';
          tagVehA.textContent = 'VEH A: EXCHANGING CREDENTIALS';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
          tagVehB.textContent = 'VEH B: VERIFYING CR-3 THRESHOLD';
          tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
          telemetryClearance.textContent = 'Mainlane Status: Live Lanes Protected';
          telemetryCompliance.textContent = 'Fully Compliant (§ 550.022 & § 550.023)';
          telemetryCompliance.className = 'text-emerald-400 font-bold';
        }}

        telemetrySpeedA.textContent = `Veh A Speed: ${{speedA}} mph`;
        telemetrySpeedB.textContent = `Veh B Speed: ${{speedB}} mph`;

        statuteTitle.textContent = 'TEXAS TRANSPORTATION CODE § 550.022';
        statuteDesc.textContent = 'Accident Involving Damage to Vehicle ("Steer It Clear It"): If an accident occurs on a freeway main lane and vehicles are drivable with no injuries, drivers MUST move to the nearest shoulder.';
      }}

      // SCENARIO MODE 2: UNLAWFUL LANE BLOCKAGE (STANDING IN LIVE FREEWAY LANE)
      else if (simulationMode === 'blocked') {{
        trajVehA.style.opacity = '0.0';
        trajVehB.style.opacity = '0.0';
        vehPolice.style.opacity = '0.0';
        hazardImpactGroup.style.opacity = '0.0';
        hazardLaneZone.style.opacity = '0.9';

        // Both cars remain stopped dead in Lane 2
        const posA = getHighwayPos(0, 0.47);
        vehA.style.left = `${{posA.xPct}}%`;
        vehA.style.top = `${{posA.yPct}}%`;

        const posB = getHighwayPos(0, 0.35);
        vehB.style.left = `${{posB.xPct}}%`;
        vehB.style.top = `${{posB.yPct}}%`;

        setHazards(false);

        // Vehicle C approaches in Lane 2, senses blockage early, smoothly transitions to Lane 3 (offset -80)
        vehC.style.opacity = '1.0';
        let progC = 0.12 + t * 0.18;
        let offsetC = 0;
        if (progC > 0.16) {{
          const pSwerve = smoothStep(progC, 0.16, 0.30);
          offsetC = -pSwerve * 80;
        }}
        const posC = getHighwayPos(offsetC, progC);
        vehC.style.left = `${{posC.xPct}}%`;
        vehC.style.top = `${{posC.yPct}}%`;

        tagVehA.textContent = 'VEH A (UNLAWFULLY STOPPED IN LANE 2)';
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-red-500/70 text-[10px] font-bold text-red-400 mono shadow-lg tracking-wider';

        tagVehB.textContent = 'VEH B (PEDESTRIANS AT RISK IN 65 MPH ZONE)';
        tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-red-500/70 text-[10px] font-bold text-red-400 mono shadow-lg tracking-wider';

        tagVehC.textContent = 'VEH C (EVADING STALLED CARS)';
        tagVehC.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-sky-500/50 text-[10px] font-bold text-sky-300 mono shadow-lg tracking-wider';

        stageStatusPill.className = 'px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-red-500/60 text-red-400 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm';
        stageStatusText.textContent = 'VIOLATION: TTC § 550.022(b) — UNLAWFUL FREEWAY OBSTRUCTION';

        statuteTitle.textContent = 'STATUTORY VIOLATION: TTC § 550.022(b)';
        statuteDesc.textContent = 'Leaving drivable vehicles in active freeway travel lanes is a Class C Misdemeanor ($200-$500 fine) and creates severe lethal risk of secondary multi-vehicle pileups.';

        telemetrySpeedA.textContent = 'Veh A Speed: 0 mph (Stalled)';
        telemetrySpeedB.textContent = 'Veh B Speed: 0 mph (Stalled)';
        telemetryClearance.textContent = 'Mainlane Status: Active Freeway Lane Blocked';
        telemetryCompliance.textContent = 'UNLAWFUL: Class C Violation (§ 550.022)';
        telemetryCompliance.className = 'text-red-400 font-bold';
      }}

      // SCENARIO MODE 3: HAZARD DEMO (SECONDARY HIGH-SPEED REAR-END IMPACT)
      else if (simulationMode === 'hazard') {{
        trajVehA.style.opacity = '0.0';
        trajVehB.style.opacity = '0.0';
        vehPolice.style.opacity = '0.0';
        hazardLaneZone.style.opacity = '0.8';

        // Both cars stopped dead in Lane 2
        const posA = getHighwayPos(0, 0.47);
        vehA.style.left = `${{posA.xPct}}%`;
        vehA.style.top = `${{posA.yPct}}%`;

        const posB = getHighwayPos(0, 0.35);
        vehB.style.left = `${{posB.xPct}}%`;
        vehB.style.top = `${{posB.yPct}}%`;

        setHazards(false);

        // Vehicle C speeds down Lane 2 at 70 mph, impacting Vehicle B at t = 3.2s
        vehC.style.opacity = '1.0';
        let progC = 0.05 + t * 0.095;
        if (progC > 0.34) progC = 0.34; // collision point
        const posC = getHighwayPos(0, progC);
        vehC.style.left = `${{posC.xPct}}%`;
        vehC.style.top = `${{posC.yPct}}%`;

        if (t >= 3.0) {{
          hazardImpactGroup.style.opacity = '1.0';
          stageStatusPill.className = 'px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-red-600 text-red-400 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm';
          stageStatusText.textContent = 'CATASTROPHIC HAZARD: HIGH-SPEED SECONDARY COLLISION IN LIVE LANE!';
          tagVehC.textContent = 'VEH C (SECONDARY IMPACT AT 65 MPH)';
          tagVehC.className = 'absolute left-1/2 -translate-x-1/2 -top-8 whitespace-nowrap px-2 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-200 mono shadow-lg tracking-wider';
          tagVehB.textContent = 'VEH B (CRUSH ZONE)';
          tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-2 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-red-500/70 text-[10px] font-bold text-red-400 mono shadow-lg tracking-wider';
        }} else {{
          hazardImpactGroup.style.opacity = '0.0';
          stageStatusPill.className = 'px-3 py-1.5 rounded-lg bg-[#0E131C]/90 border border-amber-500 text-amber-300 font-mono text-xs font-bold tracking-wide shadow-xl flex items-center space-x-2 backdrop-blur-sm';
          stageStatusText.textContent = 'IMMINENT DANGER: 70 MPH TRAFFIC APPROACHING STRANDED VEHICLES';
          tagVehC.textContent = 'VEH C (APPROACHING IN LANE 2)';
          tagVehC.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-sky-500/50 text-[10px] font-bold text-sky-300 mono shadow-lg tracking-wider';
          tagVehB.textContent = 'VEH B (STRANDED IN TRAVEL LANE)';
          tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        }}

        tagVehA.textContent = 'VEH A (STALLED IN LIVE LANE)';
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-red-500/70 text-[10px] font-bold text-red-400 mono shadow-lg tracking-wider';

        statuteTitle.textContent = 'SECONDARY FREEWAY FATALITIES';
        statuteDesc.textContent = 'Secondary collisions account for nearly 20% of all Texas highway fatalities. Clearing drivable cars to the shoulder immediately saves lives.';

        telemetrySpeedA.textContent = 'Veh A Speed: 0 mph';
        telemetrySpeedB.textContent = 'Veh B Speed: 0 mph';
        telemetryClearance.textContent = 'Mainlane Status: CATASTROPHIC COLLISION SCENE';
        telemetryCompliance.textContent = 'Secondary Crash Triggered';
        telemetryCompliance.className = 'text-red-500 font-bold';
      }}
    }}

    // Animation Loop
    function animationLoop(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      currentTime += dt * playbackSpeed;
      if (currentTime > maxDuration) {{
        if (chkAutoLoop.checked) {{
          currentTime = 0.0;
        }} else {{
          currentTime = maxDuration;
          pauseSimulation();
        }}
      }}

      updateSimulation(currentTime);

      if (isPlaying) {{
        animFrameId = requestAnimationFrame(animationLoop);
      }}
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

    // Stepper Labels per Mode
    const stepLabelsByMode = {{
      legal: [
        'Step 1: Minor Collision & Rapid Triage',
        'Step 2: 4-Way Hazards & Shoulder Egress',
        'Step 3: Complete Highway Mainlane Clearance',
        'Step 4: Driver Exchange & CR-3 Protocol'
      ],
      blocked: [
        'Step 1: Low-Speed Freeway Bumper Impact',
        'Step 2: Unlawful Refusal to Move Vehicle',
        'Step 3: Active Travel Lane Obstruction',
        'Step 4: Statutory Citation (§ 550.022)'
      ],
      hazard: [
        'Step 1: Vehicles Stranded in Lane 2',
        'Step 2: High-Speed Traffic Approaching',
        'Step 3: Imminent Rear-End Conflict',
        'Step 4: Secondary Catastrophic Collision'
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
    btnLegal.addEventListener('click', () => {{
      simulationMode = 'legal';
      btnLegal.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-emerald-500 text-black shadow';
      btnBlocked.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    btnBlocked.addEventListener('click', () => {{
      simulationMode = 'blocked';
      btnLegal.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnBlocked.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-amber-500 text-black shadow';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    btnHazard.addEventListener('click', () => {{
      simulationMode = 'hazard';
      btnLegal.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnBlocked.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-red-600 text-white shadow';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    // Spacebar Play/Pause
    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space' && e.target === document.body) {{
        e.preventDefault();
        if (isPlaying) pauseSimulation();
        else playSimulation();
      }}
    }});

    // Initial render
    updateStepButtonLabels();
    updateSimulation(0.0);
  </script>
</body>
</html>
'''

output_path = 'C:/tx_dmv/driving_rule_animations_suite/simulations/L08_T09_steer_it_clear_it.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Lesson 33 simulation built successfully at:", output_path)
