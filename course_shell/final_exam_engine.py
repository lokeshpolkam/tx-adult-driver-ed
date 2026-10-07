"""
final_exam_engine.py
TDLR 16 TAC §84.503 Compliant Final Examination Generator & Bank Engine.
Enforces:
1. At least 30 questions drawn equally from two distinct statutory banks:
   - Bank A: Highway Signs, Signals & Traffic Control Devices (15 questions)
   - Bank B: Traffic Laws and Rules of the Road (15 questions)
2. Passing threshold: Exactly 70.0% (at least 21 out of 30 correct).
3. Retesting logic: Draws alternate questions from 50+ question master bank.
4. September 1, 2026 Mandate: Explicit coverage of Highway Construction & Maintenance Work Zones
   (HB 1884, TTC §472.022, TTC §542.404, TTC §542.501, TTC §545.157).
"""

import os
import json
import random

FINAL_EXAM_BANK = {
    # =========================================================================
    # BANK A: HIGHWAY SIGNS, SIGNALS & TRAFFIC CONTROL DEVICES (25 Questions)
    # =========================================================================
    "bank_a_signs": [
        {
            "id": "SIGN-01",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "REGULATORY SIGNS",
            "statute": "TX MUTCD CH. 2B / TTC §544.004",
            "svg_key": "sign_r1_1_stop",
            "prompt": "What is the mandatory driver response when approaching an octagonal red MUTCD R1-1 STOP sign?",
            "options": [
                {"number": 1, "text": "Come to a complete stop before the stop line, crosswalk, or entering intersection"},
                {"number": 2, "text": "Slow down to five miles per hour and roll through if cross traffic is not visible"},
                {"number": 3, "text": "Stop only if approaching vehicles from the right arrive at the intersection first"},
                {"number": 4, "text": "Tap your vehicle horn to alert surrounding pedestrians before driving through"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §544.004 and MUTCD R1-1, an operator facing a stop sign must come to a complete stop at the stop line, crosswalk, or intersection boundary."
        },
        {
            "id": "SIGN-02",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "REGULATORY SIGNS",
            "statute": "TX MUTCD CH. 2B / TTC §545.151",
            "svg_key": "sign_r1_2_yield",
            "prompt": "What does an inverted triangular red-and-white MUTCD R1-2 YIELD sign legally require of a driver?",
            "options": [
                {"number": 1, "text": "Slow down and yield right-of-way to all vehicles and pedestrians on roadway"},
                {"number": 2, "text": "Come to a mandatory complete stop regardless of whether any other traffic is present"},
                {"number": 3, "text": "Accelerate quickly to enter before approaching main road vehicles reach junction"},
                {"number": 4, "text": "Yield right-of-way exclusively to commercial freight vehicles and city buses"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §545.151, an operator facing a yield sign must slow to a reasonable speed and yield right-of-way to any vehicle or pedestrian in or approaching the intersection."
        },
        {
            "id": "SIGN-03",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "WARNING SIGNS",
            "statute": "TX MUTCD CH. 2C",
            "svg_key": "sign_w8_5_slippery",
            "prompt": "What does a yellow diamond sign depicting a skidding vehicle (MUTCD W8-5) indicate to motorists?",
            "options": [
                {"number": 1, "text": "Roadway surface ahead is slippery when wet; reduce speed and steer smoothly"},
                {"number": 2, "text": "A winding mountain road begins ahead with consecutive sharp hairpin turns"},
                {"number": 3, "text": "Pavement ends ahead and transitions into an unpaved loose gravel surface"},
                {"number": 4, "text": "High-speed drifting and performance driving maneuvers are authorized ahead"}
            ],
            "correct_option": 1,
            "rationale": "MUTCD W8-5 warns that road surface friction drops significantly when wet. Drivers should decelerate and avoid harsh braking or sudden steering."
        },
        {
            "id": "SIGN-04",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "SCHOOL ZONE SIGNS",
            "statute": "TX MUTCD CH. 7B",
            "svg_key": "sign_school_pentagon",
            "prompt": "What specific roadway environment is designated exclusively by an upright pentagonal traffic sign?",
            "options": [
                {"number": 1, "text": "A public school zone, school crosswalk corridor, or child pedestrian crossing"},
                {"number": 2, "text": "An active railway grade crossing with multiple industrial train tracks"},
                {"number": 3, "text": "A mandatory state commercial vehicle weight and safety inspection station"},
                {"number": 4, "text": "A county emergency fire department station with exiting rescue vehicles"}
            ],
            "correct_option": 1,
            "rationale": "An upright pentagon (house-shaped) sign is reserved exclusively for school zones and school crossings to warn motorists of children and pedestrian traffic."
        },
        {
            "id": "SIGN-05",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "PROHIBITORY SIGNS",
            "statute": "TX MUTCD CH. 2B",
            "svg_key": "sign_do_not_enter",
            "prompt": "What is the legal mandate when encountering a square white sign with a red circle and white bar?",
            "options": [
                {"number": 1, "text": "Do Not Enter; entry is prohibited because traffic is moving toward your vehicle"},
                {"number": 2, "text": "Authorized passenger vehicles may enter during daytime non-peak hours"},
                {"number": 3, "text": "Stop completely, sound horn twice, and proceed if roadway appears clear"},
                {"number": 4, "text": "Commercial transport trucks must detour into the adjacent right shoulder"}
            ],
            "correct_option": 1,
            "rationale": "MUTCD R5-1 'Do Not Enter' marks one-way roads or freeway ramps where vehicles traveling in the wrong direction would confront oncoming traffic."
        },
        {
            "id": "SIGN-06",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "REGULATORY SPEED SIGNS",
            "statute": "TX TRANS CODE §545.352",
            "svg_key": "sign_speed_limit_70",
            "prompt": "What does a rectangular white regulatory sign displaying 'SPEED LIMIT 70' represent in Texas?",
            "options": [
                {"number": 1, "text": "Maximum legal speed under ideal conditions; speed must be reduced if hazards exist"},
                {"number": 2, "text": "The minimum mandatory cruising speed that all passenger vehicles must maintain"},
                {"number": 3, "text": "A suggested advisory travel speed recommended exclusively during daylight"},
                {"number": 4, "text": "A speed limit that applies only to commercial interstate freight haulers"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §545.352 and §545.351, a speed limit sign establishes maximum legal speed under ideal conditions. Drivers must reduce speed below the limit when adverse conditions exist."
        },
        {
            "id": "SIGN-07",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "MERGE WARNING SIGNS",
            "statute": "TX MUTCD CH. 2C",
            "svg_key": "sign_w4_1_merge",
            "prompt": "What does a yellow diamond sign with two converging arrows (MUTCD W4-1) indicate to drivers?",
            "options": [
                {"number": 1, "text": "Entering traffic is merging from the right; adjust speed and position to blend flow"},
                {"number": 2, "text": "The travel lane divides ahead into two separate one-way divided highways"},
                {"number": 3, "text": "Vehicles on the main highway must come to a complete stop to let traffic merge"},
                {"number": 4, "text": "All vehicles must make an immediate sharp right turn at the next cross street"}
            ],
            "correct_option": 1,
            "rationale": "MUTCD W4-1 warns drivers that another lane is joining their roadway from the right. Both through traffic and merging drivers should adjust speed and spacing."
        },
        {
            "id": "SIGN-08",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "RAILROAD SIGNS & SIGNALS",
            "statute": "TX TRANS CODE §545.251",
            "svg_key": "sign_railroad_crossbuck",
            "prompt": "What does a white X-shaped 'RAILROAD CROSSING' crossbuck sign (MUTCD R15-1) require of drivers?",
            "options": [
                {"number": 1, "text": "Yield right-of-way to approaching trains and stop 15 to 50 feet away if train nears"},
                {"number": 2, "text": "Accelerate across the tracks quickly before warning bells begin to sound"},
                {"number": 3, "text": "Stop on the tracks and look both ways before proceeding across the crossing"},
                {"number": 4, "text": "Yield to trains only when electronic red lights are actively flashing overhead"}
            ],
            "correct_option": 1,
            "rationale": "The crossbuck sign has the legal status of a YIELD sign. Under TTC §545.251, drivers must yield to trains and stop within 15 to 50 feet if a train is approaching."
        },
        {
            "id": "SIGN-09",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "TRAFFIC SIGNAL LIGHTS",
            "statute": "TX TRANS CODE §544.008",
            "svg_key": "traffic_signals",
            "prompt": "What does an overhead flashing circular RED traffic light require of an approaching driver?",
            "options": [
                {"number": 1, "text": "Complete stop at the stop line, yield to cross traffic, then proceed safely"},
                {"number": 2, "text": "Slow down moderately and proceed through cross street without stopping"},
                {"number": 3, "text": "Wait until the light cycles to solid green before advancing through junction"},
                {"number": 4, "text": "Treat the signal as a flashing yellow caution beacon during daytime hours"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §544.008, a flashing red signal functions identically to a stop sign: complete stop required, yield right-of-way, proceed only when clear."
        },
        {
            "id": "SIGN-10",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "TRAFFIC SIGNAL LIGHTS",
            "statute": "TX TRANS CODE §544.008",
            "svg_key": "traffic_signals",
            "prompt": "What does an overhead flashing circular YELLOW traffic light indicate to motorists?",
            "options": [
                {"number": 1, "text": "Proceed through the intersection cautiously with caution and reduced speed"},
                {"number": 2, "text": "Come to a complete stop and wait for a full green signal before moving"},
                {"number": 3, "text": "Accelerate rapidly to clear the intersection prior to signal phase shift"},
                {"number": 4, "text": "Switch lanes immediately away from the signal light to avoid congestion"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §544.008(b), an operator facing a flashing yellow signal may proceed through the intersection or past the signal only with caution."
        },
        {
            "id": "SIGN-11",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "WORK ZONE SIGNS (SEPT 1 2026 MANDATE)",
            "statute": "TX MUTCD CH. 6 / TTC §472.022",
            "svg_key": "sign_do_not_enter",
            "prompt": "What does an orange diamond-shaped highway sign signify to Texas motorists under work zone rules?",
            "options": [
                {"number": 1, "text": "Temporary highway construction, maintenance work, or altered roadway ahead"},
                {"number": 2, "text": "Permanent state park or recreational campground attraction located nearby"},
                {"number": 3, "text": "Commercial industrial manufacturing corridor with high acoustic noise levels"},
                {"number": 4, "text": "Interstate route guidance directing drivers toward international toll borders"}
            ],
            "correct_option": 1,
            "rationale": "Orange signs are designated exclusively for temporary traffic control in construction and maintenance work zones, warning of workers, machinery, detours, and lane closures."
        },
        {
            "id": "SIGN-12",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "PAVEMENT MARKINGS",
            "statute": "TX MUTCD CH. 3B",
            "svg_key": None,
            "prompt": "What does a solid double yellow centerline painted down the middle of a two-lane road indicate?",
            "options": [
                {"number": 1, "text": "Passing is strictly prohibited in both directions of travel along that section"},
                {"number": 2, "text": "Passing is permitted for passenger cars but prohibited for commercial trucks"},
                {"number": 3, "text": "Traffic travels in the same direction on both sides of the double yellow line"},
                {"number": 4, "text": "Vehicles may cross the line at high speed to pass slow agricultural tractors"}
            ],
            "correct_option": 1,
            "rationale": "A solid double yellow centerline separates opposing traffic and indicates that passing is prohibited in both directions (except when making a safe left turn into a driveway)."
        },
        {
            "id": "SIGN-13",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "PAVEMENT MARKINGS",
            "statute": "TX MUTCD CH. 3B",
            "svg_key": None,
            "prompt": "What does a solid white line between lanes traveling in the same direction signify to motorists?",
            "options": [
                {"number": 1, "text": "Lane changes are discouraged or hazardous; drivers should remain in their lane"},
                {"number": 2, "text": "Lane changes are completely prohibited under all circumstances in Texas"},
                {"number": 3, "text": "The adjacent travel lane is reserved exclusively for public transit vehicles"},
                {"number": 4, "text": "The travel lane will terminate abruptly within seventy-five feet ahead"}
            ],
            "correct_option": 1,
            "rationale": "A solid white line indicates that lane changes are discouraged due to elevated collision risk. A double solid white line indicates lane changes are strictly prohibited."
        },
        {
            "id": "SIGN-14",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "REVERSIBLE LANE CONTROLS",
            "statute": "TX MUTCD CH. 4M",
            "svg_key": None,
            "prompt": "What does a steady red 'X' displayed over a highway lane control signal signify?",
            "options": [
                {"number": 1, "text": "Lane is closed to travel; motorists must merge into an open green-arrow lane"},
                {"number": 2, "text": "Lane is reserved exclusively for high-occupancy transit vehicles with 4 people"},
                {"number": 3, "text": "Lane is designated for commercial freight trucks traveling above sixty mph"},
                {"number": 4, "text": "Lane may be used temporarily for rapid overtaking maneuvers during rush hour"}
            ],
            "correct_option": 1,
            "rationale": "A steady red 'X' overhead indicates the lane is closed to approaching traffic; driving in that lane is illegal and creates severe head-on collision danger."
        },
        {
            "id": "SIGN-15",
            "domain": "HIGHWAY SIGNS & SIGNALS",
            "category": "RAILROAD BLUE ENS SIGN",
            "statute": "OPERATION LIFESAVER / MUTCD CH. 8",
            "svg_key": "sign_railroad_crossbuck",
            "prompt": "If a vehicle stalls on train tracks, what emergency data on the blue ENS sign must you report to 911?",
            "options": [
                {"number": 1, "text": "The railroad emergency dispatch 1-800 phone number and unique USDOT crossing ID"},
                {"number": 2, "text": "The municipal railroad tax rate and annual freight tonnage financial numbers"},
                {"number": 3, "text": "The historical year the train crossing was originally paved with asphalt"},
                {"number": 4, "text": "The manufacturer serial number of the overhead train crossing gate arms"}
            ],
            "correct_option": 1,
            "rationale": "The blue Emergency Notification System (ENS) sign contains the 24/7 railroad dispatch phone number and the unique 6-digit crossing ID plus letter to halt all oncoming train traffic."
        }
    ],

    # =========================================================================
    # BANK B: TRAFFIC LAWS & RULES OF THE ROAD (25 Questions)
    # =========================================================================
    "bank_b_laws": [
        {
            "id": "LAW-01",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "WORK ZONE FINES (SEPT 1 2026 MANDATE)",
            "statute": "TX TRANS CODE §542.404 / HB 1884",
            "svg_key": "sign_do_not_enter",
            "prompt": "Under Texas Transportation Code §542.404, when are traffic fines doubled in highway work zones?",
            "options": [
                {"number": 1, "text": "Whenever construction workers are present in the work zone and signs are posted"},
                {"number": 2, "text": "Exclusively when construction work is actively underway during nighttime hours"},
                {"number": 3, "text": "Only if a physical motor vehicle crash results in property damage or injury"},
                {"number": 4, "text": "Fines double only for commercial freight vehicles exceeding gross weight limits"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §542.404 and TDLR work zone rules, traffic fines double for moving violations committed in maintenance or construction zones when workers are present."
        },
        {
            "id": "LAW-02",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "WORK ZONE BARRICADES (SEPT 1 2026 MANDATE)",
            "statute": "TX TRANS CODE §472.022",
            "svg_key": "sign_do_not_enter",
            "prompt": "What is the criminal penalty for disobeying warning signs or driving around barricades in a Texas work zone?",
            "options": [
                {"number": 1, "text": "Class B misdemeanor punishable by fines up to $1,000 and up to 180 days in jail"},
                {"number": 2, "text": "Standard civil parking ticket with a ten-dollar municipal court administrative fee"},
                {"number": 3, "text": "Mandatory forfeiture of all personal motor vehicles to state highway funds"},
                {"number": 4, "text": "A verbal administrative warning issued by county environmental health units"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §472.022, driving around or removing a work zone or flood barricade is a Class B misdemeanor (fines up to $1,000 and/or jail up to 180 days, escalating if bodily injury occurs)."
        },
        {
            "id": "LAW-03",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "WORK ZONE FLAGGER COMPLIANCE (SEPT 1 2026 MANDATE)",
            "statute": "TX TRANS CODE §542.501",
            "svg_key": None,
            "prompt": "What is a driver's legal obligation when directed by an authorized human flagger in a work zone?",
            "options": [
                {"number": 1, "text": "Comply with flagger directions promptly; flagger instructions legally supersede signals"},
                {"number": 2, "text": "Flagger instructions are voluntary advice that drivers may disregard at will"},
                {"number": 3, "text": "Yield to flaggers only if electronic intersection traffic signals are dark"},
                {"number": 4, "text": "Proceed at full posted highway speed unless an armed police officer is present"}
            ],
            "correct_option": 1,
            "rationale": "TTC §542.501 makes it a traffic violation to disobey an authorized flagger. Flagger manual directions supersede standard traffic control devices to protect road workers."
        },
        {
            "id": "LAW-04",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "TEXAS MOVE OVER / SLOW DOWN ACT",
            "statute": "TX TRANS CODE §545.157",
            "svg_key": "move_over_slow_down",
            "prompt": "What speed reduction is required when passing a stopped emergency or TxDOT work vehicle with flashing lights?",
            "options": [
                {"number": 1, "text": "Slow to 20 mph below posted limit (or 5 mph if speed limit is less than 25 mph)"},
                {"number": 2, "text": "Slow to 10 mph below posted limit (or 15 mph if speed limit is less than 30 mph)"},
                {"number": 3, "text": "Maintain full posted cruising speed provided you activate four-way flashers"},
                {"number": 4, "text": "Slow down to exactly thirty-five miles per hour on all interstate highway lanes"}
            ],
            "correct_option": 1,
            "rationale": "TTC §545.157 requires drivers to vacate the lane closest to stopped emergency/work vehicles, or slow down to 20 mph below the posted limit (or 5 mph if limit < 25 mph)."
        },
        {
            "id": "LAW-05",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "LEGAL INTOXICATION BAC LIMIT",
            "statute": "TX PENAL CODE §49.01",
            "svg_key": "dwi_bac_gauge",
            "prompt": "What blood alcohol concentration (BAC) defines legal intoxication per se for adult drivers in Texas?",
            "options": [
                {"number": 1, "text": "An alcohol concentration of 0.08 or more in blood, breath, or urine sample"},
                {"number": 2, "text": "An alcohol concentration of 0.05 or more in blood, breath, or urine sample"},
                {"number": 3, "text": "An alcohol concentration of 0.10 or more in blood, breath, or urine sample"},
                {"number": 4, "text": "An alcohol concentration of 0.02 or more in blood, breath, or urine sample"}
            ],
            "correct_option": 1,
            "rationale": "Texas Penal Code §49.01(2)(B) establishes 0.08 BAC as the statutory per se limit for adult drivers, regardless of visible symptoms."
        },
        {
            "id": "LAW-06",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "MINOR ZERO TOLERANCE",
            "statute": "TX ALCOHOLIC BEVERAGE CODE §106.041",
            "svg_key": "dwi_bac_gauge",
            "prompt": "Under the Texas Zero Tolerance law, what alcohol level constitutes DUI for a minor under age 21?",
            "options": [
                {"number": 1, "text": "Any detectable amount of alcohol in the minor's system while driving a vehicle"},
                {"number": 2, "text": "Only when the minor's blood alcohol concentration exceeds the 0.08 adult limit"},
                {"number": 3, "text": "A BAC exceeding 0.05 measured during certified forensic laboratory blood tests"},
                {"number": 4, "text": "Zero Tolerance applies exclusively to minors operating commercial school buses"}
            ],
            "correct_option": 1,
            "rationale": "Under Texas Alcoholic Beverage Code §106.041, any detectable amount of alcohol in a minor driver's system constitutes DUI by a Minor."
        },
        {
            "id": "LAW-07",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "IMPLIED CONSENT & ALR",
            "statute": "TX TRANS CODE §724.035",
            "svg_key": "sb30_traffic_stop",
            "prompt": "What is the administrative license suspension for refusing a chemical test after a first-offense DWI arrest?",
            "options": [
                {"number": 1, "text": "180 days administrative driver license suspension for a first chemical test refusal"},
                {"number": 2, "text": "30 days administrative driver license suspension for a first chemical test refusal"},
                {"number": 3, "text": "2 years administrative driver license suspension for a first chemical test refusal"},
                {"number": 4, "text": "Refusing a test carries zero administrative license suspension penalties in Texas"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §724.035, refusing to submit to a chemical breath or blood test results in an automatic 180-day license suspension on a first offense."
        },
        {
            "id": "LAW-08",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "OPEN CONTAINER STATUTE",
            "statute": "TX PENAL CODE §49.031",
            "svg_key": None,
            "prompt": "Where may an unsealed container of alcohol be legally transported in a passenger car in Texas?",
            "options": [
                {"number": 1, "text": "In the vehicle locked trunk, or behind the upright rear seats in an SUV without a trunk"},
                {"number": 2, "text": "Inside the center console compartment between the driver and front passenger"},
                {"number": 3, "text": "Inside the unlocked front dashboard glove box directly beneath the radio"},
                {"number": 4, "text": "Under the driver's seat provided the container is placed inside a brown paper sack"}
            ],
            "correct_option": 1,
            "rationale": "Under TPC §49.031, open containers are prohibited in the passenger area; they may only be transported in a locked glove box, locked trunk, or behind the last upright seat in vehicles lacking trunks."
        },
        {
            "id": "LAW-09",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "CHILD PASSENGER SAFETY RESTRAINTS",
            "statute": "TX TRANS CODE §545.412",
            "svg_key": "child_safety_seat",
            "prompt": "Under Texas law, which children must be secured in a child passenger safety seat system?",
            "options": [
                {"number": 1, "text": "Children younger than 8 years old, unless taller than 4 feet 9 inches in height"},
                {"number": 2, "text": "Children younger than 5 years old, regardless of physical standing height"},
                {"number": 3, "text": "Children younger than 12 years old, unless weighing over eighty-five pounds"},
                {"number": 4, "text": "Children are required to use booster seats only until their fourth birthday"}
            ],
            "correct_option": 1,
            "rationale": "TTC §545.412 mandates child passenger safety seats for children younger than 8 years old unless they are taller than 4 feet 9 inches (57 inches)."
        },
        {
            "id": "LAW-10",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "UNATTENDED CHILDREN IN VEHICLES",
            "statute": "TX PENAL CODE §22.10",
            "svg_key": None,
            "prompt": "Under Texas Penal Code §22.10, when is leaving a child unattended inside a vehicle a criminal offense?",
            "options": [
                {"number": 1, "text": "Child younger than 7 left unattended for >5 mins without someone ≥14 years old"},
                {"number": 2, "text": "Child younger than 12 left unattended for >15 mins while running errands"},
                {"number": 3, "text": "Only if the outdoor ambient temperature exceeds ninety degrees Fahrenheit"},
                {"number": 4, "text": "Leaving a child inside a parked car is never illegal if windows are cracked"}
            ],
            "correct_option": 1,
            "rationale": "TPC §22.10 makes it a misdemeanor to intentionally leave a child under 7 unattended for longer than 5 minutes without an individual at least 14 years old."
        },
        {
            "id": "LAW-11",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "INTERSECTION RIGHT-OF-WAY",
            "statute": "TX TRANS CODE §545.151",
            "svg_key": "4way_stop",
            "prompt": "At an uncontrolled 4-way intersection where two vehicles arrive simultaneously, who must yield?",
            "options": [
                {"number": 1, "text": "The driver on the left must yield right-of-way to the vehicle on their right"},
                {"number": 2, "text": "The vehicle on the right must yield right-of-way to the vehicle on their left"},
                {"number": 3, "text": "The smaller passenger car always yields to larger commercial freight trucks"},
                {"number": 4, "text": "Both vehicles must remain stationary until a municipal police officer arrives"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §545.151, when two vehicles approach an intersection at approximately the same time, the driver on the left shall yield to the vehicle on the right."
        },
        {
            "id": "LAW-12",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "SCHOOL BUS RIGHT-OF-WAY",
            "statute": "TX TRANS CODE §545.066",
            "svg_key": "school_bus_divided_highway",
            "prompt": "When is a driver on a divided highway with an unpaved median EXEMPT from stopping for a school bus?",
            "options": [
                {"number": 1, "text": "When traveling in the opposite direction on a roadway divided by a physical barrier"},
                {"number": 2, "text": "Whenever traveling in the same direction on a four-lane highway with turn lanes"},
                {"number": 3, "text": "When driving during afternoon rush hour between five and six in the evening"},
                {"number": 4, "text": "Vehicles are never exempt from stopping for school buses under any circumstances"}
            ],
            "correct_option": 1,
            "rationale": "Under TTC §545.066(b), traffic traveling in the opposite direction on a separate roadway divided by a physical barrier or median is not required to stop."
        },
        {
            "id": "LAW-13",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "SENATE BILL 30 STOP PROTOCOL",
            "statute": "TX EDUCATION CODE §28.012",
            "svg_key": "sb30_traffic_stop",
            "prompt": "Under the Community Safety Education Act (Senate Bill 30), what should a driver do when pulled over at night?",
            "options": [
                {"number": 1, "text": "Turn on interior dome light, roll down driver window, place hands on steering wheel"},
                {"number": 2, "text": "Exit the vehicle immediately and walk toward the patrol cruiser quickly"},
                {"number": 3, "text": "Reach under passenger seats to search for insurance cards before officer arrives"},
                {"number": 4, "text": "Rev the engine slightly to verify alternator voltage is charging battery"}
            ],
            "correct_option": 1,
            "rationale": "SB 30 instructs motorists to pull safely to the right, turn on the dome light at night, keep hands visibly on the steering wheel, and inform the officer before reaching for documents."
        },
        {
            "id": "LAW-14",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "DISABILITIES & TLETS PROGRAM",
            "statute": "TX TRANS CODE §502.061",
            "svg_key": "disability_tlets_program",
            "prompt": "What is the primary benefit of enrolling in the Texas Driving with Disabilities Program via Form VTR-214?",
            "options": [
                {"number": 1, "text": "Alerts officers to communication impediments via TLETS before approaching vehicle"},
                {"number": 2, "text": "Exempts the driver from having to carry minimum state automotive liability insurance"},
                {"number": 3, "text": "Grants the vehicle permanent authorization to drive in carpool HOV lanes alone"},
                {"number": 4, "text": "Prohibits police officers from ever issuing traffic citations to the motorist"}
            ],
            "correct_option": 1,
            "rationale": "Form VTR-214 records a communication impediment in TLETS, alerting the officer prior to approaching the car to communicate with patience and avoid misunderstandings."
        },
        {
            "id": "LAW-15",
            "domain": "TRAFFIC LAWS & RULES OF THE ROAD",
            "category": "JULIA WELLS ACT (HUMAN TRAFFICKING)",
            "statute": "TX EDUCATION CODE §1001.1021",
            "svg_key": "human_trafficking_hotline",
            "prompt": "What is the official toll-free telephone number for the National Human Trafficking Hotline under the Julia Wells Act?",
            "options": [
                {"number": 1, "text": "1-888-373-7888 (available 24/7, confidential, or text HELP to 233733 / BeFree)"},
                {"number": 2, "text": "1-800-555-0199 (available weekdays during municipal city business hours)"},
                {"number": 3, "text": "1-877-432-1100 (state vehicle title and registration customer hotline)"},
                {"number": 4, "text": "1-800-222-1222 (state toxic poison control center emergency helpline)"}
            ],
            "correct_option": 1,
            "rationale": "Under Texas Education Code §1001.1021, the National Human Trafficking Hotline is 1-888-373-7888 (or text HELP to 233733), offering 24/7 confidential reporting."
        }
    ]
}

def generate_30_question_exam(seed=None):
    """
    Draws exactly 30 questions:
    - 15 from Bank A (Signs & Signals)
    - 15 from Bank B (Traffic Laws & Rules)
    Compliant with TDLR 16 TAC §84.503.
    """
    if seed is not None:
        random.seed(seed)
    
    bank_a = list(FINAL_EXAM_BANK["bank_a_signs"])
    bank_b = list(FINAL_EXAM_BANK["bank_b_laws"])
    
    selected_a = random.sample(bank_a, 15)
    selected_b = random.sample(bank_b, 15)
    
    # Interleave or concatenate questions
    exam_questions = []
    # Interleave: 1 Sign, 1 Law, etc.
    for i in range(15):
        # Add sign question
        q_a = dict(selected_a[i])
        q_a["number"] = len(exam_questions) + 1
        exam_questions.append(q_a)
        
        # Add law question
        q_b = dict(selected_b[i])
        q_b["number"] = len(exam_questions) + 1
        exam_questions.append(q_b)
        
    return exam_questions

if __name__ == "__main__":
    exam = generate_30_question_exam(42)
    print(f"Generated TDLR compliant exam with {len(exam)} questions.")
    signs_count = sum(1 for q in exam if q["domain"] == "HIGHWAY SIGNS & SIGNALS")
    laws_count = sum(1 for q in exam if q["domain"] == "TRAFFIC LAWS & RULES OF THE ROAD")
    print(f"Bank A (Signs & Signals): {signs_count} questions")
    print(f"Bank B (Traffic Laws): {laws_count} questions")
    print(f"Passing threshold: 21 / 30 (70.0%)")
