import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        ext = os.path.splitext(path)[1].lower()
        mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/texas_highway_3lane_corridor.jpg'
car_red_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_blue_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_ne.png'
car_yellow_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_yellow_ne.png'

print("Encoding Lesson 16 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_b64 = get_base64_img(car_red_ne_path)
car_blue_b64 = get_base64_img(car_blue_ne_path)
car_yellow_b64 = get_base64_img(car_yellow_ne_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T07: Safe Stopping Distances — The Perception, Reaction &amp; Braking Curve</title>
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
    .pulse-danger {{
      animation: dangerPulse 1.2s infinite ease-in-out;
    }}
    @keyframes dangerPulse {{
      0%, 100% {{ opacity: 0.95; }}
      50% {{ opacity: 0.45; }}
    }}
    .pulse-hazard-cone {{
      animation: hazardConePulse 1.5s infinite ease-in-out;
    }}
    @keyframes hazardConePulse {{
      0%, 100% {{ opacity: 0.35; }}
      50% {{ opacity: 0.15; }}
    }}
    input[type=range]::-webkit-slider-thumb {{
      height: 16px;
      width: 16px;
      border-radius: 9999px;
      background: #3B82F6;
      cursor: pointer;
      border: 2px solid #FFFFFF;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.8);
    }}
  </style>
</head>
<body class="flex flex-col h-screen w-screen overflow-hidden p-2 bg-[#0B0E14] text-gray-100">

  <!-- TOP HEADER / SCENARIO SELECTOR BAR -->
  <header class="flex items-center justify-between px-3 py-1.5 bg-[#121620] border border-[#212836] rounded-xl shadow-lg mb-1 z-20">
    <div class="flex items-center space-x-3">
      <div class="flex items-center space-x-2">
        <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">TDLR ADE-1317</span>
        <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">2.5D VECTOR ENGINE</span>
        <span class="text-xs font-bold text-gray-400 mono">LESSON 16</span>
      </div>
      <div class="h-4 w-px bg-gray-700"></div>
      <div>
        <h1 class="text-sm font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>L05-T07: Safe Stopping Distances — The Physics Breakdown</span>
        </h1>
        <p class="text-[10px] text-gray-400 font-medium">Texas Driver Handbook Ch. 5 • TTC § 545.351 (Maximum Speed &amp; Stopping Distance Physics)</p>
      </div>
    </div>

    <!-- 3 Core Statutory Scenarios -->
    <div class="flex items-center space-x-2">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
        1: 3-Stage Total Stopping Breakdown
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
        2: Speed Comparison (30 vs 60 MPH)
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
        Hazard: Overdriving Sightline
      </button>

      <div class="h-4 w-px bg-gray-700 ml-1 mr-1"></div>
      <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-gray-300 font-medium">
        <input type="checkbox" id="auto-loop-toggle" checked class="rounded bg-gray-800 border-gray-700 text-blue-500 focus:ring-0">
        <span class="text-[11px] mono">Auto-Loop</span>
      </label>
    </div>
  </header>

  <!-- CANONICAL 4-STEP STEPPER BAR -->
  <nav class="grid grid-cols-4 gap-2 mb-1 z-20">
    <button data-step="1" class="step-btn px-2.5 py-1 rounded-lg border border-blue-500/40 bg-blue-950/30 text-left transition hover:border-blue-500">
      <div class="text-[9px] mono text-blue-400 font-bold uppercase tracking-wider">STEP 1</div>
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">Perception Phase (132 FT)</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">Reaction Phase (66 FT)</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">Braking Phase (189 FT)</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Full Halt: 387 FT Total</div>
    </button>
  </nav>

  <!-- MAIN SIMULATION DIORAMA VIEWPORT -->
  <main class="relative flex-1 w-full bg-[#0E121A] rounded-xl border border-[#1E2634] overflow-hidden flex items-center justify-center shadow-inner min-h-0">
    
    <!-- 35° ARCHITECTURAL ISOMETRIC STAGE (1024 x 571 Canvas Ratio) -->
    <div id="isometric-stage" class="relative overflow-hidden shadow-2xl rounded-lg" style="height: calc(100% - 16px); aspect-ratio: 1024 / 571; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: Texas 3-Lane Highway Base -->
      <img src="{road_b64}" alt="Texas 3-Lane Highway" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none z-0" />

      <!-- LAYER 1: SVG DYNAMIC 3-ZONE BRAKING RUNWAY, BRACKETS & VIGNETTE -->
      <svg id="stage-svg-overlay" class="absolute inset-0 w-full h-full z-10 pointer-events-none" viewBox="0 0 1024 571">
        <defs>
          <pattern id="hatch-perception" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="8" stroke="#38BDF8" stroke-width="2" stroke-opacity="0.4" />
          </pattern>
          <pattern id="hatch-reaction" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="8" stroke="#FBBF24" stroke-width="2" stroke-opacity="0.4" />
          </pattern>
          <pattern id="hatch-braking" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="8" stroke="#EF4444" stroke-width="2" stroke-opacity="0.4" />
          </pattern>
        </defs>

        <!-- NIGHT / DARK SIGHTLINE VIGNETTE (Mode 3) -->
        <g id="night-vignette-group" opacity="0.0">
          <rect x="0" y="0" width="1024" height="571" fill="#030712" fill-opacity="0.75" />
          <!-- Headlight Illuminating Beam Throw (200 FT) -->
          <polygon id="headlight-beam" points="250,500 480,260 560,330 310,540" fill="#FEF08A" fill-opacity="0.25" class="pulse-hazard-cone" />
        </g>

        <!-- 3-STAGE CORRIDOR BANDS (Mode 1: Perception, Reaction, Braking) -->
        <g id="stopping-bands-group" opacity="1.0">
          <!-- Zone 1: Perception Band (Cyan) -->
          <polygon id="band-perception" points="0,0 0,0 0,0 0,0" fill="url(#hatch-perception)" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="4,3" />
          <text id="text-perception" x="0" y="0" fill="#38BDF8" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">PERCEPTION: 132 FT (1.5s)</text>

          <!-- Zone 2: Reaction Band (Amber) -->
          <polygon id="band-reaction" points="0,0 0,0 0,0 0,0" fill="url(#hatch-reaction)" stroke="#FBBF24" stroke-width="1.5" stroke-dasharray="4,3" />
          <text id="text-reaction" x="0" y="0" fill="#FBBF24" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">REACTION: 66 FT (0.75s)</text>

          <!-- Zone 3: Mechanical Braking Band (Red) -->
          <polygon id="band-braking" points="0,0 0,0 0,0 0,0" fill="url(#hatch-braking)" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="4,3" />
          <text id="text-braking" x="0" y="0" fill="#F87171" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">BRAKING: 189 FT (ABS)</text>
        </g>

        <!-- OVERALL TOTAL STOPPING BRACKET -->
        <g id="total-bracket-group" opacity="1.0">
          <line id="total-bracket-line" x1="0" y1="0" x2="0" y2="0" stroke="#10B981" stroke-width="2.5" />
          <line id="total-tick-start" x1="0" y1="0" x2="0" y2="0" stroke="#10B981" stroke-width="2.5" />
          <line id="total-tick-end" x1="0" y1="0" x2="0" y2="0" stroke="#10B981" stroke-width="2.5" />
          <rect id="total-badge-rect" x="0" y="0" width="220" height="22" rx="11" fill="#0A1812" stroke="#10B981" stroke-width="1.8" />
          <text id="total-badge-text" x="0" y="0" fill="#34D399" font-family="'JetBrains Mono', monospace" font-size="9.5" font-weight="900" text-anchor="middle">TOTAL STOPPING DISTANCE: 387 FT</text>
        </g>

        <!-- HAZARD OBSTACLE MARKER (Stalled Vehicle / Debris in Lane 2) -->
        <g id="obstacle-marker-group" opacity="1.0">
          <circle id="obstacle-circle" cx="800" cy="180" r="16" fill="#7F1D1D" stroke="#EF4444" stroke-width="2" class="pulse-danger" />
          <text id="obstacle-icon" x="800" y="184" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" text-anchor="middle">⚠</text>
          <text id="obstacle-text" x="800" y="210" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" text-anchor="middle">HAZARD IN LANE</text>
        </g>

        <!-- MODE 3: CRITICAL IMPACT BURST & HIGH-SPEED COLLISION ZONE -->
        <g id="hazard-impact-group" opacity="0.0">
          <circle id="hazard-impact-circle" cx="0" cy="0" r="42" fill="#EF4444" fill-opacity="0.35" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="5,4" class="pulse-danger" />
          <polygon id="hazard-impact-star" points="0,-16 5,-5 17,-4 8,5 11,16 0,9 -11,16 -8,5 -17,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- EGO VEHICLE (Red Sedan, Center Lane 2) -->
      <div id="veh-ego-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 18.0%; top: 74.7%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Ego Brake Lamps (Red Glow when Braking Active) -->
          <div id="ego-brake-left" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 62%; left: 18%;"></div>
          <div id="ego-brake-right" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 72%; left: 34%;"></div>
        </div>
        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          EGO: 60 MPH • PERCEPTION PHASE
        </div>
      </div>

      <!-- COMPARISON VEHICLE (Blue Sedan, Mode 2: 30 MPH Benchmark in Lane 3) -->
      <div id="veh-comp-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 18.0%; top: 63.5%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_b64}" alt="30 MPH Comparison Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          <div id="comp-brake-left" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 62%; left: 18%;"></div>
          <div id="comp-brake-right" class="absolute w-2.5 h-2.5 rounded-full bg-red-600 filter blur-[1px] opacity-0" style="top: 72%; left: 34%;"></div>
        </div>
        <div id="tag-veh-comp" class="absolute left-0 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9px] font-bold text-cyan-300 mono shadow-lg tracking-wider">
          CAR 1 (30 MPH): STOPS IN 109 FT
        </div>
      </div>

      <!-- STALLED DISABLED VEHICLE (Yellow Sedan, Mode 3 Obstruction) -->
      <div id="veh-stalled-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 54.0%; top: 41.8%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Stalled Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>
        <div id="tag-veh-stalled" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider">
          STALLED HAZARD (220 FT AHEAD)
        </div>
      </div>

      <!-- LAYER 3: TOP STATUS NOTIFICATION PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 8px; left: 286px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS STOPPING FORMULA: PERCEPTION + REACTION + BRAKING = TOTAL DISTANCE</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-2 right-2 z-25 px-2.5 py-1 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[9.5px] font-bold shadow-lg tracking-wider flex items-center space-x-1.5 pointer-events-none">
        <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TTC § 545.351 COMPLIANT: PRUDENT SPEED &amp; STOPPING ABILITY</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER (Bottom Center Compact) -->
      <div id="hazard-banner" class="absolute bottom-3 left-1/2 -translate-x-1/2 z-30 px-4 py-1.5 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300 max-w-[460px]" style="opacity: 0.0;">
        <div class="text-[10px] font-black text-red-400 tracking-wider">⚠ CRITICAL STATUTORY VIOLATION ⚠</div>
        <div class="text-[11.5px] font-extrabold text-white">FATAL IMPACT: OVERDRIVING HEADLIGHT SIGHT DISTANCE</div>
        <div class="text-[9.5px] text-red-200">TTC § 545.351: Operating at 70 MPH requires 530 FT to stop! Traveling faster than your 200-FT visible headlight field guarantees a blind collision.</div>
      </div>

      <!-- LAYER 4: TOP-LEFT TELEMETRY HUD CARD (3-Column Layout Partition) -->
      <div id="telemetry-hud-card" class="absolute z-25 rounded-xl bg-[#0F141C]/95 border border-[#2B3548] p-3 text-xs shadow-2xl backdrop-blur-md pointer-events-none space-y-2" style="top: 8px; left: 8px; width: 270px;">
        <div class="flex items-center justify-between border-b border-gray-800 pb-1.5">
          <span class="mono text-[10px] text-gray-400 font-extrabold tracking-wider">STOPPING PHYSICS HUD</span>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono">SPEED: 60 MPH</span>
        </div>

        <div class="space-y-1 text-[10.5px]">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Current Velocity:</span>
            <span id="telem-speed" class="text-white font-bold mono">60 MPH (88 FT/S)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-cyan-400">1. Perception Dist (1.5s):</span>
            <span id="telem-perception" class="text-cyan-300 font-bold mono">132 FT</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-amber-400">2. Reaction Dist (0.75s):</span>
            <span id="telem-reaction" class="text-amber-300 font-bold mono">66 FT</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-red-400">3. Braking Dist (Dry ABS):</span>
            <span id="telem-braking" class="text-red-400 font-bold mono">189 FT</span>
          </div>
          <div class="flex justify-between items-center pt-0.5 border-t border-gray-800">
            <span class="text-emerald-400 font-bold">Total Stopping Distance:</span>
            <span id="telem-total" class="text-emerald-400 font-extrabold mono">387 FT</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Mandate:</span>
            <span id="telem-statute" class="text-blue-300 font-bold mono">TTC § 545.351</span>
          </div>
        </div>

        <div class="pt-1.5 border-t border-gray-800 text-[10px] text-gray-300 leading-tight" id="hud-narrative">
          Total stopping distance is the sum of Perception (132 FT) + Reaction (66 FT) + Mechanical Braking (189 FT) = 387 FT. At 60 MPH, stopping requires more than an entire football field!
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM CONTROL TIMELINE BAR -->
  <footer class="mt-1 px-4 py-1.5 bg-[#121620] border border-[#212836] rounded-xl shadow-lg flex flex-col justify-center space-y-1 z-20">
    <div class="flex items-center space-x-3">
      <button id="play-pause-btn" class="w-7 h-7 rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center font-bold shadow transition">
        <svg id="play-icon" class="w-3.5 h-3.5 fill-current hidden" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        <svg id="pause-icon" class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
      </button>

      <button id="reset-btn" class="w-7 h-7 rounded-lg bg-[#1C2331] hover:bg-[#252F42] text-gray-300 flex items-center justify-center transition border border-[#2B3548]">
        <svg class="w-3.5 h-3.5 stroke-current fill-none" viewBox="0 0 24 24" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
      </button>

      <span id="time-display" class="mono text-xs text-blue-400 font-bold w-12">0.00s</span>

      <div class="flex-1 relative flex items-center">
        <input type="range" id="timeline-slider" min="0" max="8.0" step="0.01" value="0" class="w-full h-1.5 bg-[#212836] rounded-lg appearance-none cursor-pointer accent-blue-500" />
      </div>

      <span class="mono text-xs text-gray-400">8.00s</span>

      <div class="flex items-center bg-[#18202F] p-0.5 rounded border border-[#2B3548] text-xs mono">
        <button data-speed="0.5" class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white">0.5x</button>
        <button data-speed="1.0" class="speed-btn px-2 py-0.5 rounded bg-blue-600 text-white font-bold">1.0x</button>
        <button data-speed="1.5" class="speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white">1.5x</button>
      </div>
    </div>

    <!-- Timeline Keyframe Legend Markers -->
    <div class="flex justify-between text-[10px] mono text-gray-500 px-1 pt-0.5">
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
        <span id="keyframe-1-text">0.8s Perception Phase (132 FT)</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-2-text">2.0s Reaction Phase (66 FT)</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-red-400"></span>
        <span id="keyframe-3-text">4.0s ABS Braking Phase (189 FT)</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="keyframe-4-text">6.5s Complete Safe Halt (387 FT Total)</span>
      </span>
      <span class="text-blue-400 font-semibold" id="legend-statute">TTC § 545.351 Prudent Speed &amp; Stopping</span>
    </div>
  </footer>

  <!-- =============================================================== -->
  <!-- SIMULATION SCRIPT: 60 FPS DETERMINISTIC ENGINE                  -->
  <!-- =============================================================== -->
  <script>
    const DURATION = 8.0;
    let currentTime = 0.0;
    let isPlaying = true;
    let playbackSpeed = 1.0;
    let currentMode = 1;
    let lastTimestamp = null;
    let autoLoop = true;

    // DOM Elements
    const playPauseBtn = document.getElementById('play-pause-btn');
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');
    const resetBtn = document.getElementById('reset-btn');
    const timeDisplay = document.getElementById('time-display');
    const timelineSlider = document.getElementById('timeline-slider');
    const autoLoopToggle = document.getElementById('auto-loop-toggle');

    const vehEgo = document.getElementById('veh-ego-container');
    const vehComp = document.getElementById('veh-comp-container');
    const vehStalled = document.getElementById('veh-stalled-container');

    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehComp = document.getElementById('tag-veh-comp');
    const tagVehStalled = document.getElementById('tag-veh-stalled');

    const egoBrakeLeft = document.getElementById('ego-brake-left');
    const egoBrakeRight = document.getElementById('ego-brake-right');
    const compBrakeLeft = document.getElementById('comp-brake-left');
    const compBrakeRight = document.getElementById('comp-brake-right');

    const nightVignetteGroup = document.getElementById('night-vignette-group');
    const headlightBeam = document.getElementById('headlight-beam');
    const stoppingBandsGroup = document.getElementById('stopping-bands-group');
    const bandPerception = document.getElementById('band-perception');
    const textPerception = document.getElementById('text-perception');
    const bandReaction = document.getElementById('band-reaction');
    const textReaction = document.getElementById('text-reaction');
    const bandBraking = document.getElementById('band-braking');
    const textBraking = document.getElementById('text-braking');

    const totalBracketGroup = document.getElementById('total-bracket-group');
    const totalBracketLine = document.getElementById('total-bracket-line');
    const totalTickStart = document.getElementById('total-tick-start');
    const totalTickEnd = document.getElementById('total-tick-end');
    const totalBadgeRect = document.getElementById('total-badge-rect');
    const totalBadgeText = document.getElementById('total-badge-text');

    const obstacleMarkerGroup = document.getElementById('obstacle-marker-group');
    const obstacleCircle = document.getElementById('obstacle-circle');
    const obstacleIcon = document.getElementById('obstacle-icon');
    const obstacleText = document.getElementById('obstacle-text');

    const hazardImpactGroup = document.getElementById('hazard-impact-group');
    const hazardImpactCircle = document.getElementById('hazard-impact-circle');
    const hazardImpactStar = document.getElementById('hazard-impact-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemSpeed = document.getElementById('telem-speed');
    const telemPerception = document.getElementById('telem-perception');
    const telemReaction = document.getElementById('telem-reaction');
    const telemBraking = document.getElementById('telem-braking');
    const telemTotal = document.getElementById('telem-total');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceBadge = document.getElementById('compliance-badge');
    const complianceText = document.getElementById('compliance-text');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Proven Roadway Lane Trajectory Math (Texas 3-Lane Highway Corridor)
    // Lane 2 (Center Lane): y = 45.46% at x = 50%, slope m = -0.914
    function getLane2Y(x) {{
      return 45.46 - 0.914 * (x - 50.0);
    }}
    // Lane 3 (Left Lane / Median side): y = 34.26% at x = 50%
    function getLane3Y(x) {{
      return 34.26 - 0.914 * (x - 50.0);
    }}

    function smoothCos(p) {{
      return 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, p)));
    }}

    // Construct isometric corridor quad for a given x range in Lane 2
    function getLane2BandPoints(x1, x2, halfWidthPx) {{
      const y1 = getLane2Y(x1);
      const y2 = getLane2Y(x2);
      const p1x = x1 * 10.24 - halfWidthPx * 0.7;
      const p1y = y1 * 5.71 - halfWidthPx * 0.7;
      const p2x = x2 * 10.24 - halfWidthPx * 0.7;
      const p2y = y2 * 5.71 - halfWidthPx * 0.7;
      const p3x = x2 * 10.24 + halfWidthPx * 0.7;
      const p3y = y2 * 5.71 + halfWidthPx * 0.7;
      const p4x = x1 * 10.24 + halfWidthPx * 0.7;
      const p4y = y1 * 5.71 + halfWidthPx * 0.7;
      return `${{p1x}},${{p1y}} ${{p2x}},${{p2y}} ${{p3x}},${{p3y}} ${{p4x}},${{p4y}}`;
    }}

    // ===============================================================
    // MODE 1: 3-STAGE TOTAL STOPPING DISTANCE BREAKDOWN (60 MPH)
    // ===============================================================
    function updateMode1(t) {{
      nightVignetteGroup.setAttribute('opacity', '0.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      vehComp.style.opacity = '0.0';
      vehStalled.style.opacity = '0.0';
      stoppingBandsGroup.setAttribute('opacity', '1.0');
      totalBracketGroup.setAttribute('opacity', '1.0');
      obstacleMarkerGroup.setAttribute('opacity', '1.0');

      // Scale: 60 MPH stopping distance = 387 FT
      // Start of braking trial: x = 18.0%
      // 1. Perception distance: 132 FT => dx = 19.8% (ends at x = 37.8%)
      // 2. Reaction distance: 66 FT => dx = 9.9% (ends at x = 47.7%)
      // 3. Braking distance: 189 FT => dx = 28.3% (ends at x = 76.0%)
      // Obstacle at x = 80.0% (cleared by 4.0% = 27 FT margin!)
      const xStart = 18.0;
      const xPercepEnd = 37.8;
      const xReactEnd = 47.7;
      const xBrakeEnd = 76.0;
      const xObstacle = 80.0;

      // Draw 3 colored segmented bands in Lane 2
      bandPerception.setAttribute('points', getLane2BandPoints(xStart, xPercepEnd, 18));
      textPerception.setAttribute('x', ((xStart + xPercepEnd) / 2) * 10.24);
      textPerception.setAttribute('y', getLane2Y((xStart + xPercepEnd) / 2) * 5.71 + 34);

      bandReaction.setAttribute('points', getLane2BandPoints(xPercepEnd, xReactEnd, 18));
      textReaction.setAttribute('x', ((xPercepEnd + xReactEnd) / 2) * 10.24);
      textReaction.setAttribute('y', getLane2Y((xPercepEnd + xReactEnd) / 2) * 5.71 + 34);

      bandBraking.setAttribute('points', getLane2BandPoints(xReactEnd, xBrakeEnd, 18));
      textBraking.setAttribute('x', ((xReactEnd + xBrakeEnd) / 2) * 10.24);
      textBraking.setAttribute('y', getLane2Y((xReactEnd + xBrakeEnd) / 2) * 5.71 + 34);

      // Master Bracket along upper median side
      const bStartX = xStart * 10.24 - 15;
      const bStartY = getLane2Y(xStart) * 5.71 - 25;
      const bEndX = xBrakeEnd * 10.24 - 15;
      const bEndY = getLane2Y(xBrakeEnd) * 5.71 - 25;

      totalBracketLine.setAttribute('x1', bStartX);
      totalBracketLine.setAttribute('y1', bStartY);
      totalBracketLine.setAttribute('x2', bEndX);
      totalBracketLine.setAttribute('y2', bEndY);

      totalTickStart.setAttribute('x1', bStartX - 6);
      totalTickStart.setAttribute('y1', bStartY - 10);
      totalTickStart.setAttribute('x2', bStartX + 6);
      totalTickStart.setAttribute('y2', bStartY + 10);

      totalTickEnd.setAttribute('x1', bEndX - 6);
      totalTickEnd.setAttribute('y1', bEndY - 10);
      totalTickEnd.setAttribute('x2', bEndX + 6);
      totalTickEnd.setAttribute('y2', bEndY + 10);

      const bMidX = (bStartX + bEndX) / 2;
      const bMidY = (bStartY + bEndY) / 2 - 14;
      totalBadgeRect.setAttribute('x', bMidX - 110);
      totalBadgeRect.setAttribute('y', bMidY - 11);
      totalBadgeText.setAttribute('x', bMidX);
      totalBadgeText.setAttribute('y', bMidY + 4);

      // Obstacle marker at x = 80.0%
      const obstScreenX = xObstacle * 10.24;
      const obstScreenY = getLane2Y(xObstacle) * 5.71;
      obstacleCircle.setAttribute('cx', obstScreenX);
      obstacleCircle.setAttribute('cy', obstScreenY);
      obstacleIcon.setAttribute('x', obstScreenX);
      obstacleIcon.setAttribute('y', obstScreenY + 4);
      obstacleText.setAttribute('x', obstScreenX);
      obstacleText.setAttribute('y', obstScreenY - 24);

      // Ego vehicle travel kinematics
      // t in [0.0, 1.5]: Perception phase (constant 60 MPH) => x: 18.0 -> 37.8
      // t in [1.5, 2.25]: Reaction phase (constant 60 MPH) => x: 37.8 -> 47.7
      // t in [2.25, 5.5]: ABS braking (decelerates 60 -> 0) => x: 47.7 -> 76.0
      // t > 5.5: Stopped at x = 76.0
      let egoX = xStart;
      let egoBraking = false;
      let phaseName = 'PERCEPTION PHASE (132 FT)';
      let speedDisplay = '60 MPH (88 FT/S)';

      if (t < 1.5) {{
        egoX = xStart + (t / 1.5) * (xPercepEnd - xStart);
        phaseName = 'PHASE 1: PERCEPTION DISTANCE (1.5s / 132 FT)';
        speedDisplay = '60 MPH (88 FT/S)';
      }} else if (t < 2.25) {{
        const p = (t - 1.5) / 0.75;
        egoX = xPercepEnd + p * (xReactEnd - xPercepEnd);
        phaseName = 'PHASE 2: REACTION TIME (0.75s / 66 FT)';
        speedDisplay = '60 MPH (FOOT MOVING TO BRAKE)';
      }} else if (t < 5.5) {{
        egoBraking = true;
        const p = (t - 2.25) / 3.25;
        // Deceleration ease curve: speed = (1 - p) * 60 MPH
        const ease = 1 - Math.pow(1 - p, 2);
        egoX = xReactEnd + ease * (xBrakeEnd - xReactEnd);
        const curMph = Math.round((1 - p) * 60);
        phaseName = `PHASE 3: MECHANICAL BRAKING (${{curMph}} MPH)`;
        speedDisplay = `${{curMph}} MPH (ABS ACTIVE)`;
      }} else {{
        egoX = xBrakeEnd;
        egoBraking = true;
        phaseName = 'SAFE COMPLETE HALT: 387 FT TOTAL';
        speedDisplay = '0 MPH (STOPPED)';
      }}

      const egoY = getLane2Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0';

      egoBrakeLeft.style.opacity = egoBraking ? '1.0' : '0.0';
      egoBrakeRight.style.opacity = egoBraking ? '1.0' : '0.0';

      // Dynamic tags & narratives
      tagVehEgo.textContent = `EGO: ${{speedDisplay}} • ${{phaseName}}`;
      tagVehEgo.className = egoBraking
        ? (t >= 5.5
            ? 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider'
            : 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider')
        : 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';

      if (t < 1.5) {{
        hudNarrative.textContent = 'Step 1: Driver sees hazard. Over 1.5 seconds of perception time, vehicle travels 132 FT at 60 MPH before the brain recognizes the danger.';
        signalStateBadge.innerHTML = 'PHASE: PERCEPTION';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 mono';
      }} else if (t < 2.25) {{
        hudNarrative.textContent = 'Step 2: Reaction lag. Driver lifts foot from accelerator and steps onto brake pedal (0.75s). Vehicle traverses another 66 FT with zero braking applied!';
        signalStateBadge.innerHTML = 'PHASE: REACTION';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
      }} else if (t < 5.5) {{
        hudNarrative.textContent = 'Step 3: Mechanical braking. Brake pads bite discs, ABS modulates traction. On dry asphalt, vehicle requires 189 FT of braking distance to reach 0 MPH.';
        signalStateBadge.innerHTML = 'PHASE: BRAKING (ABS)';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
      }} else {{
        hudNarrative.textContent = 'Step 4: Full halt completed at 387 FT. Safe 27-FT buffer preserved before obstacle. Total stopping distance strictly obeys TTC § 545.351.';
        signalStateBadge.innerHTML = 'HALT: 387 FT COMPLETE';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }}

      telemSpeed.textContent = speedDisplay;
      telemPerception.textContent = '132 FT (1.50s)';
      telemReaction.textContent = '66 FT (0.75s)';
      telemBraking.textContent = '189 FT (ABS)';
      telemTotal.textContent = '387 FT TOTAL';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TEXAS FORMULA: PERCEPTION (132 FT) + REACTION (66 FT) + BRAKING (189 FT) = 387 FT TOTAL';
      complianceText.textContent = 'TTC § 545.351 COMPLIANT: PRUDENT SPEED & STOPPING ABILITY';
    }}

    // ===============================================================
    // MODE 2: SPEED COMPARISON MULTIPLIER (30 MPH VS. 60 MPH)
    // ===============================================================
    function updateMode2(t) {{
      nightVignetteGroup.setAttribute('opacity', '0.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      vehStalled.style.opacity = '0.0';
      stoppingBandsGroup.setAttribute('opacity', '0.0');
      totalBracketGroup.setAttribute('opacity', '0.0');
      obstacleMarkerGroup.setAttribute('opacity', '1.0');

      vehComp.style.opacity = '1.0'; // Blue car in Lane 3 (30 MPH)
      vehEgo.style.opacity = '1.0';  // Red car in Lane 2 (60 MPH)

      // Obstacle in both lanes at x = 78.0%
      const obstScreenX = 78.0 * 10.24;
      const obstScreenY = getLane2Y(78.0) * 5.71;
      obstacleCircle.setAttribute('cx', obstScreenX);
      obstacleCircle.setAttribute('cy', obstScreenY);
      obstacleIcon.setAttribute('x', obstScreenX);
      obstacleIcon.setAttribute('y', obstScreenY + 4);
      obstacleText.setAttribute('x', obstScreenX);
      obstacleText.setAttribute('y', obstScreenY - 24);

      // Car 1 (Blue Sedan in Lane 3 at 30 MPH = 44 FT/S)
      // Total stopping distance at 30 MPH = 109 FT (Perception 44 FT + Reaction 22 FT + Braking 43 FT)
      // In scale: 109 FT = 16.5% dx
      const xStart = 18.0;
      const x30Halt = xStart + 16.5; // stops at x = 34.5%
      let x30 = xStart;
      let compBraking = false;
      if (t < 0.75) {{
        x30 = xStart + (t / 0.75) * 6.5; // perception
      }} else if (t < 1.5) {{
        x30 = xStart + 6.5 + ((t - 0.75) / 0.75) * 3.5; // reaction
      }} else if (t < 3.2) {{
        compBraking = true;
        const p = (t - 1.5) / 1.7;
        const ease = 1 - Math.pow(1 - p, 2);
        x30 = (xStart + 10.0) + ease * 6.5;
      }} else {{
        x30 = x30Halt;
        compBraking = true;
      }}
      const y30 = getLane3Y(x30);
      vehComp.style.left = `${{x30}}%`;
      vehComp.style.top = `${{y30}}%`;
      compBrakeLeft.style.opacity = compBraking ? '1.0' : '0.0';
      compBrakeRight.style.opacity = compBraking ? '1.0' : '0.0';

      // Car 2 (Red Sedan in Lane 2 at 60 MPH = 88 FT/S)
      // Total stopping distance at 60 MPH = 387 FT (stops at x = 76.0%)
      const x60Halt = 76.0;
      let x60 = xStart;
      let egoBraking = false;
      if (t < 1.5) {{
        x60 = xStart + (t / 1.5) * 19.8;
      }} else if (t < 2.25) {{
        x60 = xStart + 19.8 + ((t - 1.5) / 0.75) * 9.9;
      }} else if (t < 5.5) {{
        egoBraking = true;
        const p = (t - 2.25) / 3.25;
        const ease = 1 - Math.pow(1 - p, 2);
        x60 = (xStart + 29.7) + ease * (x60Halt - (xStart + 29.7));
      }} else {{
        x60 = x60Halt;
        egoBraking = true;
      }}
      const y60 = getLane2Y(x60);
      vehEgo.style.left = `${{x60}}%`;
      vehEgo.style.top = `${{y60}}%`;
      egoBrakeLeft.style.opacity = egoBraking ? '1.0' : '0.0';
      egoBrakeRight.style.opacity = egoBraking ? '1.0' : '0.0';

      tagVehComp.textContent = (t >= 3.2) ? 'CAR 1 (30 MPH): HALTED AT 109 FT' : 'CAR 1 (30 MPH): STOPPING (109 FT)';
      tagVehComp.className = (t >= 3.2)
        ? 'absolute left-0 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-emerald-950/95 border border-emerald-500 text-[9px] font-bold text-emerald-300 mono shadow-lg tracking-wider'
        : 'absolute left-0 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9px] font-bold text-cyan-300 mono shadow-lg tracking-wider';

      if (t < 3.2) {{
        tagVehEgo.textContent = 'CAR 2 (60 MPH): STILL TRAVELING 55 MPH AT 109-FT MARK!';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Quadratic Law Demonstration: Doubling speed from 30 to 60 MPH does NOT double stopping distance — it quadruples (4x) the braking distance! When Car 1 is stopped, Car 2 is still hurtling at 55 MPH.';
        signalStateBadge.innerHTML = 'QUADRATIC: 4X BRAKING';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
      }} else {{
        tagVehEgo.textContent = 'CAR 2 (60 MPH): REQUIRES 387 FT TO STOP (3.5X TOTAL DISTANCE)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        hudNarrative.textContent = 'Car 2 finally halts at 387 FT. Kinetic energy scales with velocity squared (Ek = 0.5mv²), proving why high freeway speeds drastically escalate collision severity.';
        signalStateBadge.innerHTML = 'PHYSICS VALIDATED';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
      }}

      telemSpeed.textContent = '30 MPH (109 FT) vs 60 MPH (387 FT)';
      telemPerception.textContent = '30 MPH: 44 FT | 60 MPH: 132 FT';
      telemReaction.textContent = '30 MPH: 22 FT | 60 MPH: 66 FT';
      telemBraking.textContent = '30 MPH: 43 FT | 60 MPH: 189 FT';
      telemTotal.textContent = '109 FT vs 387 FT (3.5x)';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'PHYSICS PRINCIPLE: DOUBLING SPEED QUADRUPLES (4X) THE BRAKING DISTANCE (Ek = ½mv²)';
      complianceText.textContent = 'TEXAS SPEED PHYSICS COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (OVERDRIVING HEADLIGHT SIGHTLINE)
    // ===============================================================
    function updateMode3(t) {{
      nightVignetteGroup.setAttribute('opacity', '1.0');
      stoppingBandsGroup.setAttribute('opacity', '0.0');
      totalBracketGroup.setAttribute('opacity', '0.0');
      obstacleMarkerGroup.setAttribute('opacity', '0.0');
      complianceBadge.style.opacity = '0.0';
      vehComp.style.opacity = '0.0';
      vehStalled.style.opacity = '1.0';

      // Stalled vehicle disabled in Lane 2 at x = 54.0%
      const stalledX = 54.0;
      const stalledY = getLane2Y(stalledX);
      vehStalled.style.left = `${{stalledX}}%`;
      vehStalled.style.top = `${{stalledY}}%`;

      // Ego traveling at 70 MPH (103 FT/S) at night
      // Total stopping distance at 70 MPH = 530 FT!
      // Visible headlight throw = only 200 FT (dx = 30.0%)
      // Stalled car is only 220 FT ahead!
      // Collision occurs at t = 2.8s at over 48 MPH!
      const xStart = 20.0;
      let egoX = xStart;
      let egoBraking = (t >= 1.5);

      if (t < 2.8) {{
        egoX = xStart + (t / 2.8) * (stalledX - 2.5 - xStart);
      }} else {{
        egoX = stalledX - 2.5; // Impact state!
      }}
      const egoY = getLane2Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;

      egoBrakeLeft.style.opacity = egoBraking ? '1.0' : '0.0';
      egoBrakeRight.style.opacity = egoBraking ? '1.0' : '0.0';

      // Move headlight beam cone with ego car
      const hx1 = egoX * 10.24 + 32;
      const hy1 = egoY * 5.71 - 16;
      const hx2 = hx1 + 180;
      const hy2 = hy1 - 160;
      const hx3 = hx1 + 240;
      const hy3 = hy1 - 110;
      const hx4 = hx1 + 45;
      const hy4 = hy1 + 10;
      headlightBeam.setAttribute('points', `${{hx1}},${{hy1}} ${{hx2}},${{hy2}} ${{hx3}},${{hy3}} ${{hx4}},${{hy4}}`);

      if (t < 2.8) {{
        tagVehEgo.style.opacity = '1.0';
        tagVehStalled.style.opacity = '1.0';
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        if (t < 1.5) {{
          tagVehEgo.textContent = 'EGO: 70 MPH (103 FT/S) • SIGHTLINE ONLY 200 FT';
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/40 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
          hudNarrative.textContent = 'Hazard Demo: Ego drives 70 MPH at night. Headlights only illuminate 200 FT ahead, but stopping at 70 MPH requires 530 FT! Driver is overdriving headlights.';
          signalStateBadge.innerHTML = 'OVERDRIVING HEADLIGHTS';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';
        }} else {{
          tagVehEgo.textContent = 'HAZARD APPEARS! STOPPING REQUIRES 530 FT (COLLISION IMMINENT)';
          tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
          hudNarrative.textContent = 'Stalled car illuminated at 200 FT! Driver reacts and slams brakes, but physics dictates 530 FT to stop. High-speed impact is physically unavoidable.';
          signalStateBadge.innerHTML = 'COLLISION INEVITABLE';
          signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        }}

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'WARNING: TRAVELING 70 MPH WITH ONLY 200 FT OF SIGHTLINE ILLUMINATION';
      }} else {{
        // Impact!
        tagVehEgo.style.opacity = '0.0';
        tagVehStalled.style.opacity = '0.0';
        hazardImpactGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';

        const impX = ((egoX + stalledX) / 2) * 10.24;
        const impY = ((egoY + stalledY) / 2) * 5.71;
        hazardImpactCircle.setAttribute('cx', impX);
        hazardImpactCircle.setAttribute('cy', impY);
        hazardImpactStar.setAttribute('transform', `translate(${{impX}}, ${{impY}})`);

        signalStateBadge.innerHTML = 'FATAL IMPACT: OVERDRIVING';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ CRITICAL STATUTORY VIOLATION: HIGH-SPEED COLLISION FROM OVERDRIVING SIGHTLINE ✕';
        hudNarrative.textContent = 'FATAL CRASH: Ego impacts stalled vehicle at 48 MPH. Overdriving headlights violates TTC § 545.351 (reasonable and prudent speed). Never travel faster than your ability to stop within your visible sightline!';
      }}

      telemSpeed.textContent = (t < 2.8) ? '70 MPH (103 FT/S)' : '48 MPH IMPACT';
      telemPerception.textContent = '154 FT (1.50s)';
      telemReaction.textContent = '77 FT (0.75s)';
      telemBraking.textContent = '299 FT (70 MPH)';
      telemTotal.textContent = '530 FT REQUIRED (vs 200 FT SIGHT)';
    }}

    // ===============================================================
    // MAIN UPDATE DISPATCHER
    // ===============================================================
    function updateSimulation(t) {{
      timeDisplay.textContent = t.toFixed(2) + 's';
      timelineSlider.value = t;

      if (currentMode === 1) updateMode1(t);
      else if (currentMode === 2) updateMode2(t);
      else if (currentMode === 3) updateMode3(t);

      // Stepper Active Indicator Sync
      stepBtns.forEach(btn => {{
        const stepNum = parseInt(btn.dataset.step);
        let active = false;
        if (currentMode === 1) {{
          if (stepNum === 1 && t < 1.5) active = true;
          else if (stepNum === 2 && t >= 1.5 && t < 2.25) active = true;
          else if (stepNum === 3 && t >= 2.25 && t < 5.5) active = true;
          else if (stepNum === 4 && t >= 5.5) active = true;
        }} else if (currentMode === 2) {{
          if (stepNum === 1 && t < 1.5) active = true;
          else if (stepNum === 2 && t >= 1.5 && t < 3.2) active = true;
          else if (stepNum === 3 && t >= 3.2 && t < 5.5) active = true;
          else if (stepNum === 4 && t >= 5.5) active = true;
        }} else if (currentMode === 3) {{
          if (stepNum === 1 && t < 1.5) active = true;
          else if (stepNum === 2 && t >= 1.5 && t < 2.5) active = true;
          else if (stepNum === 3 && t >= 2.5 && t < 4.0) active = true;
          else if (stepNum === 4 && t >= 4.0) active = true;
        }}

        if (active) {{
          btn.className = 'step-btn px-2.5 py-1 rounded-lg border border-blue-500/60 bg-blue-950/40 text-left transition shadow-md shadow-blue-900/30';
          btn.querySelector('.mono').className = 'text-[9px] mono text-blue-400 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-white truncate';
        }} else {{
          btn.className = 'step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600';
          btn.querySelector('.mono').className = 'text-[9px] mono text-gray-500 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-gray-300 truncate';
        }}
      }});
    }}

    // Animation Loop
    function animate(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += dt * playbackSpeed;
        if (currentTime > DURATION) {{
          if (autoLoop) {{
            currentTime = 0.0;
          }} else {{
            currentTime = DURATION;
            isPlaying = false;
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
          }}
        }}
        updateSimulation(currentTime);
      }}

      requestAnimationFrame(animate);
    }}

    // Step labels per mode
    const stepLabels = {{
      1: [
        'Perception Phase (132 FT)',
        'Reaction Phase (66 FT)',
        'Braking Phase (189 FT)',
        'Full Halt: 387 FT Total'
      ],
      2: [
        'Dual Speed Benchmark',
        '30 MPH Vehicle Halts (109 FT)',
        '60 MPH Vehicle at 55 MPH',
        'Quadratic 4x Validated'
      ],
      3: [
        '70 MPH Night Sightline',
        'Hazard Revealed at 200 FT',
        'Stopping Requires 530 FT',
        'High-Speed Impact Crash'
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
          else if (m === 3) btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/40 bg-red-600 text-white shadow-md shadow-red-900/40';
        }} else {{
          btn.className = 'mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white';
        }}
      }});

      for (let i = 1; i <= 4; i++) {{
        document.getElementById(`step-label-${{i}}`).textContent = stepLabels[mode][i - 1];
      }}

      updateSimulation(0.0);
    }}

    // Event Listeners
    playPauseBtn.addEventListener('click', () => {{
      isPlaying = !isPlaying;
      playIcon.classList.toggle('hidden', isPlaying);
      pauseIcon.classList.toggle('hidden', !isPlaying);
      lastTimestamp = null;
    }});

    resetBtn.addEventListener('click', () => {{
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    autoLoopToggle.addEventListener('change', (e) => {{
      autoLoop = e.target.checked;
    }});

    stepBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        const s = parseInt(btn.dataset.step);
        let targetTime = 0.8;
        if (currentMode === 1) {{
          if (s === 1) targetTime = 0.8;
          else if (s === 2) targetTime = 1.9;
          else if (s === 3) targetTime = 3.8;
          else if (s === 4) targetTime = 6.0;
        }} else if (currentMode === 2) {{
          if (s === 1) targetTime = 0.8;
          else if (s === 2) targetTime = 2.4;
          else if (s === 3) targetTime = 3.8;
          else if (s === 4) targetTime = 6.2;
        }} else if (currentMode === 3) {{
          if (s === 1) targetTime = 0.8;
          else if (s === 2) targetTime = 1.8;
          else if (s === 3) targetTime = 2.5;
          else if (s === 4) targetTime = 4.2;
        }}
        currentTime = targetTime;
        updateSimulation(currentTime);
      }});
    }});

    speedBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        playbackSpeed = parseFloat(btn.dataset.speed);
        speedBtns.forEach(b => {{
          if (b === btn) {{
            b.className = 'speed-btn px-2 py-0.5 rounded bg-blue-600 text-white font-bold';
          }} else {{
            b.className = 'speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white';
          }}
        }});
      }});
    }});

    modeBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        setMode(parseInt(btn.dataset.mode));
      }});
    }});

    // Initialize
    updateSimulation(0.0);
    requestAnimationFrame(animate);
  </script>
</body>
</html>
'''

output_path = 'driving_rule_animations_suite/simulations/L05_T07_safe_stopping_distances.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 16 simulation built successfully at: {output_path}")
