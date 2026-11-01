# OPEN QUESTIONS & ARCHITECTURAL DECISIONS
## Texas DMV Driving-Rule Animation Production System
**Document Version:** 1.0  
**Phase:** Gate 1 Review  
**Date:** October 2026

---

## 1. MOTION RENDERING PIPELINE & FIDELITY CONTROL

### Context:
Prior pilot attempts using pure text-to-video diffusion models (such as Gemini video diffusion) produced catastrophic instructional failures:
- Vehicles accelerated through red lights and stop signs (an immediate TDLR ADE-1317 compliance violation).
- Vehicles reversed backwards into buildings or morphed into other objects.
- Prompt hex color codes (e.g., `#ECEEEA`) were rendered by text encoders as literal graffiti painted onto walls.
- Prompts that exceeded token limits caused the models to freeze into static images.

### Question for Production Direction:
Should we transition from unconstrained generative video diffusion to a **deterministic motion graphics pipeline** (e.g., React-Remotion, GSAP/HTML5 Canvas, or controlled 2.5D vector/3D rendering) using our existing 44 verified 2.5D isometric stills as backdrops?

**Instructional Recommendation:**  
Adopt a deterministic motion pipeline where vehicle positions, stop lines, signal timings, and indicator blinkers are driven by exact statutory math. This guarantees:
1. No red light runs or illegal maneuvers.
2. 100% visual consistency with the existing 44 architectural stills in `c:\tx_dmv\course_shell\final_course_export\assets\2_5d\`.
3. Deterministic 60fps rendering at 1080p without AI morphing or random hallucinations.

---

## 2. PILOT ANIMATION SELECTION

### Candidate Recommendation: `L03-T01: Definition of Right-of-Way` (TTC § 545.151)
- **Subject**: Uncontrolled 4-way intersection right-of-way (vehicle on the left yields to vehicle on the right).
- **Existing Asset**: High-resolution 2.5D still already exists (`L03_T01_uncontrolled_intersection.jpg`).
- **Pedagogical Significance**: This is the single most tested right-of-way concept on the Texas DPS driving examination.
- **Complexity**: Moderate (2 vehicles, clear sequential timing, clear legal outcome).

**Question**:  
Does the user approve `L03-T01` as the designated pilot animation to establish the visual and motion benchmark before proceeding to the other 32 animation candidates?

---

## 3. COMMUNITY SAFETY EDUCATION ACT (SB 30) VIDEO (L07-T07)

### Context:
Texas Education Code § 28.012 and 16 TAC § 84.500 mandate instruction on the Community Safety Education Act regarding rights and responsibilities during a peace officer traffic stop. TDLR and Texas DPS provide an official 16-minute live-action instructional video for this requirement.

**Question**:  
Should `L07-T07` embed the official state-provided live-action SB 30 video, or should it feature a concise, standardized 2.5D procedural graphic summarizing the 7-step safe pulloff protocol?

**Instructional Recommendation**:  
Provide both: embed the official state educational video in `L07-T07` as legally required by TDLR, and provide a 2.5D animated procedural walkthrough in `L07-T06` ("Stopped by Law Enforcement") demonstrating proper driver hand positioning (10 and 2), dome light activation, and safe shoulder clearance.

---

## 4. COMPOUND MANEUVERS IN LESSON L05-T04

### Context:
Lesson `L05-T04` ("Passing, Turning, and Parking") covers two distinct maneuvers:
1. Passing on a two-lane rural highway (TTC § 545.053: returning to right side before coming within 200 feet of oncoming vehicle).
2. Parallel parking mechanics (TTC § 545.302: parking within 6 to 18 inches of the curb).

**Question**:  
Should `L05-T04` feature a two-part animation (Part 1: 2-Lane Passing Clearance; Part 2: Parallel Parking Maneuver), or should we prioritize the open-road passing maneuver as the primary animated asset?

**Instructional Recommendation**:  
Produce a two-part sequential animation or prioritize the two-lane highway passing maneuver, as passing head-on collisions represent the highest fatality risk in driver education, whereas parallel parking can be supplemented by a static multi-step steering diagram.

---

## 5. VIDEO ASSET STORAGE & BANDWIDTH TARGETS

### Context:
The production website is deployed on Vercel (`https://tx-drive.vercel.app`). Serving 33 uncompressed high-bitrate MP4 files could incur heavy bandwidth consumption and slow mobile initial page loads.

**Recommendation**:
- Codec: H.264 / AAC in MP4 container with WebM (VP9) fallback.
- Target bitrate: 1,500 – 2,500 kbps (1080p @ 30fps).
- Maximum file size per animation: Under 4.5 MB for a 10–15 second loop.
- Host directly in `course_shell/public/assets/videos/` with aggressive caching headers.
