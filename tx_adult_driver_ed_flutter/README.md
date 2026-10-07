# Texas Adult Driver Education (ADE-1317) — Flutter Mobile & Web App

Official, TDLR-compliant cross-platform mobile and web application for Texas Adult Driver Education (School License #C3284, Course ADE-1317, 16 TAC § 84.500).

---

## 📱 Mobile-First Enhancements (Adjusted for Phones)

While the web platform is built for desktop widescreen viewing, this Flutter application has been customized specifically for mobile phones and tablets:

1. **Responsive Ergonomics (`ResponsiveBuilder`)**:
   - Single-column scrolling tailored for one-handed thumb navigation.
   - Touch targets designed with a minimum of 48×48dp (buttons at 52dp height).
   - Dynamic viewports scaling across phones (<600dp), tablets (600–1024dp), and desktops (>1024dp).

2. **Mobile Curriculum Drawer (`CurriculumDrawer`)**:
   - Slide-out bottom sheet / navigation drawer for fast syllabus browsing.
   - Real-time progress bars and topic checkmarks.
   - Module 1 Free Preview unlocked by default; Modules 2–9 locked with inline promo redemption.

3. **Statutory Active Timer & Heartbeat (16 TAC § 84.500)**:
   - Sticky countdown timer on mobile top app bar.
   - Automatic 30-second heartbeats sent to Google Cloud Run API backend.
   - Background pausing when phone screen goes idle or app enters background.

4. **Personal Verification Questions (PVQ Modal)**:
   - 90-second statutory countdown challenge dialog.
   - Prevents bypass by adhering strictly to state identity rules.

5. **100% OFF Admin Promo Code Integration**:
   - Promo dialog with one-tap redemption for **`TEXAS100`** (and `FREE100`, `TEXASVIP`, `TDLRADMIN`).
   - Immediately unlocks all 9 modules and 75 topics locally and synchronizes with the server.

6. **Cloud Run API Synchronization**:
   - Directly connected to production Cloud Run API:
     `https://tx-ade-api-1004296326114.us-central1.run.app`

---

## 📂 Architecture & Directory Structure

```
tx_adult_driver_ed_flutter/
├── pubspec.yaml                 # Dependencies and assets configuration
├── assets/
│   └── curriculum/
│       └── curriculum_data.json # 9 modules, 75 topics, required study minutes
└── lib/
    ├── main.dart                # App entry point & multi-provider wiring
    ├── config/
    │   ├── constants.dart       # API URLs, OAuth client IDs, TDLR compliance rules
    │   └── theme.dart           # Mobile-optimized dark cyber-tech theme
    ├── models/
    │   ├── user_model.dart      # Student identity, role, enrollment status
    │   ├── curriculum_model.dart# Modules, topics, quizzes
    │   └── progress_model.dart  # Completed topics, active topic, study seconds
    ├── services/
    │   ├── api_service.dart     # Cloud Run REST client with JWT headers
    │   └── storage_service.dart # SharedPreferences local cache
    ├── providers/
    │   ├── auth_provider.dart   # Reactive auth state & promo coupon processor
    │   └── course_provider.dart # Curriculum state, navigation, statutory timers
    └── views/
        ├── common/
        │   └── responsive_builder.dart # Device break-point detector
        ├── landing/
        │   └── landing_page.dart       # Mobile-optimized hero, features & coupon card
        ├── classroom/
        │   ├── classroom_screen.dart   # Virtual classroom, topic reader & sticky timer
        │   └── curriculum_drawer.dart  # Mobile syllabus drawer with progress meters
        ├── dialogs/
        │   ├── signin_sheet.dart       # TDLR-compliant mandatory sign-in gate
        │   ├── coupon_dialog.dart      # 100% OFF code redemption bottom-sheet
        │   └── pvq_dialog.dart         # 90-second statutory PVQ identity challenge
        └── quiz/
            └── quiz_view.dart          # 70% pass-rate interactive topic assessment
```

---

## 🚀 How to Run

### Prerequisites
- Flutter SDK (3.0.0+)
- Android Studio / Xcode / Chrome

### Run Commands
```bash
# 1. Fetch dependencies
flutter pub get

# 2. Run on Mobile (Android / iOS)
flutter run

# 3. Run on Web
flutter run -d chrome
```
