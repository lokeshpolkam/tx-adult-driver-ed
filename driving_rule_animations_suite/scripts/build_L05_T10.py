import os
import base64

# Base paths
road_img_path = 'driving_rule_animations_suite/assets/roads/texas_suburban_2lane_corridor.jpg'
car_red_ne_path = 'driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_blue_sw_path = 'driving_rule_animations_suite/assets/vehicles/car_blue_sw_clean.png'
car_yellow_ne_path = 'driving_rule_animations_suite/assets/vehicles/car_yellow_ne.png'

print("Encoding Lesson 18 assets to base64...")

with open(road_img_path, 'rb') as f:
    road_b64 = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"

with open(car_red_ne_path, 'rb') as f:
    car_red_ne_b64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

with open(car_blue_sw_path, 'rb') as f:
    car_blue_sw_b64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

with open(car_yellow_ne_path, 'rb') as f:
    car_yellow_ne_b64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T10: Vehicle Lights — High Beam Dimming & Sight Distance</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #080B10;
      color: #E2E8F0;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.85; filter: drop-shadow(0 0 12px rgba(254, 240, 138, 0.8)); }}
      50% {{ opacity: 0.55; filter: drop-shadow(0 0 6px rgba(254, 240, 138, 0.4)); }}
    }}
    @keyframes glarePulse {{
      0%, 100% {{ transform: scale(1.0); opacity: 0.95; }}
      50% {{ transform: scale(1.25); opacity: 0.7; }}
    }}
    .pulse-glow {{
      animation: pulseGlow 1.8s infinite ease-in-out;
    }}
    .glare-burst {{
      animation: glarePulse 0.6s infinite ease-in-out;
      transform-origin: center;
    }}
    .custom-slider {{
      -webkit-appearance: none;
      appearance: none;
      width: 100%;
      height: 6px;
      background: #1E293B;
      border-radius: 3px;
      outline: none;
    }}
    .custom-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #38BDF8;
      cursor: pointer;
      border: 2px solid #0C4A6E;
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.8);
      transition: transform 0.1s;
    }}
    .custom-slider::-webkit-slider-thumb:hover {{
      transform: scale(1.2);
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col items-center p-3 select-none">

  <!-- TOP SUITE / LESSON HEADER -->
  <header class="w-full max-w-5xl bg-[#0F141E] border border-[#232B3A] rounded-xl px-4 py-3 mb-2 flex flex-wrap items-center justify-between gap-3 shadow-xl">
    <div class="flex items-center space-x-3">
      <span class="text-[10px] font-extrabold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 mono">TDLR ADE-1317</span>
      <span class="text-[10px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">2.5D VECTOR ENGINE</span>
      <span class="text-xs font-bold text-gray-400 mono">LESSON 18</span>
      <div>
        <h1 class="text-sm font-extrabold text-white tracking-wide">L05-T10: Vehicle Lights &mdash; High Beam Dimming & Sight Distance</h1>
        <p class="text-[11px] text-gray-400">Texas Driver Handbook Ch. 5 &bull; TTC &sect; 547.333 (Multiple-Beam Lighting Equipment)</p>
      </div>
    </div>

    <!-- SCENARIO TOGGLES -->
    <div class="flex items-center space-x-2">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
        1: Oncoming Traffic (500 FT Rule)
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
        2: Following Traffic (300 FT Rule)
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
        Hazard: Glare &amp; Centerline Drift
      </button>
      <div class="flex items-center space-x-1 pl-2 border-l border-gray-700">
        <input type="checkbox" id="auto-loop-toggle" checked class="w-3.5 h-3.5 rounded bg-gray-800 text-emerald-500 accent-emerald-500" />
        <label for="auto-loop-toggle" class="text-[11px] text-gray-300 mono cursor-pointer">Auto-Loop</label>
      </div>
    </div>
  </header>

  <!-- CANONICAL STEPPER BAR -->
  <nav class="w-full max-w-5xl bg-[#0D121B] border border-[#1E2636] rounded-xl px-3 py-2 mb-2 grid grid-cols-4 gap-2 text-xs shadow-md" aria-label="Lesson Steps">
    <button data-step="1" class="step-btn px-2.5 py-1 rounded-lg border border-blue-500/40 bg-blue-950/30 text-left transition hover:border-blue-500">
      <div class="text-[9px] mono text-blue-400 font-bold uppercase tracking-wider">STEP 1</div>
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">High Beam Cruising (500 FT)</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-400 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">Oncoming Traffic Detected</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-400 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">500 FT Dimming Point</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-400 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Safe Glare-Free Passing</div>
    </button>
  </nav>

  <!-- SIMULATION VIEWPORT -->
  <main class="w-full max-w-5xl relative aspect-[16/9] bg-[#05070C] rounded-2xl border border-[#1E2638] overflow-hidden shadow-2xl">
    
    <!-- STAGE CONTAINER (1000x600 coordinate envelope) -->
    <div id="stage-viewport" class="absolute inset-0 w-full h-full">

      <!-- LAYER 0: Texas Suburban 2-Lane Roadway Base with Deep Night Filter -->
      <img src="{road_b64}" alt="Texas 2-Lane Country Road at Night" class="w-full h-full object-cover filter brightness-[0.38] contrast-[1.22] saturate-[0.80]" />

      <!-- LAYER 1: SVG LIGHTING & PHOTOMETRY VECTORS -->
      <svg id="stage-svg" viewBox="0 0 1000 600" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <!-- Headlight Beam Gradients -->
          <linearGradient id="beam-high-grad" x1="0%" y1="0%" x2="100%" y2="0%" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#FEF08A" stop-opacity="0.95" />
            <stop offset="35%" stop-color="#FEF9C3" stop-opacity="0.65" />
            <stop offset="70%" stop-color="#38BDF8" stop-opacity="0.25" />
            <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.0" />
          </linearGradient>

          <linearGradient id="beam-low-grad" x1="0%" y1="0%" x2="100%" y2="0%" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#FDE047" stop-opacity="0.90" />
            <stop offset="45%" stop-color="#FEF08A" stop-opacity="0.55" />
            <stop offset="100%" stop-color="#FBBF24" stop-opacity="0.0" />
          </linearGradient>

          <linearGradient id="beam-oncoming-grad" x1="0%" y1="0%" x2="100%" y2="0%" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#FEF9C3" stop-opacity="0.90" />
            <stop offset="40%" stop-color="#FEF08A" stop-opacity="0.60" />
            <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.0" />
          </linearGradient>

          <!-- Glare Radial Burst -->
          <radialGradient id="glare-radial" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1.0" />
            <stop offset="30%" stop-color="#FEF08A" stop-opacity="0.85" />
            <stop offset="65%" stop-color="#F59E0B" stop-opacity="0.45" />
            <stop offset="100%" stop-color="#DC2626" stop-opacity="0.0" />
          </radialGradient>

          <!-- Beam Glow Blur Filter -->
          <filter id="beam-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        <!-- NIGHT AMBIENCE SHADOW VIGNETTE OVER SURROUNDING TERRAIN -->
        <polygon points="0,0 1000,0 1000,600 0,600" fill="#040812" fill-opacity="0.45" />

        <!-- HIGHWAY SIGHTLINE MILE MARKER POST -->
        <g id="mile-marker" transform="translate(680, 245)">
          <rect x="0" y="0" width="14" height="28" rx="2" fill="#065F46" stroke="#10B981" stroke-width="1.2" />
          <text x="7" y="10" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="900" text-anchor="middle">TX</text>
          <text x="7" y="21" fill="#A7F3D0" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="900" text-anchor="middle">144</text>
        </g>

        <!-- DYNAMIC HEADLIGHT CONES -->
        <!-- Ego Headlight Beam (High or Low) -->
        <polygon id="ego-beam-poly" points="0,0 0,0 0,0" fill="#FEF9C3" fill-opacity="0.55" filter="url(#beam-glow)" />

        <!-- Oncoming Headlight Beam -->
        <polygon id="oncoming-beam-poly" points="0,0 0,0 0,0" fill="#FEF9C3" fill-opacity="0.55" filter="url(#beam-glow)" />

        <!-- Lead Vehicle Rear Tail Glows (Mode 2) -->
        <g id="lead-tail-glows" opacity="0.0">
          <circle id="tail-left" cx="0" cy="0" r="8" fill="#EF4444" fill-opacity="0.8" />
          <circle id="tail-right" cx="0" cy="0" r="8" fill="#EF4444" fill-opacity="0.8" />
        </g>

        <!-- MIRROR GLARE REFLECTION VECTORS (Mode 2) -->
        <g id="mirror-glare-group" opacity="0.0">
          <line id="mirror-ray-left" x1="0" y1="0" x2="0" y2="0" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6,4" />
          <line id="mirror-ray-center" x1="0" y1="0" x2="0" y2="0" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="6,4" />
          <rect id="mirror-glare-badge-rect" x="0" y="0" width="190" height="20" rx="10" fill="#2B1B05" stroke="#F59E0B" stroke-width="1.5" />
          <text id="mirror-glare-badge-text" x="0" y="0" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">⚠ REARVIEW MIRROR GLARE</text>
        </g>

        <!-- DYNAMIC DISTANCE MEASURING BRACKET -->
        <g id="distance-bracket-group" opacity="1.0">
          <path id="bracket-line" d="M0,0 L0,0" stroke="#38BDF8" stroke-width="2" stroke-dasharray="8,6" />
          <circle id="bracket-dot-ego" cx="0" cy="0" r="4" fill="#38BDF8" stroke="#0C4A6E" stroke-width="1.5" />
          <circle id="bracket-dot-target" cx="0" cy="0" r="4" fill="#38BDF8" stroke="#0C4A6E" stroke-width="1.5" />
          
          <!-- Distance Value Badge -->
          <g id="distance-badge-group">
            <rect id="distance-badge-bg" x="0" y="0" width="190" height="20" rx="10" fill="#08202A" stroke="#38BDF8" stroke-width="1.5" />
            <text id="distance-badge-text" x="0" y="0" fill="#7DD3FC" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">500 FT STATUTORY DIMMING THRESHOLD</text>
          </g>
        </g>

        <!-- MODE 3: GLARE BURST & RETINAL FLASH BLINDNESS EFFECT -->
        <g id="glare-burst-group" opacity="0.0">
          <circle id="glare-burst-circle" cx="0" cy="0" r="54" fill="url(#glare-radial)" class="glare-burst" />
          <polygon id="glare-star" points="0,-22 6,-7 22,-6 10,6 14,22 0,12 -14,22 -10,6 -22,-6 -6,-7" fill="#FFFFFF" stroke="#F59E0B" stroke-width="1.5" class="glare-burst" />
          <rect id="glare-tag-rect" x="0" y="0" width="220" height="22" rx="11" fill="#3B0707" stroke="#EF4444" stroke-width="1.5" />
          <text id="glare-tag-text" x="0" y="0" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="900" text-anchor="middle">👁 FLASH BLINDNESS (3–5s RECOVERY)</text>
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- EGO VEHICLE (RED SEDAN - LANE 1 HEADING NE) -->
      <div id="veh-ego" class="absolute z-20 pointer-events-none transition-transform" style="left: 14.0%; top: 92.8%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_ne_b64}" alt="Ego Vehicle NE" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.85)]" />
          
          <!-- Headlight Lens Bulbs Glow (Front Right & Front Left) -->
          <div id="ego-lens-glow" class="absolute w-3 h-3 rounded-full bg-yellow-200 filter blur-[2px] opacity-90" style="top: 30%; right: 5%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: HIGH BEAMS (500 FT SIGHTLINE)
        </div>
      </div>

      <!-- ONCOMING VEHICLE (BLUE SEDAN - LANE 2 HEADING SW - Mode 1 & 3) -->
      <div id="veh-oncoming" class="absolute z-20 pointer-events-none transition-transform" style="left: 92.0%; top: 0.3%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_sw_b64}" alt="Oncoming Vehicle SW" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.85)]" />
          
          <!-- Oncoming Headlight Lens Bulbs Glow -->
          <div id="oncoming-lens-glow" class="absolute w-3 h-3 rounded-full bg-yellow-200 filter blur-[2px] opacity-90" style="bottom: 25%; left: 8%;"></div>
        </div>
        <div id="tag-veh-oncoming" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider">
          ONCOMING: 50 MPH (LANE 2)
        </div>
      </div>

      <!-- LEAD VEHICLE (YELLOW SEDAN - LANE 1 HEADING NE - Mode 2) -->
      <div id="veh-lead" class="absolute z-20 pointer-events-none transition-transform opacity-0" style="left: 50.0%; top: 56.6%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Lead Vehicle NE" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.85)]" />
        </div>
        <div id="tag-veh-lead" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          LEAD CAR: 42 MPH (LANE 1)
        </div>
      </div>

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 12px; left: 295px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TTC § 547.333 MANDATE: DIM HIGH BEAMS WITHIN 500 FT OF ONCOMING TRAFFIC</span>
      </div>

      <!-- BOTTOM RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-3 right-3 z-25 px-2.5 py-1 rounded-lg bg-[#081C15]/90 border border-emerald-500/50 text-emerald-400 mono text-[9px] font-bold tracking-wider pointer-events-none flex items-center space-x-1.5 shadow-md">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="compliance-text">TTC § 547.333 LIGHTING COMPLIANCE VERIFIED</span>
      </div>

      <!-- TELEMETRY & PHOTOMETRY HUD CARD (TOP-LEFT) -->
      <aside id="telemetry-hud-card" class="absolute top-3 left-3 z-30 w-[275px] bg-[#0E131D]/95 border border-[#252E40] rounded-xl p-3 shadow-2xl backdrop-blur-md space-y-2 text-xs">
        <div class="flex items-center justify-between pb-1.5 border-b border-gray-800">
          <div class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
            <span class="mono font-bold text-[10px] text-gray-300 uppercase tracking-wider">VEHICLE LIGHTING HUD</span>
          </div>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">BEAM: HIGH (500 FT)</span>
        </div>

        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-[10.5px]">
          <span class="text-gray-400">Ego Light Mode:</span>
          <span class="font-bold text-blue-400 mono text-right" id="telem-beam-mode">HIGH BEAMS</span>

          <span class="text-gray-400">Illumination Envelope:</span>
          <span class="font-bold text-white mono text-right" id="telem-illumination">500 FT (350–500 FT)</span>

          <span class="text-gray-400">Target Separation:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-distance">850 FT (CLOSING)</span>

          <span class="text-gray-400">Statutory Threshold:</span>
          <span class="font-bold text-amber-300 mono text-right" id="telem-threshold">500 FT (TTC § 547.333)</span>

          <span class="text-gray-400">Safe Stopping Sight:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-sight-margin">ADEQUATE (+188 FT)</span>

          <span class="text-gray-400">Photokeratitis Glare:</span>
          <span class="font-bold text-emerald-400 mono text-right" id="telem-glare">0% (NON-BLINDING)</span>
        </div>

        <div class="pt-1.5 border-t border-gray-800 text-[10px] text-gray-300 leading-tight" id="hud-narrative">
          Step 1: Ego vehicle travels on rural highway at 50 MPH using high beams. High beams provide 350–500 ft of illumination, safe for highway speeds.
        </div>
      </aside>

      <!-- MODE 3 HAZARD VIOLATION BANNER -->
      <div id="hazard-banner" class="absolute bottom-4 left-1/2 -translate-x-1/2 z-35 max-w-lg w-[90%] bg-red-950/95 border-2 border-red-500 rounded-xl p-2.5 text-center shadow-2xl opacity-0 pointer-events-none transition-all duration-300">
        <div class="text-[10px] mono font-black text-red-300 uppercase tracking-wider flex items-center justify-center space-x-1.5">
          <span>⚠ CRITICAL STATUTORY VIOLATION ⚠</span>
        </div>
        <div class="text-[11px] font-black text-white mt-0.5">
          FAILURE TO DIM HIGH BEAMS WITHIN 500 FT (TTC &sect; 547.333)
        </div>
        <p class="text-[9.5px] text-red-200 mt-1 leading-tight">
          Projecting high beams into an oncoming vehicle within 500 ft dazzles the driver with 50,000+ candela. Glare photokeratitis creates 3&ndash;5 seconds of flash blindness, causing involuntary centerline drift and head-on collisions. Class C Misdemeanor ($200+ fine).
        </p>
      </div>

    </div>
  </main>

  <!-- TIMELINE SCRUBBER & CONTROLS -->
  <footer class="w-full max-w-5xl bg-[#0F141E] border border-[#232B3A] rounded-xl p-2.5 mt-2 shadow-xl space-y-2">
    <div class="flex items-center space-x-3">
      <!-- Play / Pause -->
      <button id="btn-play-pause" class="w-8 h-8 rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center transition shadow-md">
        <svg id="icon-play" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        <svg id="icon-pause" class="w-4 h-4 hidden" fill="currentColor" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
      </button>

      <!-- Reset -->
      <button id="btn-reset" class="w-8 h-8 rounded-lg bg-[#1B2230] hover:bg-[#252F42] text-gray-300 hover:text-white flex items-center justify-center transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
      </button>

      <!-- Time Display -->
      <span id="time-display" class="mono text-xs font-bold text-blue-400 w-12 text-center">0.00s</span>

      <!-- Scrubber -->
      <input id="timeline-slider" type="range" min="0" max="8.0" step="0.05" value="0.0" class="custom-slider flex-1" />

      <!-- Total Duration -->
      <span class="mono text-xs text-gray-400">8.00s</span>

      <!-- Playback Speed Chips -->
      <div class="flex items-center space-x-1 pl-2 border-l border-gray-700">
        <button class="speed-btn px-2 py-0.5 rounded text-[11px] mono text-gray-400 hover:text-white" data-speed="0.5">0.5x</button>
        <button class="speed-btn px-2 py-0.5 rounded text-[11px] mono bg-blue-600 text-white font-bold" data-speed="1.0">1.0x</button>
        <button class="speed-btn px-2 py-0.5 rounded text-[11px] mono text-gray-400 hover:text-white" data-speed="1.5">1.5x</button>
      </div>
    </div>

    <!-- Timeline Keyframe Indicators -->
    <div class="flex justify-between text-[10px] text-gray-400 mono px-1 pt-1 border-t border-gray-800">
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        <span id="keyframe-1-text">0.8s High Beams Active</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
        <span id="keyframe-2-text">2.8s Closing Detection</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-3-text">4.8s 500-FT Dimming Point</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="keyframe-4-text">6.8s Safe Passage</span>
      </span>
      <span class="text-gray-500 font-bold">Texas Driver Handbook Ch. 5 &bull; TTC &sect; 547.333</span>
    </div>
  </footer>

  <!-- CORE SIMULATION ENGINE JAVASCRIPT -->
  <script>
    // State variables
    let currentMode = 1; // 1: Oncoming 500 FT, 2: Following 300 FT, 3: Hazard Glare
    let currentTime = 0.0;
    let isPlaying = false;
    let playbackSpeed = 1.0;
    const duration = 8.0;
    let lastTimestamp = 0;

    // DOM Elements
    const playPauseBtn = document.getElementById('btn-play-pause');
    const playIcon = document.getElementById('icon-play');
    const pauseIcon = document.getElementById('icon-pause');
    const resetBtn = document.getElementById('btn-reset');
    const timelineSlider = document.getElementById('timeline-slider');
    const timeDisplay = document.getElementById('time-display');
    const autoLoopToggle = document.getElementById('auto-loop-toggle');

    // Vehicles
    const vehEgo = document.getElementById('veh-ego');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const egoLensGlow = document.getElementById('ego-lens-glow');

    const vehOncoming = document.getElementById('veh-oncoming');
    const tagVehOncoming = document.getElementById('tag-veh-oncoming');
    const oncomingLensGlow = document.getElementById('oncoming-lens-glow');

    const vehLead = document.getElementById('veh-lead');
    const tagVehLead = document.getElementById('tag-veh-lead');

    // SVG Beam Polygons & Lighting Elements
    const egoBeamPoly = document.getElementById('ego-beam-poly');
    const oncomingBeamPoly = document.getElementById('oncoming-beam-poly');
    const leadTailGlows = document.getElementById('lead-tail-glows');
    const tailLeft = document.getElementById('tail-left');
    const tailRight = document.getElementById('tail-right');

    const mirrorGlareGroup = document.getElementById('mirror-glare-group');
    const mirrorRayLeft = document.getElementById('mirror-ray-left');
    const mirrorRayCenter = document.getElementById('mirror-ray-center');
    const mirrorGlareBadgeRect = document.getElementById('mirror-glare-badge-rect');
    const mirrorGlareBadgeText = document.getElementById('mirror-glare-badge-text');

    const distanceBracketGroup = document.getElementById('distance-bracket-group');
    const bracketLine = document.getElementById('bracket-line');
    const bracketDotEgo = document.getElementById('bracket-dot-ego');
    const bracketDotTarget = document.getElementById('bracket-dot-target');
    const distanceBadgeBg = document.getElementById('distance-badge-bg');
    const distanceBadgeText = document.getElementById('distance-badge-text');

    const glareBurstGroup = document.getElementById('glare-burst-group');
    const glareBurstCircle = document.getElementById('glare-burst-circle');
    const glareStar = document.getElementById('glare-star');
    const glareTagRect = document.getElementById('glare-tag-rect');
    const glareTagText = document.getElementById('glare-tag-text');

    // Telemetry & Narrative
    const telemBeamMode = document.getElementById('telem-beam-mode');
    const telemIllumination = document.getElementById('telem-illumination');
    const telemDistance = document.getElementById('telem-distance');
    const telemThreshold = document.getElementById('telem-threshold');
    const telemSightMargin = document.getElementById('telem-sight-margin');
    const telemGlare = document.getElementById('telem-glare');
    const hudNarrative = document.getElementById('hud-narrative');
    const signalStateBadge = document.getElementById('signal-state-badge');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const complianceBadge = document.getElementById('compliance-badge');
    const complianceText = document.getElementById('compliance-text');
    const hazardBanner = document.getElementById('hazard-banner');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Roadway Lane Math (Texas Suburban 2-Lane Corridor)
    // Lane 1 (South-East / Lower Lane heading NE):
    function getLane1Y(x) {{
      return 56.62 - 1.005 * (x - 50.0);
    }}
    // Lane 2 (North-West / Upper Lane heading SW):
    function getLane2Y(x) {{
      return 42.56 - 1.005 * (x - 50.0);
    }}

    // Helper: update triangular/trapezoidal SVG beam polygon
    function updateBeam(polyElem, startX, startY, lengthPx, halfWidthPx, angleDeg, colorHex, opacityVal, biasRightPx) {{
      const rad = (angleDeg * Math.PI) / 180;
      const cosA = Math.cos(rad);
      const sinA = Math.sin(rad);
      const perpX = -sinA;
      const perpY = cosA;

      const tipCenterX = startX + lengthPx * cosA + biasRightPx * perpX;
      const tipCenterY = startY + lengthPx * sinA + biasRightPx * perpY;

      const p1X = startX.toFixed(1);
      const p1Y = startY.toFixed(1);
      const p2X = (tipCenterX - halfWidthPx * perpX).toFixed(1);
      const p2Y = (tipCenterY - halfWidthPx * perpY).toFixed(1);
      const p3X = (tipCenterX + halfWidthPx * perpX).toFixed(1);
      const p3Y = (tipCenterY + halfWidthPx * perpY).toFixed(1);

      polyElem.setAttribute('points', `${{p1X}},${{p1Y}} ${{p2X}},${{p2Y}} ${{p3X}},${{p3Y}}`);
      polyElem.setAttribute('fill', colorHex);
      polyElem.setAttribute('fill-opacity', opacityVal);
    }}

    // ===============================================================
    // MODE 1: ONCOMING TRAFFIC 500-FT DIMMING MANDATE (TTC § 547.333)
    // ===============================================================
    function updateMode1(t) {{
      vehLead.style.opacity = '0.0';
      leadTailGlows.setAttribute('opacity', '0.0');
      mirrorGlareGroup.setAttribute('opacity', '0.0');
      glareBurstGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      vehOncoming.style.opacity = '1.0';

      // Motion: Vehicles approaching each other
      // Ego traveling NE in Lane 1: X from 22% to 68%
      const egoX = 22.0 + (t / 8.0) * 46.0;
      const egoY = getLane1Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;

      // Oncoming traveling SW in Lane 2: X from 86% to 40%
      const oncX = 86.0 - (t / 8.0) * 46.0;
      const oncY = getLane2Y(oncX);
      vehOncoming.style.left = `${{oncX}}%`;
      vehOncoming.style.top = `${{oncY}}%`;

      // Separation Distance (1% X ≈ 22.5 FT)
      // At t = 3.6s: deltaX = 22.6% => exactly 508 FT ≈ 500 FT
      const deltaX = Math.max(0, oncX - egoX);
      const separationFt = Math.max(0, Math.round(deltaX * 22.5));

      // Headlight State: Dim at 500 FT (t >= 3.6s)
      const isDimmed = (t >= 3.6);
      const passedEachOther = (oncX <= egoX + 4.0);

      // SVG Beam Origin Coordinates (1000 x 600)
      const egoSvgX = egoX * 10 + 26;
      const egoSvgY = egoY * 6 - 8;
      const oncSvgX = oncX * 10 - 24;
      const oncSvgY = oncY * 6 + 10;

      // Road angle in degrees pointing NE is approximately -45 degrees
      const roadAngleNE = -45.0;
      const roadAngleSW = 135.0;

      if (!isDimmed) {{
        // HIGH BEAMS ACTIVE (500 FT illumination)
        updateBeam(egoBeamPoly, egoSvgX, egoSvgY, 320, 50, roadAngleNE, '#FEF9C3', 0.55, 0);
        updateBeam(oncomingBeamPoly, oncSvgX, oncSvgY, 260, 45, roadAngleSW, '#FEF08A', 0.50, 0);
        egoLensGlow.className = 'absolute w-3.5 h-3.5 rounded-full bg-cyan-200 filter blur-[2px] opacity-95';
        oncomingLensGlow.className = 'absolute w-3 h-3 rounded-full bg-yellow-200 filter blur-[2px] opacity-90';
      }} else {{
        // LOW BEAMS ACTIVE (180 FT illumination, deflected rightward toward shoulder)
        updateBeam(egoBeamPoly, egoSvgX, egoSvgY, 125, 28, roadAngleNE, '#FDE047', 0.40, 16);
        updateBeam(oncomingBeamPoly, oncSvgX, oncSvgY, 120, 26, roadAngleSW, '#FDE047', 0.40, -14);
        egoLensGlow.className = 'absolute w-2.5 h-2.5 rounded-full bg-yellow-300 filter blur-[1px] opacity-80';
        oncomingLensGlow.className = 'absolute w-2.5 h-2.5 rounded-full bg-yellow-300 filter blur-[1px] opacity-80';
      }}

      // Distance Bracket & Live Threshold Metric
      if (!passedEachOther) {{
        distanceBracketGroup.setAttribute('opacity', '1.0');
        bracketLine.setAttribute('d', `M${{egoSvgX}},${{egoSvgY - 18}} L${{oncSvgX}},${{oncSvgY - 18}}`);
        bracketDotEgo.setAttribute('cx', egoSvgX);
        bracketDotEgo.setAttribute('cy', egoSvgY - 18);
        bracketDotTarget.setAttribute('cx', oncSvgX);
        bracketDotTarget.setAttribute('cy', oncSvgY - 18);

        const midX = (egoSvgX + oncSvgX) / 2;
        const midY = (egoSvgY + oncSvgY) / 2 - 38;
        distanceBadgeBg.setAttribute('x', midX - 95);
        distanceBadgeBg.setAttribute('y', midY - 10);
        distanceBadgeText.setAttribute('x', midX);
        distanceBadgeText.setAttribute('y', midY + 4);

        if (!isDimmed) {{
          distanceBadgeText.textContent = `${{separationFt}} FT • HIGH BEAMS (>500 FT)`;
          distanceBadgeBg.setAttribute('stroke', '#38BDF8');
          distanceBadgeText.setAttribute('fill', '#7DD3FC');
        }} else {{
          distanceBadgeText.textContent = `${{separationFt}} FT • LOW BEAMS (TTC § 547.333)`;
          distanceBadgeBg.setAttribute('stroke', '#10B981');
          distanceBadgeText.setAttribute('fill', '#6EE7B7');
        }}
      }} else {{
        distanceBracketGroup.setAttribute('opacity', '0.0');
      }}

      // Telemetry & Narrative updates per canonical step
      if (t < 2.0) {{
        tagVehEgo.textContent = 'EGO: HIGH BEAMS (500 FT SIGHTLINE) • 50 MPH';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        tagVehOncoming.textContent = 'ONCOMING (LANE 2): 50 MPH';
        tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'BEAM: HIGH (500 FT)';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        hudNarrative.textContent = 'Step 1: Ego vehicle cruises rural two-lane highway on high beams at 50 MPH. High beams illuminate 350–500 ft ahead, providing safe stopping sightlines.';
        telemBeamMode.textContent = 'HIGH BEAMS (ON)';
        telemBeamMode.className = 'font-bold text-blue-400 mono text-right';
        telemIllumination.textContent = '500 FT (HIGH BEAM)';
        telemDistance.textContent = `${{separationFt}} FT (CLEAR)`;
        telemThreshold.textContent = '500 FT (ONCOMING)';
        telemSightMargin.textContent = 'ADEQUATE (+188 FT)';
        telemGlare.textContent = '0% (CLEAR ROAD)';
      }} else if (t < 3.6) {{
        tagVehEgo.textContent = `EGO: APPROACHING 500-FT MANDATORY DIM ZONE (${{separationFt}} FT)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        tagVehOncoming.textContent = 'ONCOMING: 50 MPH (APPROACHING)';
        tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'DIMMING IMMINENT';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        hudNarrative.textContent = 'Step 2: Oncoming vehicle detected in opposite lane. Combined closing speed is 100 MPH (146 ft/s). Driver prepares to dim high beams before 500 ft.';
        telemBeamMode.textContent = 'HIGH BEAMS (DIM READY)';
        telemBeamMode.className = 'font-bold text-amber-400 mono text-right';
        telemIllumination.textContent = '500 FT (HIGH BEAM)';
        telemDistance.textContent = `${{separationFt}} FT (CLOSING)`;
        telemThreshold.textContent = '500 FT (TTC § 547.333)';
        telemSightMargin.textContent = 'TRANSITIONING';
        telemGlare.textContent = 'GLARE IMMINENT IF NOT DIMMED';
      }} else if (t < 6.0) {{
        tagVehEgo.textContent = 'EGO: LOW BEAMS ENGAGED (TTC § 547.333 COMPLIANT)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        tagVehOncoming.textContent = 'ONCOMING: LOW BEAMS ENGAGED';
        tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'BEAM: LOW (DIMMED)';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudNarrative.textContent = 'Step 3: At the 500-ft statutory threshold (TTC § 547.333(c)(1)), driver dims to low beams. Low beams project 150–200 ft down and rightward, eliminating blinding glare.';
        telemBeamMode.textContent = 'LOW BEAMS (DIMMED)';
        telemBeamMode.className = 'font-bold text-emerald-400 mono text-right';
        telemIllumination.textContent = '180 FT (LOW BEAM)';
        telemDistance.textContent = `${{separationFt}} FT (SAFE PASS)`;
        telemThreshold.textContent = '500 FT MET';
        telemSightMargin.textContent = 'SAFE AT 50 MPH';
        telemGlare.textContent = '0% (PROTECTED)';
      }} else {{
        tagVehEgo.textContent = passedEachOther ? 'EGO: PASSED ONCOMING • RESTORING HIGH BEAMS' : 'EGO: PASSING IN PROGRESS';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        tagVehOncoming.textContent = 'ONCOMING: CLEAR OF GLARE';
        signalStateBadge.innerHTML = passedEachOther ? 'HIGH BEAMS RESTORED' : 'SAFE PASSAGE';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudNarrative.textContent = 'Step 4: Both vehicles pass safely with zero flash blindness. Once past the oncoming vehicle, driver may lawfully re-engage high beams if road ahead is clear.';
        telemBeamMode.textContent = passedEachOther ? 'HIGH BEAMS RESTORED' : 'LOW BEAMS (PASSING)';
        telemBeamMode.className = 'font-bold text-blue-400 mono text-right';
        telemIllumination.textContent = passedEachOther ? '500 FT (RESTORED)' : '180 FT (LOW BEAM)';
        telemDistance.textContent = 'CLEAR (OPPOSING)';
        telemThreshold.textContent = 'PASSED';
        telemSightMargin.textContent = 'OPTIMAL (+188 FT)';
        telemGlare.textContent = '0% GLARE';
      }}

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TTC § 547.333 MANDATE: DIM HIGH BEAMS WITHIN 500 FT OF ONCOMING TRAFFIC';
      complianceText.textContent = 'TTC § 547.333 LIGHTING COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 2: FOLLOWING TRAFFIC 300-FT REAR DIMMING RULE (TTC § 547.333(c)(2))
    // ===============================================================
    function updateMode2(t) {{
      vehOncoming.style.opacity = '0.0';
      oncomingBeamPoly.setAttribute('points', '0,0 0,0 0,0');
      glareBurstGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      vehLead.style.opacity = '1.0';
      leadTailGlows.setAttribute('opacity', '1.0');

      // Both vehicles traveling NE in Lane 1
      // Lead vehicle at steady 42 MPH: X from 52% to 76%
      const leadX = 52.0 + (t / 8.0) * 24.0;
      const leadY = getLane1Y(leadX);
      vehLead.style.left = `${{leadX}}%`;
      vehLead.style.top = `${{leadY}}%`;

      // Ego vehicle approaching from behind at 54 MPH, then matching speed
      let egoX = 22.0;
      if (t < 3.6) {{
        egoX = 22.0 + (t / 3.6) * (leadX - 13.0 - 22.0);
      }} else {{
        egoX = leadX - 13.0; // Settles at ~300 FT following buffer
      }}
      const egoY = getLane1Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;

      const deltaX = Math.max(0, leadX - egoX);
      const separationFt = Math.round(deltaX * 23.0);

      const isDimmed = (t >= 3.4);

      // SVG coordinates
      const egoSvgX = egoX * 10 + 26;
      const egoSvgY = egoY * 6 - 8;
      const leadSvgX = leadX * 10 - 24;
      const leadSvgY = leadY * 6 + 10;
      const roadAngleNE = -45.0;

      // Tail lights on Lead Vehicle
      tailLeft.setAttribute('cx', leadSvgX - 2);
      tailLeft.setAttribute('cy', leadSvgY + 4);
      tailRight.setAttribute('cx', leadSvgX + 10);
      tailRight.setAttribute('cy', leadSvgY - 4);

      if (!isDimmed) {{
        // High Beams blasting into lead vehicle mirrors!
        updateBeam(egoBeamPoly, egoSvgX, egoSvgY, 320, 50, roadAngleNE, '#FEF9C3', 0.55, 0);
        egoLensGlow.className = 'absolute w-3.5 h-3.5 rounded-full bg-cyan-200 filter blur-[2px] opacity-95';

        // Mirror glare reflections bouncing back into cabin
        mirrorGlareGroup.setAttribute('opacity', '1.0');
        mirrorRayLeft.setAttribute('x1', leadSvgX - 2);
        mirrorRayLeft.setAttribute('y1', leadSvgY + 4);
        mirrorRayLeft.setAttribute('x2', leadSvgX - 30);
        mirrorRayLeft.setAttribute('y2', leadSvgY + 25);

        mirrorRayCenter.setAttribute('x1', leadSvgX + 4);
        mirrorRayCenter.setAttribute('y1', leadSvgY);
        mirrorRayCenter.setAttribute('x2', leadSvgX - 24);
        mirrorRayCenter.setAttribute('y2', leadSvgY - 20);

        mirrorGlareBadgeRect.setAttribute('x', leadSvgX - 95);
        mirrorGlareBadgeRect.setAttribute('y', leadSvgY - 38);
        mirrorGlareBadgeText.setAttribute('x', leadSvgX);
        mirrorGlareBadgeText.setAttribute('y', leadSvgY - 25);
      }} else {{
        // Low Beams compliant (180 FT range, below mirrors)
        updateBeam(egoBeamPoly, egoSvgX, egoSvgY, 125, 28, roadAngleNE, '#FDE047', 0.40, 16);
        egoLensGlow.className = 'absolute w-2.5 h-2.5 rounded-full bg-yellow-300 filter blur-[1px] opacity-80';
        mirrorGlareGroup.setAttribute('opacity', '0.0');
      }}

      // Distance Bracket between Ego and Lead
      distanceBracketGroup.setAttribute('opacity', '1.0');
      bracketLine.setAttribute('d', `M${{egoSvgX}},${{egoSvgY - 18}} L${{leadSvgX}},${{leadSvgY - 18}}`);
      bracketDotEgo.setAttribute('cx', egoSvgX);
      bracketDotEgo.setAttribute('cy', egoSvgY - 18);
      bracketDotTarget.setAttribute('cx', leadSvgX);
      bracketDotTarget.setAttribute('cy', leadSvgY - 18);

      const midX = (egoSvgX + leadSvgX) / 2;
      const midY = getLane2Y(midX / 10) * 6; // Floats peacefully in empty Lane 2
      distanceBadgeBg.setAttribute('x', midX - 95);
      distanceBadgeBg.setAttribute('y', midY - 10);
      distanceBadgeText.setAttribute('x', midX);
      distanceBadgeText.setAttribute('y', midY + 4);

      if (!isDimmed) {{
        distanceBadgeText.textContent = `${{separationFt}} FT • CLOSING TO 300 FT`;
        distanceBadgeBg.setAttribute('stroke', '#F59E0B');
        distanceBadgeText.setAttribute('fill', '#FDE68A');
      }} else {{
        distanceBadgeText.textContent = `${{separationFt}} FT • REAR DIMMED (300 FT MET)`;
        distanceBadgeBg.setAttribute('stroke', '#10B981');
        distanceBadgeText.setAttribute('fill', '#6EE7B7');
      }}

      // Step Narrative
      if (t < 2.0) {{
        tagVehEgo.textContent = `EGO: APPROACHING REAR AT 54 MPH (${{separationFt}} FT)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        tagVehLead.textContent = 'LEAD CAR: 42 MPH (LANE 1)';
        tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'REAR APPROACH (>300 FT)';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        hudNarrative.textContent = 'Step 1: Ego vehicle approaches lead car from rear on rural highway. High beams still active at > 450 ft separation.';
        telemBeamMode.textContent = 'HIGH BEAMS';
        telemBeamMode.className = 'font-bold text-blue-400 mono text-right';
        telemIllumination.textContent = '500 FT ENVELOPE';
        telemDistance.textContent = `${{separationFt}} FT (REAR)`;
        telemThreshold.textContent = '300 FT (TTC § 547.333(c)(2))';
        telemSightMargin.textContent = 'CLEAR';
        telemGlare.textContent = 'MINIMAL REAR GLARE';
      }} else if (t < 3.4) {{
        tagVehEgo.textContent = `EGO: 300 FT THRESHOLD REACHED (${{separationFt}} FT)`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        tagVehLead.textContent = 'LEAD CAR: EXPERIENCING MIRROR GLARE!';
        tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'DIM AT 300 FT';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        hudNarrative.textContent = 'Step 2: Approaching within 300 ft from the rear! TTC § 547.333(c)(2) strictly mandates dimming to low beams to prevent blinding rearview mirror reflections.';
        telemBeamMode.textContent = 'DIMMING TO LOW BEAM';
        telemBeamMode.className = 'font-bold text-amber-400 mono text-right';
        telemIllumination.textContent = '500 FT -> 180 FT';
        telemDistance.textContent = `${{separationFt}} FT (CRITICAL)`;
        telemThreshold.textContent = '300 FT REAR MANDATE';
        telemSightMargin.textContent = 'TRANSITIONING';
        telemGlare.textContent = 'MIRROR GLARE PRESENT';
      }} else if (t < 5.8) {{
        tagVehEgo.textContent = 'EGO: LOW BEAMS ACTIVE • SAFE REAR SIGHTLINE';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        tagVehLead.textContent = 'LEAD CAR: MIRROR GLARE ELIMINATED';
        tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'BEAM: LOW (300 FT OK)';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudNarrative.textContent = 'Step 3: Low beams engaged within 300 ft. Light pattern illuminates asphalt below lead vehicle bumper without projecting into driver rearview or side mirrors.';
        telemBeamMode.textContent = 'LOW BEAMS (DIMMED)';
        telemBeamMode.className = 'font-bold text-emerald-400 mono text-right';
        telemIllumination.textContent = '180 FT (LOW BEAM)';
        telemDistance.textContent = `${{separationFt}} FT (COMPLIANT)`;
        telemThreshold.textContent = '300 FT MET';
        telemSightMargin.textContent = 'MATCHED BUFFER';
        telemGlare.textContent = '0% (NO MIRROR GLARE)';
      }} else {{
        tagVehEgo.textContent = 'EGO: 3-SECOND BUFFER & LOW BEAMS MAINTAINED';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        tagVehLead.textContent = 'LEAD CAR: SAFE FORWARD VISIBILITY';
        tagVehLead.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'COMPLIANT FOLLOWING';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudNarrative.textContent = 'Step 4: Driver maintains statutory 3-second following distance buffer on low beams until ready to execute an authorized passing maneuver.';
        telemBeamMode.textContent = 'LOW BEAMS (CRUISING)';
        telemBeamMode.className = 'font-bold text-emerald-400 mono text-right';
        telemIllumination.textContent = '180 FT';
        telemDistance.textContent = `${{separationFt}} FT (3 SEC)`;
        telemThreshold.textContent = 'COMPLIANT';
        telemSightMargin.textContent = 'OPTIMAL BUFFER';
        telemGlare.textContent = '0% GLARE';
      }}

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TTC § 547.333(c)(2) MANDATE: DIM HIGH BEAMS WITHIN 300 FT FROM REAR';
      complianceText.textContent = 'TTC § 547.333 REAR DIMMING VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (HIGH BEAM GLARE & CENTERLINE DRIFT)
    // ===============================================================
    function updateMode3(t) {{
      vehLead.style.opacity = '0.0';
      leadTailGlows.setAttribute('opacity', '0.0');
      mirrorGlareGroup.setAttribute('opacity', '0.0');
      complianceBadge.style.opacity = '0.0';
      vehOncoming.style.opacity = '1.0';

      // Motion: Ego advances in Lane 1 while holding HIGH BEAMS illegally!
      const egoX = 22.0 + (t / 8.0) * 46.0;
      const egoY = getLane1Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;

      // Oncoming car in Lane 2 gets blinded, suffers flash blindness, and drifts toward centerline!
      let oncX = 86.0 - (t / 8.0) * 46.0;
      let oncY = getLane2Y(oncX);

      // Centerline drift starting at t >= 3.8s
      if (t >= 3.8) {{
        const driftAmount = Math.min(5.5, (t - 3.8) * 2.5);
        oncY += driftAmount; // Drifts across centerline toward Lane 1!
      }}
      vehOncoming.style.left = `${{oncX}}%`;
      vehOncoming.style.top = `${{oncY}}%`;

      const deltaX = Math.max(0, oncX - egoX);
      const separationFt = Math.max(0, Math.round(deltaX * 22.5));

      // SVG Coordinates
      const egoSvgX = egoX * 10 + 26;
      const egoSvgY = egoY * 6 - 8;
      const oncSvgX = oncX * 10 - 24;
      const oncSvgY = oncY * 6 + 10;
      const roadAngleNE = -45.0;
      const roadAngleSW = 135.0;

      // High Beams held ILLEGALLY across entire scene!
      updateBeam(egoBeamPoly, egoSvgX, egoSvgY, 340, 55, roadAngleNE, '#FEF9C3', 0.65, 0);
      updateBeam(oncomingBeamPoly, oncSvgX, oncSvgY, 240, 40, roadAngleSW, '#FEF08A', 0.45, 0);
      egoLensGlow.className = 'absolute w-4 h-4 rounded-full bg-cyan-200 filter blur-[2px] opacity-100';

      // Blinding Glare Burst over Oncoming Driver Windshield when distance < 500 FT (t >= 3.2s)
      if (t >= 3.2 && oncX > egoX) {{
        glareBurstGroup.setAttribute('opacity', '1.0');
        glareBurstCircle.setAttribute('cx', oncSvgX);
        glareBurstCircle.setAttribute('cy', oncSvgY);
        glareStar.setAttribute('transform', `translate(${{oncSvgX}}, ${{oncSvgY}})`);
        glareTagRect.setAttribute('x', oncSvgX - 110);
        glareTagRect.setAttribute('y', oncSvgY - 48);
        glareTagText.setAttribute('x', oncSvgX);
        glareTagText.setAttribute('y', oncSvgY - 34);
      }} else {{
        glareBurstGroup.setAttribute('opacity', '0.0');
      }}

      // Distance Bracket in Mode 3 (Active during approach; yields to violation effects at t >= 3.2s)
      if (t < 3.2 && oncX > egoX) {{
        distanceBracketGroup.setAttribute('opacity', '1.0');
        bracketLine.setAttribute('d', `M${{egoSvgX}},${{egoSvgY - 18}} L${{oncSvgX}},${{oncSvgY - 18}}`);
        bracketDotEgo.setAttribute('cx', egoSvgX);
        bracketDotEgo.setAttribute('cy', egoSvgY - 18);
        bracketDotTarget.setAttribute('cx', oncSvgX);
        bracketDotTarget.setAttribute('cy', oncSvgY - 18);

        const midX = (egoSvgX + oncSvgX) / 2;
        const midY = (egoSvgY + oncSvgY) / 2 - 38;
        distanceBadgeBg.setAttribute('x', midX - 95);
        distanceBadgeBg.setAttribute('y', midY - 10);
        distanceBadgeText.setAttribute('x', midX);
        distanceBadgeText.setAttribute('y', midY + 4);

        distanceBadgeText.textContent = `${{separationFt}} FT • HIGH BEAMS HELD`;
        distanceBadgeBg.setAttribute('stroke', '#EF4444');
        distanceBadgeText.setAttribute('fill', '#FCA5A5');
      }} else {{
        distanceBracketGroup.setAttribute('opacity', '0.0');
      }}

      // Telemetry & Narrative
      if (t < 3.2) {{
        tagVehEgo.textContent = 'EGO: 50 MPH • HIGH BEAMS HELD (UNLAWFUL HOLD)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        tagVehOncoming.textContent = 'ONCOMING (LANE 2): CLOSING';
        tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        signalStateBadge.innerHTML = 'HIGH BEAM HOLD';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        hudNarrative.textContent = 'Step 1: Ego driver approaches oncoming vehicle but fails to dim high beams. 50,000+ candela high beam cone projects directly into oncoming driver eyes.';
        hazardBanner.style.opacity = '0.0';
      }} else if (t < 5.4) {{
        tagVehEgo.textContent = `VIOLATION: HIGH BEAMS WITHIN 500 FT (${{separationFt}} FT)!`;
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border-2 border-red-500 text-[9.5px] font-black text-red-200 mono shadow-2xl tracking-wider';
        tagVehOncoming.textContent = 'ONCOMING: BLINDED! DRIFTING OVER CENTERLINE!';
        tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border-2 border-red-500 text-[9.5px] font-black text-red-200 mono shadow-2xl tracking-wider';
        signalStateBadge.innerHTML = 'STATUTORY VIOLATION';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white border border-red-400 mono animate-pulse';
        hudNarrative.textContent = 'Step 2 & 3: Extreme photokeratitis! Intense light dazzles oncoming pupils; driver suffers 3–5 seconds of flash blindness and loses sight of right edge line, drifting across centerline.';
        hazardBanner.style.opacity = '1.0';
      }} else {{
        tagVehEgo.textContent = 'EGO: EMERGENCY BRAKE & NEAR-MISS!';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border-2 border-red-500 text-[9.5px] font-black text-red-200 mono shadow-2xl tracking-wider';
        tagVehOncoming.textContent = 'ONCOMING: DISORIENTED CENTERLINE ENCROACHMENT';
        tagVehOncoming.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border-2 border-red-500 text-[9.5px] font-black text-red-200 mono shadow-2xl tracking-wider';
        signalStateBadge.innerHTML = 'NEAR HEAD-ON CRASH';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white border border-red-400 mono';
        hudNarrative.textContent = 'Step 4: Imminent head-on collision danger! TTC § 547.333 violation carries Class C Misdemeanor citations and civil liability for resulting crash damages.';
        hazardBanner.style.opacity = '1.0';
      }}

      telemBeamMode.textContent = 'HIGH BEAMS (UNLAWFUL)';
      telemBeamMode.className = 'font-bold text-red-400 mono text-right';
      telemIllumination.textContent = '500 FT (BLINDING)';
      telemDistance.textContent = `${{separationFt}} FT (< 500 FT)`;
      telemThreshold.textContent = 'VIOLATED (TTC § 547.333)';
      telemSightMargin.textContent = 'HAZARDOUS GLOW';
      telemGlare.textContent = '100% RETINAL BLINDNESS';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-200 mono text-[9.5px] font-extrabold shadow-2xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'CRITICAL STATUTORY VIOLATION: FAILURE TO DIM HIGH BEAMS (TTC § 547.333)';
    }}

    // Step labels per mode
    const stepLabels = {{
      1: [
        'High Beam Cruising (500 FT)',
        'Oncoming Traffic Detected',
        '500 FT Dimming Point',
        'Safe Glare-Free Passing'
      ],
      2: [
        'Following Slower Lead Car',
        '300 FT Rear Dimming Point',
        'Low Beams (No Mirror Glare)',
        'Safe Buffer Maintained'
      ],
      3: [
        'Unlawful High Beam Hold',
        'Retinal Flash Blindness',
        'Centerline Drift Hazard',
        'Critical Head-On Crash Risk'
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
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500 bg-red-600 text-white shadow-md shadow-red-900/40';
        }} else {{
          if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60';
          else btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white';
        }}
      }});

      for (let s = 1; s <= 4; s++) {{
        const lbl = document.getElementById(`step-label-${{s}}`);
        if (lbl && stepLabels[mode]) {{
          lbl.textContent = stepLabels[mode][s - 1];
        }}
      }}

      updateSimulation(0.0);
    }}

    function setStep(stepNum) {{
      const stepTimes = [0.8, 2.8, 4.8, 6.8];
      currentTime = stepTimes[stepNum - 1];
      timelineSlider.value = currentTime.toFixed(2);
      timeDisplay.textContent = `${{currentTime.toFixed(2)}}s`;
      updateSimulation(currentTime);
    }}

    function updateSimulation(t) {{
      timeDisplay.textContent = `${{t.toFixed(2)}}s`;
      timelineSlider.value = t.toFixed(2);

      // Active step highlight
      const stepIdx = t < 2.0 ? 1 : (t < 4.0 ? 2 : (t < 6.0 ? 3 : 4));
      stepBtns.forEach((btn, idx) => {{
        if (idx + 1 === stepIdx) {{
          btn.className = 'step-btn px-2.5 py-1 rounded-lg border border-blue-500/50 bg-blue-950/40 text-left transition';
          btn.querySelector('div:first-child').className = 'text-[9px] mono text-blue-400 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-white truncate';
        }} else {{
          btn.className = 'step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600';
          btn.querySelector('div:first-child').className = 'text-[9px] mono text-gray-400 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-gray-300 truncate';
        }}
      }});

      if (currentMode === 1) updateMode1(t);
      else if (currentMode === 2) updateMode2(t);
      else if (currentMode === 3) updateMode3(t);
    }}

    function animate(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += dt * playbackSpeed;
        if (currentTime > duration) {{
          if (autoLoopToggle.checked) {{
            currentTime = 0.0;
          }} else {{
            currentTime = duration;
            isPlaying = false;
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
          }}
        }}
        updateSimulation(currentTime);
      }}

      requestAnimationFrame(animate);
    }}

    // Event Listeners
    playPauseBtn.addEventListener('click', () => {{
      isPlaying = !isPlaying;
      if (isPlaying) {{
        if (currentTime >= duration) currentTime = 0.0;
        playIcon.classList.add('hidden');
        pauseIcon.classList.remove('hidden');
      }} else {{
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
      }}
    }});

    resetBtn.addEventListener('click', () => {{
      currentTime = 0.0;
      isPlaying = false;
      playIcon.classList.remove('hidden');
      pauseIcon.classList.add('hidden');
      updateSimulation(0.0);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    stepBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        const s = parseInt(btn.dataset.step);
        setStep(s);
      }});
    }});

    modeBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        const m = parseInt(btn.dataset.mode);
        setMode(m);
      }});
    }});

    speedBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        speedBtns.forEach(b => b.className = 'speed-btn px-2 py-0.5 rounded text-[11px] mono text-gray-400 hover:text-white');
        btn.className = 'speed-btn px-2 py-0.5 rounded text-[11px] mono bg-blue-600 text-white font-bold';
        playbackSpeed = parseFloat(btn.dataset.speed);
      }});
    }});

    // Initialize
    setMode(1);
    requestAnimationFrame(animate);
  </script>
</body>
</html>
'''

output_path = 'driving_rule_animations_suite/simulations/L05_T10_vehicle_lights.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 18 simulation built successfully at: {output_path}")
