import os
import base64

# Base paths
diorama_path = 'driving_rule_animations/asset_library/roads/uncontrolled_intersection_final.png'
car_red_path = 'driving_rule_animations/asset_library/vehicles/car_red_clean_ne.png'
car_blue_path = 'driving_rule_animations/asset_library/vehicles/car_blue_clean_nw.png'

print("Encoding Lesson 11 assets to base64...")
with open(diorama_path, 'rb') as f:
    diorama_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

with open(car_red_path, 'rb') as f:
    car_red_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

with open(car_blue_path, 'rb') as f:
    car_blue_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>L05-T02: Managing Traffic Flow — Hierarchy of Traffic Control &amp; Police Preemption</title>
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
    .glow-pulse-red {{
      animation: pulseRed 1.2s infinite ease-in-out;
    }}
    @keyframes pulseRed {{
      0%, 100% {{ filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.9)); }}
      50% {{ filter: drop-shadow(0 0 22px rgba(239, 68, 68, 1.0)); }}
    }}
    .glow-pulse-green {{
      animation: pulseGreen 1.2s infinite ease-in-out;
    }}
    @keyframes pulseGreen {{
      0%, 100% {{ filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.9)); }}
      50% {{ filter: drop-shadow(0 0 22px rgba(16, 185, 129, 1.0)); }}
    }}
    .pulse-danger {{
      animation: pulseDanger 0.8s infinite alternate;
    }}
    @keyframes pulseDanger {{
      0% {{ transform: scale(1.0); opacity: 0.85; }}
      100% {{ transform: scale(1.08); opacity: 1.0; }}
    }}
    .wave-pulse {{
      animation: waveExpand 1.4s infinite ease-out;
    }}
    @keyframes waveExpand {{
      0% {{ transform: scale(0.6); opacity: 1.0; }}
      100% {{ transform: scale(1.8); opacity: 0.0; }}
    }}
  </style>
</head>
<body class="w-screen h-screen overflow-hidden flex flex-col justify-between p-3 bg-[#0B0E14]">

  <!-- TOP HEADER / METADATA -->
  <header class="flex items-center justify-between px-3 py-1.5 bg-[#121620] border border-[#212836] rounded-xl shadow-md z-30">
    <div>
      <div class="flex items-center space-x-2">
        <span class="text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 mono">TDLR ADE-1317 • 2.5D VECTOR ENGINE</span>
        <span class="text-[10px] text-gray-400 mono">LESSON 11</span>
      </div>
      <h1 class="text-sm font-black text-white tracking-tight flex items-center space-x-2">
        <span>L05-T02: Managing Traffic Flow — Hierarchy of Traffic Control &amp; Police Preemption</span>
      </h1>
      <p class="text-[10px] text-gray-400 mono">Texas Transportation Code &sect; 544.004 &bull; &sect; 542.501 &bull; &sect; 544.007</p>
    </div>

    <!-- Multi-Scenario Mode Selector -->
    <div class="flex items-center space-x-2 bg-[#171C26] p-1 rounded-lg border border-[#283244] text-xs">
      <button id="mode-btn-1" class="mode-btn px-3 py-1 rounded font-bold transition text-black bg-emerald-400 shadow" data-mode="1">
        1: Automated Signal (Steady Red Halt)
      </button>
      <button id="mode-btn-2" class="mode-btn px-3 py-1 rounded font-semibold text-gray-400 hover:text-white transition" data-mode="2">
        2: Police Preemption (Officer Overrules Red)
      </button>
      <button id="mode-btn-3" class="mode-btn px-3 py-1 rounded font-semibold text-red-400 hover:text-red-300 transition" data-mode="3">
        Hazard: Disregarding Officer Signal
      </button>
      <div class="h-4 w-px bg-gray-700 mx-1"></div>
      <label class="flex items-center space-x-1.5 text-xs text-gray-300 cursor-pointer pr-1">
        <input type="checkbox" id="auto-loop-toggle" checked class="rounded border-gray-700 text-blue-500 focus:ring-0">
        <span class="mono text-[11px]">Auto-Loop</span>
      </label>
    </div>
  </header>

  <!-- CANONICAL 4-STEP STEPPER -->
  <nav class="grid grid-cols-4 gap-2 my-1 z-30">
    <button data-step="1" class="step-btn px-2.5 py-1.5 rounded-lg border border-blue-500/60 bg-blue-500/15 text-left transition shadow">
      <div class="text-[9px] mono text-blue-400 font-bold uppercase tracking-wider">STEP 1</div>
      <div id="step-label-1" class="text-[11px] font-extrabold text-white truncate">Approach &amp; Deceleration</div>
    </button>
    <button data-step="2" class="step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 2</div>
      <div id="step-label-2" class="text-[11px] font-extrabold text-gray-300 truncate">Statutory Halt at Stop Bar</div>
    </button>
    <button data-step="3" class="step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 3</div>
      <div id="step-label-3" class="text-[11px] font-extrabold text-gray-300 truncate">Preemption / Clearance</div>
    </button>
    <button data-step="4" class="step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600">
      <div class="text-[9px] mono text-gray-500 font-bold uppercase tracking-wider">STEP 4</div>
      <div id="step-label-4" class="text-[11px] font-extrabold text-gray-300 truncate">Lawful Traversal &amp; Exit</div>
    </button>
  </nav>

  <!-- MAIN SIMULATION VIEWPORT -->
  <main class="relative flex-1 w-full bg-[#0E121A] rounded-xl border border-[#1E2634] overflow-hidden flex items-center justify-center shadow-inner min-h-0">
    
    <!-- 35° ARCHITECTURAL ISOMETRIC STAGE -->
    <div id="isometric-stage" class="relative overflow-hidden shadow-2xl rounded-lg" style="height: calc(100% - 16px); aspect-ratio: 1024 / 667; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: Empty 4-Way Roadway Intersection Diorama Base -->
      <img src="{diorama_b64}" alt="Texas Roadway Intersection Diorama Base" class="absolute inset-0 w-full h-full object-cover pointer-events-none select-none z-0" />

      <!-- LAYER 1: SVG TRAFFIC OVERLAYS & SIGNALS -->
      <svg id="stage-svg-overlay" class="absolute inset-0 w-full h-full z-10 pointer-events-none" viewBox="0 0 1024 667">
        <defs>
          <filter id="glow-red" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="glow-green" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <marker id="arrow-head-blue" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 6 3, 0 6" fill="#38BDF8" />
          </marker>
        </defs>

        <!-- Advance White Stop Bars on Approaches -->
        <!-- SW Stop Line (Ego Approach: 34.0%, 72.0%) -->
        <line x1="322" y1="510" x2="394" y2="470" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.95" />
        <!-- SE Stop Line (Cross-Traffic Approach: 65.0%, 69.0%) -->
        <line x1="630" y1="470" x2="702" y2="510" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.95" />
        <line x1="320" y1="210" x2="390" y2="250" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" opacity="0.75" />
        <line x1="630" y1="250" x2="700" y2="210" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" opacity="0.75" />

        <!-- SW Traffic Stop Threshold Zone -->
        <g id="box-hold-sw" opacity="0.0">
          <polygon points="322,510 394,470 364,450 292,490" fill="#10B981" fill-opacity="0.25" stroke="#10B981" stroke-width="1.5" stroke-dasharray="4,4" />
        </g>

        <!-- =============================================================== -->
        <!-- TRAFFIC SIGNAL MAST HEADS                                       -->
        <!-- =============================================================== -->
        <!-- SW Signal Mast (Facing Ego Vehicle on SW Approach) -->
        <g id="mast-sw" transform="translate(303, 496)">
          <line x1="0" y1="22" x2="0" y2="45" stroke="#374151" stroke-width="3" />
          <rect x="-8" y="-22" width="16" height="44" rx="3.5" fill="#111827" stroke="#374151" stroke-width="1.5" />
          <!-- Red Lens (Top) -->
          <circle id="sw-lens-red" cx="0" cy="-12" r="5" fill="#EF4444" opacity="1.0" filter="url(#glow-red)" />
          <!-- Yellow Lens (Middle) -->
          <circle id="sw-lens-yellow" cx="0" cy="0" r="5" fill="#1F2937" opacity="0.25" />
          <!-- Green Lens (Bottom) -->
          <circle id="sw-lens-green" cx="0" cy="12" r="5" fill="#1F2937" opacity="0.25" />
        </g>

        <!-- SE Signal Mast (Facing Cross Traffic on SE Approach) -->
        <g id="mast-se" transform="translate(699, 496)">
          <line x1="0" y1="22" x2="0" y2="45" stroke="#374151" stroke-width="3" />
          <rect x="-8" y="-22" width="16" height="44" rx="3.5" fill="#111827" stroke="#374151" stroke-width="1.5" />
          <circle id="se-lens-red" cx="0" cy="-12" r="5" fill="#1F2937" opacity="0.25" />
          <circle id="se-lens-yellow" cx="0" cy="0" r="5" fill="#1F2937" opacity="0.25" />
          <circle id="se-lens-green" cx="0" cy="12" r="5" fill="#10B981" opacity="1.0" filter="url(#glow-green)" />
        </g>

        <!-- =============================================================== -->
        <!-- UNIFORMED POLICE OFFICER (Intersection Center: 512, 375)         -->
        <!-- =============================================================== -->
        <g id="police-officer-group" opacity="0.0" transform="translate(512, 375)">
          <!-- Ground Shadow -->
          <ellipse cx="0" cy="16" rx="14" ry="6" fill="#000000" opacity="0.35" />
          
          <!-- Animated Radar / Gesture Wave Ring -->
          <circle id="officer-wave-ring" cx="0" cy="4" r="18" fill="none" stroke="#38BDF8" stroke-width="2" class="wave-pulse" opacity="0.0" />

          <!-- Trousers / Boots -->
          <rect x="-5" y="4" width="4" height="12" fill="#0F172A" rx="1" />
          <rect x="1" y="4" width="4" height="12" fill="#0F172A" rx="1" />

          <!-- Torso with High-Vis ANSI Yellow Safety Vest -->
          <polygon points="-7,-7 7,-7 6,5 -6,5" fill="#EAB308" stroke="#CA8A04" stroke-width="0.8" />
          <!-- Reflective Silver Stripes -->
          <line x1="-6" y1="-1" x2="6" y2="-1" stroke="#FFFFFF" stroke-width="1.2" />
          <line x1="-6" y1="3" x2="6" y2="3" stroke="#FFFFFF" stroke-width="1.2" />

          <!-- Arms / Gesturing Hand -->
          <!-- Left Arm at side -->
          <line x1="-6" y1="-5" x2="-8" y2="2" stroke="#0F172A" stroke-width="2" stroke-linecap="round" />
          <!-- Right Arm (Preemption Gesture) -->
          <g id="officer-arm-proceed">
            <line x1="6" y1="-5" x2="14" y2="-2" stroke="#0F172A" stroke-width="2.2" stroke-linecap="round" />
            <!-- White Glove Hand -->
            <circle cx="15" cy="-2" r="2" fill="#FFFFFF" />
            <!-- Motion Wave Arc -->
            <path d="M 18 -6 Q 24 -1, 18 5" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-dasharray="3,2" />
          </g>
          <g id="officer-arm-stop" opacity="0.0">
            <line x1="6" y1="-5" x2="12" y2="-12" stroke="#0F172A" stroke-width="2.2" stroke-linecap="round" />
            <circle cx="12" cy="-13" r="2.5" fill="#EF4444" stroke="#FFFFFF" stroke-width="0.8" />
          </g>

          <!-- Head & Police Duty Cap -->
          <circle cx="0" cy="-12" r="4.5" fill="#FCD34D" />
          <ellipse cx="0" cy="-15" rx="5.5" ry="2" fill="#1E293B" />
          <polygon points="-4.5,-15 4.5,-15 3.5,-18 -3.5,-18" fill="#1E293B" />
          <circle cx="0" cy="-15.5" r="1" fill="#F59E0B" />

          <!-- Officer Directive Callout Badge -->
          <g id="officer-badge-proceed" transform="translate(0, -32)">
            <rect x="-65" y="-11" width="130" height="18" rx="4" fill="#0B132B" fill-opacity="0.95" stroke="#38BDF8" stroke-width="1.2" />
            <text x="0" y="2" fill="#38BDF8" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">OFFICER: PROCEED THROUGH RED</text>
          </g>
          <g id="officer-badge-stop" opacity="0.0" transform="translate(0, -32)">
            <rect x="-65" y="-11" width="130" height="18" rx="4" fill="#2B0505" fill-opacity="0.95" stroke="#EF4444" stroke-width="1.2" />
            <text x="0" y="2" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" text-anchor="middle">OFFICER: HALT / MUST STOP</text>
          </g>
        </g>

        <!-- Traversal Indicator Arrow for Ego Vehicle -->
        <g id="traversal-path-group" opacity="0.0">
          <path id="traversal-arrow-path" d="M 370 480 Q 440 430, 510 385" fill="none" stroke="#38BDF8" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-head-blue)" />
        </g>

        <!-- HAZARD DEMO: CRITICAL CONFLICT ZONE -->
        <g id="hazard-conflict-zone" opacity="0.0">
          <circle cx="512" cy="385" r="50" fill="#EF4444" fill-opacity="0.25" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" class="pulse-danger" />
          <polygon points="512,360 522,378 542,375 527,390 537,410 512,398 487,410 497,390 482,375 502,378" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES & NON-OVERLAPPING IDENTIFICATION BADGES -->

      <!-- EGO VEHICLE (Red Sedan, Traveling SW to NE) -->
      <div id="veh-a-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 18.0%; top: 85.0%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Ego Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Glowing Brake Lights -->
          <div id="veh-a-brake-1" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 18%; left: 16%;"></div>
          <div id="veh-a-brake-2" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 27%; left: 30%;"></div>
        </div>

        <!-- Disjoint Badge for Ego Vehicle -->
        <div id="tag-veh-a" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          EGO VEHICLE (APPROACHING)
        </div>
      </div>

      <!-- CROSS-TRAFFIC VEHICLE (Blue Sedan, Traveling SE to NW) -->
      <div id="veh-b-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 82.0%; top: 82.0%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_b64}" alt="Cross Vehicle" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Glowing Brake Lights -->
          <div id="veh-b-brake-1" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="top: 24%; right: 18%;"></div>
          <div id="veh-b-brake-2" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="top: 32%; right: 28%;"></div>
        </div>

        <div id="tag-veh-b" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          CROSS TRAFFIC
        </div>
      </div>

      <!-- LAYER 3: TOP-RIGHT STATUS NOTIFICATION PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 10px; right: 10px;">
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
        <span id="pill-status-text">STEADY RED SIGNAL ACTIVE: STATUTORY HALT MANDATORY</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div class="absolute bottom-2.5 right-2.5 z-25 px-3 py-1.5 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[10px] font-bold shadow-lg tracking-wider flex items-center space-x-2 pointer-events-none">
        <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TTC &sect; 544.004 COMPLIANCE VERIFIED</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER -->
      <div id="hazard-banner" class="absolute bottom-14 left-1/2 -translate-x-1/2 z-30 px-5 py-2 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300" style="opacity: 0.0;">
        <div class="text-xs font-black tracking-widest text-red-400 flex items-center justify-center space-x-1.5">
          <span>&#9888;</span>
          <span>CRITICAL STATUTORY VIOLATION</span>
          <span>&#9888;</span>
        </div>
        <div class="text-xs font-bold text-white">DISREGARDING LAWFUL POLICE OFFICER DIRECTION</div>
        <div class="text-[10px] text-red-300">
          TTC &sect; 542.501: Police officer hand signals strictly override automated green signals!<br>
          Accelerating into officer's stop gesture causes catastrophic intersection conflict.
        </div>
      </div>

      <!-- LAYER 4: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
      <div id="telemetry-hud-card" class="absolute top-2.5 left-2.5 z-30 max-w-[280px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-2 space-y-1 shadow-xl pointer-events-none">
        <div class="flex items-center justify-between border-b border-[#222B38] pb-1">
          <span class="text-[10px] font-bold text-gray-400 mono uppercase tracking-wider">Control Hierarchy</span>
          <span id="signal-state-badge" class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono">
            SIGNAL: STEADY RED
          </span>
        </div>

        <div class="space-y-0.5 text-xs mono">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Ego Speed:</span>
            <span id="telem-veh-a" class="text-emerald-400 font-bold">25 MPH (DECEL)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Officer Authority:</span>
            <span id="telem-officer" class="text-gray-400 font-bold">NONE PRESENT</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Supreme Order:</span>
            <span id="telem-precedence" class="text-red-400 font-bold">DEVICE: STOP BAR HALT</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Mandate:</span>
            <span id="telem-statute" class="text-emerald-300 font-bold">TTC &sect; 544.004 BASELINE</span>
          </div>
        </div>

        <div class="pt-1 border-t border-[#1F2633] text-[10px] text-gray-300 leading-snug font-sans" id="hud-narrative">
          Automated traffic control devices establish the statutory baseline. Facing a steady red light, drivers must halt before the stop line.
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM SCRUBBABLE TIMELINE & PLAYBACK CONTROLS -->
  <footer class="bg-[#121620] border border-[#212836] rounded-xl px-4 py-2.5 shadow-lg flex flex-col gap-2 mt-1 z-30">
    <div class="flex items-center space-x-3">
      <!-- Play/Pause Button -->
      <button id="play-pause-btn" class="w-8 h-8 rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center font-bold shadow transition">
        <svg id="play-icon" class="w-4 h-4 fill-current hidden" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        <svg id="pause-icon" class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
      </button>

      <!-- Reset Button -->
      <button id="reset-btn" class="w-8 h-8 rounded-lg bg-[#1C2331] hover:bg-[#252F42] text-gray-300 flex items-center justify-center transition border border-[#2B3548]">
        <svg class="w-4 h-4 stroke-current fill-none" viewBox="0 0 24 24" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
      </button>

      <!-- Time Display -->
      <span id="time-display" class="mono text-xs text-blue-400 font-bold w-12">0.00s</span>

      <!-- Scrubber Slider -->
      <div class="flex-1 relative flex items-center">
        <input type="range" id="timeline-slider" min="0" max="8.0" step="0.01" value="0" class="w-full h-1.5 bg-[#212836] rounded-lg appearance-none cursor-pointer accent-blue-500" />
      </div>

      <span class="mono text-xs text-gray-400">8.00s</span>

      <!-- Speed Selector -->
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
        <span id="keyframe-1-text">0.8s Red Signal Perception</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-2-text">2.5s Statutory Stop Bar Halt</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-3-text">4.8s Preemption / Clearance</span>
      </span>
      <span class="flex items-center space-x-1">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span id="keyframe-4-text">6.8s Lawful Traversal</span>
      </span>
      <span class="text-blue-400 font-semibold" id="legend-statute">TTC &sect; 544.004 Hierarchy</span>
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
    let currentMode = 1; // 1: Automated Baseline, 2: Police Preemption, 3: Hazard Non-Compliance
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

    const vehA = document.getElementById('veh-a-container');
    const vehB = document.getElementById('veh-b-container');
    const tagVehA = document.getElementById('tag-veh-a');
    const tagVehB = document.getElementById('tag-veh-b');
    const brakeA1 = document.getElementById('veh-a-brake-1');
    const brakeA2 = document.getElementById('veh-a-brake-2');
    const brakeB1 = document.getElementById('veh-b-brake-1');
    const brakeB2 = document.getElementById('veh-b-brake-2');

    // Signal Heads
    const swLensRed = document.getElementById('sw-lens-red');
    const swLensYellow = document.getElementById('sw-lens-yellow');
    const swLensGreen = document.getElementById('sw-lens-green');
    const seLensRed = document.getElementById('se-lens-red');
    const seLensYellow = document.getElementById('se-lens-yellow');
    const seLensGreen = document.getElementById('se-lens-green');

    // Police Officer Elements
    const policeOfficerGroup = document.getElementById('police-officer-group');
    const officerArmProceed = document.getElementById('officer-arm-proceed');
    const officerArmStop = document.getElementById('officer-arm-stop');
    const officerBadgeProceed = document.getElementById('officer-badge-proceed');
    const officerBadgeStop = document.getElementById('officer-badge-stop');
    const officerWaveRing = document.getElementById('officer-wave-ring');

    const boxHoldSW = document.getElementById('box-hold-sw');
    const traversalPathGroup = document.getElementById('traversal-path-group');
    const hazardConflictZone = document.getElementById('hazard-conflict-zone');
    const hazardBanner = document.getElementById('hazard-banner');

    // Telemetry & Badges
    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemVehA = document.getElementById('telem-veh-a');
    const telemOfficer = document.getElementById('telem-officer');
    const telemPrecedence = document.getElementById('telem-precedence');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceText = document.getElementById('compliance-text');

    const modeBtns = document.querySelectorAll('.mode-btn');
    const stepBtns = document.querySelectorAll('.step-btn');
    const speedBtns = document.querySelectorAll('.speed-btn');

    // Smooth Cosine Interpolation
    function smoothCos(p) {{
      return 0.5 * (1 - Math.cos(Math.PI * Math.max(0, Math.min(1, p))));
    }}

    // ===============================================================
    // MODE 1: AUTOMATED SIGNAL BASELINE (STEADY RED HALT -> GREEN)
    // ===============================================================
    function updateMode1(t) {{
      policeOfficerGroup.setAttribute('opacity', '0.0');
      hazardConflictZone.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';

      // Signal timing: Steady Red for t < 5.0, then Green for t >= 5.0
      const isRed = (t < 5.0);
      swLensRed.setAttribute('opacity', isRed ? '1.0' : '0.25');
      swLensRed.setAttribute('filter', isRed ? 'url(#glow-red)' : 'none');
      swLensGreen.setAttribute('opacity', isRed ? '0.25' : '1.0');
      swLensGreen.setAttribute('filter', isRed ? 'none' : 'url(#glow-green)');

      seLensGreen.setAttribute('opacity', isRed ? '1.0' : '0.25');
      seLensGreen.setAttribute('filter', isRed ? 'url(#glow-green)' : 'none');
      seLensRed.setAttribute('opacity', isRed ? '0.25' : '1.0');
      seLensRed.setAttribute('filter', isRed ? 'none' : 'url(#glow-red)');

      signalStateBadge.innerHTML = isRed ? 'SIGNAL: STEADY RED' : 'SIGNAL: GREEN';
      signalStateBadge.className = isRed 
        ? 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono'
        : 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';

      // Ego Vehicle (Red Sedan, SW to NE)
      let aX = 18.0, aY = 85.0, aSpeed = 25, brakeGlowA = 0.0;
      if (t < 2.0) {{
        const p = t / 2.0;
        const ease = smoothCos(p);
        aX = 18.0 + ease * (34.0 - 18.0);
        aY = 85.0 - ease * (85.0 - 72.0);
        aSpeed = Math.round(25 * (1 - p));
        brakeGlowA = (p > 0.3) ? 1.0 : 0.0;
        tagVehA.textContent = `EGO: BRAKING (${{aSpeed}} MPH)`;
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else if (t < 5.2) {{
        aX = 34.0; aY = 72.0; aSpeed = 0; brakeGlowA = 1.0;
        tagVehA.textContent = 'EGO: STOPPED AT RED LIGHT (0 MPH)';
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else {{
        const p = (t - 5.2) / (8.0 - 5.2);
        const ease = smoothCos(p);
        aX = 34.0 + ease * (72.0 - 34.0);
        aY = 72.0 - ease * (72.0 - 41.0);
        aSpeed = Math.round(ease * 24);
        brakeGlowA = 0.0;
        tagVehA.textContent = `EGO: GREEN LIGHT TRAVERSAL (${{aSpeed}} MPH)`;
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }}

      // Cross Traffic (Blue Sedan, SE to NW)
      let bX = 82.0, bY = 82.0, bSpeed = 24;
      tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
      if (t < 1.0) {{
        bX = 82.0; bY = 82.0; bSpeed = 24;
        tagVehB.textContent = 'CROSS TRAFFIC (GREEN PHASE)';
      }} else if (t < 4.8) {{
        const p = (t - 1.0) / (4.8 - 1.0);
        const ease = smoothCos(p);
        bX = 82.0 - ease * (82.0 - 24.0);
        bY = 82.0 - ease * (82.0 - 37.0);
        bSpeed = 24;
        tagVehB.textContent = 'CROSS TRAFFIC: CLEARING (24 MPH)';
      }} else {{
        bX = 24.0; bY = 37.0; bSpeed = 0;
        tagVehB.textContent = 'CROSS TRAFFIC: CLEARED';
      }}

      vehA.style.left = `${{aX}}%`; vehA.style.top = `${{aY}}%`;
      vehB.style.left = `${{bX}}%`; vehB.style.top = `${{bY}}%`;
      vehA.style.opacity = '1.0'; vehB.style.opacity = '1.0';
      tagVehA.style.opacity = '1.0'; tagVehB.style.opacity = (t < 5.5) ? '1.0' : '0.0';

      brakeA1.style.opacity = brakeGlowA; brakeA2.style.opacity = brakeGlowA;
      brakeB1.style.opacity = '0.0'; brakeB2.style.opacity = '0.0';

      boxHoldSW.setAttribute('opacity', (t >= 2.0 && t <= 5.2) ? '1.0' : '0.0');
      traversalPathGroup.setAttribute('opacity', (t >= 5.2 && t <= 7.2) ? '1.0' : '0.0');

      // Telemetry
      telemVehA.innerHTML = `${{aSpeed}} MPH (${{aSpeed === 0 ? 'STOPPED AT LINE' : 'MOVING'}})`;
      telemVehA.className = (aSpeed === 0) ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold';
      telemOfficer.innerHTML = 'NONE (ELECTRONIC DEVICE GOVERNS)';
      telemOfficer.className = 'text-gray-400 font-bold';
      telemPrecedence.innerHTML = isRed ? 'DEVICE: STEADY RED STOP' : 'DEVICE: GREEN PROCEED';
      telemPrecedence.className = isRed ? 'text-red-400 font-bold' : 'text-emerald-400 font-bold';
      telemStatute.innerHTML = 'TTC &sect; 544.004 BASELINE';

      if (isRed) {{
        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'STEADY RED SIGNAL ACTIVE: STATUTORY HALT MANDATORY';
        hudNarrative.textContent = 'Traffic control devices govern the baseline. Facing steady red, TTC § 544.007 requires complete halt before the stop line.';
      }} else {{
        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#062418]/95 border border-emerald-500 text-emerald-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'GREEN SIGNAL: LAWFUL PROCEED & TRAVERSAL';
        hudNarrative.textContent = 'With electronic green indication illuminated, vehicle accelerates safely across intersection pursuant to TTC § 544.007.';
      }}
    }}

    // ===============================================================
    // MODE 2: POLICE PREEMPTION (OFFICER OVERRULES STEADY RED LIGHT)
    // ===============================================================
    function updateMode2(t) {{
      hazardConflictZone.setAttribute('opacity', '0.0');
      hazardBanner.style.opacity = '0.0';

      // Signal stays permanently STEADY RED to prove officer override!
      swLensRed.setAttribute('opacity', '1.0');
      swLensRed.setAttribute('filter', 'url(#glow-red)');
      swLensGreen.setAttribute('opacity', '0.25');
      swLensGreen.setAttribute('filter', 'none');

      seLensRed.setAttribute('opacity', '1.0');
      seLensRed.setAttribute('filter', 'url(#glow-red)');
      seLensGreen.setAttribute('opacity', '0.25');
      seLensGreen.setAttribute('filter', 'none');

      signalStateBadge.innerHTML = 'SIGNAL: RED (OVERRULED)';
      signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

      // Police Officer active in intersection center
      policeOfficerGroup.setAttribute('opacity', '1.0');
      officerArmProceed.setAttribute('opacity', '1.0');
      officerArmStop.setAttribute('opacity', '0.0');
      officerBadgeProceed.setAttribute('opacity', '1.0');
      officerBadgeStop.setAttribute('opacity', '0.0');
      officerWaveRing.setAttribute('opacity', '1.0');

      // Ego Vehicle (Red Sedan, SW to NE)
      let aX = 18.0, aY = 85.0, aSpeed = 25, brakeGlowA = 0.0;
      if (t < 2.0) {{
        const p = t / 2.0;
        const ease = smoothCos(p);
        aX = 18.0 + ease * (34.0 - 18.0);
        aY = 85.0 - ease * (85.0 - 72.0);
        aSpeed = Math.round(25 * (1 - p));
        brakeGlowA = (p > 0.3) ? 1.0 : 0.0;
        tagVehA.textContent = `EGO: BRAKING FOR RED (${{aSpeed}} MPH)`;
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else if (t < 2.8) {{
        aX = 34.0; aY = 72.0; aSpeed = 0; brakeGlowA = 1.0;
        tagVehA.textContent = 'EGO: HALTED &rarr; OFFICER GESTURES GO';
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }} else {{
        const p = (t - 2.8) / (7.0 - 2.8);
        const ease = smoothCos(p);
        aX = 34.0 + ease * (72.0 - 34.0);
        aY = 72.0 - ease * (72.0 - 41.0);
        aSpeed = Math.round(ease * 22);
        brakeGlowA = 0.0;
        tagVehA.textContent = `EGO: OBEYING OFFICER THROUGH RED (${{aSpeed}} MPH)`;
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
      }}

      // Cross vehicle holds stationary at its line because officer holds them
      let bX = 68.0, bY = 71.5;
      tagVehB.textContent = 'CROSS TRAFFIC: HELD BY OFFICER';
      tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      vehA.style.left = `${{aX}}%`; vehA.style.top = `${{aY}}%`;
      vehB.style.left = `${{bX}}%`; vehB.style.top = `${{bY}}%`;
      vehA.style.opacity = '1.0'; vehB.style.opacity = '1.0';
      tagVehA.style.opacity = '1.0'; tagVehB.style.opacity = '1.0';

      brakeA1.style.opacity = brakeGlowA; brakeA2.style.opacity = brakeGlowA;
      brakeB1.style.opacity = '1.0'; brakeB2.style.opacity = '1.0';

      boxHoldSW.setAttribute('opacity', (t >= 2.0 && t <= 2.8) ? '1.0' : '0.0');
      traversalPathGroup.setAttribute('opacity', (t >= 2.8 && t <= 6.2) ? '1.0' : '0.0');

      // Status Pill
      hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#06182B]/95 border border-sky-400 text-sky-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
      pillStatusText.textContent = 'POLICE PREEMPTION ACTIVE: OFFICER HAND SIGNAL OVERRULES RED';

      // Telemetry
      telemVehA.innerHTML = `${{aSpeed}} MPH (${{aSpeed === 0 ? 'STATUTORY HALT' : 'OBEYING OFFICER'}})`;
      telemVehA.className = (aSpeed === 0) ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold';
      telemOfficer.innerHTML = 'SUPREME LEGAL AUTHORITY (TTC &sect; 544.004)';
      telemOfficer.className = 'text-sky-400 font-black animate-pulse';
      telemPrecedence.innerHTML = 'POLICE PREEMPTS RED LIGHT';
      telemPrecedence.className = 'text-sky-300 font-bold';
      telemStatute.innerHTML = 'TTC &sect; 544.004 &amp; &sect; 542.501';

      hudNarrative.textContent = 'Texas Transportation Code § 544.004 expressly mandates obedience to police officer direction over any official traffic control device. Driver MUST proceed on officer wave despite red light.';
      complianceText.textContent = 'TTC § 544.004 POLICE PREEMPTION COMPLIANCE VERIFIED';
    }}

    // ===============================================================
    // MODE 3: CRITICAL HAZARD DEMO (DISREGARDING OFFICER DIRECTION)
    // ===============================================================
    function updateMode3(t) {{
      // Electronic Signal is GREEN, BUT Police Officer gestures STOP!
      swLensRed.setAttribute('opacity', '0.25');
      swLensRed.setAttribute('filter', 'none');
      swLensGreen.setAttribute('opacity', '1.0');
      swLensGreen.setAttribute('filter', 'url(#glow-green)');

      signalStateBadge.innerHTML = 'SIGNAL: GREEN (OVERRULED BY OFFICER STOP)';
      signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';

      policeOfficerGroup.setAttribute('opacity', '1.0');
      officerArmProceed.setAttribute('opacity', '0.0');
      officerArmStop.setAttribute('opacity', '1.0');
      officerBadgeProceed.setAttribute('opacity', '0.0');
      officerBadgeStop.setAttribute('opacity', '1.0');
      officerWaveRing.setAttribute('opacity', '0.0');

      // Ego Vehicle approaches at 32 MPH and BLOWS THROUGH officer's stop gesture!
      let aX = 18.0, aY = 85.0, aSpeed = 32, brakeGlowA = 0.0;
      if (t <= 3.5) {{
        const p = t / 3.5;
        aX = 18.0 + p * (50.0 - 18.0);
        aY = 85.0 - p * (85.0 - 58.0);
        aSpeed = 32;
        brakeGlowA = (t > 2.8) ? 1.0 : 0.0; // Panic brake at last second
        tagVehA.textContent = 'EGO: DISREGARDING OFFICER STOP GESTURE!';
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';
      }} else {{
        aX = 50.0; aY = 58.0; aSpeed = 0; brakeGlowA = 1.0;
      }}

      // Cross vehicle clearing emergency path
      let bX = 82.0, bY = 82.0;
      if (t < 1.0) {{
        bX = 82.0; bY = 82.0;
      }} else if (t <= 3.5) {{
        const p = (t - 1.0) / (3.5 - 1.0);
        bX = 82.0 - p * (82.0 - 50.0);
        bY = 82.0 - p * (82.0 - 57.0);
      }} else {{
        bX = 50.0; bY = 57.0;
      }}
      tagVehB.textContent = 'CROSS VEHICLE (OFFICER-DIRECTED)';
      tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';

      vehA.style.left = `${{aX}}%`; vehA.style.top = `${{aY}}%`;
      vehB.style.left = `${{bX}}%`; vehB.style.top = `${{bY}}%`;
      vehA.style.opacity = '1.0'; vehB.style.opacity = '1.0';

      brakeA1.style.opacity = brakeGlowA; brakeA2.style.opacity = brakeGlowA;
      brakeB1.style.opacity = '0.0'; brakeB2.style.opacity = '0.0';

      boxHoldSW.setAttribute('opacity', '0.0');
      traversalPathGroup.setAttribute('opacity', '0.0');

      if (t >= 3.2 && t <= 6.5) {{
        tagVehA.style.opacity = '0.0';
        tagVehB.style.opacity = '0.0';
        hazardConflictZone.setAttribute('opacity', '1.0');
        hazardBanner.style.opacity = '1.0';

        telemVehA.innerHTML = 'CRASH IMPACT (IGNORING OFFICER)';
        telemVehA.className = 'text-red-400 font-black animate-pulse';
        telemOfficer.innerHTML = 'VIOLATION OF LAWFUL ORDER';
        telemOfficer.className = 'text-red-500 font-black';
        telemPrecedence.innerHTML = 'ILLEGAL GREEN ENTRY';
        telemPrecedence.className = 'text-red-500 font-black';
        telemStatute.innerHTML = 'TTC &sect; 542.501 MISDEMEANOR';
        telemStatute.className = 'text-red-500 font-black';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ CRITICAL VIOLATION: WILLFUL FAILURE TO OBEY POLICE OFFICER ✕';
        hudNarrative.textContent = 'CRITICAL HAZARD: Relying on green signal while disregarding police officer hand stop command violates TTC § 542.501 and results in devastating broadside crash!';
        complianceText.textContent = 'CRITICAL VIOLATION: DISREGARDED LAWFUL POLICE ORDER';
      }} else {{
        tagVehA.style.opacity = '1.0';
        tagVehB.style.opacity = '1.0';
        hazardConflictZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'WARNING: OFFICER STOP COMMAND PREEMPTS GREEN LIGHT';
      }}
    }}

    // ===============================================================
    // MAIN UPDATE DISPATCHER
    // ===============================================================
    function updateSimulation(t) {{
      timeDisplay.textContent = t.toFixed(2) + 's';
      timelineSlider.value = t;

      if (currentMode === 1) {{
        updateMode1(t);
      }} else if (currentMode === 2) {{
        updateMode2(t);
      }} else {{
        updateMode3(t);
      }}

      // Step Buttons Sync
      let activeStep = 1;
      if (currentMode === 1) {{
        if (t < 2.0) activeStep = 1;
        else if (t < 5.2) activeStep = 2;
        else if (t < 6.8) activeStep = 3;
        else activeStep = 4;
      }} else if (currentMode === 2) {{
        if (t < 2.0) activeStep = 1;
        else if (t < 2.8) activeStep = 2;
        else if (t < 5.5) activeStep = 3;
        else activeStep = 4;
      }} else {{
        if (t < 1.8) activeStep = 1;
        else if (t < 3.2) activeStep = 2;
        else if (t < 5.5) activeStep = 3;
        else activeStep = 4;
      }}

      stepBtns.forEach((btn, idx) => {{
        const s = idx + 1;
        if (s === activeStep) {{
          btn.className = 'step-btn px-2.5 py-1.5 rounded-lg border border-blue-500/60 bg-blue-500/15 text-left transition shadow';
          btn.querySelector('div:first-child').className = 'text-[9px] mono text-blue-400 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-white truncate';
        }} else {{
          btn.className = 'step-btn px-2.5 py-1.5 rounded-lg border border-[#212836] bg-[#121620] text-left transition hover:border-gray-600';
          btn.querySelector('div:first-child').className = 'text-[9px] mono text-gray-500 font-bold uppercase tracking-wider';
          btn.querySelector('div:last-child').className = 'text-[11px] font-extrabold text-gray-300 truncate';
        }}
      }});
    }}

    // ===============================================================
    // REQUEST ANIMATION FRAME LOOP
    // ===============================================================
    function tick(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const delta = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += delta * playbackSpeed;
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

      requestAnimationFrame(tick);
    }}

    requestAnimationFrame(tick);

    // ===============================================================
    // USER CONTROLS & INTERACTION LISTENERS
    // ===============================================================
    playPauseBtn.addEventListener('click', () => {{
      isPlaying = !isPlaying;
      playIcon.classList.toggle('hidden', isPlaying);
      pauseIcon.classList.toggle('hidden', !isPlaying);
    }});

    resetBtn.addEventListener('click', () => {{
      currentTime = 0.0;
      updateSimulation(currentTime);
    }});

    timelineSlider.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    autoLoopToggle.addEventListener('change', (e) => {{
      autoLoop = e.target.checked;
    }});

    speedBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        speedBtns.forEach(b => {{
          b.className = 'speed-btn px-2 py-0.5 rounded text-gray-400 hover:text-white';
        }});
        btn.className = 'speed-btn px-2 py-0.5 rounded bg-blue-600 text-white font-bold';
        playbackSpeed = parseFloat(btn.dataset.speed);
      }});
    }});

    modeBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        modeBtns.forEach(b => {{
          b.className = 'mode-btn px-3 py-1 rounded font-semibold text-gray-400 hover:text-white transition';
        }});
        currentMode = parseInt(btn.dataset.mode);
        if (currentMode === 1) {{
          btn.className = 'mode-btn px-3 py-1 rounded font-bold transition text-black bg-emerald-400 shadow';
        }} else if (currentMode === 2) {{
          btn.className = 'mode-btn px-3 py-1 rounded font-bold transition text-black bg-sky-400 shadow';
        }} else {{
          btn.className = 'mode-btn px-3 py-1 rounded font-bold transition text-white bg-red-600 shadow';
        }}

        // Update labels for mode
        const step1Lbl = document.getElementById('step-label-1');
        const step2Lbl = document.getElementById('step-label-2');
        const step3Lbl = document.getElementById('step-label-3');
        const step4Lbl = document.getElementById('step-label-4');

        if (currentMode === 1) {{
          step1Lbl.textContent = 'Approach & Deceleration';
          step2Lbl.textContent = 'Statutory Halt at Stop Bar';
          step3Lbl.textContent = 'Cross-Traffic Clearance';
          step4Lbl.textContent = 'Green Light Traversal';
        }} else if (currentMode === 2) {{
          step1Lbl.textContent = 'Approach Red Signal';
          step2Lbl.textContent = 'Officer Enters & Directs Go';
          step3Lbl.textContent = 'Preemption Overrules Red';
          step4Lbl.textContent = 'Lawful Traversal Verified';
        }} else {{
          step1Lbl.textContent = 'Green Signal / Officer Stop';
          step2Lbl.textContent = 'Disregarded Hand Signal';
          step3Lbl.textContent = 'Critical Intersection Conflict';
          step4Lbl.textContent = 'TTC § 542.501 Violation';
        }}

        currentTime = 0.0;
        updateSimulation(currentTime);
      }});
    }});

    stepBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        const step = parseInt(btn.dataset.step);
        if (currentMode === 1) {{
          if (step === 1) currentTime = 0.8;
          else if (step === 2) currentTime = 2.5;
          else if (step === 3) currentTime = 4.2;
          else currentTime = 6.8;
        }} else if (currentMode === 2) {{
          if (step === 1) currentTime = 0.8;
          else if (step === 2) currentTime = 2.4;
          else if (step === 3) currentTime = 4.5;
          else currentTime = 6.8;
        }} else {{
          if (step === 1) currentTime = 0.8;
          else if (step === 2) currentTime = 2.4;
          else if (step === 3) currentTime = 3.6;
          else currentTime = 6.0;
        }}
        updateSimulation(currentTime);
      }});
    }});

    // Initial render
    updateSimulation(0.0);
  </script>
</body>
</html>
'''

output_path = 'driving_rule_animations_suite/simulations/L05_T02_managing_traffic_flow.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 11 simulation built successfully at: {output_path}")
