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

    print("Encoding Lesson 23 assets to base64...")
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
  <title>Lesson 23: Reduce Risk — Traffic Flow & Space Cushions (TTC § 545.062 & § 545.060)</title>
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
    @keyframes pulseCushion {{
      0%, 100% {{ transform: scale(1); opacity: 0.25; }}
      50% {{ transform: scale(1.05); opacity: 0.50; filter: drop-shadow(0 0 12px #10B981); }}
    }}
    .cushion-pulse {{
      animation: pulseCushion 2.5s ease-in-out infinite;
      transform-origin: center;
    }}
    @keyframes dangerPulse {{
      0%, 100% {{ transform: scale(1); opacity: 0.75; }}
      50% {{ transform: scale(1.15); opacity: 1.0; filter: drop-shadow(0 0 16px #EF4444); }}
    }}
    .danger-pulse {{
      animation: dangerPulse 1.2s ease-in-out infinite;
      transform-origin: center;
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
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 23</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L05-T16: Traffic Flow Harmonization & Space Management
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Texas Driver Handbook Ch. 5 • TTC § 545.062 (Following Distance / Assured Clear Distance) & § 545.060 (Lane Integrity)
        </p>
      </div>

      <!-- SCENARIO TOGGLES -->
      <div class="flex flex-wrap items-center gap-2 bg-[#0C1017] p-1.5 rounded-xl border border-[#1E293B] self-start md:self-auto">
        <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
          1: 360° Space Cushion (Staggered Flow)
        </button>
        <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
          2: Escaping "Wolf Pack" Box
        </button>
        <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
          Hazard: Entrapment Box Pileup
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
      <button class="step-card bg-[#121824] border border-emerald-500/40 rounded-xl p-2.5 text-left transition hover:border-emerald-400 group relative overflow-hidden" data-step="1">
        <div class="text-[10px] font-bold text-emerald-400 mono flex items-center justify-between">
          <span>STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        </div>
        <div id="step-title-1" class="text-xs font-bold text-white mt-1 group-hover:text-emerald-200">Forward Cushion (3-4s)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="2">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-2" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Lateral Stagger (Left Open)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="3">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-3" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">Lateral Stagger (Right Open)</div>
      </button>

      <button class="step-card bg-[#121824] border border-[#1E293B] rounded-xl p-2.5 text-left transition hover:border-gray-500 group relative overflow-hidden" data-step="4">
        <div class="text-[10px] font-bold text-gray-400 mono flex items-center justify-between">
          <span>STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent"></span>
        </div>
        <div id="step-title-4" class="text-xs font-bold text-gray-300 mt-1 group-hover:text-white">360° Escape Envelope Maintained</div>
      </button>
    </section>

    <!-- MAIN SIMULATION STAGE VIEWPORT (16:9 / elevated 35 deg diorama) -->
    <div class="relative w-full aspect-[16/9] bg-[#ECEEEA] rounded-2xl overflow-hidden border border-[#1E293B] shadow-2xl">

      <!-- LAYER 0: PHOTOREALISTIC 3D HIGHWAY DIORAMA BASE -->
      <img src="{bg_b64}" alt="Texas Highway Corridor Base" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG VECTOR OVERLAYS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <marker id="arrow-emerald" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#10B981" />
          </marker>
          <marker id="arrow-danger" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <path d="M0,0 L0,6 L6,3 z" fill="#EF4444" />
          </marker>

          <!-- Safe 360 Space Cushion Gradient -->
          <radialGradient id="cushion-grad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.30" />
            <stop offset="70%" stop-color="#10B981" stop-opacity="0.15" />
            <stop offset="100%" stop-color="#10B981" stop-opacity="0.0" />
          </radialGradient>

          <!-- Danger Trapped Gradient -->
          <radialGradient id="danger-cushion-grad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#EF4444" stop-opacity="0.45" />
            <stop offset="70%" stop-color="#EF4444" stop-opacity="0.20" />
            <stop offset="100%" stop-color="#EF4444" stop-opacity="0.0" />
          </radialGradient>
        </defs>

        <!-- DYNAMIC 360-DEGREE SPACE CUSHION HALO -->
        <g id="space-cushion-group">
          <!-- Outer buffer boundary ellipse (Rotated along highway axis) -->
          <ellipse id="cushion-ellipse" cx="480" cy="275" rx="130" ry="60" transform="rotate(-26, 480, 275)" fill="url(#cushion-grad)" stroke="#10B981" stroke-width="2" stroke-dasharray="8,6" class="cushion-pulse" />
          
          <!-- Lateral Escape Path Vectors (Pointing to Lane 3 and Lane 1) -->
          <g id="escape-vectors-group">
            <!-- Left Escape Vector (towards Lane 3 / Median) -->
            <path id="esc-left-arrow" d="M 460,255 L 430,225" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrow-emerald)" />
            <g id="esc-left-badge" transform="translate(400, 185)">
              <rect x="-42" y="-10" width="84" height="16" rx="8" fill="#062418" stroke="#10B981" stroke-width="1" />
              <text x="0" y="2" fill="#6EE7B7" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">ESCAPE LANE 3</text>
            </g>

            <!-- Right Escape Vector (towards Lane 1 / Shoulder) -->
            <path id="esc-right-arrow" d="M 500,295 L 530,325" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrow-emerald)" />
            <g id="esc-right-badge" transform="translate(565, 360)">
              <rect x="-42" y="-10" width="84" height="16" rx="8" fill="#062418" stroke="#10B981" stroke-width="1" />
              <text x="0" y="2" fill="#6EE7B7" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">ESCAPE LANE 1</text>
            </g>
          </g>

          <!-- Forward Distance Bracket Line -->
          <g id="forward-gap-group">
            <line id="gap-line" x1="520" y1="235" x2="670" y2="140" stroke="#FBBF24" stroke-width="1.8" stroke-dasharray="5,4" />
            <g id="gap-pill" transform="translate(605, 175)">
              <rect x="-42" y="-10" width="84" height="16" rx="8" fill="#1C1905" stroke="#FBBF24" stroke-width="1" />
              <text x="0" y="2" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">3.5s BUFFER</text>
            </g>
          </g>
        </g>

        <!-- MODE 3: CRITICAL ENTRAPMENT PINCH VECTORS & IMPACT HAZARD -->
        <g id="spin-hazard-group" opacity="0.0">
          <ellipse cx="480" cy="270" rx="65" ry="32" fill="none" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="8,6" class="danger-pulse" />
          <polygon id="hazard-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- BLUE LEAD HIGHWAY VEHICLE (LANE 2 AHEAD AT 65 MPH) -->
      <div id="veh-blue" class="absolute z-20 pointer-events-none transition-transform" style="left: 70.0%; top: 22.4%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_ne_b64}" alt="Lead Vehicle Lane 2" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          LEAD VEHICLE: 65 MPH (LANE 2)
        </div>
      </div>

      <!-- YELLOW ADJACENT TRAFFIC VEHICLE (LANE 1 - STAGGERED OR COMPRESSING) -->
      <div id="veh-yellow" class="absolute z-20 pointer-events-none transition-transform" style="left: 28.0%; top: 78.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Traffic Lane 1" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          ADJACENT FLOW: STAGGERED (LANE 1)
        </div>
      </div>

      <!-- EGO VEHICLE (RED SEDAN - HARMONIZED FLOW & SPACE POSITIONING) -->
      <div id="veh-ego" class="absolute z-22 pointer-events-none" style="left: 48.0%; top: 44.6%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[120/70] flex items-center justify-center transition-transform duration-150" style="transform: rotate(0deg);">
          <img src="{car_red_ne_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.75)]" />
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 35%; left: 8%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: 360° SPACE CUSHION SECURED
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS SPACE RULE: 3-4s FORWARD BUFFER • STAGGER LANES • NEVER BOXED IN</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#081C15]/90 border border-emerald-500/50 text-emerald-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="compliance-text">TTC § 545.062 ASSURED CLEAR DISTANCE COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & SPACE MANAGEMENT HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[270px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">SPACE MANAGEMENT HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">360° SECURED</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Speed:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-speed">65 MPH</span>

          <span class="text-gray-400">Forward Gap:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-forward">3.5 SEC (220 FT)</span>

          <span class="text-gray-400">Lane 3 (Left):</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-left">OPEN ESCAPE PATH</span>

          <span class="text-gray-400">Lane 1 (Right):</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-right">OPEN ESCAPE PATH</span>

          <span class="text-gray-400">Wolf Pack Risk:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-risk">ZERO (STAGGERED)</span>

          <span class="text-gray-400">Traffic Status:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-status">FLOW HARMONIZED</span>
        </div>

        <!-- Dynamic Rule Narrative -->
        <div class="pt-2 border-t border-gray-800 text-[10px] text-gray-300 leading-relaxed" id="hud-narrative">
          Step 1: Driver maintains minimum 3.5s forward cushion behind lead vehicle. Both adjacent lanes open for emergency evasive steering.
        </div>
      </aside>

      <!-- MODE 3 CRITICAL VIOLATION BANNER (Positioned below status pill in clear air space) -->
      <div id="hazard-banner" class="absolute z-35 w-[265px] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300" style="top: 48px; left: 295px;">
        <div class="text-[10px] font-black text-red-300 mono flex items-center justify-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL: ENTRAPMENT PILEUP</span>
          <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
        </div>
        <div class="text-[9px] text-red-200 mt-1 leading-snug">
          <strong>TOTAL LOSS OF ESCAPE PATHS</strong><br>
          Traveling boxed between adjacent vehicles destroys all evasive options. Sudden lead braking forces unavoidable collision (TTC § 545.062).
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
    let currentMode = 1; // 1: 360 Space Cushion, 2: Escaping Wolf Pack, 3: Entrapment Box Hazard
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

    const brakeLights = document.getElementById('brake-lights');
    const spaceCushionGroup = document.getElementById('space-cushion-group');
    const cushionEllipse = document.getElementById('cushion-ellipse');
    const escapeVectorsGroup = document.getElementById('escape-vectors-group');
    const escLeftArrow = document.getElementById('esc-left-arrow');
    const escLeftBadge = document.getElementById('esc-left-badge');
    const escRightArrow = document.getElementById('esc-right-arrow');
    const escRightBadge = document.getElementById('esc-right-badge');
    const forwardGapGroup = document.getElementById('forward-gap-group');
    const gapLine = document.getElementById('gap-line');
    const gapPill = document.getElementById('gap-pill');

    const spinHazardGroup = document.getElementById('spin-hazard-group');
    const hazardStar = document.getElementById('hazard-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const telemSpeed = document.getElementById('telem-speed');
    const telemForward = document.getElementById('telem-forward');
    const telemLeft = document.getElementById('telem-left');
    const telemRight = document.getElementById('telem-right');
    const telemRisk = document.getElementById('telem-risk');
    const telemStatus = document.getElementById('telem-status');
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
        {{ time: 0.8, title: "Forward Cushion (3-4s)" }},
        {{ time: 2.2, title: "Lateral Stagger (Left Open)" }},
        {{ time: 3.6, title: "Lateral Stagger (Right Open)" }},
        {{ time: 5.0, title: "360° Envelope Maintained" }}
      ],
      2: [
        {{ time: 0.8, title: "Wolf Pack Pinch Detected" }},
        {{ time: 2.2, title: "Throttle Lift (Drop Back)" }},
        {{ time: 3.6, title: "Pocket Separation Rebuilt" }},
        {{ time: 5.0, title: "Full Escape Routes Restored" }}
      ],
      3: [
        {{ time: 0.8, title: "Boxed In Adjacent Blind Spots" }},
        {{ time: 2.2, title: "Lead Vehicle Panic Brakes!" }},
        {{ time: 3.6, title: "Zero Lateral Escape Routes" }},
        {{ time: 5.0, title: "Catastrophic Multi-Car Crash" }}
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

      // =========================================================================
      // MODE 1: IDEAL 360° SPACE CUSHION & STAGGERED FLOW (TTC § 545.062)
      // =========================================================================
      if (currentMode === 1) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        brakeLights.style.opacity = '0.0';
        spaceCushionGroup.setAttribute('opacity', '1.0');
        cushionEllipse.setAttribute('fill', 'url(#cushion-grad)');
        cushionEllipse.setAttribute('stroke', '#10B981');
        escapeVectorsGroup.setAttribute('opacity', '1.0');
        forwardGapGroup.setAttribute('opacity', '1.0');

        // Blue Lead Vehicle in Lane 2 cruising smoothly at 65 MPH
        const blueX = 68.0 + (t / duration) * 8.0; // 68% to 76%
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'LEAD FLOW: 65 MPH (LANE 2)';

        // Yellow Adjacent Vehicle in Lane 1 staggered safely behind Ego
        const yellowX = 26.0 + (t / duration) * 8.0; // 26% to 34%
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.textContent = 'ADJACENT FLOW: STAGGERED (LANE 1)';

        // Ego Car: Centered in Lane 2 at 65 MPH with perfect 3.5s cushion
        const egoX = 47.0 + (t / duration) * 8.0; // 47% to 55%
        const egoY = getLane2Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';

        // Update SVG Cushion & Brackets
        const egoSvgX = egoX * 10;
        const egoSvgY = egoY * 6;
        cushionEllipse.setAttribute('cx', egoSvgX);
        cushionEllipse.setAttribute('cy', egoSvgY);
        cushionEllipse.setAttribute('transform', `rotate(-26, ${{egoSvgX}}, ${{egoSvgY}})`);

        // Dynamic Escape Vectors relative to Ego position
        escLeftArrow.setAttribute('d', `M ${{egoSvgX - 15}},${{egoSvgY - 15}} L ${{egoSvgX - 55}},${{egoSvgY - 55}}`);
        escLeftBadge.setAttribute('transform', `translate(${{egoSvgX - 75}}, ${{egoSvgY - 75}})`);

        escRightArrow.setAttribute('d', `M ${{egoSvgX + 15}},${{egoSvgY + 15}} L ${{egoSvgX + 45}},${{egoSvgY + 45}}`);
        escRightBadge.setAttribute('transform', `translate(${{egoSvgX + 70}}, ${{egoSvgY + 60}})`);

        const blueSvgX = blueX * 10;
        const blueSvgY = blueY * 6;
        gapLine.setAttribute('x1', egoSvgX + 35);
        gapLine.setAttribute('y1', egoSvgY - 20);
        gapLine.setAttribute('x2', blueSvgX - 35);
        gapLine.setAttribute('y2', blueSvgY + 20);
        const gapPillX = egoSvgX * 0.35 + blueSvgX * 0.65;
        const gapPillY = egoSvgY * 0.35 + blueSvgY * 0.65;
        gapPill.setAttribute('transform', `translate(${{gapPillX}}, ${{gapPillY}})`);

        telemSpeed.textContent = '65 MPH';
        telemForward.textContent = '3.5 SEC (220 FT)';
        telemLeft.textContent = 'OPEN ESCAPE PATH';
        telemRight.textContent = 'OPEN ESCAPE PATH';
        telemRisk.textContent = 'ZERO (STAGGERED)';
        telemStatus.textContent = 'FLOW HARMONIZED';

        pillStatusText.textContent = 'TEXAS SPACE RULE: 3-4s FORWARD BUFFER • STAGGER LANES • NEVER BOXED IN';

        if (t < 1.6) {{
          tagVehEgo.textContent = 'EGO: 360° SPACE CUSHION SECURED';
          hudNarrative.textContent = 'Step 1: Driver establishes 3.5-second following distance behind lead vehicle. Visual horizon open for early hazard detection.';
          signalStateBadge.textContent = 'FORWARD CUSHION';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else if (t < 3.0) {{
          tagVehEgo.textContent = 'EGO: LEFT ESCAPE VECTOR OPEN (LANE 3)';
          hudNarrative.textContent = 'Step 2: Maintaining lateral stagger. Lane 3 to the left is completely vacant, providing an immediate evasive escape corridor.';
          signalStateBadge.textContent = 'LEFT ESCAPE CLEAR';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else if (t < 4.4) {{
          tagVehEgo.textContent = 'EGO: RIGHT ESCAPE VECTOR OPEN (LANE 1)';
          hudNarrative.textContent = 'Step 3: Trailing traffic in Lane 1 is staggered behind. Lane 1 and shoulder to the right remain open for lateral evasive steering.';
          signalStateBadge.textContent = 'RIGHT ESCAPE CLEAR';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: COMPLETE 360° ESCAPE ENVELOPE MAINTAINED';
          hudNarrative.textContent = 'Step 4: Continuous active space management prevents entrapment. Vehicle surrounded by protective perimeter cushions on all four sides.';
          signalStateBadge.textContent = '360° SECURED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 2: ESCAPING THE "WOLF PACK" CLUSTER (THROTTLE LIFT & POCKET DROP)
      // =========================================================================
      else if (currentMode === 2) {{
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        spinHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        brakeLights.style.opacity = '0.0';
        spaceCushionGroup.setAttribute('opacity', '1.0');

        // Blue Lead Vehicle in Lane 2
        const blueX = 66.0 + (t / duration) * 8.0;
        const blueY = getLane2Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.textContent = 'LEAD VEHICLE: 65 MPH (LANE 2)';

        // Yellow Vehicle: Compresses alongside Ego initially, then pulls ahead as Ego drops back
        let yellowX, yellowY;
        if (t < 2.0) {{
          const progress = t / 2.0;
          yellowX = 38.0 + progress * 8.0; // 38% to 46% (closing in alongside Ego)
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'WOLF PACK: MATCHING SPEED (LANE 1)';
        }} else {{
          const progress = (t - 2.0) / 4.0;
          yellowX = 46.0 + progress * 16.0; // 46% to 62% (pulls ahead as Ego lifts)
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'TRAFFIC FLOWING AHEAD (LANE 1)';
        }}
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;

        // Ego Car: Senses pinch, lifts throttle, drops from 65 -> 58 MPH, re-establishing cushion
        let egoX, egoY, egoSpeed, cushionColor;
        if (t < 2.0) {{
          // Cluster pinch begins
          const progress = t / 2.0;
          egoX = 45.0 + progress * 3.0; // 45% to 48%
          egoY = getLane2Y(egoX);
          egoSpeed = 65;
          cushionColor = '#F59E0B'; // Amber alert
          cushionEllipse.setAttribute('stroke', '#F59E0B');
          escapeVectorsGroup.setAttribute('opacity', '0.5');
        }} else if (t < 4.0) {{
          // Throttle lift: dropping back into open pocket
          const progress = (t - 2.0) / 2.0;
          egoX = 48.0 + progress * 1.5; // 48% to 49.5% (gentle speed bleed)
          egoY = getLane2Y(egoX);
          egoSpeed = Math.round(65 - progress * 7); // 65 -> 58 MPH
          cushionColor = '#10B981';
          cushionEllipse.setAttribute('stroke', '#10B981');
          escapeVectorsGroup.setAttribute('opacity', '1.0');
        }} else {{
          // Re-established 360 space pocket
          const progress = (t - 4.0) / 2.0;
          egoX = 49.5 + progress * 3.5; // 49.5% to 53%
          egoY = getLane2Y(egoX);
          egoSpeed = 65;
          cushionColor = '#10B981';
          cushionEllipse.setAttribute('stroke', '#10B981');
          escapeVectorsGroup.setAttribute('opacity', '1.0');
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        vehEgo.style.transform = 'translate(-50%, -50%)';
        vehEgoSprite.style.transform = 'rotate(0deg)';

        const egoSvgX = egoX * 10;
        const egoSvgY = egoY * 6;
        cushionEllipse.setAttribute('cx', egoSvgX);
        cushionEllipse.setAttribute('cy', egoSvgY);
        cushionEllipse.setAttribute('transform', `rotate(-26, ${{egoSvgX}}, ${{egoSvgY}})`);

        // Dynamic Escape Vectors
        escLeftArrow.setAttribute('d', `M ${{egoSvgX - 15}},${{egoSvgY - 15}} L ${{egoSvgX - 55}},${{egoSvgY - 55}}`);
        escLeftBadge.setAttribute('transform', `translate(${{egoSvgX - 75}}, ${{egoSvgY - 75}})`);

        escRightArrow.setAttribute('d', `M ${{egoSvgX + 15}},${{egoSvgY + 15}} L ${{egoSvgX + 45}},${{egoSvgY + 45}}`);
        escRightBadge.setAttribute('transform', `translate(${{egoSvgX + 70}}, ${{egoSvgY + 60}})`);

        const blueSvgX = blueX * 10;
        const blueSvgY = blueY * 6;
        gapLine.setAttribute('x1', egoSvgX + 35);
        gapLine.setAttribute('y1', egoSvgY - 20);
        gapLine.setAttribute('x2', blueSvgX - 35);
        gapLine.setAttribute('y2', blueSvgY + 20);
        const gapPillX = egoSvgX * 0.35 + blueSvgX * 0.65;
        const gapPillY = egoSvgY * 0.35 + blueSvgY * 0.65;
        gapPill.setAttribute('transform', `translate(${{gapPillX}}, ${{gapPillY}})`);

        telemSpeed.textContent = `${{egoSpeed}} MPH`;
        telemForward.textContent = (t < 2.0) ? '2.0 SEC (COMPRESSED)' : '3.8 SEC (RESTORED)';
        telemLeft.textContent = 'OPEN ESCAPE PATH';
        telemRight.textContent = (t < 2.0) ? 'PINCHED BY YELLOW' : 'OPEN ESCAPE PATH';
        telemRisk.textContent = (t < 2.0) ? 'WOLF PACK PINCH' : 'RESOLVED (POCKET)';
        telemStatus.textContent = (t < 2.0) ? 'CLUSTER FORMING' : 'OPEN POCKET RESTORED';

        pillStatusText.textContent = 'ANTI-WOLF PACK: EASE THROTTLE TO DROP OUT OF HIGH-DENSITY CLUSTERS';

        if (t < 2.0) {{
          tagVehEgo.textContent = 'EGO: WOLF PACK FORMING • LATERAL PINCH DETECTED';
          hudNarrative.textContent = 'Step 1: Traffic clusters tightly side-by-side at 65 MPH. Yellow car matches speed in adjacent blind spot, compressing lateral escape paths.';
          signalStateBadge.textContent = 'CLUSTER PINCH';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 4.0) {{
          tagVehEgo.textContent = 'EGO: THROTTLE LIFT (58 MPH) • DROPPING BACK INTO GAP';
          hudNarrative.textContent = 'Step 2: Smart driver avoids speeding up or jockeying lanes. Eases off accelerator to let cluster pull ahead, dropping smoothly into open space.';
          signalStateBadge.textContent = 'THROTTLE LIFT';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: 360° POCKET RESTORED • FULL ESCAPE MARGIN';
          hudNarrative.textContent = 'Step 3 & 4: Speed stabilized at 65 MPH in clear highway pocket. 360° perimeter cushion and all lateral escape vectors 100% re-established.';
          signalStateBadge.textContent = 'POCKET SECURED';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        }}
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: ENTRAPMENT BOX PILEUP (TTC § 545.062)
      // =========================================================================
      else if (currentMode === 3) {{
        if (t < 2.0) {{
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        }} else {{
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 top-full mt-2 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        }}
        spaceCushionGroup.setAttribute('opacity', '0.0');

        // Blue Lead Vehicle: Cruising, then sudden panic brake for debris!
        let blueX, blueY;
        if (t < 2.0) {{
          const progress = t / 2.0;
          blueX = 70.0 + progress * 4.0; // 70% to 74%
          blueY = getLane2Y(blueX);
          tagVehBlue.textContent = 'LEAD VEHICLE: 65 MPH (LANE 2)';
        }} else {{
          // Emergency threshold stop at x = 74%
          blueX = 74.0;
          blueY = getLane2Y(blueX);
          tagVehBlue.textContent = 'PANIC BRAKING! HIGHWAY DEBRIS';
        }}
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;

        // Yellow Vehicle: Traveling tightly pinned directly alongside Ego in Lane 1
        let yellowX, yellowY;
        if (t < 3.2) {{
          const progress = t / 3.2;
          yellowX = 46.0 + progress * 8.0; // 46% to 54%
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'PINNING FLANK: 65 MPH (LANE 1)';
        }} else {{
          yellowX = 54.0;
          yellowY = getLane1Y(yellowX);
          tagVehYellow.textContent = 'LATERAL SIDESWIPE IMPACT!';
        }}
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;

        // Ego Car: Boxed in with 1.2s gap, no side escape routes, crashes into Lead & Yellow
        let egoX, egoY, yawAngle, egoSpeed;
        if (t < 2.0) {{
          const progress = t / 2.0;
          egoX = 45.0 + progress * 4.0; // 45% to 49%
          egoY = getLane2Y(egoX);
          yawAngle = 0;
          egoSpeed = 65;
          brakeLights.style.opacity = '0.0';
          spinHazardGroup.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
        }} else if (t < 3.2) {{
          const progress = (t - 2.0) / 1.2;
          egoX = 49.0 + progress * 19.0; // 49% to 68% (unavoidable forward slam)
          egoY = getLane2Y(egoX);
          yawAngle = progress * 24.0; // violent swerve impact
          egoSpeed = Math.round(65 * (1 - progress * 0.7)); // 65 -> 20 MPH
          brakeLights.style.opacity = '1.0';
          spinHazardGroup.setAttribute('opacity', '1.0');
          hazardStar.setAttribute('transform', `translate(${{egoX * 10}}, ${{egoY * 6}})`);
          hazardBanner.style.opacity = '1.0';
        }} else {{
          // Crashed behind Blue (x = 68%) and sideswipes Yellow
          egoX = 68.0;
          egoY = getLane2Y(egoX);
          yawAngle = 24.0;
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

        telemSpeed.textContent = (egoSpeed === 0) ? '0 MPH (CRASHED)' : `${{egoSpeed}} MPH`;
        telemForward.textContent = (t < 2.0) ? '1.2 SEC (TAILGATING)' : '0 FT (COLLISION)';
        telemLeft.textContent = 'BLOCKED (MEDIAN BARRIER)';
        telemRight.textContent = 'BLOCKED BY YELLOW CAR';
        telemRisk.textContent = 'FATAL ENTRAPMENT';
        telemStatus.textContent = (t < 2.0) ? 'NO ESCAPE ENVELOPE' : 'MULTI-CAR PILEUP';

        pillStatusText.textContent = 'CRITICAL ENTRAPMENT ERROR: NEVER DRIVE BOXED IN WITH ZERO LATERAL ESCAPE PATHS';

        if (t < 2.0) {{
          tagVehEgo.textContent = 'EGO: TRAPPED IN WOLF PACK • ZERO ESCAPE PATHS';
          hudNarrative.textContent = 'Step 1: Driver drives boxed between median barrier and adjacent vehicle with only 1.2s following gap. Zero margin for error.';
          signalStateBadge.textContent = 'BOXED IN';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else if (t < 3.2) {{
          tagVehEgo.textContent = 'EGO: LEAD BRAKES SLAMMED! NO LATERAL ESCAPE';
          hudNarrative.textContent = 'Step 2: Lead vehicle emergency brakes for highway debris. Trapped driver cannot swerve left or right; collision physics inevitable.';
          signalStateBadge.textContent = 'COLLISION INEVITABLE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500 text-white mono';
        }} else {{
          tagVehEgo.textContent = 'EGO: MULTI-CAR HIGHWAY PILEUP • CRASH REPORTABLE';
          hudNarrative.textContent = 'Step 3 & 4: Violent impact with lead vehicle pushes Ego into adjacent lane, causing secondary sideswipe. Violation of TTC § 545.062.';
          signalStateBadge.textContent = 'CHAIN REACTION';
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
          card.classList.add('border-emerald-500/60', 'bg-emerald-950/20');
        }} else {{
          card.classList.remove('border-emerald-500/60', 'bg-emerald-950/20');
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

    out_file = r"c:\tx_dmv\driving_rule_animations_suite\simulations\L05_T16_flow_harmonization.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 23 simulation built successfully at: {out_file}")

if __name__ == "__main__":
    build_simulation()
