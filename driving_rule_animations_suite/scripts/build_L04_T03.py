import os
import base64

def get_base64_img(path):
    with open(path, 'rb') as f:
        ext = os.path.splitext(path)[1].lower()
        mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

road_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/roads/texas_suburban_2lane_corridor.jpg'
car_red_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_red_ne.png'
car_yellow_ne_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_yellow_ne.png'
car_blue_sw_path = 'C:/tx_dmv/driving_rule_animations_suite/assets/vehicles/car_blue_sw_clean.png'

print("Encoding Lesson 9 assets to base64...")
road_b64 = get_base64_img(road_path)
car_red_ne_b64 = get_base64_img(car_red_ne_path)
car_yellow_ne_b64 = get_base64_img(car_yellow_ne_path)
car_blue_sw_b64 = get_base64_img(car_blue_sw_path)
print("Assets successfully encoded.")

html_content = f'''<!DOCTYPE html>
<html lang="en" class="h-full bg-[#0B0E11] text-[#ECEFF1] antialiased">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Lesson L04-T03: Pavement Markings — Solid vs. Broken Yellow Lines & Legal Passing (TTC § 545.055)</title>
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
    .turn-signal-blinking {{
      animation: blinkerPulse 0.6s infinite ease-in-out;
    }}

    @keyframes pennantGlow {{
      0%, 100% {{ filter: drop-shadow(0 0 4px #F59E0B); }}
      50% {{ filter: drop-shadow(0 0 14px #FBBF24); }}
    }}
    .pennant-active {{
      animation: pennantGlow 1.2s infinite ease-in-out;
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
        <p class="text-[11px] text-gray-400">Lesson L04–T03: Pavement Markings — Solid vs. Broken Yellow Lines &amp; Legal Passing Corridors (Texas Transportation Code § 545.055)</p>
      </div>
    </div>

    <!-- TRI-SCENARIO MODE TOGGLE -->
    <div class="flex items-center space-x-3">
      <div class="flex items-center rounded-lg bg-[#19202B] p-0.5 border border-[#2B3545]">
        <button id="scenario-btn-pass" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-emerald-500 text-black shadow">
          <span>1: Legal Pass (Broken Yellow Side)</span>
        </button>
        <button id="scenario-btn-solid" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1">
          <span>2: Double Solid Yellow (No Passing)</span>
        </button>
        <button id="scenario-btn-hazard" class="scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1">
          <span>Hazard: Illegal Pass Collision</span>
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
          Step 1: Impediment &amp; Sightline Check
        </button>
        <button data-step="2" data-time="2.5" class="step-btn px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition">
          Step 2: 100-Ft Signal &amp; Departure
        </button>
        <button data-step="3" data-time="4.8" class="step-btn px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition">
          Step 3: Overtaking Traversal
        </button>
        <button data-step="4" data-time="6.8" class="step-btn px-3 py-1 rounded text-xs font-semibold border border-[#2D3748] bg-[#1E2533] text-gray-300 hover:text-white transition">
          Step 4: 200-Ft Buffer Return
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
      
      <!-- LAYER 0: BASE HIGH-RESOLUTION 2.5D SUBURBAN TWO-LANE CORRIDOR -->
      <img src="{road_b64}" alt="Texas 2-Lane Highway Corridor" class="absolute inset-0 w-full h-full object-cover pointer-events-none" />

      <!-- LAYER 1: SVG DYNAMIC ROADWAY MARKINGS & TRAJECTORY GUIDES -->
      <svg id="stage-svg-overlay" viewBox="0 0 1376 768" class="absolute inset-0 w-full h-full pointer-events-none z-10">
        <defs>
          <filter id="glow-amber" x="-30%" y="-30%" width="160%" height="160%">
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

        <!-- CENTERLINE STRIPING OVERLAYS (Clamped precisely to asphalt road boundaries) -->
        <!-- Lane 2 (Oncoming NW Side): Solid Yellow Line -->
        <line id="centerline-solid-lane2" x1="277" y1="607" x2="1027" y2="186" stroke="#F59E0B" stroke-width="4" opacity="0.95" />

        <!-- Lane 1 (Passing SE Side): Broken Dashed Yellow Line (Mode 1 Legal Passing Zone) -->
        <line id="centerline-broken-lane1" x1="283" y1="613" x2="1033" y2="192" stroke="#FBBF24" stroke-width="4" stroke-dasharray="24,16" opacity="0.95" />

        <!-- Lane 1 (Passing SE Side): Solid Yellow Line (Active in Mode 2 & 3: No Passing) -->
        <line id="centerline-solid-lane1" x1="283" y1="613" x2="1033" y2="192" stroke="#F59E0B" stroke-width="4" opacity="0.0" />

        <!-- OVERTAKING PASSING TRAJECTORY ARROW GUIDE (Mode 1: strictly on asphalt corridor) -->
        <path id="pass-trajectory-guide" d="M 300 610 L 370 570 C 430 530, 490 395, 540 370 L 800 235 C 850 215, 920 235, 1007 255" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="6,4" opacity="0.85" />

        <!-- 200-FOOT SAFE RETURN BUFFER ZONE INDICATOR -->
        <g id="buffer-zone-group" opacity="0.0">
          <line id="buffer-line-start" x1="810" y1="365" x2="860" y2="405" stroke="#10B981" stroke-width="2" stroke-dasharray="4,4" />
          <line id="buffer-line-end" x1="945" y1="275" x2="995" y2="315" stroke="#10B981" stroke-width="2" stroke-dasharray="4,4" />
          <text x="760" y="445" fill="#34D399" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" letter-spacing="1">&gt; 200 FT SAFE BUFFER (TTC § 545.054)</text>
        </g>

        <!-- MUTCD W14-3 "NO PASSING ZONE" YELLOW PENNANT SIGN (Positioned on Left Shoulder) -->
        <g id="sign-pennant-w14" transform="translate(320, 275)" opacity="0.0" class="pennant-active">
          <!-- Sign Pole -->
          <line x1="0" y1="0" x2="0" y2="45" stroke="#4B5563" stroke-width="3" />
          <!-- Yellow Pennant Shape (Points right across roadway) -->
          <polygon points="0,-22 68,0 0,22" fill="#FBBF24" stroke="#111827" stroke-width="2.5" filter="url(#glow-amber)" />
          <text x="8" y="-4" fill="#111827" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900">NO</text>
          <text x="8" y="5" fill="#111827" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900">PASSING</text>
          <text x="8" y="14" fill="#111827" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900">ZONE</text>
        </g>

        <!-- HAZARD DEMO: CRITICAL HEAD-ON COLLISION / NEAR-MISS ZONE IN LANE 2 -->
        <g id="hazard-collision-zone" opacity="0.0">
          <circle cx="700" cy="320" r="60" fill="#EF4444" fill-opacity="0.25" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" class="pulse-danger" />
          <circle cx="700" cy="320" r="32" fill="#DC2626" fill-opacity="0.45" stroke="#FCA5A5" stroke-width="2" />
          <line x1="630" y1="320" x2="770" y2="320" stroke="#EF4444" stroke-width="2.5" />
          <line x1="700" y1="250" x2="700" y2="390" stroke="#EF4444" stroke-width="2.5" />
          <polygon points="700,295 710,313 730,310 715,325 725,345 700,333 675,345 685,325 670,310 690,313" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" />
        </g>
      </svg>

      <!-- LAYER 2: VEHICLE SPRITES & DYNAMIC METADATA BADGES -->

      <!-- VEHICLE A (Red Passing Sedan: Follows -> Pulls Out -> Passes -> Returns) -->
      <div id="veh-a-container" class="absolute z-25 transition-transform pointer-events-none" style="left: 16.0%; top: 90.8%; transform: translate(-50%, -50%);">
        <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
          <img src="{car_red_ne_b64}" alt="Vehicle A Passing" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
          
          <!-- Turn Signal Elements -->
          <!-- Left Front Blinker -->
          <div id="veh-a-blinker-left-front" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="top: 22%; right: 20%;"></div>
          <!-- Left Rear Blinker -->
          <div id="veh-a-blinker-left-rear" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 24%; left: 16%;"></div>

          <!-- Right Front Blinker -->
          <div id="veh-a-blinker-right-front" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 18%; right: 14%;"></div>
          <!-- Right Rear Blinker -->
          <div id="veh-a-blinker-right-rear" class="absolute w-2 h-2 rounded-full bg-amber-400 opacity-0" style="bottom: 12%; left: 32%;"></div>

          <!-- Brake Taillights -->
          <div id="veh-a-brake-left" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 22%; left: 16%;"></div>
          <div id="veh-a-brake-right" class="absolute w-2.5 h-2.5 rounded-full bg-red-500 filter blur-[1.5px] opacity-0" style="bottom: 14%; left: 30%;"></div>
        </div>

        <!-- Non-overlapping Identification Badge ABOVE vehicle A (points away from centerline) -->
        <div id="tag-veh-a" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider">
          VEHICLE A (PASSING VEHICLE)
        </div>
      </div>

      <!-- VEHICLE S (Slow Lead Vehicle: Yellow Sedan in Lane 1) -->
      <div id="veh-s-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 44.0%; top: 62.7%; transform: translate(-50%, -50%);">
        <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
          <img src="{car_yellow_ne_b64}" alt="Vehicle S Slow Lead" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>

        <!-- Non-overlapping Identification Badge BELOW vehicle S (points away from centerline) -->
        <div id="tag-veh-s" class="absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider">
          VEHICLE S (SLOW LEAD TRAFFIC - 22 MPH)
        </div>
      </div>

      <!-- VEHICLE B (Oncoming Priority Traffic: Blue Sedan Heading SW in Lane 2 for Mode 3) -->
      <div id="veh-b-container" class="absolute z-20 transition-transform pointer-events-none" style="left: 82.0%; top: 10.4%; transform: translate(-50%, -50%); opacity: 0.0;">
        <div class="relative w-28 md:w-32 aspect-[120/70] flex items-center justify-center">
          <img src="{car_blue_sw_b64}" alt="Vehicle B Oncoming" class="w-full h-full object-contain filter drop-shadow-[0_12px_10px_rgba(0,0,0,0.65)]" />
        </div>

        <!-- Non-overlapping Identification Badge above vehicle -->
        <div id="tag-veh-b" class="absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-blue-500/50 text-[10px] font-bold text-blue-300 mono shadow-lg tracking-wider">
          VEHICLE B (ONCOMING FLOW - 50 MPH)
        </div>
      </div>

      <!-- STRIPING STATUS INSET PILL (Top-Right corner of stage, zero overlap) -->
      <div id="hud-status-pill" class="absolute z-25 px-3 py-1.5 rounded-xl bg-[#051F14]/95 border border-emerald-400 text-emerald-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2" style="top: 10px; right: 10px;">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="pill-status-text">LEGAL PASSING CORRIDOR: BROKEN YELLOW LINE ON YOUR SIDE</span>
      </div>

      <!-- HAZARD DEMO VIOLATION BANNER (Positioned near bottom, unobstructed) -->
      <div id="hazard-banner" class="absolute bottom-14 left-1/2 -translate-x-1/2 z-30 px-5 py-2 rounded-xl bg-red-950/95 border-2 border-red-500 text-red-100 shadow-2xl mono text-center space-y-0.5 pointer-events-none transition-opacity duration-300" style="opacity: 0.0;">
        <div class="text-xs font-black tracking-widest text-red-400 flex items-center justify-center space-x-1.5">
          <span>✕ CRITICAL HAZARD: ILLEGAL PASS ACROSS SOLID YELLOW LINE ✕</span>
        </div>
        <div class="text-[11px] font-semibold text-gray-200">
          TTC § 545.055 Mandate: Never cross into opposing traffic across a solid yellow line on your side!
        </div>
      </div>

      <!-- LAYER 3: ON-STAGE TELEMETRY HUD (Top-Left Fixed Compact Glassmorphism Card) -->
      <div id="telemetry-hud-card" class="absolute top-2.5 left-2.5 z-30 max-w-[340px] w-full bg-[#10141C]/90 backdrop-blur-md rounded-xl border border-[#2B3545] p-3 space-y-2 shadow-xl pointer-events-none">
        <div class="flex items-center justify-between border-b border-[#222B38] pb-1.5">
          <span class="text-[10px] font-bold text-gray-400 mono uppercase tracking-wider">Telemetry &amp; Markings</span>
          <span id="striping-state-badge" class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono">
            STRIPING: BROKEN YELLOW
          </span>
        </div>

        <div class="space-y-1 text-xs mono">
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Vehicle A (Passing):</span>
            <span id="telem-veh-a" class="text-emerald-400 font-bold">25 MPH (TRAILING SAFELY)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Vehicle S (Lead Slow):</span>
            <span id="telem-veh-s" class="text-amber-400 font-bold">22 MPH (IMPEDING FLOW)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Passing Authorization:</span>
            <span id="telem-pass-auth" class="text-emerald-300 font-bold">PERMITTED (BROKEN LINE)</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-400">Statutory Mandate:</span>
            <span id="telem-statute" class="text-emerald-300 font-bold">TTC § 545.055 PASSING ZONE</span>
          </div>
        </div>

        <div class="pt-1.5 border-t border-[#1F2633] text-[11px] text-gray-300 leading-relaxed font-sans" id="hud-narrative">
          A broken yellow centerline on your side indicates a legal passing zone under TTC § 545.055. Vehicle A may pass only when the oncoming lane is clear of traffic for safe passing distance.
        </div>
      </div>

      <!-- ON-STAGE STATUTORY BADGE (Bottom-Right) -->
      <div class="absolute bottom-2.5 right-2.5 z-30 flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-[#0F131A]/90 border border-[#2B3545] text-[10px] mono text-emerald-400 font-semibold shadow-lg pointer-events-none">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="compliance-text">TTC § 545.055 PASSING CORRIDOR COMPLIANCE VERIFIED</span>
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
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400"></span><span>0.5s Broken Line &amp; Sightline Check</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-amber-400"></span><span>2.5s 100-Ft Signal &amp; Pull-Out</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-cyan-400"></span><span>4.8s 45 MPH Rapid Overtake</span></span>
        <span class="flex items-center space-x-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400"></span><span>6.8s &gt;200-Ft Safe Buffer Return</span></span>
      </div>
      <div class="text-[10px] text-gray-400">
        TDLR ADE-1317: Pavement Marking Phasing Protocol (TTC § 545.055)
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

    // Modes: 'pass' (legal broken yellow pass), 'solid' (double solid yellow hold), 'hazard' (illegal solid pass crash)
    let simulationMode = 'pass';

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
    const btnPass = document.getElementById('scenario-btn-pass');
    const btnSolid = document.getElementById('scenario-btn-solid');
    const btnHazard = document.getElementById('scenario-btn-hazard');

    // Sprites & Tags
    const vehA = document.getElementById('veh-a-container');
    const vehS = document.getElementById('veh-s-container');
    const vehB = document.getElementById('veh-b-container');
    const tagVehA = document.getElementById('tag-veh-a');
    const tagVehS = document.getElementById('tag-veh-s');
    const tagVehB = document.getElementById('tag-veh-b');

    // Lights
    const blinkerLF = document.getElementById('veh-a-blinker-left-front');
    const blinkerLR = document.getElementById('veh-a-blinker-left-rear');
    const blinkerRF = document.getElementById('veh-a-blinker-right-front');
    const blinkerRR = document.getElementById('veh-a-blinker-right-rear');
    const brakeA1 = document.getElementById('veh-a-brake-left');
    const brakeA2 = document.getElementById('veh-a-brake-right');

    // SVG Overlays
    const lineBrokenLane1 = document.getElementById('centerline-broken-lane1');
    const lineSolidLane1 = document.getElementById('centerline-solid-lane1');
    const passTrajectoryGuide = document.getElementById('pass-trajectory-guide');
    const bufferZoneGroup = document.getElementById('buffer-zone-group');
    const signPennantW14 = document.getElementById('sign-pennant-w14');
    const hazardCollisionZone = document.getElementById('hazard-collision-zone');
    const hazardBanner = document.getElementById('hazard-banner');
    const hudStatusPill = document.getElementById('hud-status-pill');
    const pillStatusText = document.getElementById('pill-status-text');

    // Telemetry HUD
    const stripingStateBadge = document.getElementById('striping-state-badge');
    const telemVehA = document.getElementById('telem-veh-a');
    const telemVehS = document.getElementById('telem-veh-s');
    const telemPassAuth = document.getElementById('telem-pass-auth');
    const telemStatute = document.getElementById('telem-statute');
    const hudNarrative = document.getElementById('hud-narrative');
    const complianceText = document.getElementById('compliance-text');

    // Canonical Stepper timestamps
    const stepTimes = [0.5, 2.5, 4.8, 6.8];
    let currentStepIdx = 0;

    // Roadway Trajectory Equations (m = -1.005)
    function getLane1Y(x) {{
      return 56.62 - 1.005 * (x - 50.0);
    }}
    function getLane2Y(x) {{
      return 42.56 - 1.005 * (x - 50.0);
    }}

    // S-curve smooth interpolation
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
      stepIndicator.textContent = `Step ${{activeStep + 1}} of 4`;

      if (simulationMode === 'pass') {{
        // =====================================================================
        // MODE 1: LEGAL PASS ON BROKEN YELLOW SIDE (TTC § 545.055a)
        // =====================================================================
        // Visual Pavement Striping: Broken yellow on Lane 1 side, solid on Lane 2
        lineBrokenLane1.setAttribute('opacity', '0.95');
        lineSolidLane1.setAttribute('opacity', '0.0');
        passTrajectoryGuide.setAttribute('opacity', '0.85');
        bufferZoneGroup.setAttribute('opacity', (t >= 5.0 && t <= 7.2) ? '1.0' : '0.0');
        signPennantW14.setAttribute('opacity', '0.0');
        hazardCollisionZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#051F14]/95 border border-emerald-400 text-emerald-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'LEGAL PASSING CORRIDOR: BROKEN YELLOW LINE ON YOUR SIDE';
        stripingStateBadge.innerHTML = 'STRIPING: BROKEN YELLOW';
        stripingStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mono';

        // Vehicle S: Cruising steadily at 22 MPH in Lane 1
        const sX = 40.0 + (t / 8.0) * 18.0;
        const sY = getLane1Y(sX);
        vehS.style.left = `${{sX}}%`;
        vehS.style.top = `${{sY}}%`;
        tagVehS.textContent = 'VEHICLE S (SLOW LEAD TRAFFIC - 22 MPH)';
        tagVehS.style.opacity = '1.0';

        // Vehicle B: Hidden (no oncoming traffic during lawful passing pass)
        vehB.style.opacity = '0.0';
        tagVehB.style.opacity = '0.0';

        // Vehicle A: Multi-Phase Overtaking Traversal
        let aX = 20.0, aY = getLane1Y(20.0);
        let aSpeed = 25;
        let leftBlinker = false, rightBlinker = false, brakeGlow = 0.0;

        if (t < 1.8) {{
          // Phase 1: Trailing in Lane 1 & verifying sightline
          const p = t / 1.8;
          aX = 20.0 + p * (27.0 - 20.0);
          aY = getLane1Y(aX);
          aSpeed = 25;
          tagVehA.textContent = 'VEHICLE A (VERIFYING PASSING SIGHTLINE)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }} else if (t < 3.2) {{
          // Phase 2: 100-Ft Left Signal & Pulling out into Lane 2
          const p = (t - 1.8) / (3.2 - 1.8);
          aX = 27.0 + p * (39.0 - 27.0);
          const ease = smoothCos(p);
          aY = (1 - ease) * getLane1Y(aX) + ease * getLane2Y(aX);
          aSpeed = Math.round(25 + p * 15);
          leftBlinker = true;
          tagVehA.textContent = 'VEHICLE A (SIGNALING 100 FT & PULLING OUT)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }} else if (t < 5.0) {{
          // Phase 3: Overtaking rapidly in Lane 2 at 45 MPH
          const p = (t - 3.2) / (5.0 - 3.2);
          aX = 39.0 + p * (66.0 - 39.0);
          aY = getLane2Y(aX);
          aSpeed = 45;
          tagVehA.textContent = 'VEHICLE A (OVERTAKING IN PASSING LANE - 45 MPH)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-cyan-500/50 text-[10px] font-bold text-cyan-300 mono shadow-lg tracking-wider';
        }} else if (t < 6.6) {{
          // Phase 4: Right Signal & Returning to Lane 1 well ahead (>200 ft buffer)
          const p = (t - 5.0) / (6.6 - 5.0);
          aX = 66.0 + p * (73.0 - 66.0);
          const ease = smoothCos(p);
          aY = (1 - ease) * getLane2Y(aX) + ease * getLane1Y(aX);
          aSpeed = Math.round(45 - p * 5);
          rightBlinker = true;
          tagVehA.textContent = 'VEHICLE A (SIGNALING RIGHT & RE-ENTERING LANE)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }} else {{
          // Phase 5: Pass Completed in Lane 1
          const p = (t - 6.6) / (8.0 - 6.6);
          aX = 73.0 + p * (74.5 - 73.0);
          aY = getLane1Y(aX);
          aSpeed = 40;
          tagVehA.textContent = 'VEHICLE A (LAWFUL PASS COMPLETE)';
          tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-emerald-500/50 text-[10px] font-bold text-emerald-300 mono shadow-lg tracking-wider';
        }}

        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;
        tagVehA.style.opacity = '1.0';

        // Blinker / Brake light state
        const blinkFlash = (Math.floor(t * 4) % 2 === 0);
        blinkerLF.style.opacity = (leftBlinker && blinkFlash) ? '1.0' : '0.0';
        blinkerLR.style.opacity = (leftBlinker && blinkFlash) ? '1.0' : '0.0';
        blinkerRF.style.opacity = (rightBlinker && blinkFlash) ? '1.0' : '0.0';
        blinkerRR.style.opacity = (rightBlinker && blinkFlash) ? '1.0' : '0.0';
        brakeA1.style.opacity = brakeGlow;
        brakeA2.style.opacity = brakeGlow;

        // Telemetry
        telemVehA.innerHTML = `${{aSpeed}} MPH (${{aSpeed > 35 ? 'OVERTAKING FLOW' : 'PASSING SEQUENCE'}})`;
        telemVehA.className = 'text-emerald-400 font-bold';
        telemVehS.innerHTML = '22 MPH (IMPEDING FLOW)';
        telemVehS.className = 'text-amber-400 font-bold';
        telemPassAuth.innerHTML = 'PERMITTED (BROKEN LINE)';
        telemPassAuth.className = 'text-emerald-300 font-bold';
        telemStatute.innerHTML = 'TTC § 545.055(a) LAWFUL PASS';
        telemStatute.className = 'text-emerald-300 font-bold';
        complianceText.textContent = 'TTC § 545.055 PASSING CORRIDOR COMPLIANCE VERIFIED';

        if (t < 2.0) {{
          hudNarrative.textContent = 'A broken yellow line on your side indicates a legal passing zone under TTC § 545.055. Vehicle A checks oncoming traffic sightline.';
        }} else if (t < 4.8) {{
          hudNarrative.textContent = 'With clear sightline, Vehicle A signals left for 100+ feet (TTC § 545.104), enters Lane 2, and accelerates to cleanly overtake Vehicle S.';
        }} else if (t < 6.8) {{
          hudNarrative.textContent = 'Vehicle A signals right and returns to Lane 1 well ahead of Vehicle S, maintaining statutory clearance exceeding 200 feet (TTC § 545.054).';
        }} else {{
          hudNarrative.textContent = 'Passing maneuver safely completed. Both vehicles proceed lawfully in Lane 1 with full right-of-way honored.';
        }}

      }} else if (simulationMode === 'solid') {{
        // =====================================================================
        // MODE 2: DOUBLE SOLID YELLOW LINE — PASSING PROHIBITED (TTC § 545.055b)
        // =====================================================================
        lineBrokenLane1.setAttribute('opacity', '0.0');
        lineSolidLane1.setAttribute('opacity', '0.95');
        passTrajectoryGuide.setAttribute('opacity', '0.0');
        bufferZoneGroup.setAttribute('opacity', '0.0');
        signPennantW14.setAttribute('opacity', '1.0');
        hazardCollisionZone.setAttribute('opacity', '0.0');
        hazardBanner.style.opacity = '0.0';

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B1B05]/95 border border-amber-400 text-amber-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = 'NO PASSING ZONE: DOUBLE SOLID YELLOW LINE // HOLD LANE';
        stripingStateBadge.innerHTML = 'STRIPING: DOUBLE SOLID';
        stripingStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 mono';

        // Vehicle S: Cruising in Lane 1 at 22 MPH
        const sX = 42.0 + (t / 8.0) * 24.0;
        const sY = getLane1Y(sX);
        vehS.style.left = `${{sX}}%`;
        vehS.style.top = `${{sY}}%`;
        tagVehS.textContent = 'VEHICLE S (SLOW LEAD TRAFFIC - 22 MPH)';
        tagVehS.style.opacity = '1.0';

        // Vehicle B: Hidden
        vehB.style.opacity = '0.0';
        tagVehB.style.opacity = '0.0';

        // Vehicle A: Approaching in Lane 1, brakes, holds steady following distance behind Vehicle S
        let aX = 22.0, aSpeed = 30, brakeGlow = 0.0;
        if (t < 2.0) {{
          const p = t / 2.0;
          aX = 22.0 + p * ((sX - 18.0) - 22.0);
          aSpeed = Math.round(30 - p * 8);
          brakeGlow = (p > 0.4) ? 1.0 : 0.0;
        }} else {{
          aX = sX - 18.0;
          aSpeed = 22;
          brakeGlow = 0.0;
        }}
        const aY = getLane1Y(aX);
        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;
        tagVehA.textContent = (t < 2.5) ? 'VEHICLE A (DECELERATING BEHIND TRAFFIC)' : 'VEHICLE A (HOLDING LANE — NO PASSING)';
        tagVehA.className = 'absolute left-1/2 -translate-x-1/2 mt-1 whitespace-nowrap px-2.5 py-0.5 rounded bg-[#10141C]/90 border border-amber-500/50 text-[10px] font-bold text-amber-300 mono shadow-lg tracking-wider';
        tagVehA.style.opacity = '1.0';

        blinkerLF.style.opacity = '0.0';
        blinkerLR.style.opacity = '0.0';
        blinkerRF.style.opacity = '0.0';
        blinkerRR.style.opacity = '0.0';
        brakeA1.style.opacity = brakeGlow;
        brakeA2.style.opacity = brakeGlow;

        telemVehA.innerHTML = `${{aSpeed}} MPH (HOLDING 3-SEC BUFFER)`;
        telemVehA.className = 'text-amber-400 font-bold';
        telemVehS.innerHTML = '22 MPH (IMPEDING FLOW)';
        telemVehS.className = 'text-amber-400 font-bold';
        telemPassAuth.innerHTML = 'STRICTLY PROHIBITED';
        telemPassAuth.className = 'text-red-400 font-bold';
        telemStatute.innerHTML = 'TTC § 545.055(b) NO PASSING';
        telemStatute.className = 'text-red-400 font-bold';
        complianceText.textContent = 'TTC § 545.055(b) NO-PASSING ZONE COMPLIANCE VERIFIED';

        hudNarrative.textContent = 'Facing double solid yellow lines or MUTCD W14-3 pennant, passing is strictly prohibited in either direction under TTC § 545.055(b). Vehicle A maintains safe buffer.';

      }} else {{
        // =====================================================================
        // MODE 3: HAZARD DEMO (ILLEGAL PASS ACROSS SOLID LINE // ONCOMING HEAD-ON)
        // =====================================================================
        lineBrokenLane1.setAttribute('opacity', '0.0');
        lineSolidLane1.setAttribute('opacity', '0.95');
        passTrajectoryGuide.setAttribute('opacity', '0.0');
        bufferZoneGroup.setAttribute('opacity', '0.0');
        signPennantW14.setAttribute('opacity', '1.0');

        hudStatusPill.className = 'absolute z-25 px-3 py-1.5 rounded-xl bg-[#2B0505]/95 border border-red-500 text-red-300 mono text-[10px] font-extrabold shadow-xl tracking-wider transition-all pointer-events-none flex items-center space-x-2';
        pillStatusText.textContent = '✕ HAZARD: ILLEGAL PASS ACROSS SOLID YELLOW LINE ✕';
        stripingStateBadge.innerHTML = 'STRIPING: SOLID VIOLATION';
        stripingStateBadge.className = 'text-[9px] font-extrabold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 mono';

        // Vehicle S: in Lane 1
        const sX = 42.0 + (t / 8.0) * 20.0;
        const sY = getLane1Y(sX);
        vehS.style.left = `${{sX}}%`;
        vehS.style.top = `${{sY}}%`;
        tagVehS.textContent = 'VEHICLE S (SLOW LEAD TRAFFIC)';
        tagVehS.style.opacity = '1.0';

        // Vehicle B arrives fast from NE heading SW in Lane 2
        let bX = 74.0, bY = getLane2Y(74.0), bOpacity = 1.0;
        if (t <= 3.4) {{
          const p = t / 3.4;
          bX = 74.0 - p * (74.0 - 56.0);
          bY = getLane2Y(bX);
        }} else {{
          bX = 56.0; bY = getLane2Y(56.0); // Emergency stop position
        }}
        vehB.style.left = `${{bX}}%`;
        vehB.style.top = `${{bY}}%`;
        vehB.style.opacity = bOpacity;
        tagVehB.textContent = 'VEHICLE B (ONCOMING FLOW - 50 MPH)';
        tagVehB.style.opacity = (t >= 3.2 && t <= 5.8) ? '0.0' : '1.0';

        // Vehicle A illegally crosses solid yellow line into Lane 2!
        let aX = 22.0, aY = getLane1Y(22.0), aSpeed = 25;
        if (t <= 1.0) {{
          aX = 22.0; aY = getLane1Y(22.0); aSpeed = 25;
        }} else if (t <= 3.4) {{
          const p = (t - 1.0) / (3.4 - 1.0);
          aX = 22.0 + p * (46.0 - 22.0);
          const ease = smoothCos(p);
          aY = (1 - ease) * getLane1Y(aX) + ease * getLane2Y(aX);
          aSpeed = Math.round(25 + p * 18);
        }} else {{
          aX = 46.0; aY = getLane2Y(46.0); aSpeed = 0; // Emergency stop position
        }}
        vehA.style.left = `${{aX}}%`;
        vehA.style.top = `${{aY}}%`;

        blinkerLF.style.opacity = (t > 1.0 && t < 3.2 && (Math.floor(t * 4) % 2 === 0)) ? '1.0' : '0.0';
        blinkerLR.style.opacity = blinkerLF.style.opacity;
        blinkerRF.style.opacity = '0.0';
        blinkerRR.style.opacity = '0.0';
        brakeA1.style.opacity = (t >= 3.2) ? '1.0' : '0.0';
        brakeA2.style.opacity = (t >= 3.2) ? '1.0' : '0.0';

        if (t >= 3.2 && t <= 5.8) {{
          tagVehA.style.opacity = '0.0';
          tagVehB.style.opacity = '0.0';
          hazardCollisionZone.setAttribute('opacity', '1.0');
          hazardBanner.style.opacity = '1.0';

          telemVehA.innerHTML = 'EMERGENCY BRAKE (HEAD-ON NEAR-MISS)';
          telemVehA.className = 'text-red-400 font-black animate-pulse';
          telemVehS.innerHTML = '22 MPH (IN LANE 1)';
          telemPassAuth.innerHTML = 'ILLEGAL (SOLID YELLOW)';
          telemPassAuth.className = 'text-red-400 font-black';
          telemStatute.innerHTML = 'TTC § 545.055 VIOLATION';
          telemStatute.className = 'text-red-500 font-black';

          hudNarrative.textContent = 'CRITICAL HAZARD: Driver crossed solid yellow line into oncoming 50 MPH traffic! Catastrophic head-on near-miss/collision in Lane 2.';
          complianceText.textContent = 'CRITICAL VIOLATION: ILLEGAL PASSING ACROSS SOLID YELLOW LINE';
        }} else {{
          tagVehA.style.opacity = '1.0';
          hazardCollisionZone.setAttribute('opacity', '0.0');
          hazardBanner.style.opacity = '0.0';

          if (t < 3.2) {{
            tagVehA.textContent = 'VEHICLE A (ILLEGAL PASS ACROSS SOLID LINE)';
            tagVehA.className = 'absolute left-1/2 -translate-x-1/2 -top-7 whitespace-nowrap px-2.5 py-0.5 rounded bg-red-950/90 border border-red-500 text-[10px] font-bold text-red-300 mono shadow-lg tracking-wider';
            telemVehA.innerHTML = `${{aSpeed}} MPH (ILLEGAL PASSING CORRIDOR)`;
            telemVehA.className = 'text-red-400 font-bold';
            telemVehS.innerHTML = '22 MPH (IN LANE 1)';
            hudNarrative.textContent = 'Vehicle A impatiently crosses solid yellow line without verified sightline. Oncoming traffic poses immediate hazard!';
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
      pass: [
        'Step 1: Impediment & Sightline Check',
        'Step 2: 100-Ft Signal & Departure',
        'Step 3: Overtaking Traversal',
        'Step 4: 200-Ft Buffer Return'
      ],
      solid: [
        'Step 1: Double Solid Yellow Recognition',
        'Step 2: W14-3 No Passing Compliance',
        'Step 3: Deceleration Behind Traffic',
        'Step 4: Safe Following Cushion Held'
      ],
      hazard: [
        'Step 1: Solid Yellow Display & Impatience',
        'Step 2: Illegal Incursion into Lane 2',
        'Step 3: High-Speed Head-On Conflict',
        'Step 4: Failure to Yield Citation (§ 545.055)'
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
    btnPass.addEventListener('click', () => {{
      simulationMode = 'pass';
      btnPass.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-emerald-500 text-black shadow';
      btnSolid.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    btnSolid.addEventListener('click', () => {{
      simulationMode = 'solid';
      btnPass.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnSolid.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center space-x-1 bg-amber-500 text-black shadow';
      btnHazard.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      updateStepButtonLabels();
      pauseSimulation();
      currentTime = 0.0;
      updateSimulation(0.0);
    }});

    btnHazard.addEventListener('click', () => {{
      simulationMode = 'hazard';
      btnPass.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
      btnSolid.className = 'scenario-toggle-btn px-2.5 py-1 rounded-md text-xs font-semibold text-gray-400 hover:text-white transition flex items-center space-x-1';
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

output_path = 'C:/tx_dmv/driving_rule_animations_suite/simulations/L04_T03_pavement_markings_passing.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Lesson 9 simulation built successfully at:", output_path)
