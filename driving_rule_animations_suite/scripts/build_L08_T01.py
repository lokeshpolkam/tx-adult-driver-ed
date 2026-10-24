import os
import base64

def build_l08_t01():
    # Asset Paths
    bg_img_path = r"C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\texas_highway_corridor_isometric_1792731326478.jpg"
    car_red_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_red_clean_ne.png"
    car_yellow_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_yellow_clean_ne.png"
    car_blue_path = r"C:\tx_dmv\driving_rule_animations\asset_library\vehicles\car_blue_clean_ne.png"

    print("Encoding Lesson 29 assets to base64...")
    with open(car_red_path, "rb") as f:
        car_red_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_yellow_path, "rb") as f:
        car_yellow_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(car_blue_path, "rb") as f:
        car_blue_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    with open(bg_img_path, "rb") as f:
        bg_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

    print("Assets successfully encoded.")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>L08-T01: 7 Keys to Safe Driving &amp; SIPDE Cognitive Scan Cycle</title>
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
    @keyframes pulse-scan {{
      0%, 100% {{ opacity: 0.18; transform: scaleY(0.96); }}
      50% {{ opacity: 0.38; transform: scaleY(1.04); }}
    }}
    .scan-cone {{
      animation: pulse-scan 2.0s infinite ease-in-out;
      transform-origin: 460px 480px;
    }}
    @keyframes pulse-danger {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.95); }}
      50% {{ opacity: 0.9; transform: scale(1.05); }}
    }}
    .danger-pulse {{
      animation: pulse-danger 0.9s infinite ease-in-out;
    }}
    @keyframes radar-sweep {{
      0% {{ stroke-dashoffset: 60; }}
      100% {{ stroke-dashoffset: 0; }}
    }}
    .radar-flow {{
      stroke-dasharray: 6, 6;
      animation: radar-sweep 1.2s linear infinite;
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
          <span class="text-xs font-semibold text-gray-400 mono">LESSON 29</span>
        </div>
        <h1 class="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2">
          L08-T01: 7 Keys to Safe Driving &amp; SIPDE Cognitive Scan
        </h1>
        <p class="text-xs md:text-sm text-gray-400 mt-0.5">
          Proactive Risk Management &bull; Search &bull; Identify &bull; Predict &bull; Decide &bull; Execute (TTC &sect; 545.351 &amp; &sect; 545.401)
        </p>
      </div>

      <!-- SCENARIO MODE SELECTOR -->
      <div class="flex items-center gap-2 bg-[#0B0E14] p-1.5 rounded-xl border border-[#232C3D] flex-wrap">
        <button id="mode-1" data-mode="1" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-blue-500/40 bg-blue-600 text-white shadow-md shadow-blue-900/40">
          1: Proactive SIPDE Scan Cycle
        </button>
        <button id="mode-2" data-mode="2" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60">
          Hazard: Fixed Gaze "Tunnel Vision"
        </button>
        <button id="mode-3" data-mode="3" class="mode-btn px-3 py-1.5 rounded-lg text-xs font-bold transition border border-amber-500/30 bg-amber-950/40 text-amber-300 hover:bg-amber-900/60">
          Hazard: Boxed-In "No Escape" Trap
        </button>
        <label class="flex items-center gap-1.5 ml-2 text-xs text-gray-400 cursor-pointer mono">
          <input type="checkbox" id="auto-loop" checked class="rounded border-gray-700 bg-gray-900 text-blue-500 focus:ring-0">
          Auto-Loop
        </label>
      </div>
    </header>

    <!-- STEPPER NAVIGATION (MODE 1: SIPDE 4 PEDAGOGICAL STEPS) -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
      <button data-step="1" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-blue-400 mono">STEP 1</span>
          <span class="w-1.5 h-1.5 rounded-full bg-blue-400 step-dot"></span>
        </div>
        <p id="step-title-1" class="text-xs font-bold text-gray-200 mt-1 leading-snug">S — Search (12-15s Horizon)</p>
      </button>

      <button data-step="2" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 2</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p id="step-title-2" class="text-xs font-bold text-gray-400 mt-1 leading-snug">I &amp; P — Identify &amp; Predict</p>
      </button>

      <button data-step="3" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 3</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p id="step-title-3" class="text-xs font-bold text-gray-400 mt-1 leading-snug">D — Decide Space Cushion</p>
      </button>

      <button data-step="4" class="step-card group text-left p-2.5 rounded-xl border border-[#232C3D] bg-[#121722] hover:border-blue-500/50 transition">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-extrabold text-gray-500 mono">STEP 4</span>
          <span class="w-1.5 h-1.5 rounded-full bg-transparent step-dot"></span>
        </div>
        <p id="step-title-4" class="text-xs font-bold text-gray-400 mt-1 leading-snug">E — Execute 360&deg; Defense</p>
      </button>
    </div>

    <!-- MAIN SIMULATION CANVAS VIEWPORT -->
    <div id="simulation-container" class="relative w-full aspect-[16/10.5] max-h-[640px] bg-[#0E131E] rounded-2xl border border-[#232C3D] overflow-hidden shadow-2xl">

      <!-- ISOMETRIC 3-LANE TEXAS HIGHWAY BASE LAYER -->
      <img src="{bg_b64}" alt="Texas Highway 3-Lane Corridor" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none" />

      <!-- LAYER 1: SVG SPATIAL OVERLAYS (SIPDE CONES, TARGET RETICLES, ESCAPE CORRIDORS, HAZARDS) -->
      <svg id="sim-svg-layer" viewBox="0 0 1280 840" class="absolute inset-0 w-full h-full pointer-events-none select-none z-10">
        <defs>
          <!-- Gradient for 12-15s Scanning Radar Cone -->
          <linearGradient id="grad-scan-cone" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.35" />
            <stop offset="60%" stop-color="#10B981" stop-opacity="0.18" />
            <stop offset="100%" stop-color="#10B981" stop-opacity="0.0" />
          </linearGradient>

          <!-- Gradient for Tunnel Vision Narrow Cone -->
          <linearGradient id="grad-tunnel" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#EF4444" stop-opacity="0.5" />
            <stop offset="100%" stop-color="#EF4444" stop-opacity="0.05" />
          </linearGradient>

          <marker id="arrow-emerald" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#10B981" />
          </marker>
          <marker id="arrow-danger" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#EF4444" />
          </marker>
        </defs>

        <!-- FORWARD 12-15 SECOND COGNITIVE SCAN CONE (SEARCH STAGE) -->
        <g id="scan-cone-group" opacity="1.0">
          <polygon id="scan-cone-poly" points="460,480 820,180 990,320" fill="url(#grad-scan-cone)" stroke="#60A5FA" stroke-width="1.2" stroke-dasharray="5,4" class="scan-cone" />
          <line id="scan-axis" x1="460" y1="480" x2="905" y2="250" stroke="#34D399" stroke-width="1.8" class="radar-flow" />
          <g id="scan-badge" transform="translate(680, 360)">
            <rect x="-95" y="-10" width="190" height="20" rx="10" fill="#064E3B" stroke="#10B981" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#A7F3D0" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="800" text-anchor="middle">
              SEARCH: 12–15s VISUAL HORIZON
            </text>
          </g>
        </g>

        <!-- IDENTIFY & PREDICT TARGET RETICLE & CONFLICT VECTOR (STEP 2) -->
        <g id="identify-reticle-group" opacity="0.0">
          <circle id="threat-reticle" cx="820" cy="355" r="32" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-dasharray="6,4" class="danger-pulse" />
          <!-- Predicted swerve trajectory -->
          <path id="predicted-path" d="M 820,355 C 780,380 730,420 680,450" fill="none" stroke="#EF4444" stroke-width="2.2" stroke-dasharray="4,3" marker-end="url(#arrow-danger)" />
          <g id="threat-badge" transform="translate(820, 305)">
            <rect x="-90" y="-9" width="180" height="18" rx="9" fill="#451A03" stroke="#F59E0B" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">
              ⚠ PREDICT: LANE SWERVE HAZARD
            </text>
          </g>
        </g>

        <!-- 360-DEGREE SAFETY SPACE CUSHION / ESCAPE PATH ENVELOPE (DECIDE & EXECUTE) -->
        <g id="cushion-bubble-group" opacity="0.0">
          <!-- Dynamic safety bubble around Ego -->
          <ellipse id="safety-bubble" cx="460" cy="480" rx="95" ry="50" fill="#10B981" fill-opacity="0.14" stroke="#10B981" stroke-width="2" stroke-dasharray="6,4" />
          <!-- Designated Lateral Escape Route Arrow -->
          <path id="escape-arrow" d="M 460,480 L 360,400" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#arrow-emerald)" />
          <g id="escape-badge" transform="translate(360, 375)">
            <rect x="-85" y="-9" width="170" height="18" rx="9" fill="#064E3B" stroke="#10B981" stroke-width="1.2" />
            <text x="0" y="3.5" fill="#A7F3D0" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="900" text-anchor="middle">
              ✓ 360° ESCAPE ROUTE PRESERVED
            </text>
          </g>
        </g>

        <!-- MODE 2: FIXED GAZE "TUNNEL VISION" HAZARD OVERLAY -->
        <g id="tunnel-hazard-group" opacity="0.0">
          <!-- Very narrow 2-second tunnel cone straight ahead -->
          <polygon id="tunnel-poly" points="460,480 640,360 670,390" fill="url(#grad-tunnel)" stroke="#EF4444" stroke-width="1.8" />
          <circle cx="655" cy="375" r="28" fill="#EF4444" fill-opacity="0.25" stroke="#EF4444" stroke-width="2" class="danger-pulse" />
          <g id="tunnel-callout" transform="translate(655, 330)">
            <rect x="-105" y="-12" width="210" height="24" rx="12" fill="#450A0A" stroke="#EF4444" stroke-width="1.5" />
            <text x="0" y="3.5" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">
              💥 2-SEC TUNNEL GAZE: REACTION FAILURE!
            </text>
          </g>
        </g>

        <!-- MODE 3: BOXED-IN NO ESCAPE TRAP OVERLAY -->
        <g id="boxed-hazard-group" opacity="0.0">
          <!-- Red containment brackets surrounding Ego -->
          <rect id="boxed-rect" x="380" y="430" width="160" height="100" rx="8" fill="#7F1D1D" fill-opacity="0.2" stroke="#EF4444" stroke-width="2" stroke-dasharray="5,4" />
          <line x1="380" y1="430" x2="540" y2="530" stroke="#EF4444" stroke-width="1.5" />
          <line x1="380" y1="530" x2="540" y2="430" stroke="#EF4444" stroke-width="1.5" />
          <g id="boxed-callout" transform="translate(460, 410)">
            <rect x="-110" y="-12" width="220" height="24" rx="12" fill="#450A0A" stroke="#EF4444" stroke-width="1.5" />
            <text x="0" y="3.5" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">
              💥 ZERO ESCAPE PATH: BOXED ON ALL SIDES!
            </text>
          </g>
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- EGO DEFENSIVE VEHICLE (BURNT ORANGE SEDAN IN LANE 2) -->
      <div id="veh-ego" class="absolute z-21 pointer-events-none transition-transform" style="left: 36.0%; top: 56.6%; transform: translate(-50%, -50%);">
        <div id="veh-ego-sprite" class="relative w-20 aspect-[215/153] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
          
          <!-- Turn Signal Indicator (Left) -->
          <div id="blinker-left" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 28%; right: 28%;"></div>
          <!-- Brake Lights -->
          <div id="brake-lights" class="absolute w-3.5 h-1.5 rounded bg-red-500 filter blur-[1px] opacity-0" style="top: 65%; left: 8%;"></div>
        </div>

        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: 60 MPH • SCANNING 12–15s HORIZON
        </div>
      </div>

      <!-- LEAD VEHICLE (YELLOW SEDAN IN LANE 1 — POTENTIAL CONFLICT) -->
      <div id="veh-yellow" class="absolute z-20 pointer-events-none transition-transform" style="left: 64.0%; top: 42.5%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[215/153] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Lead Traffic" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
          <!-- Yellow Brake Lights -->
          <div id="yellow-brakes" class="absolute w-3.5 h-1.5 rounded bg-red-500 filter blur-[1px] opacity-0" style="top: 65%; left: 8%;"></div>
        </div>

        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          LEAD TRAFFIC: 50 MPH (LANE 1)
        </div>
      </div>

      <!-- PASSING VEHICLE (BLUE SEDAN IN LANE 3 — HIGH SPEED TRAFFIC) -->
      <div id="veh-blue" class="absolute z-19 pointer-events-none transition-transform" style="left: 70.0%; top: 8.4%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[215/153] flex items-center justify-center">
          <img src="{car_blue_b64}" alt="Passing Traffic" class="w-full h-full object-contain filter drop-shadow-[0_12px_12px_rgba(0,0,0,0.7)]" />
        </div>

        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/30 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          PASSING TRAFFIC: 70 MPH (LANE 3)
        </div>
      </div>

      <!-- LAYER 3: TELEMETRY HUD & CONTROL OVERLAYS -->

      <!-- TOP FLOATING STATUS PILL -->
      <div id="hud-status-pill" class="absolute top-4 left-72 z-30 pointer-events-none flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#0E131E]/90 border border-blue-500/40 backdrop-blur-md shadow-lg">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
        <span id="pill-status-text" class="text-xs font-bold text-blue-300 mono">
          SIPDE CYCLE: SEARCH 12–15s AHEAD • IDENTIFY HAZARDS • PREDICT MOVEMENT • PRESERVE ESCAPE CUSHION
        </span>
      </div>

      <!-- TELEMETRY HUD CARD (LEFT OVERLAY) -->
      <div id="telemetry-hud-card" class="absolute top-4 left-4 z-30 w-[270px] bg-[#0E131E]/95 border border-[#232C3D] rounded-xl p-3.5 backdrop-blur-md shadow-2xl flex flex-col gap-2.5">
        <div class="flex items-center justify-between border-b border-gray-800 pb-2">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-500"></span>
            <span class="text-xs font-extrabold text-white tracking-wider mono uppercase">SIPDE COGNITIVE HUD</span>
          </div>
          <span id="compliance-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">
            SEARCHING
          </span>
        </div>

        <div class="space-y-1.5 text-xs">
          <div class="flex justify-between items-center text-gray-400">
            <span>Scan Horizon:</span>
            <span id="telem-horizon" class="font-bold text-emerald-400 mono">12–15 SEC (1,000 FT)</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Following Buffer:</span>
            <span id="telem-buffer" class="font-bold text-emerald-400 mono">3.0s (180 FT)</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Threat Detection:</span>
            <span id="telem-threat" class="font-bold text-blue-400 mono">MONITORING FLOW</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Escape Route:</span>
            <span id="telem-escape" class="font-bold text-emerald-400 mono">360° OPEN CUSHION</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Ego Speed:</span>
            <span id="telem-speed" class="font-bold text-white mono">60 MPH (STEADY)</span>
          </div>
          <div class="flex justify-between items-center text-gray-400">
            <span>Crash Risk:</span>
            <span id="telem-risk" class="font-bold text-emerald-400 mono">MINIMAL (&lt; 5%)</span>
          </div>
        </div>

        <div class="border-t border-gray-800 pt-2">
          <p id="hud-narrative" class="text-[11px] text-gray-300 leading-relaxed">
            Step 1: Driver actively scans 12–15 seconds down the road rather than fixating on the car ahead. Constant visual scanning eliminates surprise hazards and allows ample processing time.
          </p>
        </div>
      </div>

      <!-- CRITICAL HAZARD CALLOUT BANNER -->
      <div id="hazard-banner" class="absolute top-4 left-1/2 -translate-x-1/2 z-30 max-w-md w-full px-4 py-2.5 rounded-xl bg-red-950/90 border border-red-500 text-center shadow-2xl transition-opacity duration-300 opacity-0 pointer-events-none">
        <div id="hazard-banner-title" class="text-xs font-black text-red-400 mono tracking-wider uppercase">
          CRITICAL HAZARD: FIXED GAZE "TUNNEL VISION"
        </div>
        <div id="hazard-banner-body" class="text-[11px] text-gray-200 mt-0.5 leading-snug">
          Fixating strictly on the car ahead reduces warning time from 15 seconds to under 2 seconds, causing violent panic stops and multi-car chain reactions.
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
    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const complianceBadge = document.getElementById('compliance-badge');
    const hazardBanner = document.getElementById('hazard-banner');
    const hazardBannerTitle = document.getElementById('hazard-banner-title');
    const hazardBannerBody = document.getElementById('hazard-banner-body');

    // Telemetry fields
    const telemHorizon = document.getElementById('telem-horizon');
    const telemBuffer = document.getElementById('telem-buffer');
    const telemThreat = document.getElementById('telem-threat');
    const telemEscape = document.getElementById('telem-escape');
    const telemSpeed = document.getElementById('telem-speed');
    const telemRisk = document.getElementById('telem-risk');
    const hudNarrative = document.getElementById('hud-narrative');

    // Vehicles
    const vehEgo = document.getElementById('veh-ego');
    const tagVehEgo = document.getElementById('tag-veh-ego');
    const blinkerLeft = document.getElementById('blinker-left');
    const brakeLights = document.getElementById('brake-lights');

    const vehYellow = document.getElementById('veh-yellow');
    const tagVehYellow = document.getElementById('tag-veh-yellow');
    const yellowBrakes = document.getElementById('yellow-brakes');

    const vehBlue = document.getElementById('veh-blue');
    const tagVehBlue = document.getElementById('tag-veh-blue');

    // SVG Overlays
    const scanConeGroup = document.getElementById('scan-cone-group');
    const identifyReticleGroup = document.getElementById('identify-reticle-group');
    const cushionBubbleGroup = document.getElementById('cushion-bubble-group');
    const tunnelHazardGroup = document.getElementById('tunnel-hazard-group');
    const boxedHazardGroup = document.getElementById('boxed-hazard-group');

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
        {{ time: 0.8, title: "S — Search (12-15s Horizon)" }},
        {{ time: 2.2, title: "I & P — Identify & Predict" }},
        {{ time: 3.6, title: "D — Decide Space Cushion" }},
        {{ time: 5.0, title: "E — Execute 360° Defense" }}
      ],
      2: [
        {{ time: 0.8, title: "Fixed 2-Sec Tunnel Stare" }},
        {{ time: 2.2, title: "Unseen Hazard Sudden Braking" }},
        {{ time: 3.6, title: "Delayed Panic Reaction" }},
        {{ time: 5.0, title: "High-Speed Rear-End Crash" }}
      ],
      3: [
        {{ time: 0.8, title: "Cruising in Blind Spot Pocket" }},
        {{ time: 2.2, title: "Surrounded by Adjacent Flow" }},
        {{ time: 3.6, title: "Road Hazard Closes Live Lane" }},
        {{ time: 5.0, title: "Zero Escape Route Collision" }}
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

      // =========================================================================
      // MODE 1: PROACTIVE SIPDE SCAN CYCLE & CUSHION DEFENSE
      // =========================================================================
      if (currentMode === 1) {{
        tunnelHazardGroup.setAttribute('opacity', '0.0');
        boxedHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        hudStatusPill.style.opacity = '1.0';

        // Background Traffic:
        // Blue car in Lane 3 cruises past up-road
        const blueX = 52.0 + (t / duration) * 6.0; // 52% to 58% in Lane 3
        const blueY = getLane3Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/30 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider";
        tagVehBlue.textContent = 'PASSING TRAFFIC: 70 MPH (LANE 3)';

        // Yellow car in Lane 1 ahead
        const yellowX = 62.0 + (t / duration) * 4.0; // 62% to 66%
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider";
        tagVehYellow.textContent = 'LEAD TRAFFIC: 50 MPH (LANE 1)';

        let egoX, egoY, egoSpeed;

        if (t < 1.6) {{
          // Step 1: SEARCH (12-15s visual horizon scanning)
          const p = t / 1.6;
          egoX = 35.0 + p * 3.0; // 35% to 38% in Lane 2
          egoY = getLane2Y(egoX);
          egoSpeed = 60;

          blinkerLeft.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          yellowBrakes.style.opacity = '0.0';

          scanConeGroup.setAttribute('opacity', '1.0');
          identifyReticleGroup.setAttribute('opacity', '0.0');
          cushionBubbleGroup.setAttribute('opacity', '0.0');

          // Scanning cone extends from Ego front
          const egoFrontX = egoX * 12.8 + 25;
          const egoFrontY = egoY * 8.4 - 10;
          document.getElementById('scan-cone-poly').setAttribute('points', `${{egoFrontX}},${{egoFrontY}} ${{egoFrontX + 380}},${{egoFrontY - 260}} ${{egoFrontX + 540}},${{egoFrontY - 140}}`);
          document.getElementById('scan-axis').setAttribute('x1', `${{egoFrontX}}`);
          document.getElementById('scan-axis').setAttribute('y1', `${{egoFrontY}}`);
          document.getElementById('scan-axis').setAttribute('x2', `${{egoFrontX + 460}}`);
          document.getElementById('scan-axis').setAttribute('y2', `${{egoFrontY - 200}}`);
          document.getElementById('scan-badge').setAttribute('transform', `translate(${{egoFrontX + 160}}, ${{egoFrontY - 140}})`);

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: 60 MPH • SCANNING 12–15s HORIZON';

          telemHorizon.textContent = '12–15 SEC (1,000 FT)';
          telemBuffer.textContent = '3.0s (180 FT)';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemThreat.textContent = 'MONITORING ROADWAY';
          telemThreat.className = 'font-bold text-blue-400 mono text-right';
          telemEscape.textContent = '360° OPEN CUSHION';
          telemSpeed.textContent = '60 MPH (STEADY)';
          telemRisk.textContent = 'MINIMAL (< 5%)';
          telemRisk.className = 'font-bold text-emerald-400 mono text-right';

          complianceBadge.textContent = 'SEARCHING';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 1 (Search): Driver keeps eyes moving and scans 12–15 seconds down the roadway corridor. Constant visual sweeps across all quadrants detect emerging hazards early.';
        }} else if (t < 3.0) {{
          // Step 2: IDENTIFY & PREDICT (detect yellow brake lights & predict swerve)
          const p = (t - 1.6) / 1.4;
          egoX = 38.0 + p * 3.0; // 38% to 41% in Lane 2
          egoY = getLane2Y(egoX);
          egoSpeed = 58;

          blinkerLeft.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          yellowBrakes.style.opacity = '1.0'; // Lead vehicle taps brakes!

          scanConeGroup.setAttribute('opacity', '0.0');
          identifyReticleGroup.setAttribute('opacity', '1.0');
          cushionBubbleGroup.setAttribute('opacity', '0.0');

          const yelCx = yellowX * 12.8;
          const yelCy = yellowY * 8.4;
          document.getElementById('threat-reticle').setAttribute('cx', `${{yelCx}}`);
          document.getElementById('threat-reticle').setAttribute('cy', `${{yelCy}}`);
          document.getElementById('threat-badge').setAttribute('transform', `translate(${{yelCx}}, ${{yelCy - 70}})`);
          document.getElementById('predicted-path').setAttribute('d', `M ${{yelCx}},${{yelCy}} C ${{yelCx - 40}},${{yelCy + 25}} ${{yelCx - 90}},${{yelCy + 60}} ${{yelCx - 140}},${{yelCy + 90}}`);

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: IDENTIFIES THREAT • PREDICTS SWERVE';

          tagVehYellow.textContent = 'LEAD TRAFFIC: BRAKE ON • SWERVE RISK';

          telemHorizon.textContent = 'HAZARD PINPOINTED';
          telemBuffer.textContent = '3.5s (EXPANDING)';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemThreat.textContent = 'SLOWER VEHICLE BRAKING';
          telemThreat.className = 'font-bold text-amber-400 mono text-right';
          telemEscape.textContent = 'IDENTIFYING EXITS';
          telemSpeed.textContent = '58 MPH (EASING OFF)';
          telemRisk.textContent = 'MODERATE (PREDICTED)';
          telemRisk.className = 'font-bold text-amber-400 mono text-right';

          complianceBadge.textContent = 'IDENTIFIED';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
          hudNarrative.textContent = 'Step 2 (Identify & Predict): Driver spots brake lights ahead in Lane 1. Predicts the driver may swerve into Lane 2. Driver anticipates potential conflict before it materializes.';
        }} else if (t < 4.4) {{
          // Step 3: DECIDE (calculate space cushion & select escape route)
          const p = (t - 3.0) / 1.4;
          egoX = 41.0 + p * 2.0; // 41% to 43% in Lane 2
          egoY = getLane2Y(egoX);
          egoSpeed = 54;

          blinkerLeft.style.opacity = '0.0';
          brakeLights.style.opacity = '0.6'; // smooth deceleration
          yellowBrakes.style.opacity = '1.0';

          scanConeGroup.setAttribute('opacity', '0.0');
          identifyReticleGroup.setAttribute('opacity', '0.6');
          cushionBubbleGroup.setAttribute('opacity', '1.0');

          const egoCx = egoX * 12.8;
          const egoCy = egoY * 8.4;
          document.getElementById('safety-bubble').setAttribute('cx', `${{egoCx}}`);
          document.getElementById('safety-bubble').setAttribute('cy', `${{egoCy}}`);
          document.getElementById('escape-arrow').setAttribute('d', `M ${{egoCx}},${{egoCy}} L ${{egoCx - 100}},${{egoCy - 80}}`);
          document.getElementById('escape-badge').setAttribute('transform', `translate(${{egoCx - 100}}, ${{egoCy - 110}})`);

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: DECIDES TO HOLD 4-SEC BUFFER & ESCAPE';

          telemHorizon.textContent = 'CUSHION EXPANDED';
          telemBuffer.textContent = '4.2s (250+ FT)';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemThreat.textContent = 'DEFUSED BY BUFFER';
          telemThreat.className = 'font-bold text-emerald-400 mono text-right';
          telemEscape.textContent = 'LANE 3 CORRIDOR OPEN';
          telemSpeed.textContent = '54 MPH (DECELERATING)';
          telemRisk.textContent = 'LOW (BUFFERED)';
          telemRisk.className = 'font-bold text-emerald-400 mono text-right';

          complianceBadge.textContent = 'DECIDED';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
          hudNarrative.textContent = 'Step 3 (Decide): Rather than rushing forward into a squeeze, driver decides to ease off the accelerator, expanding buffer to 4+ seconds and maintaining an open escape path to the left.';
        }} else {{
          // Step 4: EXECUTE (360-degree defense executed, threat neutralized)
          const p = (t - 4.4) / 0.6;
          egoX = 43.0 + p * 2.0; // 43% to 45% in Lane 2
          egoY = getLane2Y(egoX);
          egoSpeed = 52;

          blinkerLeft.style.opacity = '0.0';
          brakeLights.style.opacity = '0.0';
          yellowBrakes.style.opacity = '0.0';

          scanConeGroup.setAttribute('opacity', '0.0');
          identifyReticleGroup.setAttribute('opacity', '0.0');
          cushionBubbleGroup.setAttribute('opacity', '1.0');

          const egoCx = egoX * 12.8;
          const egoCy = egoY * 8.4;
          document.getElementById('safety-bubble').setAttribute('cx', `${{egoCx}}`);
          document.getElementById('safety-bubble').setAttribute('cy', `${{egoCy}}`);
          document.getElementById('escape-arrow').setAttribute('d', `M ${{egoCx}},${{egoCy}} L ${{egoCx - 100}},${{egoCy - 80}}`);
          document.getElementById('escape-badge').setAttribute('transform', `translate(${{egoCx - 100}}, ${{egoCy - 110}})`);

          tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider";
          tagVehEgo.textContent = 'EGO: 360° SPACE CUSHION PRESERVED';

          telemHorizon.textContent = 'CYCLE RESTARTS';
          telemBuffer.textContent = '4.5s (SAFE CUSHION)';
          telemBuffer.className = 'font-bold text-emerald-400 mono text-right';
          telemThreat.textContent = 'CLEAR OF HAZARD';
          telemThreat.className = 'font-bold text-emerald-400 mono text-right';
          telemEscape.textContent = 'PERIMETER SECURE';
          telemSpeed.textContent = '52 MPH (CONTROLLED)';
          telemRisk.textContent = 'ZERO (< 1%)';
          telemRisk.className = 'font-bold text-emerald-400 mono text-right';

          complianceBadge.textContent = 'EXECUTED';
          complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500 text-black mono';
          hudNarrative.textContent = 'Step 4 (Execute): Execution complete without abrupt panic braking or swerving. The 360-degree perimeter cushion remains fully intact. SIPDE scan cycle continuously loops.';
        }}

        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        pillStatusText.textContent = 'SIPDE CYCLE: SEARCH 12–15s AHEAD • IDENTIFY HAZARDS • PREDICT MOVEMENT • PRESERVE ESCAPE CUSHION';
      }}

      // =========================================================================
      // MODE 2: CRITICAL HAZARD: FIXED GAZE "TUNNEL VISION" FAILURE
      // =========================================================================
      else if (currentMode === 2) {{
        scanConeGroup.setAttribute('opacity', '0.0');
        identifyReticleGroup.setAttribute('opacity', '0.0');
        cushionBubbleGroup.setAttribute('opacity', '0.0');
        tunnelHazardGroup.setAttribute('opacity', '1.0');
        boxedHazardGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '1.0';
        hudStatusPill.style.opacity = '0.0';
        blinkerLeft.style.opacity = '0.0';
        yellowBrakes.style.opacity = '1.0';

        hazardBannerTitle.textContent = 'CRITICAL HAZARD: FIXED GAZE "TUNNEL VISION"';
        hazardBannerBody.innerHTML = "<strong>FAILURE TO SCAN 12–15 SECONDS AHEAD (TTC § 545.351)</strong><br>Staring solely at the bumper ahead cuts warning time to &lt; 2.0 seconds, causing late panic braking and severe multi-car rear-end collisions.";

        // Yellow car slams brakes directly in Lane 2 at x = 54%
        const yellowX = 54.0;
        const yellowY = getLane2Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[9px] font-bold text-amber-300 mono shadow-xl tracking-wider";
        tagVehYellow.textContent = 'LEAD CAR: ABRUPT EMERGENCY BRAKE!';

        // Ego tailgating with tunnel vision behind Yellow at x = 46%
        const egoX = 46.0;
        const egoY = getLane2Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;
        brakeLights.style.opacity = '1.0';

        tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
        tagVehEgo.textContent = 'EGO: FIXED GAZE • LATE PANIC BRAKE!';

        // Blue car distant in Lane 3
        const blueX = 58.0;
        const blueY = getLane3Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/30 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider";
        tagVehBlue.textContent = 'LANE 3 TRAFFIC: 70 MPH';

        // Tunnel poly connecting Ego to Yellow
        const egoCx = egoX * 12.8;
        const egoCy = egoY * 8.4;
        const yelCx = yellowX * 12.8;
        const yelCy = yellowY * 8.4;
        document.getElementById('tunnel-poly').setAttribute('points', `${{egoCx}},${{egoCy}} ${{yelCx - 20}},${{yelCy - 20}} ${{yelCx + 20}},${{yelCy + 20}}`);
        document.getElementById('tunnel-callout').setAttribute('transform', `translate(${{(egoCx + yelCx)/2}}, ${{egoCy - 60}})`);

        telemHorizon.textContent = '< 2 SEC (TUNNEL GAZE)';
        telemHorizon.className = 'font-bold text-red-500 mono text-right';
        telemBuffer.textContent = '< 1.0s (CRITICAL DEFICIT)';
        telemBuffer.className = 'font-bold text-red-500 mono text-right';
        telemThreat.textContent = 'UNPERCEIVED SUDDEN STOP';
        telemThreat.className = 'font-bold text-red-500 mono text-right';
        telemEscape.textContent = 'TRAPPED IN LANE';
        telemEscape.className = 'font-bold text-red-500 mono text-right';
        telemSpeed.textContent = '0 MPH (COLLISION)';
        telemRisk.textContent = '100% (REAR-END IMPACT)';
        telemRisk.className = 'font-bold text-red-500 mono text-right';

        complianceBadge.textContent = 'PANIC CRASH';
        complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
        pillStatusText.textContent = 'CRITICAL ERROR: FIXED GAZE ON IMMEDIATE BUMPER DESTROYS REACTION HORIZON!';
        hudNarrative.textContent = 'Catastrophic Error: Driver stares only at the lead bumper. Lacking a 12–15 second forward horizon, the driver fails to perceive braking down-road until under 2 seconds remain, causing an unavoidable high-speed crash.';
      }}

      // =========================================================================
      // MODE 3: CRITICAL HAZARD: BOXED-IN "NO ESCAPE ROUTE" TRAP
      // =========================================================================
      else if (currentMode === 3) {{
        scanConeGroup.setAttribute('opacity', '0.0');
        identifyReticleGroup.setAttribute('opacity', '0.0');
        cushionBubbleGroup.setAttribute('opacity', '0.0');
        tunnelHazardGroup.setAttribute('opacity', '0.0');
        boxedHazardGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';
        hudStatusPill.style.opacity = '0.0';
        blinkerLeft.style.opacity = '0.0';
        yellowBrakes.style.opacity = '0.0';
        brakeLights.style.opacity = '1.0';

        hazardBannerTitle.textContent = 'CRITICAL HAZARD: BOXED-IN WITH NO ESCAPE PATH';
        hazardBannerBody.innerHTML = "<strong>FAILURE TO MAINTAIN 360° SPACE CUSHIONS (TTC § 545.062)</strong><br>Driving alongside adjacent vehicles in their blind spots leaves zero lateral escape paths when roadway emergencies strike.";

        // Ego in Lane 2 at x = 50%
        const egoX = 50.0;
        const egoY = getLane2Y(egoX);
        vehEgo.style.left = `${{egoX}}%`;
        vehEgo.style.top = `${{egoY}}%`;

        tagVehEgo.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-red-500/50 text-[9px] font-bold text-red-300 mono shadow-xl tracking-wider";
        tagVehEgo.textContent = 'EGO: 0 ESCAPE ROUTES (BOXED IN)!';

        // Yellow car matching speed alongside in Lane 1 at x = 51%
        const yellowX = 51.0;
        const yellowY = getLane1Y(yellowX);
        vehYellow.style.left = `${{yellowX}}%`;
        vehYellow.style.top = `${{yellowY}}%`;
        tagVehYellow.className = "absolute left-1/2 -translate-x-1/2 top-full mt-2.5 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9px] font-bold text-amber-300 mono shadow-lg tracking-wider";
        tagVehYellow.textContent = 'BLOCKING RIGHT (LANE 1)';

        // Blue car matching speed alongside in Lane 3 at x = 49%
        const blueX = 49.0;
        const blueY = getLane3Y(blueX);
        vehBlue.style.left = `${{blueX}}%`;
        vehBlue.style.top = `${{blueY}}%`;
        tagVehBlue.className = "absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9px] font-bold text-blue-300 mono shadow-lg tracking-wider";
        tagVehBlue.textContent = 'BLOCKING LEFT (LANE 3)';

        const egoCx = egoX * 12.8;
        const egoCy = egoY * 8.4;
        document.getElementById('boxed-rect').setAttribute('x', `${{egoCx - 75}}`);
        document.getElementById('boxed-rect').setAttribute('y', `${{egoCy - 45}}`);
        document.getElementById('boxed-callout').setAttribute('transform', `translate(${{egoCx - 20}}, ${{egoCy - 85}})`);

        telemHorizon.textContent = 'OBSCURED BY TRAFFIC';
        telemHorizon.className = 'font-bold text-amber-400 mono text-right';
        telemBuffer.textContent = '0 LATERAL CLEARANCE';
        telemBuffer.className = 'font-bold text-red-500 mono text-right';
        telemThreat.textContent = 'SURROUNDED BY TRAFFIC';
        telemThreat.className = 'font-bold text-red-500 mono text-right';
        telemEscape.textContent = '0 ESCAPE PATHS';
        telemEscape.className = 'font-bold text-red-500 mono text-right';
        telemSpeed.textContent = '65 MPH (TRAPPED)';
        telemRisk.textContent = 'CRITICAL (BOXED IN)';
        telemRisk.className = 'font-bold text-red-500 mono text-right';

        complianceBadge.textContent = 'ENTRAPPED';
        complianceBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-600 text-white mono';
        pillStatusText.textContent = 'CRITICAL ERROR: NEVER RIDE ALONGSIDE VEHICLES IN TRAFFIC PACKS! ADJUST SPEED FOR ESCAPE BUFFER.';
        hudNarrative.textContent = 'High-Risk Error: Driver cruises directly between two vehicles in adjacent lanes, surrendering all lateral escape cushions. If any vehicle swerves or blows a tire, a multi-car chain-reaction collision is guaranteed.';
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

    output_path = os.path.abspath("driving_rule_animations_suite/simulations/L08_T01_sipde_scan_cycle.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Lesson 29 simulation built successfully at: {output_path}")

if __name__ == '__main__':
    build_l08_t01()
