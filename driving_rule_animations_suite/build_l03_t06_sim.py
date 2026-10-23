import base64
import os

def get_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

road_b64 = get_b64(r'C:\tx_dmv\driving_rule_animations_suite\assets\roads\texas_suburban_crosswalk_corridor.jpg')
car_red_b64 = get_b64(r'C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_red_ne.png')
car_blue_b64 = get_b64(r'C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\car_blue_sw_clean.png')

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson L03-T06: Pedestrian Right-of-Way at Crosswalk (TTC § 552.003) - Texas Adult Driver Ed</title>
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
    /* Brake Glow */
    .brake-light {{
      box-shadow: 0 0 10px 4px rgba(255, 30, 30, 0.85);
      border-radius: 50%;
    }}
    /* Pedestrian Green Safety Halo */
    .ped-halo {{
      box-shadow: 0 0 16px 6px rgba(16, 185, 129, 0.6);
      border-radius: 50%;
    }}
    /* Hazard Danger Halo */
    .danger-halo {{
      box-shadow: 0 0 20px 8px rgba(239, 68, 68, 0.8);
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
        <span class="px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 font-bold text-xs mono">2.5D VECTOR ENGINE</span>
        <div>
          <h1 class="text-base md:text-lg font-bold text-white tracking-tight">TEXAS DRIVING–RULE ANIMATION SYSTEM</h1>
          <p class="text-xs text-gray-400">Lesson L03–T06: Pedestrian Right-of-Way at Crosswalk (Texas Transportation Code &sect; 552.003)</p>
        </div>
      </div>

      <!-- SCENARIO MODE TOGGLE -->
      <div class="flex items-center space-x-2 bg-[#0E131D] p-1.5 rounded-xl border border-[#232D3F]">
        <button id="modeYieldBtn" onclick="setScenarioMode('yield')" class="px-3 py-1 rounded-lg text-xs font-bold transition bg-emerald-500 text-black shadow-md">
          Primary: Dual-Direction Yielding
        </button>
        <button id="modePassHazardBtn" onclick="setScenarioMode('passHazard')" class="px-3 py-1 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition">
          Hazard Demo: Prohibited Passing (&sect; 552.003c)
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
          Step 1: Crosswalk &amp; Pedestrian Detection
        </button>
        <button id="stepBtn2" onclick="jumpToStep(2)" class="px-3 py-2 rounded-xl border border-gray-800 bg-[#121620] text-gray-400 font-bold text-xs text-center transition hover:bg-[#1A202C]">
          Step 2: Advance Stop Bar Full Stop
        </button>
        <button id="stepBtn3" onclick="jumpToStep(3)" class="px-3 py-2 rounded-xl border border-gray-800 bg-[#121620] text-gray-400 font-bold text-xs text-center transition hover:bg-[#1A202C]">
          Step 3: Protected Crosswalk Traversal
        </button>
        <button id="stepBtn4" onclick="jumpToStep(4)" class="px-3 py-2 rounded-xl border border-gray-800 bg-[#121620] text-gray-400 font-bold text-xs text-center transition hover:bg-[#1A202C]">
          Step 4: Clearance &amp; Lawful Resumption
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

      <!-- 2.5D SUBURBAN ROADWAY WITH CONTINENTAL CROSSWALK -->
      <img src="data:image/jpeg;base64,{road_b64}" alt="Texas Suburban Crosswalk Corridor" class="sim-bg">

      <!-- MUTCD W11-2 PEDESTRIAN CROSSING SIGN (Roadside curb mount) -->
      <div class="absolute" style="left: 47.0%; top: 62.0%; width: 32px; pointer-events: none; z-index: 20;">
        <svg viewBox="0 0 100 120" class="drop-shadow-lg w-full">
          <!-- Sign Post -->
          <line x1="50" y1="65" x2="50" y2="120" stroke="#718096" stroke-width="5"/>
          <!-- Diamond Warning Sign (Fluorescent Yellow-Green) -->
          <polygon points="50,5 95,50 50,95 5,50" fill="#CCFF00" stroke="#1A202C" stroke-width="4"/>
          <!-- Pedestrian Silhouette -->
          <circle cx="50" cy="30" r="7" fill="#1A202C"/>
          <path d="M 44 40 L 56 40 L 54 58 L 62 75 L 56 78 L 50 63 L 44 78 L 38 75 L 46 56 Z" fill="#1A202C"/>
          <!-- Walking arm -->
          <line x1="44" y1="45" x2="36" y2="55" stroke="#1A202C" stroke-width="4" stroke-linecap="round"/>
          <line x1="56" y1="45" x2="64" y2="52" stroke="#1A202C" stroke-width="4" stroke-linecap="round"/>
        </svg>
      </div>

      <!-- 1. VEHICLE A (Heading NE in Lane 1) -->
      <div id="vehA" class="sim-veh" style="left: 20.0%; top: 86.8%; width: 105px; z-index: 25;">
        <img src="data:image/png;base64,{car_red_b64}" alt="Vehicle A" class="w-full">
        <!-- Brake Lights Flares -->
        <div id="vehABrakeL" class="absolute brake-light hidden" style="left: 14px; top: 48px; width: 7px; height: 7px; background: #FF0033;"></div>
        <div id="vehABrakeR" class="absolute brake-light hidden" style="left: 26px; top: 56px; width: 7px; height: 7px; background: #FF0033;"></div>
        <!-- Tag -->
        <div id="tagA" class="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-red-500/60 text-[10px] font-bold text-red-300 mono pointer-events-none">
          VEHICLE A (APPROACHING 30 MPH)
        </div>
      </div>

      <!-- 2. VEHICLE B (In Lane 2 opposing in Primary, or trailing in Hazard Demo) -->
      <div id="vehB" class="sim-veh" style="left: 78.0%; top: 14.4%; width: 105px; z-index: 22;">
        <img id="vehBImg" src="data:image/png;base64,{car_blue_b64}" alt="Vehicle B" class="w-full">
        <!-- Brake Lights Flares -->
        <div id="vehBBrakeL" class="absolute brake-light hidden" style="left: 66px; top: 20px; width: 6px; height: 6px; background: #FF0033;"></div>
        <div id="vehBBrakeR" class="absolute brake-light hidden" style="left: 78px; top: 28px; width: 6px; height: 6px; background: #FF0033;"></div>
        <!-- Tag -->
        <div id="tagB" class="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-blue-500/60 text-[10px] font-bold text-blue-300 mono pointer-events-none">
          VEHICLE B (OPPOSING TRAFFIC)
        </div>
      </div>

      <!-- 3. PEDESTRIAN (Walking across crosswalk) -->
      <div id="ped" class="absolute pointer-events-none transition-all z-30" style="left: 55.0%; top: 56.0%; transform: translate(-50%, -50%);">
        <!-- Safety Ring Overlay -->
        <div id="pedSafetyRing" class="absolute inset-0 ped-halo pointer-events-none scale-125"></div>
        <svg width="28" height="42" viewBox="0 0 28 42" class="drop-shadow-lg">
          <ellipse cx="14" cy="39" rx="8" ry="3" fill="rgba(0,0,0,0.5)"/>
          <!-- Legs -->
          <line id="legL" x1="11" y1="28" x2="9" y2="38" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>
          <line id="legR" x1="17" y1="28" x2="19" y2="38" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>
          <!-- Torso -->
          <rect x="8" y="14" width="12" height="15" rx="3" fill="#0D9488"/>
          <!-- Head -->
          <circle cx="14" cy="9" r="6" fill="#FBBF24"/>
        </svg>
        <!-- Tag -->
        <div id="tagPed" class="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-emerald-950/90 border border-emerald-500/80 text-[9px] font-bold text-emerald-300 mono">
          PEDESTRIAN (RIGHT-OF-WAY)
        </div>
      </div>

      <!-- PROHIBITED PASSING VIOLATION HAZARD OVERLAY (Rendered only in Hazard Mode) -->
      <div id="hazardWarningZone" class="absolute inset-0 pointer-events-none hidden z-35">
        <div class="absolute top-[34%] left-[45%] -translate-x-1/2 px-3 py-1.5 rounded-xl bg-red-950/95 border border-red-500 text-red-200 text-[10px] font-bold mono shadow-2xl flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping"></span>
          <span>CRITICAL VIOLATION: TTC &sect; 552.003(c) OVERTAKING STOPPED VEHICLE PROHIBITED</span>
        </div>
      </div>

      <!-- HUD TELEMETRY & RULE EXPLANATION OVERLAY -->
      <div class="absolute top-4 left-4 max-w-sm rounded-xl bg-[#0D1117]/95 border border-[#232B39] p-4 text-xs shadow-2xl backdrop-blur space-y-3 z-40">
        <div class="space-y-1 border-b border-gray-800 pb-2">
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Vehicle A (Lane 1):</span>
            <span id="hudSpeedA" class="font-bold text-emerald-400">30 MPH</span>
          </div>
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Vehicle B (Lane 2):</span>
            <span id="hudSpeedB" class="font-bold text-blue-400">30 MPH</span>
          </div>
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Crosswalk State:</span>
            <span id="hudCrosswalkState" class="font-bold text-amber-400">Pedestrian Crossing</span>
          </div>
          <div class="flex items-center justify-between mono">
            <span class="text-gray-400">Legal Mandate:</span>
            <span id="hudMandate" class="font-bold text-amber-300">Mandatory Yield at Stop Bar</span>
          </div>
        </div>

        <div id="hudExplanation" class="text-gray-300 leading-relaxed text-[11px]">
          Vehicle A detects pedestrian entering marked continental crosswalk. Under TTC &sect; 552.003, driver must yield right-of-way and halt before the marked stop line.
        </div>
      </div>

      <!-- STATUTORY RULE VERIFICATION BADGE -->
      <div id="statuteBadge" class="absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-emerald-500/50 text-emerald-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="statuteBadgeText">TTC &sect; 552.003: PEDESTRIAN RIGHT-OF-WAY VERIFIED</span>
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
        <input type="range" id="timeSlider" min="0" max="8.5" step="0.02" value="0" class="w-full" oninput="onScrub(this.value)">
        <span class="mono text-xs text-gray-500">8.50s</span>
      </div>

      <!-- STATUTORY BADGE -->
      <div class="flex items-center space-x-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span class="text-xs text-gray-300 font-medium">TTC &sect; 552.003 Compliance Verified</span>
      </div>
    </footer>

  </div>

  <script>
    // SIMULATION STATE & CONFIGURATION
    let isPlaying = true;
    let simTime = 0.0;
    const maxTime = 8.5;
    let speed = 1.0;
    let lastTimestamp = null;
    let scenarioMode = 'yield'; // 'yield' or 'passHazard'

    // DOM ELEMENTS
    const stageContainer = document.getElementById('stageContainer');
    const hazardWarningZone = document.getElementById('hazardWarningZone');

    const vehA = document.getElementById('vehA');
    const vehABrakeL = document.getElementById('vehABrakeL');
    const vehABrakeR = document.getElementById('vehABrakeR');
    const tagA = document.getElementById('tagA');

    const vehB = document.getElementById('vehB');
    const vehBImg = document.getElementById('vehBImg');
    const vehBBrakeL = document.getElementById('vehBBrakeL');
    const vehBBrakeR = document.getElementById('vehBBrakeR');
    const tagB = document.getElementById('tagB');

    const ped = document.getElementById('ped');
    const pedSafetyRing = document.getElementById('pedSafetyRing');
    const tagPed = document.getElementById('tagPed');
    const legL = document.getElementById('legL');
    const legR = document.getElementById('legR');

    const hudSpeedA = document.getElementById('hudSpeedA');
    const hudSpeedB = document.getElementById('hudSpeedB');
    const hudCrosswalkState = document.getElementById('hudCrosswalkState');
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
      let crossStateStr = "Pedestrian Entering Crosswalk";
      let mandateStr = "Yield Right-of-Way at Stop Bar";
      let explanationStr = "";

      // 1. PEDESTRIAN TRAJECTORY (Crosses from Right Curb [u=+125] to Far Curb [u=-120])
      // Crosswalk mid point: cx_mid = 620 px -> 45.06% in X, 54.3% in Y
      // Trajectory along cross-direction (dx = +0.8722, dy = +0.4891 in pixel coords)
      // Percentage conversion: dx% = 0.8722 / 13.76 = 0.0634% per unit u
      //                        dy% = 0.4891 / 7.68 = 0.0637% per unit u
      // Right curb: u = +125 -> x = 45.06 + 125 * 0.0634 = 53.0%, y = 54.3 + 125 * 0.0637 = 62.3%
      // Far curb: u = -120 -> x = 45.06 - 120 * 0.0634 = 37.4%, y = 54.3 - 120 * 0.0637 = 46.6%
      let px, py;
      if (t < 1.0) {{
        // Waiting at curb / stepping out
        px = 52.8;
        py = 62.0;
      }} else if (t < 6.4) {{
        // Walking across crosswalk
        let p = (t - 1.0) / 5.4; // 0 to 1
        px = 52.8 - p * 15.4; // 52.8% to 37.4%
        py = 62.0 - p * 15.4; // 62.0% to 46.6%
        // Animate legs walking
        let walkPhase = Math.sin(t * 12);
        legL.setAttribute('x2', (11 + walkPhase * 4).toString());
        legR.setAttribute('x2', (17 - walkPhase * 4).toString());
      }} else {{
        // Cleared onto far sidewalk
        px = 37.4;
        py = 46.6;
      }}
      ped.style.left = px + "%";
      ped.style.top = py + "%";

      // 2. VEHICLE A (Heading NE in Lane 1)
      let ax, ay;
      // Stop bar is at x = 36.5%
      if (t < 2.4) {{
        // Approaching from x=18%, braking
        let p = t / 2.4;
        ax = 18.0 + p * 17.5; // 18% to 35.5%
        ay = getLane1Y(ax);
        vehABrakeL.classList.remove('hidden');
        vehABrakeR.classList.remove('hidden');
        let sp = Math.max(0, Math.round(30 - p * 30));
        speedAStr = sp + " MPH (Braking)";
        tagA.innerHTML = "VEHICLE A (DECELERATING)";
        tagA.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-yellow-500/60 text-[10px] font-bold text-yellow-300 mono pointer-events-none";
      }} else if (t < 6.5) {{
        // Stopped behind white stop line
        ax = 35.5;
        ay = getLane1Y(ax);
        vehABrakeL.classList.remove('hidden');
        vehABrakeR.classList.remove('hidden');
        speedAStr = "0 MPH (STOPPED AT STOP LINE)";
        tagA.innerHTML = "VEHICLE A (YIELDING AT STOP LINE)";
        tagA.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-emerald-500/70 text-[10px] font-bold text-emerald-300 mono pointer-events-none";
      }} else {{
        // Crosswalk clear -> Accelerates forward
        let p = (t - 6.5) / 2.0;
        let ease = p * p;
        ax = 35.5 + ease * 35.0; // 35.5% to 70.5%
        ay = getLane1Y(ax);
        vehABrakeL.classList.add('hidden');
        vehABrakeR.classList.add('hidden');
        let sp = Math.min(26, Math.round(p * 26));
        speedAStr = sp + " MPH (Resuming)";
        tagA.innerHTML = "VEHICLE A (PROCEEDING - CLEAR)";
        tagA.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-emerald-500/60 text-[10px] font-bold text-emerald-300 mono pointer-events-none";
      }}
      vehA.style.left = ax + "%";
      vehA.style.top = ay + "%";

      // 3. VEHICLE B (Scenario dependent)
      let bx, by;
      if (scenarioMode === 'yield') {{
        // PRIMARY SCENARIO: Opposing Traffic in Lane 2 (heading SW)
        // Stop bar for Lane 2 is at x = 55.5%
        if (t < 2.4) {{
          let p = t / 2.4;
          bx = 76.0 - p * 19.5; // 76% down to 56.5%
          by = getLane2Y(bx);
          vehBBrakeL.classList.remove('hidden');
          vehBBrakeR.classList.remove('hidden');
          let sp = Math.max(0, Math.round(30 - p * 30));
          speedBStr = sp + " MPH (Braking)";
          tagB.innerHTML = "VEHICLE B (OPPOSING - DECELERATING)";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-yellow-500/60 text-[10px] font-bold text-yellow-300 mono pointer-events-none";
        }} else if (t < 6.5) {{
          // Stopped before stop bar in Lane 2
          bx = 56.5;
          by = getLane2Y(bx);
          vehBBrakeL.classList.remove('hidden');
          vehBBrakeR.classList.remove('hidden');
          speedBStr = "0 MPH (STOPPED AT STOP LINE)";
          tagB.innerHTML = "VEHICLE B (YIELDING - TTC &sect; 552.003)";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-emerald-500/70 text-[10px] font-bold text-emerald-300 mono pointer-events-none";
        }} else {{
          // Pedestrian cleared -> Vehicle B resumes SW
          let p = (t - 6.5) / 2.0;
          let ease = p * p;
          bx = 56.5 - ease * 34.0; // 56.5% down to 22.5%
          by = getLane2Y(bx);
          vehBBrakeL.classList.add('hidden');
          vehBBrakeR.classList.add('hidden');
          let sp = Math.min(26, Math.round(p * 26));
          speedBStr = sp + " MPH (Resuming)";
          tagB.innerHTML = "VEHICLE B (PROCEEDING - CLEAR)";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-emerald-500/60 text-[10px] font-bold text-emerald-300 mono pointer-events-none";
        }}
      }} else {{
        // HAZARD DEMO SCENARIO: Vehicle B attempts illegal overtake behind Vehicle A
        // Vehicle B is in Lane 2 heading NE alongside Vehicle A
        if (t < 2.0) {{
          bx = 14.0 + (t / 2.0) * 20.0;
          by = getLane2Y(bx);
          speedBStr = "35 MPH (Approaching Fast)";
          tagB.innerHTML = "VEHICLE B (APPROACHING REAR)";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/85 border border-yellow-500/60 text-[10px] font-bold text-yellow-300 mono pointer-events-none";
        }} else if (t < 5.0) {{
          // Vehicle B illegally overtakes stopped Vehicle A
          let p = (t - 2.0) / 3.0;
          bx = 34.0 + p * 18.0; // 34% to 52%
          by = getLane2Y(bx);
          speedBStr = "30 MPH (ILLEGAL PASS)";
          tagB.innerHTML = "<span class='text-red-400 font-bold'>&times; ILLEGAL PASS (&sect; 552.003c)</span>";
          tagB.className = "absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded bg-black/95 border border-red-500 text-[10px] font-bold text-red-300 mono pointer-events-none";
        }} else {{
          bx = 52.0 + ((t - 5.0) / 3.5) * 22.0;
          by = getLane2Y(bx);
          speedBStr = "25 MPH";
        }}
      }}
      vehB.style.left = bx + "%";
      vehB.style.top = by + "%";

      // 4. STEP PROGRESSION & HUD DESCRIPTIONS
      if (t < 2.2) {{
        activeStep = 1;
        crossStateStr = "Pedestrian Entering Crosswalk";
        mandateStr = "Prepare to Yield Right-of-Way";
        explanationStr = "Pedestrian steps from curb into marked continental crosswalk. TTC &sect; 552.003 mandates that approaching drivers must immediately prepare to yield right-of-way.";
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-yellow-500/50 text-yellow-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
        statuteBadgeText.innerHTML = "STEP 1: PEDESTRIAN CROSSWALK DETECTION";
      }} else if (t < 4.0) {{
        activeStep = 2;
        crossStateStr = "Pedestrian on Travel Half";
        mandateStr = "FULL STOP AT ADVANCE STOP LINE";
        if (scenarioMode === 'yield') {{
          explanationStr = "Vehicle A and opposing Vehicle B come to a full stop before marked advance stop lines. Under TTC &sect; 552.003(a), vehicles must halt when a pedestrian is in their half or approaching so closely as to be in danger.";
          statuteBadgeText.innerHTML = "TTC &sect; 552.003(a): DUAL ADVANCE STOP MANDATORY";
        }} else {{
          explanationStr = "CRITICAL HAZARD: TTC &sect; 552.003(c) explicitly forbids overtaking and passing any vehicle stopped at a marked crosswalk. Passing here creates an immediate blind collision hazard!";
          statuteBadgeText.innerHTML = "TTC &sect; 552.003(c): OVERTAKING STOPPED VEHICLE FORBIDDEN";
        }}
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-red-500/60 text-red-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
      }} else if (t < 6.4) {{
        activeStep = 3;
        crossStateStr = "Pedestrian Traversing Active Lanes";
        mandateStr = "REMAIN FULLY STOPPED &bull; PEDESTRIAN CROSSING";
        explanationStr = "Pedestrian safely traverses both travel lanes within marked continental stripes. Both vehicles remain completely stationary with brake lights glowing until crosswalk is fully vacated.";
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-emerald-500/60 text-emerald-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
        statuteBadgeText.innerHTML = "ACTIVE PROTECTED CROSSWALK ZONE";
      }} else {{
        activeStep = 4;
        crossStateStr = "Crosswalk Fully Cleared";
        mandateStr = "Proceed Lawfully When Clear";
        explanationStr = "Pedestrian reaches the opposite curb safely. Both travel halves are completely clear. Vehicles A and B smoothly accelerate through the crosswalk under normal right-of-way rules.";
        statuteBadge.className = "absolute bottom-4 right-4 px-3 py-2 rounded-xl bg-black/90 border border-emerald-500/60 text-emerald-300 text-xs mono font-bold shadow-2xl flex items-center space-x-2 z-50";
        statuteBadgeText.innerHTML = "TTC &sect; 552.003 COMPLIANCE VERIFIED";
      }}

      // Update HUD text
      hudSpeedA.innerText = speedAStr;
      hudSpeedB.innerText = speedBStr;
      hudCrosswalkState.innerText = crossStateStr;
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
      const yieldBtn = document.getElementById('modeYieldBtn');
      const passHazardBtn = document.getElementById('modePassHazardBtn');

      if (mode === 'yield') {{
        yieldBtn.className = "px-3 py-1 rounded-lg text-xs font-bold transition bg-emerald-500 text-black shadow-md";
        passHazardBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition";
        hazardWarningZone.classList.add('hidden');
        pedSafetyRing.className = "absolute inset-0 ped-halo pointer-events-none scale-125";
      }} else {{
        passHazardBtn.className = "px-3 py-1 rounded-lg text-xs font-bold transition bg-red-600 text-white shadow-md";
        yieldBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition";
        hazardWarningZone.classList.remove('hidden');
        pedSafetyRing.className = "absolute inset-0 danger-halo pointer-events-none scale-150 animate-pulse";
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
    const stepTimes = [0.5, 3.0, 5.0, 7.2];
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

out_file = r'C:\tx_dmv\driving_rule_animations_suite\simulations\L03_T06_pedestrian_crosswalk.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Successfully built L03_T06 simulation: {out_file}, size: {len(html_content) // 1024} KB')
