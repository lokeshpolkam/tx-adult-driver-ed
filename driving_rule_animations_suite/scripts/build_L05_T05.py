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
school_bus_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/school_bus_tx_ne_clean.png'

print("Encoding Lesson 14 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_b64 = get_base64_img(car_red_ne_path)
car_blue_b64 = get_base64_img(car_blue_ne_path)
car_yellow_b64 = get_base64_img(car_yellow_ne_path)
school_bus_b64 = get_base64_img(school_bus_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T05: Blind Spot Driving — Convex vs. Flat Mirror Coverage & Mandatory Shoulder Head-Check</title>
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
      0%, 100% {{ opacity: 0.9; }}
      50% {{ opacity: 0.4; }}
    }}
    .pulse-sightline {{
      animation: sightlinePulse 1.0s infinite ease-in-out;
    }}
    @keyframes sightlinePulse {{
      0%, 100% {{ opacity: 0.95; stroke-width: 2.5; }}
      50% {{ opacity: 0.45; stroke-width: 1.5; }}
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
        <span class="text-xs font-bold text-gray-400 mono">LESSON 14</span>
      </div>
      <div class="h-4 w-px bg-gray-700"></div>
      <div>
        <h1 class="text-sm font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>L05-T05: Blind Spot Driving — Mirror Coverage &amp; Shoulder Head-Check</span>
        </h1>
        <p class="text-[10px] text-gray-400 font-medium">Texas Driver Handbook Ch. 5 • TTC § 545.060 (Safe Lane Change Mandate)</p>
      </div>
    </div>

    <!-- 3 Core Statutory Scenarios -->
    <div class="flex items-center space-x-2">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-emerald-500/40 bg-emerald-600 text-white shadow-md shadow-emerald-900/40" data-mode="1">
        1: BGE Mirror Field &amp; Shoulder Check
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-[#2B3548] bg-[#171D2A] text-gray-300 hover:text-white" data-mode="2">
        2: CMV Commercial "No-Zone" Rules
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded-lg text-xs font-bold transition border border-red-500/30 bg-red-950/40 text-red-300 hover:bg-red-900/60" data-mode="3">
        Hazard: Blind Sideswipe Collision
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
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">Mirror Cone vs. Blind Spot</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">100-Ft Signal &amp; Mirror Check</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">Chin-to-Shoulder Head-Check</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Cushion Maintained &amp; Safe Entry</div>
    </button>
  </nav>

  <!-- MAIN SIMULATION VIEWPORT -->
  <main class="relative flex-1 w-full bg-[#0E121A] rounded-xl border border-[#1E2634] overflow-hidden flex items-center justify-center shadow-inner min-h-0">
    
    <!-- 35° ARCHITECTURAL ISOMETRIC STAGE (1024 x 571 Canvas Ratio) -->
    <div id="isometric-stage" class="relative overflow-hidden shadow-2xl rounded-lg" style="height: calc(100% - 16px); aspect-ratio: 1024 / 571; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: Texas 3-Lane Highway Base -->
      <img src="{road_b64}" alt="Texas 3-Lane Highway" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none z-0" />

      <!-- LAYER 1: SVG DYNAMIC SIGHTLINE CONES, BLIND SPOTS & NO-ZONES -->
      <svg id="stage-svg-overlay" class="absolute inset-0 w-full h-full z-10 pointer-events-none" viewBox="0 0 1024 571">
        <defs>
          <!-- Hatch Pattern for Blind Spot -->
          <pattern id="blind-spot-hatch" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="8" stroke="#EF4444" stroke-width="2.5" stroke-opacity="0.6" />
          </pattern>
          <pattern id="no-zone-hatch" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="10" stroke="#F59E0B" stroke-width="2.5" stroke-opacity="0.5" />
          </pattern>
        </defs>

        <!-- MODE 1 & 3: EGO SIGHTLINE & BLIND SPOT OVERLAYS -->
        <g id="ego-vision-group" opacity="1.0">
          <!-- 1. Center Rearview Mirror Cone (Emerald Green) -->
          <polygon id="rearview-cone" points="0,0 0,0 0,0" fill="#10B981" fill-opacity="0.18" stroke="#10B981" stroke-width="1.8" stroke-dasharray="4,3" />
          
          <!-- 2. Side Mirror Field of View Cone (Cyan) -->
          <polygon id="side-mirror-cone" points="0,0 0,0 0,0" fill="#06B6D4" fill-opacity="0.22" stroke="#06B6D4" stroke-width="1.8" stroke-dasharray="4,3" />

          <!-- 3. Red Blind Spot Danger Wedge (0% Mirror Coverage) -->
          <polygon id="blind-spot-wedge" points="0,0 0,0 0,0" fill="url(#blind-spot-hatch)" stroke="#EF4444" stroke-width="2.2" class="pulse-danger" />
          <text id="blind-spot-label" x="0" y="0" fill="#F87171" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="900" text-anchor="middle" opacity="0.0">⚠ BLIND SPOT</text>

          <!-- 4. Mandatory Shoulder Head-Check Beam (Yellow Eye-Check) -->
          <g id="shoulder-check-beam" opacity="0.0">
            <polygon id="shoulder-check-cone" points="0,0 0,0 0,0" fill="#FBBF24" fill-opacity="0.32" stroke="#FBBF24" stroke-width="2" class="pulse-sightline" />
            <circle id="shoulder-eye-circle" cx="0" cy="0" r="12" fill="#1E293B" stroke="#FBBF24" stroke-width="1.5" />
            <text id="shoulder-eye-text" x="0" y="4" fill="#FBBF24" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="900" text-anchor="middle">👁</text>
          </g>
        </g>

        <!-- MODE 2: COMMERCIAL MOTOR VEHICLE (CMV) 4 NO-ZONES -->
        <g id="cmv-no-zones-group" opacity="0.0">
          <!-- Front No-Zone -->
          <polygon id="cmv-front-zone" points="0,0 0,0 0,0 0,0" fill="url(#no-zone-hatch)" stroke="#F59E0B" stroke-width="1.5" />
          <!-- Rear No-Zone (200 Ft) -->
          <polygon id="cmv-rear-zone" points="0,0 0,0 0,0 0,0" fill="url(#no-zone-hatch)" stroke="#F59E0B" stroke-width="1.5" />
          <!-- Left No-Zone (1 Lane) -->
          <polygon id="cmv-left-zone" points="0,0 0,0 0,0 0,0" fill="url(#no-zone-hatch)" stroke="#F59E0B" stroke-width="1.5" />
          <!-- Right No-Zone (2 Lanes Wide - High Danger) -->
          <polygon id="cmv-right-zone" points="0,0 0,0 0,0 0,0" fill="#EF4444" fill-opacity="0.22" stroke="#EF4444" stroke-width="2" class="pulse-danger" />
          <text id="cmv-right-text" x="0" y="0" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="900" text-anchor="middle">⚠ RIGHT NO-ZONE (2 LANES WIDE)</text>
        </g>

        <!-- MODE 3: CRITICAL IMPACT FLASH & SIDESWIPE ZONE -->
        <g id="hazard-impact-group" opacity="0.0">
          <circle id="hazard-impact-circle" cx="0" cy="0" r="38" fill="#EF4444" fill-opacity="0.35" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="5,4" class="pulse-danger" />
          <polygon id="hazard-impact-star" points="0,-15 5,-5 16,-4 8,4 11,15 0,8 -11,15 -8,4 -16,-4 -5,-5" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES -->

      <!-- EGO VEHICLE (Red Sedan, Center Lane 2) -->
      <div id="veh-ego-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 45.0%; top: 50.0%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Turn Signal Blinkers -->
          <div id="blinker-left-front" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 24%; left: 74%;"></div>
          <div id="blinker-left-rear" class="absolute w-2.5 h-2.5 rounded-full bg-amber-400 filter blur-[1px] opacity-0" style="top: 18%; left: 24%;"></div>
        </div>

        <div id="tag-veh-ego" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO: MONITORING LANE 2
        </div>
      </div>

      <!-- ADJACENT VEHICLE (Blue Sedan, Left Lane 3) -->
      <div id="veh-blue-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 38.0%; top: 40.0%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_b64}" alt="Adjacent Overtaking Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>
        <div id="tag-veh-blue" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          OVERTAKING VEHICLE (LANE 3)
        </div>
      </div>

      <!-- TRAILING VEHICLE (Yellow Sedan, Lane 2 Behind Ego) -->
      <div id="veh-yellow-container" class="absolute z-18 transition-transform pointer-events-none" style="left: 25.0%; top: 68.0%; transform: translate(-50%, -50%);">
        <div class="relative w-20 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_b64}" alt="Trailing Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>
        <div id="tag-veh-yellow" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          TRAILING CAR (VISIBLE IN REARVIEW)
        </div>
      </div>

      <!-- COMMERCIAL MOTOR VEHICLE (School Bus, Mode 2) -->
      <div id="veh-cmv-container" class="absolute z-19 transition-transform pointer-events-none" style="left: 50.0%; top: 45.0%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-32 aspect-[180/75] flex items-center justify-center">
          <img src="{school_bus_b64}" alt="Commercial Motor Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_16px_12px_rgba(0,0,0,0.7)]" />
        </div>
        <div id="tag-veh-cmv" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          COMMERCIAL VEHICLE (4 MAJOR NO-ZONES)
        </div>
      </div>

      <!-- LAYER 3: TOP STATUS NOTIFICATION PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 8px; left: 286px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">TEXAS SAFETY STANDARD: ZERO LANE CHANGES WITHOUT SHOULDER HEAD-CHECK</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div id="compliance-badge" class="absolute bottom-2 right-2 z-25 px-2.5 py-1 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[9.5px] font-bold shadow-lg tracking-wider flex items-center space-x-1.5 pointer-events-none">
        <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TTC § 545.060 BLIND SPOT COMPLIANCE VERIFIED</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER (Bottom Center Compact) -->
      <div id="hazard-banner" class="absolute bottom-3 left-1/2 -translate-x-1/2 z-30 px-4 py-1.5 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300 max-w-[440px]" style="opacity: 0.0;">
        <div class="text-[10.5px] font-black tracking-widest text-red-400 flex items-center justify-center space-x-1">
          <span>⚠</span>
          <span>CRITICAL STATUTORY VIOLATION</span>
          <span>⚠</span>
        </div>
        <div class="text-[10px] font-bold text-white">SIDESWIPE COLLISION: LANE CHANGE INTO OCCUPIED BLIND SPOT</div>
        <div class="text-[9px] text-red-300 leading-tight">
          TTC § 545.060: Moving from lane without verifying blind spot safety forces severe sideswipe crash!
        </div>
      </div>

      <!-- LAYER 4: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
      <div id="telemetry-hud-card" class="absolute top-2 left-2 z-30 max-w-[270px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-2 space-y-1 shadow-xl pointer-events-none">
        <div class="flex items-center justify-between border-b border-[#222B38] pb-1">
          <span class="text-[9.5px] font-bold text-gray-400 mono uppercase tracking-wider">Blind Spot Telemetry</span>
          <span id="signal-state-badge" class="text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">
            STATUS: SECURE
          </span>
        </div>

        <div class="space-y-0.5 text-[11px] mono">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Inside Mirror:</span>
            <span id="telem-inside-mirror" class="text-emerald-400 font-bold">TRAILING CAR (CLEAR)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Side Mirror:</span>
            <span id="telem-side-mirror" class="text-amber-400 font-bold">EMPTY (BLIND GAP)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Shoulder Glance:</span>
            <span id="telem-shoulder-check" class="text-emerald-300 font-bold">VERIFIED CLEAR</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Rule:</span>
            <span id="telem-statute" class="text-emerald-300 font-bold">TTC § 545.060</span>
          </div>
        </div>

        <div class="pt-1 border-t border-[#1F2633] text-[9.5px] text-gray-300 leading-snug font-sans" id="hud-narrative">
          Mirrors cannot cover the direct B-pillar quarter zone. Drivers must perform a physical chin-to-shoulder glance before any lane change.
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM SCRUBBABLE TIMELINE & PLAYBACK CONTROLS -->
  <footer class="bg-[#121620] border border-[#212836] rounded-xl px-4 py-2 shadow-lg flex flex-col gap-1.5 mt-1 z-30">
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
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-1-text">0.8s Mirror Field vs. Blind Spot</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-2-text">2.5s Turn Signal &amp; Mirror Check</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        <span id="keyframe-3-text">4.5s Shoulder Head-Check</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span id="keyframe-4-text">6.5s Safe Maneuver Complete</span>
      </span>
      <span class="text-blue-400 font-semibold" id="legend-statute">TTC § 545.060 Safety Standard</span>
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
    const vehBlue = document.getElementById('veh-blue-container');
    const vehYellow = document.getElementById('veh-yellow-container');
    const vehCmv = document.getElementById('veh-cmv-container');

    const tagVehEgo = document.getElementById('tag-veh-ego');
    const tagVehBlue = document.getElementById('tag-veh-blue');
    const tagVehYellow = document.getElementById('tag-veh-yellow');
    const tagVehCmv = document.getElementById('tag-veh-cmv');

    const blinkerLF = document.getElementById('blinker-left-front');
    const blinkerLR = document.getElementById('blinker-left-rear');

    const egoVisionGroup = document.getElementById('ego-vision-group');
    const rearviewCone = document.getElementById('rearview-cone');
    const sideMirrorCone = document.getElementById('side-mirror-cone');
    const blindSpotWedge = document.getElementById('blind-spot-wedge');
    const blindSpotLabel = document.getElementById('blind-spot-label');
    const shoulderCheckBeam = document.getElementById('shoulder-check-beam');
    const shoulderCheckCone = document.getElementById('shoulder-check-cone');
    const shoulderEyeCircle = document.getElementById('shoulder-eye-circle');
    const shoulderEyeText = document.getElementById('shoulder-eye-text');

    const cmvNoZonesGroup = document.getElementById('cmv-no-zones-group');
    const cmvFrontZone = document.getElementById('cmv-front-zone');
    const cmvRearZone = document.getElementById('cmv-rear-zone');
    const cmvLeftZone = document.getElementById('cmv-left-zone');
    const cmvRightZone = document.getElementById('cmv-right-zone');
    const cmvRightText = document.getElementById('cmv-right-text');

    const hazardImpactGroup = document.getElementById('hazard-impact-group');
    const hazardImpactCircle = document.getElementById('hazard-impact-circle');
    const hazardImpactStar = document.getElementById('hazard-impact-star');
    const hazardBanner = document.getElementById('hazard-banner');

    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemInsideMirror = document.getElementById('telem-inside-mirror');
    const telemSideMirror = document.getElementById('telem-side-mirror');
    const telemShoulderCheck = document.getElementById('telem-shoulder-check');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceBadge = document.getElementById('compliance-badge');
    const complianceText = document.getElementById('compliance-text');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Proven Roadway Lane Trajectory Math (Texas 3-Lane Highway Corridor)
    // Lane 1 (South-East / Right Lane): y = 56.66% at x = 50%
    // Lane 2 (Middle Lane): y = 45.46% at x = 50%
    // Lane 3 (North-West / Left Fast Lane): y = 34.26% at x = 50%
    // Slope m = -0.914
    function getLane1Y(x) {{
      return 56.66 - 0.914 * (x - 50.0);
    }}
    function getLane2Y(x) {{
      return 45.46 - 0.914 * (x - 50.0);
    }}
    function getLane3Y(x) {{
      return 34.26 - 0.914 * (x - 50.0);
    }}

    function smoothCos(p) {{
      return 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, p)));
    }}

    // ===============================================================
    // MODE 1: BGE MIRROR FIELD & MANDATORY SHOULDER HEAD-CHECK
    // ===============================================================
    function updateMode1(t) {{
      cmvNoZonesGroup.setAttribute('opacity', '0.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      vehCmv.style.opacity = '0.0';
      egoVisionGroup.setAttribute('opacity', '1.0');

      // Ego Passing Vehicle (Red Sedan) in Lane 2
      const egoX = 38.0 + (t / 8.0) * 26.0; // 38% -> 64%
      let egoLaneY = getLane2Y(egoX);
      let leftBlink = false;

      if (t >= 1.8 && t < 4.8) {{
        leftBlink = true;
      }} else if (t >= 5.5) {{
        // Transitions safely from Lane 2 to Lane 3 after blue car clears
        const p = (t - 5.5) / 1.5;
        const ease = smoothCos(p);
        egoLaneY = (1 - ease) * getLane2Y(egoX) + ease * getLane3Y(egoX);
        leftBlink = (t < 7.0);
      }}

      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoLaneY}}%`;
      vehEgo.style.opacity = '1.0';

      // Trailing Vehicle (Yellow Sedan) in Lane 2 strictly behind Ego (maintains >20% gap)
      const yellowX = egoX - 22.0;
      const yellowY = getLane2Y(yellowX);
      vehYellow.style.left = `${{yellowX}}%`;
      vehYellow.style.top = `${{yellowY}}%`;
      vehYellow.style.opacity = '1.0';
      tagVehYellow.textContent = 'TRAILING CAR (VISIBLE IN REARVIEW)';
      tagVehYellow.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/40 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';

      // Adjacent Vehicle (Blue Sedan) in Lane 3 (Overtaking)
      // At t=0.8s: x=30% (behind ego). At t=2.5s: x=43% (in ego blind spot). At t=4.5s: x=55% (clearing). At t=6.5s: x=82% (far ahead).
      let blueX = 25.0 + (t / 8.0) * 58.0; // 25% -> 83%
      const blueY = getLane3Y(blueX);
      vehBlue.style.left = `${{blueX}}%`;
      vehBlue.style.top = `${{blueY}}%`;
      vehBlue.style.opacity = '1.0';
      tagVehBlue.textContent = (t >= 1.5 && t <= 4.2) ? 'OVERTAKING (IN EGO BLIND SPOT!)' : 'OVERTAKING (LANE 3)';
      tagVehBlue.className = (t >= 1.5 && t <= 4.2)
        ? 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider'
        : 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[9.5px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      // Blinker Flash
      const flash = (Math.sin(t * 14) > 0);
      blinkerLF.style.opacity = (leftBlink && flash) ? '1.0' : '0.0';
      blinkerLR.style.opacity = (leftBlink && flash) ? '1.0' : '0.0';

      // SVG Sightline Cones Math centered on Ego Driver Seat (1024 x 571 viewBox)
      const driverX = egoX * 10.24 - 8;
      const driverY = egoLaneY * 5.71 + 4;

      if (t >= 5.5) {{
        egoVisionGroup.setAttribute('opacity', '0.0');
      }} else {{
        egoVisionGroup.setAttribute('opacity', '1.0');
      }}

      // 1. Center Rearview Mirror Cone (Emerald Green, pointing SW along Lane 2)
      const rvP1x = driverX - 120; const rvP1y = driverY + 75;
      const rvP2x = driverX - 100; const rvP2y = driverY + 35;
      rearviewCone.setAttribute('points', `${{driverX}},${{driverY}} ${{rvP1x}},${{rvP1y}} ${{rvP2x}},${{rvP2y}}`);

      // 2. Side Mirror Field (Cyan Cone, angled outward)
      const smP1x = driverX - 100; const smP1y = driverY + 35;
      const smP2x = driverX - 75;  const smP2y = driverY - 5;
      sideMirrorCone.setAttribute('points', `${{driverX}},${{driverY}} ${{smP1x}},${{smP1y}} ${{smP2x}},${{smP2y}}`);

      // 3. Blind Spot Danger Wedge (Red Hatch, direct B-pillar zone into Lane 3)
      const bsP1x = driverX - 75;  const bsP1y = driverY - 5;
      const bsP2x = driverX - 35;  const bsP2y = driverY - 45;
      blindSpotWedge.setAttribute('points', `${{driverX}},${{driverY}} ${{bsP1x}},${{bsP1y}} ${{bsP2x}},${{bsP2y}}`);

      const midBsX = driverX - 55;
      const midBsY = driverY - 25;
      blindSpotLabel.setAttribute('x', midBsX);
      blindSpotLabel.setAttribute('y', midBsY);
      blindSpotLabel.setAttribute('opacity', (t < 5.0) ? '1.0' : '0.0');

      // 4. Mandatory Shoulder Head-Check Beam (Step 3: t >= 3.8 && t <= 5.2)
      if (t >= 3.8 && t <= 5.2) {{
        shoulderCheckBeam.setAttribute('opacity', '1.0');
        const scP1x = driverX - 75; const scP1y = driverY - 5;
        const scP2x = driverX - 35; const scP2y = driverY - 45;
        shoulderCheckCone.setAttribute('points', `${{driverX}},${{driverY}} ${{scP1x}},${{scP1y}} ${{scP2x}},${{scP2y}}`);
        shoulderEyeCircle.setAttribute('cx', driverX - 22);
        shoulderEyeCircle.setAttribute('cy', driverY - 6);
        shoulderEyeText.setAttribute('x', driverX - 22);
        shoulderEyeText.setAttribute('y', driverY - 2);
      }} else {{
        shoulderCheckBeam.setAttribute('opacity', '0.0');
      }}

      // Dynamic Tag Content & Badges
      if (t < 2.0) {{
        tagVehEgo.textContent = 'EGO: REARVIEW CLEAR • BLIND SPOT UNVERIFIED';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        telemInsideMirror.textContent = 'TRAILING CAR (VISIBLE)';
        telemInsideMirror.className = 'text-emerald-400 font-bold';
        telemSideMirror.textContent = 'EMPTY (BLIND GAP)';
        telemSideMirror.className = 'text-amber-400 font-bold';
        telemShoulderCheck.textContent = 'PENDING';
        telemShoulderCheck.className = 'text-gray-400 font-bold';
        signalStateBadge.innerHTML = 'STATUS: MONITORING';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 mono';
        hudNarrative.textContent = 'Ego car monitors traffic. Rearview mirror clearly reflects trailing traffic, but flat and convex mirrors fail to display the left B-pillar quarter zone.';
      }} else if (t < 3.8) {{
        tagVehEgo.textContent = 'EGO: 100-FT SIGNAL ON • MIRRORS REPORT CLEAR (FALSE!)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#2B1B05]/95 border border-amber-400 text-[9.5px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        telemInsideMirror.textContent = 'CLEAR BEHIND';
        telemInsideMirror.className = 'text-emerald-400 font-bold';
        telemSideMirror.textContent = 'CLEAR (FALSE NEGATIVE!)';
        telemSideMirror.className = 'text-red-400 font-bold';
        telemShoulderCheck.textContent = 'MANDATORY NEXT';
        telemShoulderCheck.className = 'text-amber-400 font-bold';
        signalStateBadge.innerHTML = 'BLIND SPOT: OCCUPIED!';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        hudNarrative.textContent = 'Ego activates left blinker. Both inside and side mirrors show no car in Lane 3. However, an overtaking vehicle is concealed entirely inside the red blind spot!';
      }} else if (t < 5.5) {{
        tagVehEgo.textContent = 'SHOULDER HEAD-CHECK: VEHICLE DETECTED! ABORT SWERVE';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-400 text-[9.5px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        telemInsideMirror.textContent = 'CLEAR BEHIND';
        telemSideMirror.textContent = 'BLIND (HIDDEN)';
        telemShoulderCheck.textContent = 'DETECTED IN BLIND SPOT!';
        telemShoulderCheck.className = 'text-emerald-400 font-black animate-pulse';
        signalStateBadge.innerHTML = 'HEAD-CHECK: SAVED CRASH';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudNarrative.textContent = 'Driver executes mandatory chin-to-shoulder glance. The blue vehicle is immediately spotted in peripheral vision! Ego aborts lateral movement and protects cushion.';
      }} else {{
        tagVehEgo.textContent = 'EGO: THREAT CLEARED • SAFE LANE CHANGE COMPLETE';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        telemInsideMirror.textContent = 'CLEAR';
        telemSideMirror.textContent = 'CLEAR';
        telemShoulderCheck.textContent = 'VERIFIED 100% CLEAR';
        telemShoulderCheck.className = 'text-emerald-400 font-bold';
        signalStateBadge.innerHTML = 'LANE CHANGE: VERIFIED';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudNarrative.textContent = 'The overtaking car safely clears ahead. Ego re-verifies shoulder clearance and transitions smoothly into Lane 3 in full compliance with TTC § 545.060.';
      }}

      tagVehEgo.style.opacity = '1.0';
      tagVehYellow.style.opacity = '1.0';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TEXAS SAFETY STANDARD: ZERO LANE CHANGES WITHOUT SHOULDER HEAD-CHECK';
      complianceText.textContent = 'TTC § 545.060 BLIND SPOT COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 2: COMMERCIAL MOTOR VEHICLE (CMV) "NO-ZONE"
    // ===============================================================
    function updateMode2(t) {{
      egoVisionGroup.setAttribute('opacity', '0.0');
      hazardImpactGroup.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';
      complianceBadge.style.opacity = '1.0';
      cmvNoZonesGroup.setAttribute('opacity', '1.0');
      vehBlue.style.opacity = '0.0';
      vehYellow.style.opacity = '0.0';
      vehCmv.style.opacity = '1.0';

      // Commercial Motor Vehicle (School Bus / CMV) in Lane 2
      const cmvX = 42.0 + (t / 8.0) * 18.0; // 42% -> 60%
      const cmvY = getLane2Y(cmvX);
      vehCmv.style.left = `${{cmvX}}%`;
      vehCmv.style.top = `${{cmvY}}%`;

      // Ego car in Lane 1 (Right Lane)
      let egoX = 44.0;
      if (t < 3.0) {{
        // Cruising alongside in the dangerous Right No-Zone
        egoX = cmvX + 2.0;
      }} else {{
        // Dropping back to re-establish mirror line of sight
        const p = (t - 3.0) / 5.0;
        egoX = (cmvX + 2.0) - p * 18.0;
      }}
      const egoY = getLane1Y(egoX);
      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoY}}%`;
      vehEgo.style.opacity = '1.0';

      blinkerLF.style.opacity = '0.0';
      blinkerLR.style.opacity = '0.0';

      // Draw CMV 4 No-Zones around Bus (1024 x 571)
      const cx = cmvX * 10.24; const cy = cmvY * 5.71;

      // 1. Front No-Zone (20 ft ahead: +60px NE)
      cmvFrontZone.setAttribute('points', `${{cx+35}},${{cy-20}} ${{cx+85}},${{cy-55}} ${{cx+110}},${{cy-40}} ${{cx+60}},${{cy-5}}`);
      
      // 2. Rear No-Zone (200 ft behind: -120px SW)
      cmvRearZone.setAttribute('points', `${{cx-55}},${{cy+35}} ${{cx-160}},${{cy+100}} ${{cx-135}},${{cy+115}} ${{cx-30}},${{cy+50}}`);

      // 3. Left No-Zone (1 lane wide NW into Lane 3)
      cmvLeftZone.setAttribute('points', `${{cx-40}},${{cy+20}} ${{cx-85}},${{cy-10}} ${{cx-25}},${{cy-45}} ${{cx+20}},${{cy-15}}`);

      // 4. Right No-Zone (2 lanes wide SE across Lane 1)
      cmvRightZone.setAttribute('points', `${{cx-20}},${{cy+45}} ${{cx+45}},${{cy+5}} ${{cx+125}},${{cy+55}} ${{cx+60}},${{cy+95}}`);
      cmvRightText.setAttribute('x', cx + 65);
      cmvRightText.setAttribute('y', cy + 68);

      if (t < 3.5) {{
        tagVehEgo.textContent = 'EGO: IN RIGHT NO-ZONE (BUS DRIVER CANNOT SEE YOU!)';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        telemInsideMirror.textContent = 'N/A';
        telemSideMirror.textContent = 'NO-ZONE BLIND!';
        telemSideMirror.className = 'text-red-400 font-bold';
        telemShoulderCheck.textContent = 'DANGER: IN CMV NO-ZONE';
        telemShoulderCheck.className = 'text-red-400 font-black animate-pulse';
        signalStateBadge.innerHTML = 'CMV NO-ZONE: CRITICAL';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';
        hudNarrative.textContent = 'Rule: If you cannot see the driver’s face in their side mirror, they CANNOT see you! The right side No-Zone extends across 2 full lanes and is extremely dangerous.';
      }} else {{
        tagVehEgo.textContent = 'EGO: DROPPING BACK TO RESTORE MIRROR SIGHTLINE';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[9.5px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        telemInsideMirror.textContent = 'N/A';
        telemSideMirror.textContent = 'CMV MIRROR VISIBLE';
        telemSideMirror.className = 'text-emerald-400 font-bold';
        telemShoulderCheck.textContent = 'CLEAR LINE-OF-SIGHT';
        telemShoulderCheck.className = 'text-emerald-400 font-bold';
        signalStateBadge.innerHTML = 'NO-ZONE: EVACUATED';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';
        hudNarrative.textContent = 'Ego decelerates slightly, safely exiting the CMV blind zone. Ego establishes clear visual contact with the driver’s side mirror, restoring statutory cushion.';
      }}

      tagVehEgo.style.opacity = '1.0';

      hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'TEXAS CMV SAFETY RULE: STAY OUT OF THE 4 NO-ZONES (FRONT, REAR, SIDES)';
      complianceText.textContent = 'TEXAS CMV NO-ZONE COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (BLIND SIDESWIPE COLLISION)
    // ===============================================================
    function updateMode3(t) {{
      cmvNoZonesGroup.setAttribute('opacity', '0.0');
      complianceBadge.style.opacity = '0.0';
      vehCmv.style.opacity = '0.0';
      egoVisionGroup.setAttribute('opacity', '1.0');

      // Trailing vehicle in Lane 2
      const yellowX = 22.0 + (t / 8.0) * 26.0;
      const yellowY = getLane2Y(yellowX);
      vehYellow.style.left = `${{yellowX}}%`;
      vehYellow.style.top = `${{yellowY}}%`;
      vehYellow.style.opacity = '1.0';

      // Blue car in Lane 3 cruising alongside
      const blueX = 38.0 + (t / 8.0) * 26.0;
      const blueY = getLane3Y(blueX);
      vehBlue.style.left = `${{blueX}}%`;
      vehBlue.style.top = `${{blueY}}%`;
      vehBlue.style.opacity = '1.0';

      // Ego car in Lane 2, cuts blindly into Lane 3 without shoulder check
      const egoX = 40.0 + (t / 8.0) * 26.0;
      let egoLaneY = getLane2Y(egoX);
      let leftBlink = false;

      if (t >= 1.5 && t < 3.2) {{
        leftBlink = true;
      }} else if (t >= 3.2) {{
        leftBlink = true;
        const p = Math.min(1.0, (t - 3.2) / 1.0);
        const ease = smoothCos(p);
        egoLaneY = (1 - ease) * getLane2Y(egoX) + ease * getLane3Y(egoX); // cuts directly into Lane 3
      }}

      vehEgo.style.left = `${{egoX}}%`;
      vehEgo.style.top = `${{egoLaneY}}%`;
      vehEgo.style.opacity = '1.0';

      const flash = (Math.sin(t * 14) > 0);
      blinkerLF.style.opacity = (leftBlink && flash) ? '1.0' : '0.0';
      blinkerLR.style.opacity = (leftBlink && flash) ? '1.0' : '0.0';

      // Sightline cones
      const driverX = egoX * 10.24 - 8;
      const driverY = egoLaneY * 5.71 + 4;
      const rvP1x = driverX - 120; const rvP1y = driverY + 75;
      const rvP2x = driverX - 100; const rvP2y = driverY + 35;
      rearviewCone.setAttribute('points', `${{driverX}},${{driverY}} ${{rvP1x}},${{rvP1y}} ${{rvP2x}},${{rvP2y}}`);
      const smP1x = driverX - 100; const smP1y = driverY + 35;
      const smP2x = driverX - 75;  const smP2y = driverY - 5;
      sideMirrorCone.setAttribute('points', `${{driverX}},${{driverY}} ${{smP1x}},${{smP1y}} ${{smP2x}},${{smP2y}}`);
      const bsP1x = driverX - 75;  const bsP1y = driverY - 5;
      const bsP2x = driverX - 35;  const bsP2y = driverY - 45;
      blindSpotWedge.setAttribute('points', `${{driverX}},${{driverY}} ${{bsP1x}},${{bsP1y}} ${{bsP2x}},${{bsP2y}}`);
      shoulderCheckBeam.setAttribute('opacity', '0.0'); // NEVER CHECKS SHOULDER!

      if (t >= 3.8) {{
        egoVisionGroup.setAttribute('opacity', '0.0');
        tagVehEgo.style.opacity = '0.0';
        tagVehBlue.style.opacity = '0.0';
        tagVehYellow.style.opacity = '0.0';
        hazardImpactGroup.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';

        const impX = ((egoX + blueX) / 2) * 10.24;
        const impY = ((egoLaneY + blueY) / 2) * 5.71;
        hazardImpactCircle.setAttribute('cx', impX);
        hazardImpactCircle.setAttribute('cy', impY);
        hazardImpactStar.setAttribute('transform', `translate(${{impX}}, ${{impY}})`);

        signalStateBadge.innerHTML = 'VIOLATION: SIDESWIPE';
        signalStateBadge.className = 'text-[8.5px] font-extrabold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        telemInsideMirror.textContent = 'REPORTED CLEAR';
        telemSideMirror.textContent = 'REPORTED CLEAR';
        telemShoulderCheck.textContent = 'OMITTED (CRITICAL ERROR!)';
        telemShoulderCheck.className = 'text-red-500 font-black animate-pulse';

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ CRITICAL HAZARD: SIDESWIPE CRASH FROM UNCHECKED BLIND SPOT ✕';
        hudNarrative.textContent = 'FATAL ERROR: Relying solely on mirrors without a chin-to-shoulder glance violates TTC § 545.060 and causes severe highway sideswipe collisions.';
      }} else {{
        tagVehEgo.style.opacity = '1.0';
        tagVehBlue.style.opacity = '1.0';
        tagVehYellow.style.opacity = '1.0';
        hazardImpactGroup.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';
        tagVehEgo.textContent = 'EGO: INITIATING LANE CHANGE WITHOUT HEAD-CHECK...';
        tagVehEgo.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';
        tagVehBlue.textContent = 'OVERTAKING (TRAPPED IN BLIND SPOT)';
        tagVehBlue.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/95 border border-red-500 text-[9.5px] font-bold text-red-300 mono shadow-lg tracking-wider';

        hudStatusPill.className = 'absolute z-25 px-3 py-1 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[9.5px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'WARNING: LANE CHANGE INITIATED WITHOUT PHYSICAL SHOULDER GLANCE';
      }}
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
          if (stepNum === 1 && t < 1.8) active = true;
          else if (stepNum === 2 && t >= 1.8 && t < 3.8) active = true;
          else if (stepNum === 3 && t >= 3.8 && t < 5.5) active = true;
          else if (stepNum === 4 && t >= 5.5) active = true;
        }} else if (currentMode === 2) {{
          if (stepNum === 1 && t < 2.0) active = true;
          else if (stepNum === 2 && t >= 2.0 && t < 4.0) active = true;
          else if (stepNum === 3 && t >= 4.0 && t < 6.0) active = true;
          else if (stepNum === 4 && t >= 6.0) active = true;
        }} else if (currentMode === 3) {{
          if (stepNum === 1 && t < 1.8) active = true;
          else if (stepNum === 2 && t >= 1.8 && t < 3.5) active = true;
          else if (stepNum === 3 && t >= 3.5 && t < 5.5) active = true;
          else if (stepNum === 4 && t >= 5.5) active = true;
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
        'Mirror Cone vs. Blind Spot',
        '100-Ft Signal & Mirror Check',
        'Chin-to-Shoulder Head-Check',
        'Cushion Maintained & Safe Entry'
      ],
      2: [
        'CMV 4 No-Zones Identified',
        'Right No-Zone Danger Zone',
        'Drop Back to Restore Sightline',
        'CMV Cushion Re-established'
      ],
      3: [
        'Mirror-Only Complacency',
        'Lane Departure without Glance',
        'Blind Sideswipe Impact',
        'TTC § 545.060 Violation'
      ]
    }};

    // Mode Switching
    function setMode(mode) {{
      currentMode = mode;
      currentTime = 0.0;
      isPlaying = true;
      playIcon.classList.add('hidden');
      pauseIcon.classList.remove('hidden');

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
        if (s === 1) targetTime = 0.8;
        else if (s === 2) targetTime = 2.5;
        else if (s === 3) targetTime = 4.5;
        else if (s === 4) targetTime = 6.5;
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
</html>'''

out_path = 'driving_rule_animations_suite/simulations/L05_T05_blind_spot_driving.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 14 simulation rebuilt successfully at: {out_path}")
