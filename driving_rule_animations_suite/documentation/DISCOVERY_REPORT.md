# PHASE 1 — PROJECT DISCOVERY REPORT
## Texas DMV (ADE-1317) Driving-Rule Animation Production System
**Date:** October 2026  
**Auditor / Roles:** Senior Instructional Designer, Texas Driver-Ed SME, 2.5D Animation Director, Motion-Graphics Engineer, QA Engineer, Production Manager  
**Production Target:** `https://tx-drive.vercel.app` (`dogbyte-dels-projects/tx-drive`)  
**Non-Production Workspace:** `C:\tx_dmv\driving_rule_animations\`

---

## 1. PROJECT STRUCTURE & RELEVANT FILES

A comprehensive audit of the `C:\tx_dmv` repository was conducted to inspect curriculum sources, frontend shell implementations, media containers, assessment engines, and existing visual assets.

### 1.1 Core Directories and System Architecture
- **Canonical Course Shell**: [`c:\tx_dmv\course_shell\`](file:///c:/tx_dmv/course_shell)
  - `classroom.html`: Primary student learning portal containing the authoritative `COURSE_DATA` JavaScript object which governs module hierarchy, topic sequence, pass thresholds, and time tracking.
  - `player.html`: Alternate/standalone lesson player supporting iframe-based curriculum delivery.
  - `app_lessons/`: Contains 75 modular HTML lesson source files (`L01-T01.html` through `L08-T10.html`, and `L09-T01.html`).
  - `final_course_export/`: Symmetrical desktop-optimized package containing the matching 75 HTML lesson files and legacy static assets.
  - `mcqs/`: Modular assessment engine containing 75 individual lesson quiz HTML files and `final_exam.html`.
  - `mcqs/final_exam.html`: Authoritative Texas DPS 30-Question Highway Sign and Traffic Law summative examination.
- **Curriculum Specifications & Statutory Indexes**:
  - [`c:\tx_dmv\curriculum\MASTER_CURRICULUM_INDEX.md`](file:///c:/tx_dmv/curriculum/MASTER_CURRICULUM_INDEX.md): Curriculum map linking TDLR POI (Program of Instruction) requirements, Texas Driver Handbook chapters, and statutory citations.
  - `c:\tx_dmv\MASTER_CURRICULUM_INDEX_V2.json`: Machine-readable mapping of curriculum units, topics, estimated times, and handbook sections.
- **Visual Assets**:
  - [`c:\tx_dmv\course_shell\final_course_export\assets\2_5d\`](file:///c:/tx_dmv/course_shell/final_course_export/assets/2_5d): 44 verified 1920×1080 architectural isometric static illustrations.
  - `c:\tx_dmv\course_shell\app_lessons\assets\`: Mirrored assets directory for the mobile/app shell.
  - `c:\tx_dmv\gemini_videos\`: Directory containing experimental video renders (e.g. `L01-T01.mp4`).

---

## 2. CANONICAL COURSE INVENTORY & COMPLETENESS VERIFICATION

### 2.1 How Completeness Was Established
Completeness was established through 4-way cross-verification:
1. **Frontend Driver Verification**: Parsing `COURSE_DATA.modules` in `course_shell/classroom.html`.
2. **File System Verification**: Verifying the presence of all 75 instructional HTML files in both `course_shell/app_lessons/` and `course_shell/final_course_export/`.
3. **Assessment Engine Mapping**: Verifying that each instructional topic maps 1:1 to an MCQ quiz file in `course_shell/mcqs/` and that the final exam resides at `course_shell/mcqs/final_exam.html`.
4. **Curriculum Index Alignment**: Cross-referencing against `MASTER_CURRICULUM_INDEX_V2.json` and TDLR ADE-1317 Program of Instruction (POI) standards.

### 2.2 Canonical Course Hierarchy (76 Items Total)
The Texas Adult Driver Education (ADE-1317) 6-hour curriculum consists of 9 modules comprising exactly **76 canonical items** (74 instructional topics, 1 identity verification checkpoint, and 1 final examination):

| Module | Code | Title | Topics | Key Subject Matter |
|---|---|---|---|---|
| **Module 1** | MOD 01 | Course Intro & Safety | 3 topics (L01-T01 to L01-T03) | ADE value, traffic laws framework, driving as a privilege |
| **Module 2** | MOD 02 | Your License to Drive | 7 topics (L02-T01 to L02-T07) | DL qualifications, license classes, suspensions, inspection, insurance (Safety Responsibility Act), disability program |
| **Module 3** | MOD 03 | Right-of-Way Rules | 7 topics (L03-T01 to L03-T07) | Uncontrolled intersections, T-intersections, 4-way stops, roundabouts, Move Over/Slow Down, school buses, defensive scanning |
| **Module 4** | MOD 04 | Traffic Control Devices | 4 topics (L04-T01 to L04-T04) | Signs & shapes, signal phases (flashing yellow arrow), pavement markings, dark/malfunctioning signals |
| **Module 5** | MOD 05 | Controlling Traffic Flow | 18 topics (L05-T01 to L05-T18) | Basic speed rule, lane selection, signaling (100 ft), passing & parking, blind spots, 3-sec interval, stopping distance, floods, speed limits, freeway merging, breakdowns, tire blowout, winter skids, work zones |
| **Module 6** | MOD 06 | Alcohol & Drug Awareness | 7 topics (L06-T01 to L06-T07) | 0.08 legal intoxication definition, physiological impairment, DWI penalties, Minor Zero Tolerance, open container, ALR / implied consent |
| **Module 7** | MOD 07 | Sharing the Road | 18 topics (L07-T01 to L07-T18) | Road users, Good Samaritan Act, commercial blind spots (No-Zones), vulnerable users, seatbelts, police stops, SB 30, road rage, oversize loads, Texas Driving with Disabilities workflow |
| **Module 8** | MOD 08 | Managing Risk | 10 topics (L08-T01 to L08-T10) | SIPDE process, decision errors, vehicle maintenance, distracted driving (cell phones), street racing, railroad crossings, overdriving headlights, Steer It & Clear It, human trafficking (Julia Wells Act) |
| **Module 9** | MOD 09 | Final Exam Prep & Review | 2 topics (L09-T01 to L09-T02) | L09-T01: Identity Verification Checkpoint (16 TAC § 84.500); L09-T02: Official DPS 30-Question Final Exam |

---

## 3. EXISTING ASSETS & REUSABLE RESOURCES

### 3.1 2.5D Isometric Architectural Stills (44 Stills)
- Located in `course_shell/final_course_export/assets/2_5d/`.
- Rendered in high-resolution (1920×1080) isometric perspective with uniform architectural styling:
  - Neutral warm grey roadway surface (`#ECEEEA` / `#D9DDD8`)
  - Crisp lane markings (MUTCD standard yellow double lines and white dashed lines)
  - Cohesive vehicle models (sedans, SUVs, transit trucks, police cruisers)
  - Clear technical overhead lighting with soft directional shadows
- **Instructional Value**: These 44 assets provide an authoritative visual reference standard. They prove that consistent 2.5D visual design can be maintained across the entire course.

### 3.2 Prior Video Generation Audit & Root-Cause Failure Analysis
Inspection of previously generated MP4 files in `c:\tx_dmv\pending_25d_video_lessons\assets\videos\` revealed severe fidelity and instructional failures:
1. **Red Light Violations**: Prompting models to change lights dynamically resulted in vehicles accelerating through solid red lights, violating Texas Transportation Code § 544.007 and invalidating the educational credibility of the course.
2. **Diffusion Hallucinations**: Standard diffusion video generators suffered from vehicle cloning, spontaneous color morphing, vehicles reversing into buildings, and phantom camera rotations.
3. **Hex Code Bleed**: Over-specified color codes in text prompts (e.g. `#ECEEEA`) were literally painted by diffusion text encoders as alphanumeric graffiti onto road surfaces and buildings.
4. **Token Bloat & Motion Stagnation**: Extremely lengthy text prompts (14,000+ characters) choked diffusion text encoders, producing frozen still images with zero motion.

**Conclusion**: Generative diffusion video without deterministic vector or procedural motion constraints is unsuitable for legally regulated driver education. Driver education requires absolute geometric precision: vehicles must stop at stop lines, obey signal indications, and signal at exact distances.

---

## 4. EXISTING TECHNICAL CONSTRAINTS

### 4.1 Production Hosting & Deployment Constraints
- **Target URL**: `https://tx-drive.vercel.app` (Project: `dogbyte-dels-projects/tx-drive`).
- **No In-Lesson Popups**: Per state accreditation and user rules, no popup modals or timed challenge interruptions may be added during lessons.
- **Module 9, Topic 1 (L09-T01) Constraint**: PVQ Checkpoint must render all 5 personal verification questions on a single page (no wizards or pagination).
- **Module 9, Topic 2 (L09-T02) Constraint**: The 30 state exam questions in `mcqs/final_exam.html` must remain untouched and un-prepended.

### 4.2 Web Media Container Standard
All 75 lesson files in `course_shell/app_lessons/` utilize a standard Tailwind CSS technical container:
```html
<section class="bg-white border border-[#D9DDD8] rounded-xl p-3 sm:p-6 md:p-10 shadow-sm">
  <div class="w-full h-56 sm:h-80 md:h-[440px] bg-[#ECEEEA] border border-[#D9DDD8] rounded-lg relative overflow-hidden bg-tech-grid flex items-center justify-center group">
    <img src="./assets/2_5d/Lxx_Txx_example.jpg" class="w-full h-full object-cover rounded-lg" alt="..." />
  </div>
</section>
```
To preserve backward compatibility, zero HTML layout restructuring is required: an approved video asset will drop directly into this exact container using a matching `<video playsinline controls loop muted>` element or maintain the static image where appropriate.

---

## 5. MISSING INFORMATION & UNRESOLVED QUESTIONS

1. **State-Mandated SB 30 Video vs Custom 2.5D Animation (L07-T07)**:
   - Senate Bill 30 / Community Safety Education Act instructional guidelines reference an official state-produced video for law enforcement interaction. We need to confirm whether the platform will embed the official Texas DPS/TDLR video asset or a customized 2.5D schematic of the stop protocol.
2. **Animation Engine & Technology Stack for Motion**:
   - Given the fatal defects of purely generative AI diffusion models (running red lights, hallucinated vehicles), what technical motion pipeline will be used? (e.g., Code-driven SVG/Canvas/Remotion animations, controlled 2.5D motion graphics, or highly constrained video compositing).
3. **Compound Maneuvers in L05-T04**:
   - Lesson L05-T04 covers two complex maneuvers: 2-lane highway passing (TTC § 545.053) and parallel parking (TTC § 545.302). Should these be staged as a single dual-part animation or prioritized for the high-risk passing maneuver?

---

## 6. PROPOSED NEXT STEPS

1. **Complete Phase 2 Review**: Review the 76-item `DRIVING_RULE_LESSON_INVENTORY` (CSV and JSON) and the `LESSON_COVERAGE_AUDIT`.
2. **Reach Approval Gate 1**: Stop and present the inventory classifications to the user for formal approval.
3. **Upon Approval (Phase 3)**: Select 1 pilot animation candidate (e.g., L03-T01 Uncontrolled Intersection Right-of-Way) and draft its comprehensive, legally verified Texas storyboard.
