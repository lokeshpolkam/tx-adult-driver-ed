import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/uncontrolled_intersection_final.png'
car_red_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_blue_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_nw.png'

print("Encoding Lesson 10 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_b64 = get_base64_img(car_red_path)
car_blue_b64 = get_base64_img(car_blue_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson L04-T04: Dark / Malfunctioning Signals — 4-Way Stop Rule (TTC § 544.007(x))</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0B0E14;
      color: #E2E8F0;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      user-select: none;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .stepper-btn.active {{
      background-color: #2563EB;
      color: #FFFFFF;
      border-color: #60A5FA;
      box-shadow: 0 0 14px rgba(37, 99, 235, 0.5);
    }}
    .scenario-btn.active {{
      background-color: #059669;
      color: #FFFFFF;
      border-color: #34D399;
      box-shadow: 0 0 14px rgba(5, 150, 105, 0.45);
    }}
    .scenario-btn-hazard.active {{
      background-color: #DC2626;
      color: #FFFFFF;
      border-color: #F87171;
      box-shadow: 0 0 16px rgba(220, 38, 38, 0.55);
    }}
    @keyframes pulseDanger {{
      0%, 100% {{ transform: scale(1); opacity: 0.9; }}
      50% {{ transform: scale(1.15); opacity: 0.4; }}
    }}
    .pulse-danger {{
      animation: pulseDanger 1.4s infinite ease-in-out;
      transform-origin: center;
    }}
    @keyframes flashRedLens {{
      0%, 49% {{ opacity: 1.0; filter: drop-shadow(0 0 8px #EF4444); }}
      50%, 100% {{ opacity: 0.2; filter: none; }}
    }}
    .flash-red-active {{
      animation: flashRedLens 1.0s infinite;
    }}
    @keyframes blinkAmberOutline {{
      0%, 100% {{ opacity: 0.9; }}
      50% {{ opacity: 0.3; }}
    }}
    .blink-amber {{
      animation: blinkAmberOutline 1.2s infinite ease-in-out;
    }}
  </style>
</head>
<body class="flex flex-col h-screen justify-between p-2 md:p-3 max-w-[1440px] mx-auto">

  <!-- TOP HEADER / CONTROLS BAR -->
  <header class="bg-[#121620] border border-[#212836] rounded-xl px-4 py-2.5 shadow-lg flex flex-wrap items-center justify-between gap-2 z-30">
    <div class="flex items-center space-x-3">
      <div class="flex flex-col">
        <span class="text-[10px] font-bold text-blue-400 mono tracking-wider">TDLR ADE-1317 &bull; 2.5D VECTOR ENGINE</span>
        <h1 class="text-sm md:text-base font-extrabold text-white tracking-wide">
          L04-T04: Dark / Malfunctioning Signals &mdash; 4-Way Stop Rule
        </h1>
        <span class="text-[11px] text-gray-400 mono">Texas Transportation Code § 544.007(x) &bull; § 545.151</span>
      </div>
    </div>

    <!-- SCENARIO TOGGLES -->
    <div class="flex items-center bg-[#18202F] p-1 rounded-lg border border-[#2B3548] space-x-1 text-xs mono">
      <button id="mode-dark-btn" class="scenario-btn active px-3 py-1.5 rounded-md font-bold transition flex items-center space-x-1.5">
        <span>1: Dark Signal (First-In, First-Out)</span>
      </button>
      <button id="mode-simult-btn" class="scenario-btn px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5">
        <span>2: Simultaneous Arrival (Yield to Right)</span>
      </button>
      <button id="mode-hazard-btn" class="scenario-btn-hazard px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5">
        <span>Hazard: Failure to Stop Collision</span>
      </button>
    </div>

    <!-- LOOP TOGGLE -->
    <div class="flex items-center space-x-2 text-xs mono text-gray-300">
      <label class="flex items-center cursor-pointer space-x-1.5">
        <input type="checkbox" id="auto-loop" checked class="form-checkbox h-3.5 w-3.5 text-blue-600 rounded bg-[#10141D] border-gray-700">
        <span class="text-[11px]">Auto-Loop</span>
      </label>
    </div>
  </header>

  <!-- CANONICAL 4-STEP STEPPER BAR -->
  <div class="grid grid-cols-2 md:grid-cols-4 gap-2 my-1 z-30">
    <button data-step="1" class="stepper-btn active py-1.5 px-3 rounded-lg bg-[#141923] border border-[#242C3C] text-xs font-semibold text-gray-300 hover:bg-[#1B2230] transition flex flex-col items-center justify-center text-center">
      <span class="text-[9px] mono text-blue-400 font-bold uppercase tracking-wider">Step 1</span>
      <span id="step-label-1" class="text-[11px] font-bold">Dark Signal Perception &amp; Decel</span>
    </button>
    <button data-step="2" class="stepper-btn py-1.5 px-3 rounded-lg bg-[#141923] border border-[#242C3C] text-xs font-semibold text-gray-300 hover:bg-[#1B2230] transition flex flex-col items-center justify-center text-center">
      <span class="text-[9px] mono text-gray-400 font-bold uppercase tracking-wider">Step 2</span>
      <span id="step-label-2" class="text-[11px] font-bold">Dual Full Halt at Stop Bars</span>
    </button>
    <button data-step="3" class="stepper-btn py-1.5 px-3 rounded-lg bg-[#141923] border border-[#242C3C] text-xs font-semibold text-gray-300 hover:bg-[#1B2230] transition flex flex-col items-center justify-center text-center">
      <span class="text-[9px] mono text-gray-400 font-bold uppercase tracking-wider">Step 3</span>
      <span id="step-label-3" class="text-[11px] font-bold">Precedence Right-of-Way Traversal</span>
    </button>
    <button data-step="4" class="stepper-btn py-1.5 px-3 rounded-lg bg-[#141923] border border-[#242C3C] text-xs font-semibold text-gray-300 hover:bg-[#1B2230] transition flex flex-col items-center justify-center text-center">
      <span class="text-[9px] mono text-gray-400 font-bold uppercase tracking-wider">Step 4</span>
      <span id="step-label-4" class="text-[11px] font-bold">Clearance &amp; Secondary Traversal</span>
    </button>
  </div>

  <!-- MAIN SIMULATION DIORAMA VIEWPORT -->
  <main class="relative flex-1 bg-[#090C12] rounded-2xl border border-[#1E2638] overflow-hidden shadow-2xl flex items-center justify-center min-h-[460px]">
    
    <!-- 2.5D INTERSECTION DIORAMA CONTAINER (Responsive responsive sizing based on viewport height and 1024/667 aspect ratio) -->
    <div id="diorama-stage" class="relative rounded-2xl overflow-hidden shadow-2xl border border-[#262F3D] bg-[#000000]" style="height: calc(100% - 16px); aspect-ratio: 1024 / 667; max-width: calc(100% - 16px);">
      
      <!-- LAYER 0: BASE HIGH-RESOLUTION ISOMETRIC ROADWAY -->
      <img src="{road_b64}" alt="Intersection Diorama" class="absolute inset-0 w-full h-full object-cover select-none pointer-events-none" />

      <!-- LAYER 1: SVG OVERLAYS (Signal Heads, Placards, Stop Lines, Conflict Markers) -->
      <svg id="svg-overlay" class="absolute inset-0 w-full h-full pointer-events-none z-10" viewBox="0 0 1024 667">
        <defs>
          <!-- Glowing Red Flasher Filter -->
          <filter id="glow-red" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <!-- Glowing Amber Filter -->
          <filter id="glow-amber" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <!-- ADVANCE WHITE STOP LINES ON APPROACHES -->
        <!-- SW Stop Line (Vehicle A Approach: 34.0%, 72.0%) -->
        <line x1="322" y1="510" x2="394" y2="470" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.95" />
        <!-- SE Stop Line (Vehicle B Approach: 65.0%, 69.0%) -->
        <line x1="630" y1="470" x2="702" y2="510" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" opacity="0.95" />
        <!-- NW Stop Line (NW Approach) -->
        <line x1="320" y1="210" x2="390" y2="250" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" opacity="0.75" />
        <!-- NE Stop Line (NE Approach) -->
        <line x1="630" y1="250" x2="700" y2="210" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" opacity="0.75" />

        <!-- STOPPING HOLD THRESHOLD BOX INDICATORS -->
        <g id="box-hold-sw" opacity="0.0">
          <polygon points="322,510 394,470 364,450 292,490" fill="#10B981" fill-opacity="0.2" stroke="#10B981" stroke-width="1.5" stroke-dasharray="3,3" />
        </g>
        <g id="box-hold-se" opacity="0.0">
          <polygon points="630,470 702,510 732,490 660,450" fill="#10B981" fill-opacity="0.2" stroke="#10B981" stroke-width="1.5" stroke-dasharray="3,3" />
        </g>

        <!-- =============================================================== -->
        <!-- TRAFFIC SIGNAL MAST HEADS (SW, SE, NW, NE)                      -->
        <!-- Mode 1: 100% Dark Unlit Lenses + Auxiliary "4-WAY STOP" Placard -->
        <!-- Mode 2: Flashing Red Lenses (All-Way Flashing Red Malfunction)  -->
        <!-- =============================================================== -->

        <!-- SIGNAL 1: SW Corner (Facing Inbound SW Approach Vehicle A) -->
        <g id="mast-sw" transform="translate(303, 496)">
          <!-- Mast Pole -->
          <line x1="0" y1="22" x2="0" y2="45" stroke="#374151" stroke-width="3" />
          <!-- 3-Section Signal Housing Body -->
          <rect x="-8" y="-22" width="16" height="44" rx="3.5" fill="#111827" stroke="#374151" stroke-width="1.5" />
          <!-- Red Lens (Top) -->
          <circle id="sw-lens-red" cx="0" cy="-12" r="5" fill="#1F2937" opacity="0.25" />
          <!-- Yellow Lens (Middle) -->
          <circle id="sw-lens-yellow" cx="0" cy="0" r="5" fill="#1F2937" opacity="0.25" />
          <!-- Green Lens (Bottom) -->
          <circle id="sw-lens-green" cx="0" cy="12" r="5" fill="#1F2937" opacity="0.25" />
          
          <!-- R1-1 STOP Auxiliary Sign Attached Under Signal Head -->
          <g id="sw-stop-sign-aux" transform="translate(0, 30)">
            <polygon points="-8,-4 0,-8 8,-4 8,4 0,8 -8,4" fill="#DC2626" stroke="#FFFFFF" stroke-width="0.8" />
            <text x="0" y="2.5" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="5" font-weight="900" text-anchor="middle">STOP</text>
          </g>
        </g>

        <!-- SIGNAL 2: SE Corner (Facing Inbound SE Approach Vehicle B) -->
        <g id="mast-se" transform="translate(699, 496)">
          <!-- Mast Pole -->
          <line x1="0" y1="22" x2="0" y2="45" stroke="#374151" stroke-width="3" />
          <!-- 3-Section Signal Housing Body -->
          <rect x="-8" y="-22" width="16" height="44" rx="3.5" fill="#111827" stroke="#374151" stroke-width="1.5" />
          <!-- Red Lens (Top) -->
          <circle id="se-lens-red" cx="0" cy="-12" r="5" fill="#1F2937" opacity="0.25" />
          <!-- Yellow Lens (Middle) -->
          <circle id="se-lens-yellow" cx="0" cy="0" r="5" fill="#1F2937" opacity="0.25" />
          <!-- Green Lens (Bottom) -->
          <circle id="se-lens-green" cx="0" cy="12" r="5" fill="#1F2937" opacity="0.25" />
          
          <!-- R1-1 STOP Auxiliary Sign Attached Under Signal Head -->
          <g id="se-stop-sign-aux" transform="translate(0, 30)">
            <polygon points="-8,-4 0,-8 8,-4 8,4 0,8 -8,4" fill="#DC2626" stroke="#FFFFFF" stroke-width="0.8" />
            <text x="0" y="2.5" fill="#FFFFFF" font-family="'JetBrains Mono', monospace" font-size="5" font-weight="900" text-anchor="middle">STOP</text>
          </g>
        </g>

        <!-- SIGNAL 3: NW Corner (Facing NW Inbound) -->
        <g id="mast-nw" transform="translate(297, 184)">
          <rect x="-7" y="-18" width="14" height="36" rx="3" fill="#111827" stroke="#374151" stroke-width="1.2" />
          <circle id="nw-lens-red" cx="0" cy="-9" r="4" fill="#1F2937" opacity="0.25" />
          <circle id="nw-lens-yellow" cx="0" cy="0" r="4" fill="#1F2937" opacity="0.25" />
          <circle id="nw-lens-green" cx="0" cy="9" r="4" fill="#1F2937" opacity="0.25" />
        </g>

        <!-- SIGNAL 4: NE Corner (Facing NE Inbound) -->
        <g id="mast-ne" transform="translate(690, 184)">
          <rect x="-7" y="-18" width="14" height="36" rx="3" fill="#111827" stroke="#374151" stroke-width="1.2" />
          <circle id="ne-lens-red" cx="0" cy="-9" r="4" fill="#1F2937" opacity="0.25" />
          <circle id="ne-lens-yellow" cx="0" cy="0" r="4" fill="#1F2937" opacity="0.25" />
          <circle id="ne-lens-green" cx="0" cy="9" r="4" fill="#1F2937" opacity="0.25" />
        </g>

        <!-- YIELD / PRECEDENCE INDICATOR ARROW (Visualizes Right-of-Way Precedence) -->
        <g id="precedence-arrow-group" opacity="0.0">
          <path id="precedence-arrow-path" d="M 370 480 Q 440 430, 510 385" fill="none" stroke="#10B981" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-head)" />
          
        </g>

        <!-- HAZARD DEMO: CRITICAL T-BONE IMPACT CONFLICT ZONE (Center Box: 512, 385) -->
        <g id="hazard-collision-zone" opacity="0.0">
          <circle cx="512" cy="385" r="55" fill="#EF4444" fill-opacity="0.25" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" class="pulse-danger" />
          <circle cx="512" cy="385" r="30" fill="#DC2626" fill-opacity="0.45" stroke="#FCA5A5" stroke-width="2" />
          <line x1="445" y1="385" x2="580" y2="385" stroke="#EF4444" stroke-width="2.5" />
          <line x1="512" y1="320" x2="512" y2="450" stroke="#EF4444" stroke-width="2.5" />
          <polygon points="512,360 522,378 542,375 527,390 537,410 512,398 487,410 497,390 482,375 502,378" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES & NON-OVERLAPPING IDENTIFICATION BADGES -->

      <!-- VEHICLE A (Ego Sedan - Red, Traveling SW to NE) -->
      <div id="veh-a-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 18.0%; top: 85.0%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_b64}" alt="Vehicle A" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Glowing Brake Lights -->
          <div id="veh-a-brake-1" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 18%; left: 16%;"></div>
          <div id="veh-a-brake-2" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 27%; left: 30%;"></div>
        </div>

        <!-- Non-overlapping Identification Badge strictly ABOVE Vehicle A (Points up-left into SW/NW shoulder) -->
        <div id="tag-veh-a" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          VEHICLE A (DECELERATING)
        </div>
      </div>

      <!-- VEHICLE B (Cross-Traffic Sedan - Blue, Traveling SE to NW) -->
      <div id="veh-b-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 82.0%; top: 82.0%; transform: translate(-50%, -50%);">
        <div class="relative w-24 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_b64}" alt="Vehicle B" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Glowing Brake Lights for Vehicle B -->
          <div id="veh-b-brake-1" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="top: 24%; right: 18%;"></div>
          <div id="veh-b-brake-2" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="top: 32%; right: 28%;"></div>
        </div>

        <!-- Non-overlapping Identification Badge strictly ABOVE Vehicle B (Points up-right into SE shoulder) -->
        <div id="tag-veh-b" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          VEHICLE B (CROSS TRAFFIC)
        </div>
      </div>

      <!-- LAYER 3: TOP-RIGHT STATUS NOTIFICATION PILL -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 10px; right: 10px;">
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
        <span id="pill-status-text">DARK SIGNAL DETECTED: TREAT AS ALL-WAY STOP</span>
      </div>

      <!-- LAYER 3: BOTTOM-RIGHT STATUTORY COMPLIANCE BADGE -->
      <div class="absolute bottom-2.5 right-2.5 z-25 px-3 py-1.5 rounded-lg bg-[#0F141C]/90 border border-emerald-500/30 text-emerald-400 mono text-[10px] font-bold shadow-lg tracking-wider flex items-center space-x-2 pointer-events-none">
        <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
        <span id="compliance-text">TTC § 544.007(x) ALL-WAY STOP COMPLIANCE VERIFIED</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER (Placed near bottom, completely unobstructed) -->
      <div id="hazard-banner" class="absolute bottom-14 left-1/2 -translate-x-1/2 z-30 px-5 py-2 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300" style="opacity: 0.0;">
        <div class="text-xs font-black tracking-widest text-red-400 flex items-center justify-center space-x-1.5">
          <span>✕ CRITICAL HAZARD: FAILURE TO STOP AT DARK SIGNAL ✕</span>
        </div>
        <div class="text-[11px] font-semibold text-gray-200">
          TTC § 544.007(x) Mandate: All-way stop required! Disregarding dark signal causes fatal T-bone collision.
        </div>
      </div>

      <!-- LAYER 4: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
      <div id="telemetry-hud-card" class="absolute top-2.5 left-2.5 z-30 max-w-[280px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-2 space-y-1 shadow-xl pointer-events-none">
        <div class="flex items-center justify-between border-b border-[#222B38] pb-1.5">
          <span class="text-[10px] font-bold text-gray-400 mono uppercase tracking-wider">Signal Status &amp; Telemetry</span>
          <span id="signal-state-badge" class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono">
            SIGNAL: DARK / OUT OF SERVICE
          </span>
        </div>

        <div class="space-y-1 text-xs mono">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Vehicle A (Ego - SW):</span>
            <span id="telem-veh-a" class="text-emerald-400 font-bold">25 MPH (DECELERATING)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Vehicle B (Cross - SE):</span>
            <span id="telem-veh-b" class="text-blue-400 font-bold">25 MPH (DECELERATING)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Precedence Order:</span>
            <span id="telem-precedence" class="text-emerald-300 font-bold">VEHICLE A (FIRST ARRIVED)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Mandate:</span>
            <span id="telem-statute" class="text-emerald-300 font-bold">TTC § 544.007(x) 4-WAY STOP</span>
          </div>
        </div>

        <div class="pt-1 border-t border-[#1F2633] text-[10px] text-gray-300 leading-snug font-sans" id="hud-narrative">
          Approaching a dark or out-of-order traffic signal, drivers must stop before the stop bar and treat the intersection as a 4-way all-way stop under Texas law.
        </div>
      </div>

    </div>
  </main>

  <!-- BOTTOM SCRUBBABLE TIMELINE & PLAYBACK CONTROLS -->
  <footer class="bg-[#121620] border border-[#212836] rounded-xl px-4 py-2.5 shadow-lg flex flex-col gap-2 mt-1 z-30">
    <div class="flex items-center space-x-3">
      <!-- Play/Pause Button -->
      <button id="play-pause-btn" class="w-8 h-8 rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center transition shadow-md">
        <svg id="icon-play" class="w-4 h-4 fill-current ml-0.5" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        <svg id="icon-pause" class="w-4 h-4 fill-current hidden" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
      </button>

      <!-- Reset Button -->
      <button id="reset-btn" class="w-8 h-8 rounded-lg bg-[#1C2333] hover:bg-[#252E42] text-gray-300 flex items-center justify-center transition border border-[#2B3548]">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
      </button>

      <!-- Time Display -->
      <span id="time-display" class="mono text-xs font-bold text-blue-400 w-12 text-center">0.00s</span>

      <!-- Scrubbable Range Slider -->
      <input type="range" id="scrubber" min="0" max="8.0" step="0.01" value="0" class="flex-1 h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500">

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
      <span>● 0.5s Dark Signal Recognition</span>
      <span>● 2.5s Statutory Stop Lines</span>
      <span>● 4.8s Precedence Traversal</span>
      <span>● 6.8s Secondary Clearance</span>
      <span class="text-emerald-400 font-semibold">TTC § 544.007(x) All-Way Stop</span>
    </div>
  </footer>

  <!-- CORE ANIMATION ENGINE JAVASCRIPT -->
  <script>
    // State Variables
    let currentTime = 0.0;
    const duration = 8.0;
    let isPlaying = false;
    let playbackSpeed = 1.0;
    let lastTimestamp = 0;
    let simulationMode = 'dark'; // 'dark', 'simultaneous', 'hazard'

    // Step Timestamp Reference for 4 canonical steps
    const stepTimes = [0.5, 2.5, 4.8, 6.8];
    let currentStepIdx = 0;

    // DOM Elements
    const scrubber = document.getElementById('scrubber');
    const timeDisplay = document.getElementById('time-display');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const resetBtn = document.getElementById('reset-btn');
    const iconPlay = document.getElementById('icon-play');
    const iconPause = document.getElementById('icon-pause');
    const autoLoop = document.getElementById('auto-loop');
    const speedBtns = document.querySelectorAll('.speed-btn');
    const stepBtns = document.querySelectorAll('.stepper-btn');

    // Scenario Mode Buttons
    const modeDarkBtn = document.getElementById('mode-dark-btn');
    const modeSimultBtn = document.getElementById('mode-simult-btn');
    const modeHazardBtn = document.getElementById('mode-hazard-btn');

    // Vehicles & Tags
    const vehA = document.getElementById('veh-a-container');
    const vehB = document.getElementById('veh-b-container');
    const tagVehA = document.getElementById('tag-veh-a');
    const tagVehB = document.getElementById('tag-veh-b');
    const brakeA1 = document.getElementById('veh-a-brake-1');
    const brakeA2 = document.getElementById('veh-a-brake-2');
    const brakeB1 = document.getElementById('veh-b-brake-1');
    const brakeB2 = document.getElementById('veh-b-brake-2');

    // Signal Heads & Lenses
    const swLensRed = document.getElementById('sw-lens-red');
    const swLensYellow = document.getElementById('sw-lens-yellow');
    const swLensGreen = document.getElementById('sw-lens-green');
    const seLensRed = document.getElementById('se-lens-red');
    const seLensYellow = document.getElementById('se-lens-yellow');
    const seLensGreen = document.getElementById('se-lens-green');
    const nwLensRed = document.getElementById('nw-lens-red');
    const nwLensYellow = document.getElementById('nw-lens-yellow');
    const nwLensGreen = document.getElementById('nw-lens-green');
    const neLensRed = document.getElementById('ne-lens-red');
    const neLensYellow = document.getElementById('ne-lens-yellow');
    const neLensGreen = document.getElementById('ne-lens-green');

    // Overlays
    const precedenceArrowGroup = document.getElementById('precedence-arrow-group');
    const precedenceArrowPath = document.getElementById('precedence-arrow-path');
    const boxHoldSW = document.getElementById('box-hold-sw');
    const boxHoldSE = document.getElementById('box-hold-se');
    const hazardCollisionZone = document.getElementById('hazard-collision-zone');
    const hazardBanner = document.getElementById('hazard-banner');

    // Telemetry & Badges
    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');
    const signalStateBadge = document.getElementById('signal-state-badge');
    const telemVehA = document.getElementById('telem-veh-a');
    const telemVehB = document.getElementById('telem-veh-b');
    const telemPrecedence = document.getElementById('telem-precedence');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceText = document.getElementById('compliance-text');

    // Stepper button labels by Mode
    const stepLabelsByMode = {{
      dark: [
        'Dark Signal Perception & Decel',
        'Dual Full Halt at Stop Bars',
        'Vehicle A First-In Precedence',
        'Vehicle B Secondary Departure'
      ],
      simultaneous: [
        'Flashing Red Malfunction Arrival',
        'Simultaneous Halt at Stop Bars',
        'Vehicle B (on Right) Precedence',
        'Vehicle A Secondary Traversal'
      ],
      hazard: [
        'Approaching Dark Signal',
        'Vehicle B Halts / Veh A Speeding',
        'Disregarded Stop Bar Violation',
        'Catastrophic T-Bone Crash'
      ]
    }};

    // S-curve smooth easing
    function smoothCos(p) {{
      return 0.5 - 0.5 * Math.cos(p * Math.PI);
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
        if (t >= stepTimes[i] - 0.25) activeStep = i;
      }}
      currentStepIdx = activeStep;
      stepBtns.forEach((btn, idx) => {{
        if (idx === activeStep) btn.classList.add('active');
        else btn.classList.remove('active');
      }});

      if (simulationMode === 'dark') {{
        // =====================================================================
        // MODE 1: COMPLETELY DARK SIGNAL (FIRST-IN, FIRST-OUT ALL-WAY STOP)
        // =====================================================================
        // All signal lenses 100% unlit
        swLensRed.setAttribute('opacity', '0.25');
        swLensYellow.setAttribute('opacity', '0.25');
        swLensGreen.setAttribute('opacity', '0.25');
        swLensRed.classList.remove('flash-red-active');

        seLensRed.setAttribute('opacity', '0.25');
        seLensYellow.setAttribute('opacity', '0.25');
        seLensGreen.setAttribute('opacity', '0.25');
        seLensRed.classList.remove('flash-red-active');

        nwLensRed.setAttribute('opacity', '0.25');
        neLensRed.setAttribute('opacity', '0.25');

        hazardCollisionZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'DARK SIGNAL DETECTED: TREAT AS ALL-WAY STOP';
        signalStateBadge.innerHTML = 'SIGNAL: DARK / OUT OF SERVICE';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';

        // Vehicle A: Arrives at stop bar at t = 1.8s (First to arrive!)
        // Holds stationary at stop bar until t = 3.6s
        // Departs first from t = 3.6s to t = 6.0s
        let aX = 18.0, aY = 85.0, aSpeed = 25, brakeGlowA = 0.0;
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        if (t < 1.8) {{
          const p = t / 1.8;
          const ease = smoothCos(p);
          aX = 18.0 + ease * (34.0 - 18.0);
          aY = 85.0 - ease * (85.0 - 72.0);
          aSpeed = Math.round(25 * (1 - p));
          brakeGlowA = (p > 0.3) ? 1.0 : 0.0;
          tagVehA.textContent = `VEHICLE A: BRAKING (${{aSpeed}} MPH)`;
        }} else if (t < 3.6) {{
          aX = 34.0; aY = 72.0; aSpeed = 0; brakeGlowA = 1.0;
          tagVehA.textContent = 'VEHICLE A: STOPPED (1ST ARRIVAL)';
        }} else if (t < 6.0) {{
          const p = (t - 3.6) / (6.0 - 3.6);
          const ease = smoothCos(p);
          aX = 34.0 + ease * (72.0 - 34.0);
          aY = 72.0 - ease * (72.0 - 41.0);
          aSpeed = Math.round(ease * 24);
          brakeGlowA = 0.0;
          tagVehA.textContent = `VEHICLE A: DEPARTING 1ST (${{aSpeed}} MPH)`;
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }} else {{
          aX = 72.0; aY = 41.0; aSpeed = 24; brakeGlowA = 0.0;
          tagVehA.textContent = 'VEHICLE A: CLEARED';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }}

        // Vehicle B: Arrives at stop bar at t = 2.4s (Arrived second!)
        // Holds stationary until t = 5.6s (waits for Vehicle A to clear)
        // Departs second from t = 5.6s to t = 8.0s
        let bX = 82.0, bY = 82.0, bSpeed = 25, brakeGlowB = 0.0;
        tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        if (t < 2.4) {{
          const p = t / 2.4;
          const ease = smoothCos(p);
          bX = 82.0 - ease * (82.0 - 68.0);
          bY = 82.0 - ease * (82.0 - 71.5);
          bSpeed = Math.round(25 * (1 - p));
          brakeGlowB = (p > 0.3) ? 1.0 : 0.0;
          tagVehB.textContent = `VEHICLE B: BRAKING (${{bSpeed}} MPH)`;
        }} else if (t < 5.6) {{
          bX = 68.0; bY = 71.5; bSpeed = 0; brakeGlowB = 1.0;
          tagVehB.textContent = 'VEHICLE B: STOPPED (YIELDING)';
        }} else {{
          const p = (t - 5.6) / (8.0 - 5.6);
          const ease = smoothCos(p);
          bX = 68.0 - ease * (68.0 - 24.0);
          bY = 71.5 - ease * (71.5 - 37.0);
          bSpeed = Math.round(ease * 22);
          brakeGlowB = 0.0;
          tagVehB.textContent = `VEHICLE B: DEPARTING 2ND (${{bSpeed}} MPH)`;
        }}

        // Position & visibility
        vehA.style.left = `${{aX}}%`; vehA.style.top = `${{aY}}%`;
        vehB.style.left = `${{bX}}%`; vehB.style.top = `${{bY}}%`;
        vehA.style.opacity = '1.0'; vehB.style.opacity = '1.0';
        tagVehA.style.opacity = '1.0'; tagVehB.style.opacity = '1.0';

        brakeA1.style.opacity = brakeGlowA; brakeA2.style.opacity = brakeGlowA;
        brakeB1.style.opacity = brakeGlowB; brakeB2.style.opacity = brakeGlowB;

        // Visual Precedence Arrow
        if (t >= 2.0 && t <= 5.0) {{
          precedenceArrowGroup.setAttribute('opacity', '1.0');
          precedenceArrowPath.setAttribute('d', 'M 370 480 Q 440 430, 510 385');
          }} else {{
          precedenceArrowGroup.setAttribute('opacity', '0.0');
        }}

        boxHoldSW.setAttribute('opacity', (t >= 1.8 && t <= 3.6) ? '1.0' : '0.0');
        boxHoldSE.setAttribute('opacity', (t >= 2.4 && t <= 5.6) ? '1.0' : '0.0');

        // Telemetry Update
        telemVehA.innerHTML = `${{aSpeed}} MPH (${{aSpeed === 0 ? 'STOPPED AT LINE' : 'MOVING'}})`;
        telemVehA.className = (aSpeed === 0) ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold';
        telemVehB.innerHTML = `${{bSpeed}} MPH (${{bSpeed === 0 ? 'HOLDING YIELD' : 'MOVING'}})`;
        telemVehB.className = (bSpeed === 0) ? 'text-blue-400 font-bold' : 'text-blue-300 font-bold';
        telemPrecedence.innerHTML = (t < 3.6) ? 'VEHICLE A (FIRST TO ARRIVE)' : (t < 5.6 ? 'VEHICLE A TRAVERSING' : 'VEHICLE B PROCEEDING');
        telemPrecedence.className = 'text-emerald-300 font-bold';
        telemStatute.innerHTML = 'TTC § 544.007(x) FIRST-IN RULE';
        complianceText.textContent = 'TTC § 544.007(x) ALL-WAY STOP COMPLIANCE VERIFIED';

        if (t < 1.8) {{
          hudNarrative.textContent = 'Approaching dark signal heads, both drivers perceive the power failure and smoothly brake to stop before their stop lines.';
        }} else if (t < 3.6) {{
          hudNarrative.textContent = 'Both vehicles come to a complete statutory stop. Vehicle A arrived at the stop line first, earning immediate right-of-way under the all-way stop rule.';
        }} else if (t < 5.6) {{
          hudNarrative.textContent = 'Vehicle A accelerates and traverses through the intersection first while Vehicle B holds stationary behind its stop line.';
        }} else {{
          hudNarrative.textContent = 'With the intersection cleared, Vehicle B accelerates second and proceeds safely across under full legal compliance.';
        }}

      }} else if (simulationMode === 'simultaneous') {{
        // =====================================================================
        // MODE 2: SIMULTANEOUS ARRIVAL (YIELD TO VEHICLE ON RIGHT - TTC § 545.151)
        // =====================================================================
        // All-way flashing red malfunction mode
        const isFlashOn = (Math.floor(t * 2) % 2 === 0);
        swLensRed.setAttribute('opacity', isFlashOn ? '1.0' : '0.25');
        swLensYellow.setAttribute('opacity', '0.25');
        swLensGreen.setAttribute('opacity', '0.25');
        swLensRed.setAttribute('filter', isFlashOn ? 'url(#glow-red)' : 'none');

        seLensRed.setAttribute('opacity', isFlashOn ? '1.0' : '0.25');
        seLensYellow.setAttribute('opacity', '0.25');
        seLensGreen.setAttribute('opacity', '0.25');
        seLensRed.setAttribute('filter', isFlashOn ? 'url(#glow-red)' : 'none');

        nwLensRed.setAttribute('opacity', isFlashOn ? '1.0' : '0.25');
        neLensRed.setAttribute('opacity', isFlashOn ? '1.0' : '0.25');

        hazardCollisionZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'FLASHING RED / SIMULTANEOUS ARRIVAL: YIELD TO RIGHT';
        signalStateBadge.innerHTML = 'SIGNAL: ALL-WAY FLASHING RED';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        // Both vehicles arrive and stop at the EXACT SAME TIME: t = 2.0s!
        // From Vehicle A\'s perspective, Vehicle B is on Vehicle A\'s RIGHT!
        // Under TTC § 545.151, Vehicle A must yield to Vehicle B on the right!
        // Vehicle B proceeds first (t = 3.6s to 6.0s); Vehicle A proceeds second (t = 5.8s to 8.0s).
        let aX = 18.0, aY = 85.0, aSpeed = 25, brakeGlowA = 0.0;
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        if (t < 2.0) {{
          const p = t / 2.0;
          const ease = smoothCos(p);
          aX = 18.0 + ease * (34.0 - 18.0);
          aY = 85.0 - ease * (85.0 - 72.0);
          aSpeed = Math.round(25 * (1 - p));
          brakeGlowA = (p > 0.3) ? 1.0 : 0.0;
          tagVehA.textContent = `VEHICLE A: STOPPING (${{aSpeed}} MPH)`;
        }} else if (t < 5.8) {{
          aX = 34.0; aY = 72.0; aSpeed = 0; brakeGlowA = 1.0;
          tagVehA.textContent = 'VEHICLE A: YIELDING TO RIGHT';
        }} else {{
          const p = (t - 5.8) / (8.0 - 5.8);
          const ease = smoothCos(p);
          aX = 34.0 + ease * (72.0 - 34.0);
          aY = 72.0 - ease * (72.0 - 41.0);
          aSpeed = Math.round(ease * 22);
          brakeGlowA = 0.0;
          tagVehA.textContent = `VEHICLE A: DEPARTING 2ND (${{aSpeed}} MPH)`;
        }}

        let bX = 82.0, bY = 82.0, bSpeed = 25, brakeGlowB = 0.0;
        tagVehB.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        if (t < 2.0) {{
          const p = t / 2.0;
          const ease = smoothCos(p);
          bX = 82.0 - ease * (82.0 - 68.0);
          bY = 82.0 - ease * (82.0 - 71.5);
          bSpeed = Math.round(25 * (1 - p));
          brakeGlowB = (p > 0.3) ? 1.0 : 0.0;
          tagVehB.textContent = `VEHICLE B: STOPPING (${{bSpeed}} MPH)`;
        }} else if (t < 3.6) {{
          bX = 68.0; bY = 71.5; bSpeed = 0; brakeGlowB = 1.0;
          tagVehB.textContent = 'VEHICLE B: PRIORITY ON RIGHT';
        }} else if (t < 6.0) {{
          const p = (t - 3.6) / (6.0 - 3.6);
          const ease = smoothCos(p);
          bX = 68.0 - ease * (68.0 - 24.0);
          bY = 71.5 - ease * (71.5 - 37.0);
          bSpeed = Math.round(ease * 24);
          brakeGlowB = 0.0;
          tagVehB.textContent = `VEHICLE B: DEPARTING 1ST (${{bSpeed}} MPH)`;
        }} else {{
          bX = 24.0; bY = 37.0; bSpeed = 24; brakeGlowB = 0.0;
          tagVehB.textContent = 'VEHICLE B: CLEARED';
        }}

        vehA.style.left = `${{aX}}%`; vehA.style.top = `${{aY}}%`;
        vehB.style.left = `${{bX}}%`; vehB.style.top = `${{bY}}%`;
        vehA.style.opacity = '1.0'; vehB.style.opacity = '1.0';
        tagVehA.style.opacity = '1.0'; tagVehB.style.opacity = '1.0';

        brakeA1.style.opacity = brakeGlowA; brakeA2.style.opacity = brakeGlowA;
        brakeB1.style.opacity = brakeGlowB; brakeB2.style.opacity = brakeGlowB;

        // Visual Precedence Arrow towards Vehicle B
        if (t >= 2.0 && t <= 5.0) {{
          precedenceArrowGroup.setAttribute('opacity', '1.0');
          precedenceArrowPath.setAttribute('d', 'M 650 490 Q 580 440, 510 385');
          }} else {{
          precedenceArrowGroup.setAttribute('opacity', '0.0');
        }}

        boxHoldSW.setAttribute('opacity', (t >= 2.0 && t <= 5.8) ? '1.0' : '0.0');
        boxHoldSE.setAttribute('opacity', (t >= 2.0 && t <= 3.6) ? '1.0' : '0.0');

        telemVehA.innerHTML = `${{aSpeed}} MPH (${{aSpeed === 0 ? 'YIELDING ON LEFT' : 'MOVING'}})`;
        telemVehA.className = (aSpeed === 0) ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold';
        telemVehB.innerHTML = `${{bSpeed}} MPH (${{bSpeed === 0 ? 'STOPPED ON RIGHT' : 'MOVING'}})`;
        telemVehB.className = (bSpeed === 0) ? 'text-blue-400 font-bold' : 'text-blue-300 font-bold';
        telemPrecedence.innerHTML = (t < 3.6) ? 'VEHICLE B HAS PRIORITY (ON RIGHT)' : (t < 5.8 ? 'VEHICLE B TRAVERSING' : 'VEHICLE A PROCEEDING');
        telemPrecedence.className = 'text-blue-300 font-bold';
        telemStatute.innerHTML = 'TTC § 545.151 YIELD TO RIGHT';
        complianceText.textContent = 'TTC § 545.151 RIGHT-OF-WAY COMPLIANCE VERIFIED';

        if (t < 2.0) {{
          hudNarrative.textContent = 'Both vehicles approach an all-way flashing red signal and come to a full stop at the exact same moment.';
        }} else if (t < 3.6) {{
          hudNarrative.textContent = 'On simultaneous arrival, Texas law (TTC § 545.151) dictates that the driver on the left (Vehicle A) must yield right-of-way to the vehicle on the immediate right (Vehicle B).';
        }} else if (t < 5.8) {{
          hudNarrative.textContent = 'Vehicle B exercises statutory right-of-way and departs first through the intersection while Vehicle A holds stationary.';
        }} else {{
          hudNarrative.textContent = 'Once Vehicle B has cleared, Vehicle A proceeds safely across the intersection.';
        }}

      }} else {{
        // =====================================================================
        // MODE 3: HAZARD DEMO (FAILURE TO STOP AT DARK SIGNAL / T-BONE COLLISION)
        // =====================================================================
        swLensRed.setAttribute('opacity', '0.25');
        swLensYellow.setAttribute('opacity', '0.25');
        swLensGreen.setAttribute('opacity', '0.25');
        swLensRed.classList.remove('flash-red-active');

        seLensRed.setAttribute('opacity', '0.25');
        seLensYellow.setAttribute('opacity', '0.25');
        seLensGreen.setAttribute('opacity', '0.25');
        seLensRed.classList.remove('flash-red-active');

        nwLensRed.setAttribute('opacity', '0.25');
        neLensRed.setAttribute('opacity', '0.25');

        precedenceArrowGroup.setAttribute('opacity', '0.0');
        boxHoldSW.setAttribute('opacity', '0.0');
        boxHoldSE.setAttribute('opacity', '0.0');

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ HAZARD: FAILURE TO STOP AT DARK SIGNAL ✕';
        signalStateBadge.innerHTML = 'SIGNAL: DARK VIOLATION';
        signalStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        // Vehicle B approaches lawfully, stops at t = 1.8s, begins traversing at t = 2.6s
        let bX = 82.0, bY = 82.0, bSpeed = 25, brakeGlowB = 0.0;
        tagVehB.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/40 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider';
        if (t < 1.8) {{
          const p = t / 1.8;
          const ease = smoothCos(p);
          bX = 82.0 - ease * (82.0 - 67.0);
          bY = 82.0 - ease * (82.0 - 70.5);
          bSpeed = Math.round(25 * (1 - p));
          brakeGlowB = (p > 0.3) ? 1.0 : 0.0;
          tagVehB.textContent = `VEHICLE B (LAWFUL STOP: ${{bSpeed}} MPH)`;
        }} else if (t < 2.6) {{
          bX = 67.0; bY = 70.5; bSpeed = 0; brakeGlowB = 1.0;
          tagVehB.textContent = 'VEHICLE B (STOPPED & PROCEEDING)';
        }} else if (t <= 3.5) {{
          const p = (t - 2.6) / (3.5 - 2.6);
          bX = 67.0 - p * (67.0 - 50.0);
          bY = 70.5 - p * (70.5 - 57.0);
          bSpeed = Math.round(p * 15);
          brakeGlowB = 0.0;
          tagVehB.textContent = 'VEHICLE B (IN INTERSECTION)';
        }} else {{
          bX = 50.0; bY = 57.0; bSpeed = 0; brakeGlowB = 0.0; // Collision stop
        }}

        // Vehicle A BLOWS THROUGH DARK SIGNAL WITHOUT STOPPING!
        // Approaches at 35 MPH, crosses stop line without braking, T-bones Vehicle B at t = 3.5s!
        let aX = 18.0, aY = 85.0, aSpeed = 35, brakeGlowA = 0.0;
        if (t <= 3.5) {{
          const p = t / 3.5;
          aX = 18.0 + p * (50.0 - 18.0);
          aY = 85.0 - p * (85.0 - 58.0);
          aSpeed = 35;
          brakeGlowA = (t > 3.0) ? 1.0 : 0.0; // Late emergency panic brake
          tagVehA.textContent = (t < 2.2) ? 'VEHICLE A (IGNORING DARK SIGNAL: 35 MPH)' : 'VEHICLE A (BLOWING STOP LINE: 35 MPH)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';
        }} else {{
          aX = 50.0; aY = 58.0; aSpeed = 0; brakeGlowA = 1.0; // Collision stop
        }}

        vehA.style.left = `${{aX}}%`; vehA.style.top = `${{aY}}%`;
        vehB.style.left = `${{bX}}%`; vehB.style.top = `${{bY}}%`;
        vehA.style.opacity = '1.0'; vehB.style.opacity = '1.0';

        brakeA1.style.opacity = brakeGlowA; brakeA2.style.opacity = brakeGlowA;
        brakeB1.style.opacity = brakeGlowB; brakeB2.style.opacity = brakeGlowB;

        if (t >= 3.2 && t <= 6.2) {{
          tagVehA.style.opacity = '0.0';
          tagVehB.style.opacity = '0.0';
          hazardCollisionZone.setAttribute('opacity', '1.0');
          hazardBanner.style.opacity = '1.0';

          telemVehA.innerHTML = 'CRASH IMPACT (35 MPH BLOWTHROUGH)';
          telemVehA.className = 'text-red-400 font-black animate-pulse';
          telemVehB.innerHTML = 'T-BONE BROADSIDE COLLISION';
          telemVehB.className = 'text-red-400 font-black';
          telemPrecedence.innerHTML = 'VIOLATION OF TTC § 544.007(x)';
          telemPrecedence.className = 'text-red-500 font-black';
          telemStatute.innerHTML = 'CLASS C MISDEMEANOR CITATION';
          telemStatute.className = 'text-red-500 font-black';

          hudNarrative.textContent = 'CRITICAL HAZARD: Vehicle A failed to stop at the dark traffic signal! Disregarding TTC § 544.007(x) results in a devastating broadside T-bone crash.';
          complianceText.textContent = 'CRITICAL VIOLATION: FAILURE TO STOP AT MALFUNCTIONING SIGNAL';
        }} else {{
          hazardCollisionZone.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';
          tagVehA.style.opacity = '1.0';
          tagVehB.style.opacity = '1.0';

          telemVehA.innerHTML = `${{aSpeed}} MPH (DISREGARDING SIGNAL)`;
          telemVehA.className = 'text-red-400 font-bold';
          telemVehB.innerHTML = `${{bSpeed}} MPH (LAWFUL APPROACH)`;
          telemVehB.className = 'text-blue-400 font-bold';
          telemPrecedence.innerHTML = 'VIOLATION IMMINENT';
          telemPrecedence.className = 'text-red-400 font-bold';
          telemStatute.innerHTML = 'TTC § 544.007(x) VIOLATION';
          telemStatute.className = 'text-red-400 font-bold';
          complianceText.textContent = 'TTC § 544.007(x) FAILURE TO STOP VIOLATION';
        }}
      }}
    }}

    // =========================================================================
    // 60 FPS DETERMINISTIC REQUEST ANIMATION FRAME LOOP
    // =========================================================================
    function animationLoop(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const deltaTime = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        currentTime += deltaTime * playbackSpeed;
        if (currentTime >= duration) {{
          if (autoLoop.checked) {{
            currentTime = 0.0;
          }} else {{
            currentTime = duration;
            pauseSimulation();
          }}
        }}
        updateSimulation(currentTime);
      }}

      requestAnimationFrame(animationLoop);
    }}
    requestAnimationFrame(animationLoop);

    // =========================================================================
    // PLAYBACK CONTROLS & LISTENERS
    // =========================================================================
    function playSimulation() {{
      isPlaying = true;
      iconPlay.classList.add('hidden');
      iconPause.classList.remove('hidden');
    }}

    function pauseSimulation() {{
      isPlaying = false;
      iconPlay.classList.remove('hidden');
      iconPause.classList.add('hidden');
    }}

    playPauseBtn.addEventListener('click', () => {{
      if (isPlaying) pauseSimulation();
      else {{
        if (currentTime >= duration) currentTime = 0.0;
        playSimulation();
      }}
    }});

    resetBtn.addEventListener('click', () => {{
      currentTime = 0.0;
      updateSimulation(0.0);
      pauseSimulation();
    }});

    scrubber.addEventListener('input', (e) => {{
      currentTime = parseFloat(e.target.value);
      updateSimulation(currentTime);
    }});

    // Stepper Button Clicks
    stepBtns.forEach((btn) => {{
      btn.addEventListener('click', () => {{
        const stepNum = parseInt(btn.getAttribute('data-step'));
        currentTime = stepTimes[stepNum - 1];
        updateSimulation(currentTime);
        pauseSimulation();
      }});
    }});

    // Speed Controls
    speedBtns.forEach((btn) => {{
      btn.addEventListener('click', () => {{
        speedBtns.forEach(b => {{
          b.classList.remove('bg-blue-600', 'text-white', 'font-bold');
          b.classList.add('text-gray-400');
        }});
        btn.classList.add('bg-blue-600', 'text-white', 'font-bold');
        btn.classList.remove('text-gray-400');
        playbackSpeed = parseFloat(btn.getAttribute('data-speed'));
      }});
    }});

    // Update Stepper Button Labels based on active scenario mode
    function updateStepButtonLabels() {{
      const labels = stepLabelsByMode[simulationMode];
      document.getElementById('step-label-1').textContent = labels[0];
      document.getElementById('step-label-2').textContent = labels[1];
      document.getElementById('step-label-3').textContent = labels[2];
      document.getElementById('step-label-4').textContent = labels[3];
    }}

    // Mode Switch Handlers
    modeDarkBtn.addEventListener('click', () => {{
      simulationMode = 'dark';
      modeDarkBtn.className = 'scenario-btn active px-3 py-1.5 rounded-md font-bold transition flex items-center space-x-1.5';
      modeSimultBtn.className = 'scenario-btn px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      modeHazardBtn.className = 'scenario-btn-hazard px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      updateStepButtonLabels();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    modeSimultBtn.addEventListener('click', () => {{
      simulationMode = 'simultaneous';
      modeSimultBtn.className = 'scenario-btn active px-3 py-1.5 rounded-md font-bold transition flex items-center space-x-1.5';
      modeDarkBtn.className = 'scenario-btn px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      modeHazardBtn.className = 'scenario-btn-hazard px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      updateStepButtonLabels();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    modeHazardBtn.addEventListener('click', () => {{
      simulationMode = 'hazard';
      modeHazardBtn.className = 'scenario-btn-hazard active px-3 py-1.5 rounded-md font-bold transition flex items-center space-x-1.5';
      modeDarkBtn.className = 'scenario-btn px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      modeSimultBtn.className = 'scenario-btn px-3 py-1.5 rounded-md font-bold text-gray-400 hover:text-white transition flex items-center space-x-1.5';
      updateStepButtonLabels();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    // Initial setup
    updateStepButtonLabels();
    updateSimulation(0.0);
  </script>
</body>
</html>
'''

output_path = 'C:/tx_dmv/driving_rule_animations_suite/simulations/L04_T04_dark_malfunctioning_signals.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Lesson 10 simulation built successfully at: {output_path}")
