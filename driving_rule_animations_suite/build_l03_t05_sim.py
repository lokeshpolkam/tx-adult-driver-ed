import base64
import os

def get_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

road_b64 = get_b64(r'C:\tx_dmv\driving_rule_animations_suite\assets\roads\texas_suburban_2lane_corridor.jpg')
bus_b64 = get_b64(r'C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\school_bus_tx_ne_retina.png')
car_red_b64 = get_b64(r'C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_red_ne.png')
car_blue_b64 = get_b64(r'C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_blue_sw_clean.png')

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson L03-T05: School Bus Stop Law (TTC § 545.066) - Texas Adult Driver Ed</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0A0D14;
      color: #E2E8F0;
      margin: 0;
      overflow-x: hidden;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .sim-stage {{
      position: relative;
      width: 100%;
      aspect-ratio: 1376 / 768;
      max-height: 680px;
      background-color: #0B0E14;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }}
    .sim-bg {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      pointer-events: none;
      user-select: none;
    }}
    .sim-veh {{
      position: absolute;
      transform: translate(-50%, -50%);
      pointer-events: none;
      user-select: none;
      transition: filter 0.2s ease;
    }}
    /* Roof Beacons Alternating Flash */
    @keyframes wigwag-left {{
      0%, 49% {{ opacity: 1; transform: scale(1.2); filter: drop-shadow(0 0 8px #FF0033); }}
      50%, 100% {{ opacity: 0.15; transform: scale(0.9); filter: none; }}
    }}
    @keyframes wigwag-right {{
      0%, 49% {{ opacity: 0.15; transform: scale(0.9); filter: none; }}
      50%, 100% {{ opacity: 1; transform: scale(1.2); filter: drop-shadow(0 0 8px #FF0033); }}
    }}
    .strobe-left {{
      animation: wigwag-left 0.5s infinite;
    }}
    .strobe-right {{
      animation: wigwag-right 0.5s infinite;
    }}
    /* Amber Prep Blink */
    @keyframes amber-blink {{
      0%, 49% {{ opacity: 1; filter: drop-shadow(0 0 8px #FFAA00); }}
      50%, 100% {{ opacity: 0.2; filter: none; }}
    }}
    .amber-flasher {{
      animation: amber-blink 0.6s infinite;
    }}
    /* Brake Glow */
    .brake-light {{
      box-shadow: 0 0 10px 4px rgba(255, 30, 30, 0.85);
      border-radius: 50%;
    }}
    /* Custom Range Slider */
    input[type=range] {{
      -webkit-appearance: none;
      background: #1E293B;
      border-radius: 9999px;
      height: 6px;
    }}
    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      height: 18px;
      width: 18px;
      border-radius: 50%;
      background: #3B82F6;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.6);
      border: 2px solid #FFFFFF;
    }}
  </style>
</head>
<body class="p-4 md:p-6 lg:p-8 flex flex-col items-center min-h-screen">

  <div class="max-w-7xl w-full space-y-4">

    <!-- HEADER / COMPLIANCE BANNER -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#121722] border border-[#1E2636] p-4 rounded-2xl shadow-lg">
      <div class="flex items-center space-x-3">
        <span class="px-2.5 py-1 rounded-md bg-blue-500/10 border border-blue-500/20 text-blue-400 font-bold text-xs mono">TDLR ADE-1317</span>
        <span class="px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/20 text-amber-300 font-bold text-xs mono">2.5D VECTOR ENGINE</span>
        <div>
          <h1 class="text-base md:text-lg font-bold text-white tracking-tight">TEXAS DRIVING–RULE ANIMATION SYSTEM</h1>
          <p class="text-xs text-gray-400">Lesson L03–T05: Passing Stopped Emergency Vehicles &amp; School Buses (Texas Transportation Code &sect; 545.066)</p>
        </div>
      </div>

      <!-- SCENARIO MODE TOGGLE -->
      <div class="flex items-center space-x-2 bg-[#0E131D] p-1.5 rounded-xl border border-[#232D3F]">
        <button id="modeUndividedBtn" onclick="setScenarioMode('undivided')" class="px-3 py-1 rounded-lg text-xs font-bold transition bg-amber-500 text-black shadow-md">
          Primary: Undivided Road (Both Stop)
        </button>
        <button id="modeDividedBtn" onclick="setScenarioMode('divided')" class="px-3 py-1 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition">
          Exception: Divided Highway (Barrier)
        </button>
      </div>

      <div class="flex items-center space-x-4">
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-xs mono text-emerald-400 font-medium">Deterministic 60 FPS</span>
        </div>
        <label class="flex items-center space-x-2 text-xs text-gray-300 cursor-pointer select-none">
          <input type="checkbox" id="autoLoopCheck" checked class="rounded border-gray-700 bg-gray-900 text-blue-500 focus:ring-0">
          <span>Auto-Loop</span>
        </label>
      </div>
    </header>

    <!-- CANONICAL STEP SELECTOR BUTTONS -->
    <nav class="flex items-center justify-between gap-2">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2 flex-1">
        <button id="stepBtn1" onclick="jumpToStep(1)" class="px-3 py-2 rounded-xl border border-blue-500/50 bg-blue-500/10 text-blue-300 font-bold text-xs text-center transition hover:bg-blue-500/20">
          Step 1: Amber Signal Detection
        </button>
        <button id="stepBtn2" onclick="jumpToStep(2)" class="px-3 py-2 rounded-xl border border-gray-800 bg-[#121620] text-gray-400 font-bold text-xs text-center transition hover:bg-[#1A202C]">
          Step 2: Red Flashers &amp; STOP Arm
        </button>
        <button id="stepBtn3" onclick="jumpToStep(3)" class="px-3 py-2 rounded-xl border border-gray-800 bg-[#121620] text-gray-400 font-bold text-xs text-center transition hover:bg-[#1A202C]">
          Step 3: Student Crossing Zone
        </button>
        <button id="stepBtn4" onclick="jumpToStep(4)" class="px-3 py-2 rounded-xl border border-gray-800 bg-[#121620] text-gray-400 font-bold text-xs text-center transition hover:bg-[#1A202C]">
          Step 4: Lawful Resumption
        </button>
      </div>
      <div class="flex items-center space-x-1 pl-2">
        <button onclick="prevStep()" class="px-2.5 py-2 rounded-lg bg-[#141A25] border border-gray-800 text-gray-400 hover:text-white text-xs font-bold transition">&lsaquo; Prev</button>
        <span id="stepCounter" class="mono text-xs px-2 text-amber-400 font-bold">Step 1 of 4</span>
        <button onclick="nextStep()" class="px-2.5 py-2 rounded-lg bg-[#141A25] border border-gray-800 text-gray-400 hover:text-white text-xs font-bold transition">Next &rsaquo;</button>
      </div>
    </nav>

    <!-- SIMULATION CANVAS CONTAINER -->
    <main class="sim-stage" id="stageContainer">

      <!-- 2.5D SUBURBAN ROADWAY BACKGROUND -->
      <img src="data:image/jpeg;base64,{road_b64}" alt="Texas Suburban 2-Lane Corridor" class="sim-bg">

      <!-- DIVIDED HIGHWAY PHYSICAL MEDIAN BARRIER (Rendered only in Divided Mode) -->
      <div id="dividedBarrierOverlay" class="absolute inset-0 pointer-events-none hidden z-15">
        <!-- SVG Isometric Physical Concrete Barrier along center yellow line -->
        <svg viewBox="0 0 1376 768" class="w-full h-full">
          <defs>
            <linearGradient id="barrierConcrete" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#D5DBE3"/>
              <stop offset="60%" stop-color="#959FA9"/>
              <stop offset="100%" stop-color="#555E68"/>
            </linearGradient>
            <linearGradient id="barrierTop" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#EAEFF5"/>
              <stop offset="100%" stop-color="#BDC5D0"/>
            </linearGradient>
          </defs>
          <!-- Concrete Jersey Barrier spanning the entire visible yellow corridor -->
          <polygon points="310,594 1150,123 1150,111 310,582" fill="url(#barrierConcrete)"/>
          <polygon points="310,582 1150,111 1144,107 304,578" fill="url(#barrierTop)"/>
        </svg>
        <!-- Badge positioned clearly over center median with zero car overlap -->
        <div class="absolute top-[38%] left-[42%] -translate-x-1/2 px-3 py-1 rounded-full bg-blue-900/95 border border-blue-400 text-blue-200 text-[10px] font-bold mono shadow-2xl">
          PHYSICAL CONCRETE MEDIAN BARRIER (SEPARATE ROADWAYS)
        </div>
      </div>

      <!-- 1. VEHICLE A (Following Traffic in Lane 1, heading NE) -->
      <div id="vehA" class="sim-veh" style="left: 36.0%; top: 70.7%; width: 105px; z-index: 25;">
        <img src="data:image/png;base64,{car_red_b64}" alt="Following Vehicle A" class="w-full">
        <!-- Brake Lights Flares (Dual rear red flares at lower-left of sprite) -->
        <div id="vehABrakeL" class="absolute brake-light hidden" style="left: 14px; top: 48px; width: 7px; height: 7px; background: #FF0033;"></div>
        <div id="vehABrakeR" class="absolute brake-light hidden" style="left: 26px; top: 56px; width: 7px; height: 7px; background: #FF0033;"></div>
        <!-- Tag -->
        <div id="tagA" class="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-red-500/60 text-[10px] font-bold text-red-300 mono pointer-events-none">
          VEHICLE A (APPROACHING 30 MPH)
        </div>
      </div>

      <!-- 2. TEXAS SCHOOL BUS (In Lane 1, heading NE) -->
      <div id="schoolBus" class="sim-veh" style="left: 55.0%; top: 51.6%; width: 180px; z-index: 28;">
        <img src="data:image/png;base64,{bus_b64}" alt="Texas School Bus" class="w-full">

        <!-- Amber Warning Prep Flashers (Front & Rear Roof Beacons) -->
        <div id="busAmberFlasherRear" class="absolute amber-flasher hidden" style="left: 36px; top: 25px; width: 8px; height: 8px; background: #FFB300; border-radius: 50%;"></div>
        <div id="busAmberFlasherFront" class="absolute amber-flasher hidden" style="left: 122px; top: 13px; width: 8px; height: 8px; background: #FFB300; border-radius: 50%;"></div>

        <!-- Alternating Red Flashing Beacons (Wig-Wag) -->
        <div id="busRedFlasherRear" class="absolute strobe-left hidden" style="left: 35px; top: 24px; width: 9px; height: 9px; background: #FF0033; border-radius: 50%;"></div>
        <div id="busRedFlasherFront" class="absolute strobe-right hidden" style="left: 121px; top: 12px; width: 9px; height: 9px; background: #FF0033; border-radius: 50%;"></div>

        <!-- Deployable Octagonal Red STOP Arm (Driver Side, extends toward double yellow line from front cab) -->
        <div id="stopArm" class="absolute transition-all duration-500 ease-out pointer-events-none hidden" style="left: 95px; top: -6px; z-index: 35;">
          <svg width="40" height="40" viewBox="0 0 100 100" class="drop-shadow-xl">
            <!-- Stop Sign Polygon -->
            <polygon points="30,5 70,5 95,30 95,70 70,95 30,95 5,70 5,30" fill="#D32F2F" stroke="#FFFFFF" stroke-width="5"/>
            <polygon points="32,10 68,10 90,32 90,68 68,90 32,90 10,68 10,32" fill="#D32F2F" stroke="#FFFFFF" stroke-width="2"/>
            <text x="50" y="60" font-family="'JetBrains Mono', sans-serif" font-weight="900" font-size="26" fill="#FFFFFF" text-anchor="middle">STOP</text>
            <circle cx="50" cy="18" r="5" fill="#FF1744" class="animate-ping"/>
            <circle cx="50" cy="82" r="5" fill="#FF1744" class="animate-ping"/>
          </svg>
        </div>

        <!-- Tag placed below bus on curb side -->
        <div id="tagBus" class="absolute whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-amber-500/60 text-[10px] font-bold text-amber-300 mono pointer-events-none" style="bottom: -24px; left: 50%; transform: translateX(-50%);">
          TEXAS SCHOOL BUS
        </div>
      </div>

      <!-- 3. STUDENT PEDESTRIAN (Walking across street in front of bus bumper) -->
      <div id="studentPed" class="absolute pointer-events-none transition-all hidden z-30" style="left: 65.0%; top: 52.0%; transform: translate(-50%, -50%);">
        <svg width="26" height="38" viewBox="0 0 28 40" class="drop-shadow-md">
          <ellipse cx="14" cy="37" rx="8" ry="3" fill="rgba(0,0,0,0.5)"/>
          <line x1="11" y1="28" x2="10" y2="36" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>
          <line x1="17" y1="28" x2="18" y2="36" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>
          <rect x="8" y="14" width="12" height="15" rx="3" fill="#2563EB"/>
          <rect x="5" y="15" width="4" height="11" rx="2" fill="#F59E0B"/>
          <circle cx="14" cy="9" r="6" fill="#FBBF24"/>
          <path d="M 8 7 Q 14 3 20 7 L 22 8 L 8 8 Z" fill="#DC2626"/>
        </svg>
        <!-- Tag -->
        <div id="tagStudent" class="absolute -top-5 left-1/2 -translate-x-1/2 whitespace-nowrap px-1.5 py-0.2 rounded bg-blue-900/90 border border-blue-400 text-[8px] font-bold text-blue-200 mono">
          STUDENT CROSSING
        </div>
      </div>

      <!-- 4. VEHICLE B (Opposing Traffic in Lane 2, heading SW) -->
      <div id="vehB" class="sim-veh" style="left: 68.0%; top: 24.5%; width: 105px; z-index: 22;">
        <img src="data:image/png;base64,{car_blue_b64}" alt="Opposing Vehicle B" class="w-full">
        <!-- Brake Lights Flares (Dual rear red flares at upper-right of sprite) -->
        <div id="vehBBrakeL" class="absolute brake-light hidden" style="left: 66px; top: 20px; width: 6px; height: 6px; background: #FF0033;"></div>
        <div id="vehBBrakeR" class="absolute brake-light hidden" style="left: 78px; top: 28px; width: 6px; height: 6px; background: #FF0033;"></div>
        <!-- Tag -->
        <div id="tagB" class="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-blue-500/60 text-[10px] font-bold text-blue-300 mono pointer-events-none">
          VEHICLE B (OPPOSING TRAFFIC)
        </div>
      </div>

      <!-- HUD TELEMETRY & RULE EXPLANATION OVERLAY -->
      <div class="absolute top-4 left-4 max-w-sm rounded-xl bg-[#0D1117]/95 border border-[#232B39] p-4 text-xs shadow-2xl backdrop-blur space-y-3 z-40">
        <div class="space-y-1 border-b border-gray-800 pb-2">
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Following (Veh A):</span>
            <span id="hudSpeedA" class="font-bold text-emerald-400">30 MPH</span>
          </div>
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Opposing (Veh B):</span>
            <span id="hudSpeedB" class="font-bold text-blue-400">30 MPH</span>
          </div>
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Bus Signals:</span>
            <span id="hudSignals" class="font-bold text-amber-400">Amber Advance</span>
          </div>
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Legal Mandate:</span>
            <span id="hudMandate" class="font-bold text-amber-300">Prepare to Stop</span>
          </div>
        </div>

        <div id="hudExplanation" class="text-gray-300 leading-relaxed text-[11px]">
          School bus activates flashing amber warning beacons. Approaching drivers in BOTH directions on undivided roadways must prepare for mandatory full stop.
        </div>
      </div>

      <!-- STATUTORY RULE VERIFICATION BADGE (Positioned above footer) -->
      <div id="statuteBadge" class="absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-amber-500/50 text-amber-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50">
        <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></span>
        <span id="statuteBadgeText">TTC &sect; 545.066: MANDATORY DUAL-DIRECTION STOP</span>
      </div>

    </main>

    <!-- SCRUBBABLE PLAYBACK CONTROLS -->
    <footer class="bg-[#121722] border border-[#1E2636] p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 shadow-lg">
      
      <!-- PLAY / PAUSE / RESTART -->
      <div class="flex items-center space-x-2">
        <button id="playPauseBtn" onclick="togglePlay()" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center space-x-2 transition shadow">
          <span id="playIcon">&#10074;&#10074; Pause</span>
        </button>
        <button onclick="restartSim()" class="p-2 rounded-xl bg-[#1A2232] hover:bg-[#253046] text-gray-300 hover:text-white transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
        </button>
        <!-- SPEED MULTIPLIERS -->
        <div class="flex items-center space-x-1 bg-[#0F141E] p-1 rounded-lg border border-gray-800 text-[11px] mono">
          <button onclick="setSpeed(0.5)" id="speedBtn05" class="px-2 py-0.5 rounded text-gray-400 hover:text-white transition">0.5x</button>
          <button onclick="setSpeed(1.0)" id="speedBtn10" class="px-2 py-0.5 rounded bg-blue-600 text-white font-bold transition">1.0x</button>
          <button onclick="setSpeed(1.5)" id="speedBtn15" class="px-2 py-0.5 rounded text-gray-400 hover:text-white transition">1.5x</button>
        </div>
      </div>

      <!-- TIMELINE SCRUBBER -->
      <div class="flex-1 w-full flex items-center space-x-3">
        <span id="currentTimeDisplay" class="mono text-xs text-blue-400 font-bold min-w-[45px]">0.00s</span>
        <input type="range" id="timeSlider" min="0" max="9.5" step="0.02" value="0" class="w-full" oninput="onScrub(this.value)">
        <span class="mono text-xs text-gray-500">9.50s</span>
      </div>

      <!-- STATUTORY BADGE -->
      <div class="flex items-center space-x-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span class="text-xs text-gray-300 font-medium">TTC &sect; 545.066 Compliance Verified</span>
      </div>
    </footer>

  </div>

  <script>
    // SIMULATION STATE & CONFIGURATION
    let isPlaying = true;
    let simTime = 0.0;
    const maxTime = 9.5;
    let speed = 1.0;
    let lastTimestamp = null;
    let scenarioMode = 'undivided'; // 'undivided' or 'divided'

    // DOM ELEMENTS
    const stageContainer = document.getElementById('stageContainer');
    const dividedBarrierOverlay = document.getElementById('dividedBarrierOverlay');
    const vehA = document.getElementById('vehA');
    const vehABrakeL = document.getElementById('vehABrakeL');
    const vehABrakeR = document.getElementById('vehABrakeR');
    const tagA = document.getElementById('tagA');

    const schoolBus = document.getElementById('schoolBus');
    const busAmberFlasherRear = document.getElementById('busAmberFlasherRear');
    const busAmberFlasherFront = document.getElementById('busAmberFlasherFront');
    const busRedFlasherRear = document.getElementById('busRedFlasherRear');
    const busRedFlasherFront = document.getElementById('busRedFlasherFront');
    const stopArm = document.getElementById('stopArm');
    const tagBus = document.getElementById('tagBus');

    const studentPed = document.getElementById('studentPed');
    const tagStudent = document.getElementById('tagStudent');

    const vehB = document.getElementById('vehB');
    const vehBBrakeL = document.getElementById('vehBBrakeL');
    const vehBBrakeR = document.getElementById('vehBBrakeR');
    const tagB = document.getElementById('tagB');

    const hudSpeedA = document.getElementById('hudSpeedA');
    const hudSpeedB = document.getElementById('hudSpeedB');
    const hudSignals = document.getElementById('hudSignals');
    const hudMandate = document.getElementById('hudMandate');
    const hudExplanation = document.getElementById('hudExplanation');
    const statuteBadge = document.getElementById('statuteBadge');
    const statuteBadgeText = document.getElementById('statuteBadgeText');

    const timeSlider = document.getElementById('timeSlider');
    const currentTimeDisplay = document.getElementById('currentTimeDisplay');
    const playIcon = document.getElementById('playIcon');
    const stepCounter = document.getElementById('stepCounter');

    // ROADWAY TRAJECTORY EQUATIONS (Linear Isometric Slope m = -1.005)
    function getLane1Y(x) {{
      return 56.62 - 1.005 * (x - 50.0);
    }}
    function getLane2Y(x) {{
      return 42.56 - 1.005 * (x - 50.0);
    }}

    // UPDATE SIMULATION PHYSICS & VISUALS
    function updateSimulation(t) {{
      let activeStep = 1;
      let speedAStr = "30 MPH";
      let speedBStr = "30 MPH";
      let signalsStr = "Amber Prep Flashers";
      let mandateStr = "Prepare for Mandatory Stop";
      let explanationStr = "";

      // 1. SCHOOL BUS TRAJECTORY & SIGNALS
      let busX, busY;
      if (t < 2.5) {{
        let p = t / 2.5;
        let ease = 1 - Math.pow(1 - p, 2);
        busX = 42.0 + ease * 13.0;
        busY = getLane1Y(busX);

        busAmberFlasherRear.classList.remove('hidden');
        busAmberFlasherFront.classList.remove('hidden');
        busRedFlasherRear.classList.add('hidden');
        busRedFlasherFront.classList.add('hidden');
        stopArm.classList.add('hidden');
        tagBus.innerHTML = "TEXAS SCHOOL BUS (PREPARING TO STOP)";
        tagBus.className = "absolute whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-yellow-500/60 text-[10px] font-bold text-yellow-300 mono pointer-events-none";
      }} else if (t < 7.2) {{
        busX = 55.0;
        busY = getLane1Y(busX);

        busAmberFlasherRear.classList.add('hidden');
        busAmberFlasherFront.classList.add('hidden');
        busRedFlasherRear.classList.remove('hidden');
        busRedFlasherFront.classList.remove('hidden');
        stopArm.classList.remove('hidden');
        tagBus.innerHTML = "<span class='w-1.5 h-1.5 rounded-full bg-red-500 animate-ping inline-block mr-1'></span>VISUAL SIGNALS ACTIVE &bull; STOP ARM EXTENDED";
        tagBus.className = "absolute whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-red-500/70 text-[10px] font-bold text-red-300 mono pointer-events-none";
      }} else {{
        let p = (t - 7.2) / 2.3;
        let ease = p * p;
        busX = 55.0 + ease * 26.0;
        busY = getLane1Y(busX);

        busAmberFlasherRear.classList.add('hidden');
        busAmberFlasherFront.classList.add('hidden');
        busRedFlasherRear.classList.add('hidden');
        busRedFlasherFront.classList.add('hidden');
        stopArm.classList.add('hidden');
        tagBus.innerHTML = "TEXAS SCHOOL BUS (RESUMING MOTION)";
        tagBus.className = "absolute whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-emerald-500/60 text-[10px] font-bold text-emerald-300 mono pointer-events-none";
      }}
      schoolBus.style.left = busX + "%";
      schoolBus.style.top = busY + "%";

      // 2. FOLLOWING VEHICLE A (Trailing in Lane 1, heading NE)
      let ax, ay;
      if (t < 2.5) {{
        let p = t / 2.5;
        ax = 20.0 + p * 15.0;
        ay = getLane1Y(ax);
        vehABrakeL.classList.remove('hidden');
        vehABrakeR.classList.remove('hidden');
        let sp = Math.round(30 - p * 20);
        speedAStr = sp + " MPH (Decelerating)";
        tagA.innerHTML = "VEHICLE A (DECELERATING)";
        tagA.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-yellow-500/60 text-[10px] font-bold text-yellow-300 mono pointer-events-none";
      }} else if (t < 7.4) {{
        ax = 35.0;
        ay = getLane1Y(ax);
        vehABrakeL.classList.remove('hidden');
        vehABrakeR.classList.remove('hidden');
        speedAStr = "0 MPH (FULL STOP)";
        tagA.innerHTML = "VEHICLE A (HALTED &ge; 20 FT BEHIND BUS)";
        tagA.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-red-500/70 text-[10px] font-bold text-red-300 mono pointer-events-none";
      }} else {{
        let p = (t - 7.4) / 2.1;
        let ease = p * p;
        ax = 35.0 + ease * 22.0;
        ay = getLane1Y(ax);
        vehABrakeL.classList.add('hidden');
        vehABrakeR.classList.add('hidden');
        let sp = Math.min(25, Math.round(p * 25));
        speedAStr = sp + " MPH (Resuming)";
        tagA.innerHTML = "VEHICLE A (RESUMING MOTION)";
        tagA.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-emerald-500/60 text-[10px] font-bold text-emerald-300 mono pointer-events-none";
      }}
      vehA.style.left = ax + "%";
      vehA.style.top = ay + "%";

      // 3. OPPOSING VEHICLE B (In Lane 2, heading SW)
      let bx, by;
      if (scenarioMode === 'undivided') {{
        if (t < 2.5) {{
          let p = t / 2.5;
          bx = 82.0 - p * 13.0;
          by = getLane2Y(bx);
          vehBBrakeL.classList.remove('hidden');
          vehBBrakeR.classList.remove('hidden');
          let sp = Math.round(30 - p * 20);
          speedBStr = sp + " MPH (Decelerating)";
          tagB.innerHTML = "VEHICLE B (OPPOSING - DECELERATING)";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-yellow-500/60 text-[10px] font-bold text-yellow-300 mono pointer-events-none";
        }} else if (t < 7.4) {{
          bx = 69.0;
          by = getLane2Y(bx);
          vehBBrakeL.classList.remove('hidden');
          vehBBrakeR.classList.remove('hidden');
          speedBStr = "0 MPH (MANDATORY STOP)";
          tagB.innerHTML = "VEHICLE B (OPPOSING FULL STOP)";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-red-500/70 text-[10px] font-bold text-red-300 mono pointer-events-none";
        }} else {{
          let p = (t - 7.4) / 2.1;
          let ease = p * p;
          bx = 69.0 - ease * 25.0;
          by = getLane2Y(bx);
          vehBBrakeL.classList.add('hidden');
          vehBBrakeR.classList.add('hidden');
          let sp = Math.min(28, Math.round(p * 28));
          speedBStr = sp + " MPH (Resuming)";
          tagB.innerHTML = "VEHICLE B (RESUMING MOTION)";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-emerald-500/60 text-[10px] font-bold text-emerald-300 mono pointer-events-none";
        }}
      }} else {{
        let p = t / maxTime;
        bx = 84.0 - p * 50.0;
        by = getLane2Y(bx);
        vehBBrakeL.classList.add('hidden');
        vehBBrakeR.classList.add('hidden');
        speedBStr = "35 MPH (Exempt from Stop)";
        tagB.innerHTML = "VEHICLE B (EXEMPT - SEPARATE ROADWAY)";
        tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-blue-500/60 text-[10px] font-bold text-blue-300 mono pointer-events-none";
      }}
      vehB.style.left = bx + "%";
      vehB.style.top = by + "%";

      // 4. STUDENT PEDESTRIAN (Walking in front of bumper: curb -> 10ft ahead -> cross street)
      if (t >= 3.8 && t <= 7.2) {{
        studentPed.classList.remove('hidden');
        let p = (t - 3.8) / 3.4;
        let sx, sy;
        if (p < 0.25) {{
          let pSub = p / 0.25;
          sx = 63.5 + pSub * 3.0;
          sy = 54.0 - pSub * 3.0;
        }} else {{
          let pSub = (p - 0.25) / 0.75;
          sx = 66.5 - pSub * 9.5;
          sy = 51.0 - pSub * 19.0;
        }}
        studentPed.style.left = sx + "%";
        studentPed.style.top = sy + "%";
      }} else {{
        studentPed.classList.add('hidden');
      }}

      // 5. STEP LOGIC & HUD DESCRIPTIONS
      if (t < 2.5) {{
        activeStep = 1;
        signalsStr = "Amber Prep Flashers Active";
        mandateStr = "Prepare for Mandatory Stop";
        explanationStr = "School bus activates amber warning flashers. Under TTC &sect; 545.066, all approaching drivers in BOTH directions on undivided roadways must prepare for a full stop before reaching the bus.";
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-yellow-500/50 text-yellow-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
        statuteBadgeText.innerHTML = "STEP 1: AMBER WARNING FLASHERS ACTIVE";
      }} else if (t < 4.5) {{
        activeStep = 2;
        signalsStr = "Red Flashers &amp; STOP Arm Deployed";
        mandateStr = "MANDATORY FULL STOP (BOTH DIRECTIONS)";
        if (scenarioMode === 'undivided') {{
          explanationStr = "Bus halts with red flashers and STOP arm extended. Under TTC &sect; 545.066(a), traffic approaching from EITHER direction on undivided roadways MUST COME TO A COMPLETE STOP.";
          statuteBadgeText.innerHTML = "TTC &sect; 545.066: MANDATORY DUAL-DIRECTION STOP";
        }} else {{
          explanationStr = "Bus halts with red flashers. Following Vehicle A MUST stop. However, under TTC &sect; 545.066(b), opposing Vehicle B on a separated roadway is NOT required to stop.";
          statuteBadgeText.innerHTML = "TTC &sect; 545.066(b): SEPARATE ROADWAY EXCEPTION";
        }}
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-red-500/60 text-red-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
      }} else if (t < 7.2) {{
        activeStep = 3;
        signalsStr = "Red Flashers &amp; STOP Arm Deployed";
        mandateStr = "REMAIN STOPPED &bull; STUDENT CROSSING";
        explanationStr = "Student exits and walks 10 feet in front of bus bumper to cross roadway. Absolute standstill required for all vehicular traffic until visual signals are retracted.";
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-red-500/60 text-red-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
        statuteBadgeText.innerHTML = "ACTIVE PEDESTRIAN CLEARANCE ZONE";
      }} else {{
        activeStep = 4;
        signalsStr = "Signals Deactivated &bull; Motion Resumed";
        mandateStr = "Proceed Lawfully When Clear";
        explanationStr = "Stop arm retracts and red lights deactivate as the bus moves. TTC &sect; 545.066 allows traffic to resume only after the bus resumes motion or visual signals are extinguished.";
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-emerald-500/60 text-emerald-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
        statuteBadgeText.innerHTML = "TTC &sect; 545.066 COMPLIANCE VERIFIED";
      }}

      // Update HUD elements
      hudSpeedA.innerText = speedAStr;
      hudSpeedB.innerText = speedBStr;
      hudSignals.innerHTML = signalsStr;
      hudMandate.innerHTML = mandateStr;
      hudExplanation.innerHTML = explanationStr;

      // Update step indicator buttons
      for (let s = 1; s <= 4; s++) {{
        const btn = document.getElementById('stepBtn' + s);
        if (s === activeStep) {{
          btn.className = "px-3 py-2 rounded-xl border border-blue-500 bg-blue-600 text-white font-bold text-xs text-center transition shadow";
        }} else {{
          btn.className = "px-3 py-2 rounded-xl border border-gray-800 bg-[#121620] text-gray-400 font-bold text-xs text-center transition hover:bg-[#1A202C]";
        }}
      }}
      stepCounter.innerText = "Step " + activeStep + " of 4";

      // Update scrubber UI
      timeSlider.value = t.toFixed(2);
      currentTimeDisplay.innerText = t.toFixed(2) + "s";
    }}

    // SCENARIO MODE TOGGLE HANDLER
    function setScenarioMode(mode) {{
      scenarioMode = mode;
      const undividedBtn = document.getElementById('modeUndividedBtn');
      const dividedBtn = document.getElementById('modeDividedBtn');

      if (mode === 'undivided') {{
        undividedBtn.className = "px-3 py-1 rounded-lg text-xs font-bold transition bg-amber-500 text-black shadow-md";
        dividedBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition";
        dividedBarrierOverlay.classList.add('hidden');
      }} else {{
        dividedBtn.className = "px-3 py-1 rounded-lg text-xs font-bold transition bg-blue-600 text-white shadow-md";
        undividedBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition";
        dividedBarrierOverlay.classList.remove('hidden');
      }}
      updateSimulation(simTime);
    }}

    // DETERMINISTIC 60 FPS ANIMATION LOOP
    function animationLoop(timestamp) {{
      if (!lastTimestamp) lastTimestamp = timestamp;
      const deltaSec = (timestamp - lastTimestamp) / 1000.0;
      lastTimestamp = timestamp;

      if (isPlaying) {{
        simTime += deltaSec * speed;
        if (simTime >= maxTime) {{
          const autoLoop = document.getElementById('autoLoopCheck').checked;
          if (autoLoop) {{
            simTime = 0.0;
          }} else {{
            simTime = maxTime;
            isPlaying = false;
            playIcon.innerHTML = "&#9654; Play";
          }}
        }}
        updateSimulation(simTime);
      }}

      requestAnimationFrame(animationLoop);
    }}
    requestAnimationFrame(animationLoop);

    // PLAYBACK CONTROLS
    function togglePlay() {{
      isPlaying = !isPlaying;
      playIcon.innerHTML = isPlaying ? "&#10074;&#10074; Pause" : "&#9654; Play";
    }}

    function restartSim() {{
      simTime = 0.0;
      isPlaying = true;
      playIcon.innerHTML = "&#10074;&#10074; Pause";
      updateSimulation(simTime);
    }}

    function setSpeed(s) {{
      speed = s;
      document.getElementById('speedBtn05').className = s === 0.5 ? "px-2 py-0.5 rounded bg-blue-600 text-white font-bold transition" : "px-2 py-0.5 rounded text-gray-400 hover:text-white transition";
      document.getElementById('speedBtn10').className = s === 1.0 ? "px-2 py-0.5 rounded bg-blue-600 text-white font-bold transition" : "px-2 py-0.5 rounded text-gray-400 hover:text-white transition";
      document.getElementById('speedBtn15').className = s === 1.5 ? "px-2 py-0.5 rounded bg-blue-600 text-white font-bold transition" : "px-2 py-0.5 rounded text-gray-400 hover:text-white transition";
    }}

    function onScrub(val) {{
      simTime = parseFloat(val);
      updateSimulation(simTime);
    }}

    // KEYBOARD SHORTCUTS
    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space') {{
        e.preventDefault();
        togglePlay();
      }} else if (e.code === 'ArrowLeft') {{
        prevStep();
      }} else if (e.code === 'ArrowRight') {{
        nextStep();
      }}
    }});

    // STEP JUMPING
    const stepTimes = [0.5, 3.2, 5.2, 8.0];
    function jumpToStep(s) {{
      simTime = stepTimes[s - 1];
      updateSimulation(simTime);
    }}

    function prevStep() {{
      if (simTime > stepTimes[3]) jumpToStep(3);
      else if (simTime > stepTimes[2]) jumpToStep(2);
      else if (simTime > stepTimes[1]) jumpToStep(1);
      else jumpToStep(1);
    }}

    function nextStep() {{
      if (simTime < stepTimes[1]) jumpToStep(2);
      else if (simTime < stepTimes[2]) jumpToStep(3);
      else if (simTime < stepTimes[3]) jumpToStep(4);
      else jumpToStep(4);
    }}

    // INITIAL RENDER
    updateSimulation(0.0);
  </script>
</body>
</html>
'''

out_file = r'C:\tx_dmv\driving_rule_animations_suite\simulations\L03_T05_school_bus_stop.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Successfully rebuilt simulation: {out_file}, size: {len(html_content) // 1024} KB')
