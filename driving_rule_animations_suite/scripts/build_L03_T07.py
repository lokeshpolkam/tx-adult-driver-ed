import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/uncontrolled_intersection_final.png'
car_red_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_blue_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_nw.png'

print("Encoding assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_b64 = get_base64_img(car_red_path)
car_blue_b64 = get_base64_img(car_blue_path)
print("Assets encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en" class="h-full bg-[#0B0E11] text-[#ECEFF1] antialiased">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Lesson L03-T07: Defensive Driving — Quadrant Scanning on Green Light (TTC § 544.007b)</title>
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

    @keyframes sweepCone {{
      0%, 100% {{ opacity: 0.85; }}
      50% {{ opacity: 0.65; }}
    }}
    .sweep-glow {{
      animation: sweepCone 1.8s infinite ease-in-out;
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
        <p class="text-[11px] text-gray-400">Lesson L03–T07: Defensive Driving — Quadrant Scanning on Green Light (Texas Transportation Code § 544.007b)</p>
      </div>
    </div>

    <!-- DUAL SCENARIO TOGGLE -->
    <div class="flex items-center space-x-3">
      <div class="flex items-center rounded-lg bg-[#19202B] p-0.5 border border-[#2B3545]">
        <button id="scenario-btn-primary" class="scenario-toggle-btn px-3 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1.5 bg-emerald-500 text-black shadow">
          <span>Primary: 4-Quadrant Scan (§ 544.007b)</span>
        </button>
        <button id="scenario-btn-hazard" class="scenario-toggle-btn px-3 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1.5">
          <span>Hazard Demo: Blind Green Launch</span>
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
        Step 1: Fresh Green &amp; Defensive Hold
      </button>
      <button class="step-btn px-3 py-1 rounded-md text-xs font-semibold bg-[#212732] border border-[#2F3746] text-gray-300 hover:text-white hover:bg-[#2B3342] transition" data-step="2" data-time="2.5">
        Step 2: 4-Quadrant Visual Sweep
      </button>
      <button class="step-btn px-3 py-1 rounded-md text-xs font-semibold bg-[#212732] border border-[#2F3746] text-gray-300 hover:text-white hover:bg-[#2B3342] transition" data-step="3" data-time="4.2">
        Step 3: Red-Light Runner Hazard Evasion
      </button>
      <button class="step-btn px-3 py-1 rounded-md text-xs font-semibold bg-[#212732] border border-[#2F3746] text-gray-300 hover:text-white hover:bg-[#2B3342] transition" data-step="4" data-time="6.5">
        Step 4: Clearance &amp; Lawful Entry
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

        <!-- LAYER 1: DYNAMIC SVG OVERLAYS (Traffic Lights, Vision Cones, Conflict Zone) -->
        <svg id="stage-svg" viewBox="0 0 1024 667" class="absolute inset-0 w-full h-full pointer-events-none z-10">
          <defs>
            <!-- Glowing Red Filter -->
            <filter id="glow-red" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <!-- Glowing Green Filter -->
            <filter id="glow-green" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <!-- Glowing Yellow Filter -->
            <filter id="glow-yellow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            
            <!-- Cyan Vision Cone Gradient -->
            <radialGradient id="cone-cyan-grad" cx="0%" cy="50%" r="100%" fx="0%" fy="50%">
              <stop offset="0%" stop-color="#06B6D4" stop-opacity="0.8" />
              <stop offset="40%" stop-color="#06B6D4" stop-opacity="0.35" />
              <stop offset="100%" stop-color="#06B6D4" stop-opacity="0.0" />
            </radialGradient>

            <!-- Threat Vision Cone Gradient (Amber/Red) -->
            <radialGradient id="cone-threat-grad" cx="0%" cy="50%" r="100%" fx="0%" fy="50%">
              <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.9" />
              <stop offset="40%" stop-color="#EF4444" stop-opacity="0.45" />
              <stop offset="100%" stop-color="#EF4444" stop-opacity="0.0" />
            </radialGradient>
          </defs>

          <!-- ADVANCE STOP LINE & CROSSWALK ACCENTUATIONS -->
          <!-- SW Stop Line (Vehicle A) -->
          <line x1="322" y1="510" x2="394" y2="470" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.9" />
          <!-- SE Stop Line (Vehicle B Approach) -->
          <line x1="630" y1="470" x2="702" y2="510" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.9" />

          <!-- TRAFFIC SIGNAL 1: SW Approach (Controls Vehicle A) at x=303, y=496 -->
          <g id="signal-sw-housing" transform="translate(303, 496)">
            <!-- Red Lens (Top) -->
            <circle id="sw-lens-red" cx="0" cy="-12" r="5" fill="#EF4444" filter="url(#glow-red)" />
            <!-- Yellow Lens (Middle) -->
            <circle id="sw-lens-yellow" cx="0" cy="0" r="5" fill="#374151" opacity="0.4" />
            <!-- Green Lens (Bottom) -->
            <circle id="sw-lens-green" cx="0" cy="12" r="5" fill="#10B981" filter="url(#glow-green)" opacity="0.2" />
          </g>

          <!-- TRAFFIC SIGNAL 2: SE Approach (Controls Cross-Street / Vehicle B) at x=699, y=496 -->
          <g id="signal-se-housing" transform="translate(699, 496)">
            <!-- Red Lens (Top) -->
            <circle id="se-lens-red" cx="0" cy="-12" r="5" fill="#EF4444" filter="url(#glow-red)" opacity="0.2" />
            <!-- Yellow Lens (Middle) -->
            <circle id="se-lens-yellow" cx="0" cy="0" r="5" fill="#F59E0B" filter="url(#glow-yellow)" opacity="0.3" />
            <!-- Green Lens (Bottom) -->
            <circle id="se-lens-green" cx="0" cy="12" r="5" fill="#10B981" filter="url(#glow-green)" opacity="0.2" />
          </g>

          <!-- TRAFFIC SIGNAL 3: NW Corner (Facing Inbound) at x=297, y=184 -->
          <g id="signal-nw-housing" transform="translate(297, 184)">
            <circle id="nw-lens-red" cx="0" cy="-10" r="4.5" fill="#EF4444" filter="url(#glow-red)" opacity="0.3" />
            <circle id="nw-lens-green" cx="0" cy="10" r="4.5" fill="#10B981" filter="url(#glow-green)" opacity="0.2" />
          </g>

          <!-- DYNAMIC VISION SCANNING CONE (Anchored to Vehicle A Windshield: 345, 475) -->
          <g id="vision-cone-group" opacity="0.0">
            <!-- Sweep Cone Polygon / Path -->
            <path id="vision-cone-path" d="M 345 475 L 180 340 A 240 240 0 0 1 270 290 Z" fill="url(#cone-cyan-grad)" stroke="#06B6D4" stroke-width="1.5" stroke-dasharray="4,3" class="sweep-glow" />
            <!-- Focus Reticle Center Ray -->
            <line id="vision-ray-line" x1="345" y1="475" x2="225" y2="315" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
            <circle id="vision-ray-target" cx="225" cy="315" r="7" fill="#0284C7" fill-opacity="0.4" stroke="#38BDF8" stroke-width="1.8" />
          </g>

          <!-- HAZARD DEMO: T-BONE IMPACT CONFLICT ZONE (Center Box: 505, 395) -->
          <g id="hazard-collision-zone" opacity="0.0">
            <!-- Pulsing Crash Radial Circles -->
            <circle cx="505" cy="395" r="55" fill="#EF4444" fill-opacity="0.22" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" class="pulse-danger" />
            <circle cx="505" cy="395" r="30" fill="#DC2626" fill-opacity="0.4" stroke="#FCA5A5" stroke-width="2" />
            <!-- Impact Crosshairs -->
            <line x1="440" y1="395" x2="570" y2="395" stroke="#EF4444" stroke-width="2.5" />
            <line x1="505" y1="330" x2="505" y2="460" stroke="#EF4444" stroke-width="2.5" />
            <!-- Impact Explosion Symbol -->
            <polygon points="505,370 515,388 535,385 520,400 530,420 505,408 480,420 490,400 475,385 495,388" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
          </g>

          <!-- RED-LIGHT RUNNER THREAT DETECTION RETICLE -->
          <g id="threat-reticle" opacity="0.0">
            <circle id="threat-circle" cx="0" cy="0" r="38" fill="none" stroke="#EF4444" stroke-width="2" stroke-dasharray="5,3" class="pulse-danger" />
            <line id="threat-l1" x1="-48" y1="0" x2="-28" y2="0" stroke="#EF4444" stroke-width="2" />
            <line id="threat-l2" x1="28" y1="0" x2="48" y2="0" stroke="#EF4444" stroke-width="2" />
            <line id="threat-l3" x1="0" y1="-48" x2="0" y2="-28" stroke="#EF4444" stroke-width="2" />
            <line id="threat-l4" x1="0" y1="28" x2="0" y2="48" stroke="#EF4444" stroke-width="2" />
          </g>
        </svg>

        <!-- LAYER 2: VEHICLE SPRITES & DYNAMIC METADATA BADGES -->
        
        <!-- VEHICLE A (Ego Sedan - Red, Heading NE) -->
        <div id="veh-a-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 34.0%; top: 72.0%; transform: translate(-50%, -50%);">
          <!-- Vehicle Sprite Image -->
          <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
            <img src="{car_red_b64}" alt="Vehicle A" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
            
            <!-- Left & Right Glowing Brake Taillights -->
            <div id="veh-a-brake-left" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-100" style="bottom: 18%; left: 16%;"></div>
            <div id="veh-a-brake-right" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-100" style="bottom: 27%; left: 30%;"></div>
          </div>

          <!-- Non-overlapping Identification Badge below vehicle -->
          <div id="tag-veh-a" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
            VEHICLE A (DEFENSIVE HOLD)
          </div>
        </div>

        <!-- VEHICLE B (Cross Traffic - Blue Sedan, Heading NW) -->
        <div id="veh-b-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 82.0%; top: 82.0%; transform: translate(-50%, -50%); opacity: 0;">
          <!-- Vehicle Sprite Image -->
          <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
            <img src="{car_blue_b64}" alt="Vehicle B" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          </div>

          <!-- Non-overlapping Identification Badge above vehicle -->
          <div id="tag-veh-b" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#1B1114]/90 border border-red-500/50 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider">
            VEHICLE B (RED-LIGHT RUNNER)
          </div>
        </div>

        <!-- QUADRANT SCAN HUD PILL (Positioned clearly above scan cone without overlapping vehicle tags) -->
        <div id="hud-scan-pill" class="absolute z-25 px-3 py-1 rounded-full bg-[#032B30]/90 border border-cyan-400 text-cyan-200 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none" style="left: 20%; top: 44%; opacity: 0.0; transform: translate(-50%, -50%);">
          QUADRANT 1: SCAN LEFT
        </div>

        <!-- HAZARD DEMO VIOLATION BANNER -->
        <div id="hazard-banner" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-30 px-5 py-2 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-1 pointer-events-none transition-opacity duration-300" style="opacity: 0.0;">
          <div class="text-xs font-black tracking-widest text-red-400 flex items-center justify-center space-x-1.5">
            <span>✕ CRITICAL HAZARD: FATAL T-BONE SIDE-IMPACT CRASH ✕</span>
          </div>
          <div class="text-[11px] font-semibold text-gray-200">
            TTC § 544.007(b) Mandate: Facing a green signal does NOT grant blind entry. You must clear all quadrants!
          </div>
        </div>

        <!-- LAYER 3: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
        <div class="absolute top-2.5 left-2.5 z-30 max-w-[340px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-3 space-y-2 shadow-xl pointer-events-none">
          <div class="flex items-center justify-between border-b border-[#222B38] pb-1.5">
            <span class="text-[10px] font-bold text-gray-400 mono uppercase tracking-wider">Telemetry &amp; Scan Phase</span>
            <span id="signal-state-badge" class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">
              SIGNAL: GREEN
            </span>
          </div>

          <div class="space-y-1 text-xs mono">
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Vehicle A (Ego):</span>
              <span id="telem-veh-a" class="text-emerald-400 font-bold">0 MPH (DEFENSIVE HOLD)</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Vehicle B (Cross):</span>
              <span id="telem-veh-b" class="text-blue-400 font-bold">APPROACHING</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Visual Sweep:</span>
              <span id="telem-scan" class="text-cyan-400 font-bold">INITIAL GREEN PAUSE</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-400">Legal Mandate:</span>
              <span id="telem-statute" class="text-amber-300 font-bold">TTC § 544.007(b) CLEARANCE</span>
            </div>
          </div>

          <div class="pt-1.5 border-t border-[#1F2633] text-[11px] text-gray-300 leading-relaxed font-sans" id="hud-narrative">
            Vehicle A faces fresh green signal. Rather than immediately accelerating, the driver holds brake to sweep intersection quadrants for red-light runners.
          </div>
        </div>

        <!-- ON-STAGE STATUTORY BADGE (Bottom-Right) -->
        <div class="absolute bottom-2.5 right-2.5 z-30 flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-[#0F131A]/90 border border-[#2B3545] text-[10px] mono text-emerald-400 font-semibold shadow-lg pointer-events-none">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span id="compliance-text">TTC § 544.007(b) DEFENSIVE COMPLIANCE VERIFIED</span>
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
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400"></span><span>1.0s Green Light</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-cyan-400"></span><span>1.5s–3.5s 4-Quadrant Scan</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-red-400"></span><span>4.0s Red-Light Runner Passes</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-purple-400"></span><span>5.5s Safe Acceleration</span></span>
      </div>
      <div class="text-[10px] text-gray-400">
        TDLR ADE-1317: Right-of-Way Anticipation Protocol
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

    // Modes: 'primary' (defensive scan) vs 'hazard' (blind green launch)
    let simulationMode = 'primary';

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
    const btnPrimary = document.getElementById('scenario-btn-primary');
    const btnHazard = document.getElementById('scenario-btn-hazard');

    // Sprites & Tags
    const vehA = document.getElementById('veh-a-container');
    const vehB = document.getElementById('veh-b-container');
    const tagVehA = document.getElementById('tag-veh-a');
    const tagVehB = document.getElementById('tag-veh-b');
    const brakeA1 = document.getElementById('veh-a-brake-left');
    const brakeA2 = document.getElementById('veh-a-brake-right');

    // SVG elements
    const swLensRed = document.getElementById('sw-lens-red');
    const swLensYellow = document.getElementById('sw-lens-yellow');
    const swLensGreen = document.getElementById('sw-lens-green');

    const seLensRed = document.getElementById('se-lens-red');
    const seLensYellow = document.getElementById('se-lens-yellow');
    const seLensGreen = document.getElementById('se-lens-green');

    const nwLensRed = document.getElementById('nw-lens-red');
    const nwLensGreen = document.getElementById('nw-lens-green');

    const visionConeGroup = document.getElementById('vision-cone-group');
    const visionConePath = document.getElementById('vision-cone-path');
    const visionRayLine = document.getElementById('vision-ray-line');
    const visionRayTarget = document.getElementById('vision-ray-target');

    const hudScanPill = document.getElementById('hud-scan-pill');
    const hazardCollisionZone = document.getElementById('hazard-collision-zone');
    const hazardBanner = document.getElementById('hazard-banner');
    const threatReticle = document.getElementById('threat-reticle');
    const threatCircle = document.getElementById('threat-circle');

    // Telemetry DOM
    const telemVehA = document.getElementById('telem-veh-a');
    const telemVehB = document.getElementById('telem-veh-b');
    const telemScan = document.getElementById('telem-scan');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const complianceText = document.getElementById('compliance-text');

    // Canonical Stepper timestamps
    const stepTimes = [0.5, 2.5, 4.2, 6.5];
    let currentStepIdx = 0;

    // Helper Math Functions
    function easeOutQuad(x) {{ return 1 - (1 - x) * (1 - x); }}
    function easeInOutQuad(x) {{ return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }}

    // =========================================================================
    // UPDATE SIMULATION (Core Deterministic State at time t)
    // =========================================================================
    function updateSimulation(t) {{
      scrubber.value = t;
      timeDisplay.textContent = t.toFixed(2) + 's';

      // 1. Stepper active pill update
      let activeStep = 0;
      if (t < 1.6) activeStep = 0;
      else if (t < 3.6) activeStep = 1;
      else if (t < 5.2) activeStep = 2;
      else activeStep = 3;

      currentStepIdx = activeStep;
      stepIndicator.textContent = `Step ${{activeStep + 1}} of 4`;
      stepBtns.forEach((btn, idx) => {{
        if (idx === activeStep) btn.classList.add('active');
        else btn.classList.remove('active');
      }});

      // 2. Traffic Signal Logic
      // Ego direction (SW approach): Red until t = 1.0s, then Green
      // Cross direction (SE approach): Yellow until t = 0.8s, then Red
      const egoIsGreen = (t >= 1.0);
      const crossIsRed = (t >= 0.8);

      if (egoIsGreen) {{
        swLensRed.setAttribute('opacity', '0.15');
        swLensYellow.setAttribute('opacity', '0.15');
        swLensGreen.setAttribute('opacity', '1.0');

        nwLensRed.setAttribute('opacity', '0.15');
        nwLensGreen.setAttribute('opacity', '1.0');

        signalStateBadge.innerHTML = 'SIGNAL: GREEN';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }} else {{
        swLensRed.setAttribute('opacity', '1.0');
        swLensYellow.setAttribute('opacity', '0.15');
        swLensGreen.setAttribute('opacity', '0.15');

        nwLensRed.setAttribute('opacity', '1.0');
        nwLensGreen.setAttribute('opacity', '0.15');

        signalStateBadge.innerHTML = 'SIGNAL: RED';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
      }}

      if (crossIsRed) {{
        seLensRed.setAttribute('opacity', '1.0');
        seLensYellow.setAttribute('opacity', '0.15');
        seLensGreen.setAttribute('opacity', '0.15');
      }} else {{
        seLensRed.setAttribute('opacity', '0.15');
        seLensYellow.setAttribute('opacity', '1.0');
        seLensGreen.setAttribute('opacity', '0.15');
      }}

      // 3. VEHICLE B (Cross-Traffic Red-Light Runner)
      // Approaching from SE (82%, 82%), through center (50%, 57%), exiting NW (24%, 37%)
      // Runs through between t = 1.2s and t = 6.2s
      let bX = 82.0, bY = 82.0, bOpacity = 0.0;
      if (t >= 1.2 && t <= 6.2) {{
        const bProg = (t - 1.2) / (6.2 - 1.2);
        bX = 82.0 - bProg * (82.0 - 24.0);
        bY = 82.0 - bProg * (82.0 - 37.0);

        if (t < 1.6) bOpacity = (t - 1.2) / 0.4;
        else if (t > 5.8) bOpacity = Math.max(0.0, 1.0 - (t - 5.8) / 0.4);
        else bOpacity = 1.0;
      }}
      vehB.style.left = `${{bX}}%`;
      vehB.style.top = `${{bY}}%`;
      vehB.style.opacity = bOpacity;

      // Position Threat Reticle on Vehicle B
      if (bOpacity > 0.1) {{
        const svgBX = (bX / 100.0) * 1024;
        const svgBY = (bY / 100.0) * 667;
        threatReticle.setAttribute('transform', `translate(${{svgBX}}, ${{svgBY}})`);
      }}

      // =======================================================================
      // MODE SPECIFIC BRANCHING: PRIMARY (DEFENSIVE) vs HAZARD (BLIND LAUNCH)
      // =======================================================================
      if (simulationMode === 'primary') {{
        hazardCollisionZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        // Vehicle A Motion:
        // Holds at stop line (34.0%, 72.0%) until t = 5.2s
        // Then smoothly accelerates from t = 5.2s to t = 7.8s to (72.0%, 41.0%)
        let aX = 34.0, aY = 72.0, aSpeed = 0;
        let brakeGlow = 1.0;

        if (t <= 5.2) {{
          aX = 34.0;
          aY = 72.0;
          aSpeed = 0;
          brakeGlow = 1.0;
        }} else {{
          const p = easeInOutQuad((t - 5.2) / (7.8 - 5.2));
          aX = 34.0 + p * (72.0 - 34.0);
          aY = 72.0 - p * (72.0 - 41.0);
          aSpeed = Math.round(p * 22);
          brakeGlow = 0.0;
        }}

        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;
        brakeA1.style.opacity = brakeGlow;
        brakeA2.style.opacity = brakeGlow;

        if (aSpeed === 0) {{
          telemVehA.innerHTML = '0 MPH (DEFENSIVE HOLD)';
          telemVehA.className = 'text-emerald-400 font-bold';
          tagVehA.textContent = 'VEHICLE A (DEFENSIVE HOLD)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }} else {{
          telemVehA.innerHTML = `${{aSpeed}} MPH (PROCEEDING - CLEAR)`;
          telemVehA.className = 'text-blue-400 font-bold';
          tagVehA.textContent = 'VEHICLE A (PROCEEDING - CLEAR)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        }}

        // Vision Cone & Scanning Phases (t = 1.4s to 5.2s)
        const originX = 345, originY = 475; // Windshield SVG coordinates

        if (t < 1.4) {{
          // Initial pause on green
          visionConeGroup.setAttribute('opacity', '0.0');
          hudScanPill.style.opacity = '0.0';
          threatReticle.setAttribute('opacity', '0.0');
          telemScan.innerHTML = 'INITIAL GREEN PAUSE (HOLDING)';
          telemScan.className = 'text-gray-400 font-bold';
          telemVehB.innerHTML = 'APPROACHING FROM SE';
          telemVehB.className = 'text-gray-400 font-bold';
          hudNarrative.textContent = 'Signal turns green. Under TTC § 544.007(b), driver holds brake and pauses 2 seconds before entering to eliminate dilemma zone collisions.';
        }} else if (t < 2.3) {{
          // QUADRANT 1: SCAN LEFT
          const targetX = 220, targetY = 320;
          updateVisionCone(originX, originY, targetX, targetY, -25, 25, false);
          visionConeGroup.setAttribute('opacity', '0.9');
          threatReticle.setAttribute('opacity', '0.0');

          hudScanPill.style.opacity = '1.0';
          hudScanPill.style.left = '20%';
          hudScanPill.style.top = '44%';
          hudScanPill.textContent = 'QUADRANT 1: SCAN LEFT';

          telemScan.innerHTML = 'Q1: SCAN LEFT (ONCOMING NEAR)';
          telemScan.className = 'text-cyan-400 font-bold';
          telemVehB.innerHTML = '45 MPH (APPROACHING)';
          hudNarrative.textContent = 'Quadrant 1: Driver scans left towards the nearest cross-street lane to ensure no early stragglers or left-turning traffic violate the signal.';
        }} else if (t < 3.2) {{
          // QUADRANT 2: SCAN CENTER BOX
          const targetX = 490, targetY = 320;
          updateVisionCone(originX, originY, targetX, targetY, -22, 22, false);
          visionConeGroup.setAttribute('opacity', '0.9');
          threatReticle.setAttribute('opacity', '0.0');

          hudScanPill.style.opacity = '1.0';
          hudScanPill.style.left = '48%';
          hudScanPill.style.top = '44%';
          hudScanPill.textContent = 'QUADRANT 2: SCAN CENTER BOX';

          telemScan.innerHTML = 'Q2: SCAN CENTER INTERSECTION BOX';
          telemScan.className = 'text-cyan-400 font-bold';
          hudNarrative.textContent = 'Quadrant 2: Driver sweeps center intersection box, verifying it is completely free of clearing vehicles, turning cars, or pedestrians.';
        }} else if (t < 4.4) {{
          // QUADRANT 3: SCAN RIGHT — THREAT DETECTED!
          const targetX = (bX / 100.0) * 1024, targetY = (bY / 100.0) * 667;
          updateVisionCone(originX, originY, targetX, targetY, -20, 20, true);
          visionConeGroup.setAttribute('opacity', '1.0');
          threatReticle.setAttribute('opacity', '1.0');

          // Position pill safely in upper quadrant area without overlapping Vehicle B's badge
          hudScanPill.style.opacity = '1.0';
          hudScanPill.style.left = '52%';
          hudScanPill.style.top = '26%';
          hudScanPill.textContent = 'QUADRANT 3: SCAN RIGHT — HAZARD DETECTED!';

          telemScan.innerHTML = 'Q3: SCAN RIGHT • THREAT SPOTTED!';
          telemScan.className = 'text-red-400 font-black animate-pulse';
          telemVehB.innerHTML = '45 MPH (BLOWING RED LIGHT)';
          telemVehB.className = 'text-red-400 font-black';
          hudNarrative.textContent = 'Quadrant 3: Driver spots Vehicle B approaching from the right at 45 MPH failing to brake for the red light. Driver holds position behind stop line.';
        }} else if (t < 5.2) {{
          // QUADRANT 4: RE-SCAN LEFT & CLEARANCE
          const targetX = 230, targetY = 320;
          updateVisionCone(originX, originY, targetX, targetY, -22, 22, false);
          visionConeGroup.setAttribute('opacity', '0.6');
          threatReticle.setAttribute('opacity', '0.0');

          hudScanPill.style.opacity = '1.0';
          hudScanPill.style.left = '22%';
          hudScanPill.style.top = '44%';
          hudScanPill.textContent = 'QUADRANT 4: RE-SCAN LEFT';

          telemScan.innerHTML = 'Q4: RE-SCAN LEFT (CLEAR)';
          telemScan.className = 'text-emerald-400 font-bold';
          telemVehB.innerHTML = '45 MPH (EXITING NW)';
          telemVehB.className = 'text-gray-400 font-bold';
          hudNarrative.textContent = 'Red-light runner safely blasts through empty intersection. Driver performs final left re-scan. Intersection is now 100% verified clear.';
        }} else {{
          // All quadrants cleared, proceeding
          visionConeGroup.setAttribute('opacity', '0.0');
          hudScanPill.style.opacity = '0.0';
          threatReticle.setAttribute('opacity', '0.0');

          telemScan.innerHTML = 'INTERSECTION 100% CLEARED';
          telemScan.className = 'text-emerald-400 font-bold';
          telemVehB.innerHTML = 'CLEARED NW';
          telemVehB.className = 'text-gray-500 font-bold';
          hudNarrative.textContent = 'Under TTC § 544.007(b), right-of-way is lawfully accepted. Vehicle A accelerates safely through the intersection without conflict.';
        }}

        telemStatute.innerHTML = 'TTC § 544.007(b) CLEARANCE COMPLIANCE';
        telemStatute.className = 'text-emerald-400 font-bold';
        complianceText.textContent = 'TTC § 544.007(b) DEFENSIVE COMPLIANCE VERIFIED';

      }} else {{
        // =====================================================================
        // HAZARD DEMO: BLIND GREEN JACKRABBIT START
        // =====================================================================
        visionConeGroup.setAttribute('opacity', '0.0');
        hudScanPill.style.opacity = '0.0';

        // Vehicle A immediately accelerates when light turns green at t = 1.0s
        let aX = 34.0, aY = 72.0, aSpeed = 0;
        let brakeGlow = 1.0;

        if (t <= 1.0) {{
          aX = 34.0; aY = 72.0; aSpeed = 0; brakeGlow = 1.0;
        }} else if (t <= 3.8) {{
          // Rapid acceleration towards center
          const p = easeInOutQuad((t - 1.0) / (3.8 - 1.0));
          aX = 34.0 + p * (48.0 - 34.0);
          aY = 72.0 - p * (72.0 - 60.0);
          aSpeed = Math.round(p * 28);
          brakeGlow = 0.0;
        }} else {{
          // Collision stop at center
          aX = 48.0; aY = 60.0; aSpeed = 0; brakeGlow = 1.0;
        }}

        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;
        brakeA1.style.opacity = brakeGlow;
        brakeA2.style.opacity = brakeGlow;

        if (t > 3.6 && t < 5.8) {{
          hazardCollisionZone.setAttribute('opacity', '1.0');
          hazardBanner.style.opacity = '1.0';
          telemVehA.innerHTML = 'COLLISION AT INTERSECTION CENTER';
          telemVehA.className = 'text-red-400 font-black animate-pulse';
          tagVehA.innerHTML = '✕ CRITICAL SIDE-IMPACT VIOLATION';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';

          telemVehB.innerHTML = '45 MPH (T-BONE STRIKE)';
          telemVehB.className = 'text-red-400 font-black';

          telemScan.innerHTML = 'NO SCAN PERFORMED • ZERO DEFENSE';
          telemScan.className = 'text-red-400 font-black';

          telemStatute.innerHTML = 'TTC § 544.007(b) VIOLATION';
          telemStatute.className = 'text-red-500 font-black';

          hudNarrative.textContent = 'CRITICAL HAZARD: Immediate acceleration on green without quadrant scanning creates a lethal T-bone collision with the red-light runner!';
          complianceText.textContent = 'CRITICAL VIOLATION: FAILURE TO YIELD BEFORE ENTRY (§ 544.007b)';
        }} else {{
          hazardCollisionZone.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';

          if (t <= 1.0) {{
            telemVehA.innerHTML = '0 MPH (AT RED LIGHT)';
            telemVehA.className = 'text-gray-400 font-bold';
            tagVehA.textContent = 'VEHICLE A (WAITING)';
            telemScan.innerHTML = 'NO DEFENSIVE SCAN PLANNED';
            telemScan.className = 'text-gray-400 font-bold';
            hudNarrative.textContent = 'Hazard Demonstration: Driver plans an immediate jackrabbit launch the instant the light turns green without clearing intersection quadrants.';
          }} else {{
            telemVehA.innerHTML = `${{aSpeed}} MPH (BLIND GREEN LAUNCH)`;
            telemVehA.className = 'text-amber-400 font-bold';
            tagVehA.textContent = 'VEHICLE A (BLIND LAUNCH)';
            tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-amber-950/90 border border-amber-500 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
            telemVehB.innerHTML = '45 MPH (RUNNING RED)';
            telemVehB.className = 'text-red-400 font-bold';
            telemScan.innerHTML = 'BLIND ENTRY INTO INTERSECTION';
            telemScan.className = 'text-amber-400 font-bold';
            hudNarrative.textContent = 'Vehicle A surges forward into intersection. Vehicle B barrels in from right on fresh red. Direct collision trajectory developing!';
          }}
        }}
      }}
    }}

    // Helper: calculate SVG vision cone polygon and ray
    function updateVisionCone(x0, y0, tx, ty, leftAngleDeg, rightAngleDeg, isThreat) {{
      const dx = tx - x0;
      const dy = ty - y0;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const baseAngle = Math.atan2(dy, dx);

      const radL = baseAngle + (leftAngleDeg * Math.PI / 180);
      const radR = baseAngle + (rightAngleDeg * Math.PI / 180);

      const lx = x0 + dist * Math.cos(radL);
      const ly = y0 + dist * Math.sin(radL);
      const rx = x0 + dist * Math.cos(radR);
      const ry = y0 + dist * Math.sin(radR);

      visionConePath.setAttribute('d', `M ${{x0}} ${{y0}} L ${{lx.toFixed(1)}} ${{ly.toFixed(1)}} A ${{dist.toFixed(1)}} ${{dist.toFixed(1)}} 0 0 1 ${{rx.toFixed(1)}} ${{ry.toFixed(1)}} Z`);
      visionConePath.setAttribute('fill', isThreat ? 'url(#cone-threat-grad)' : 'url(#cone-cyan-grad)');
      visionConePath.setAttribute('stroke', isThreat ? '#EF4444' : '#06B6D4');

      visionRayLine.setAttribute('x1', x0);
      visionRayLine.setAttribute('y1', y0);
      visionRayLine.setAttribute('x2', tx);
      visionRayLine.setAttribute('y2', ty);
      visionRayLine.setAttribute('stroke', isThreat ? '#EF4444' : '#38BDF8');

      visionRayTarget.setAttribute('cx', tx);
      visionRayTarget.setAttribute('cy', ty);
      visionRayTarget.setAttribute('stroke', isThreat ? '#EF4444' : '#38BDF8');
      visionRayTarget.setAttribute('fill', isThreat ? '#DC2626' : '#0284C7');
    }}

    // =========================================================================
    // ANIMATION LOOP & CONTROLS
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

      if (currentTime > maxTime) {{
        endHoldAccumulator += dt;
        if (endHoldAccumulator >= holdTimeAtEnd) {{
          if (chkAutoLoop.checked) {{
            currentTime = 0.0;
            endHoldAccumulator = 0.0;
          }} else {{
            currentTime = maxTime;
            pauseSimulation();
          }}
        }} else {{
          currentTime = maxTime;
        }}
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

    btnPlayPause.addEventListener('click', () => {{
      if (isPlaying) pauseSimulation();
      else playSimulation();
    }});

    btnReset.addEventListener('click', () => {{
      pauseSimulation();
      currentTime = 0.0;
      endHoldAccumulator = 0.0;
      updateSimulation(0.0);
    }});

    scrubber.addEventListener('input', (e) => {{
      pauseSimulation();
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    // Stepper Button Click Handlers
    stepBtns.forEach((btn, idx) => {{
      btn.addEventListener('click', () => {{
        pauseSimulation();
        currentStepIdx = idx;
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

    // Speed Controls
    speedBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        speedBtns.forEach(b => {{
          b.classList.remove('bg-emerald-500', 'text-black', 'font-bold');
          b.classList.add('text-gray-400');
        }});
        btn.classList.add('bg-emerald-500', 'text-black', 'font-bold');
        btn.classList.remove('text-gray-400');
        playbackSpeed = parseFloat(btn.dataset.speed);
      }});
    }});

    // Scenario Mode Controls
    btnPrimary.addEventListener('click', () => {{
      simulationMode = 'primary';
      btnPrimary.className = 'scenario-toggle-btn px-3 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1.5 bg-emerald-500 text-black shadow';
      btnHazard.className = 'scenario-toggle-btn px-3 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    btnHazard.addEventListener('click', () => {{
      simulationMode = 'hazard';
      btnHazard.className = 'scenario-toggle-btn px-3 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1.5 bg-red-600 text-white shadow';
      btnPrimary.className = 'scenario-toggle-btn px-3 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    // Initial render
    updateSimulation(0.0);
  </script>
</body>
</html>
'''

output_path = 'C:/tx_dmv/driving_rule_animations_suite/simulations/L03_T07_defensive_quadrant_scanning.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Simulation updated successfully!")
