path = 'C:/tx_dmv/driving_rule_animations_suite/documentation/DRIVING_RULE_ANIMATION_PRODUCTION_ROADMAP.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

old_phase1 = """| # | Lesson ID | Topic Title | Cat | Statutory Anchor | Core Driving Rule | Status |
| :-: | :--- | :--- | :-: | :--- | :--- | :--- | :---: |
| 1 | **L03-T01** | Definition of Right-of-Way | A | TTC § 545.151 | Uncontrolled intersection: yield to vehicle on immediate right. | **APPROVED** |
| 2 | **L03-T02** | Traditional & Non-Traditional Intersections | A | TTC § 545.152 | T-intersection: terminating stem yields to through highway platoon. | **VERIFIED** |
| 3 | **L03-T03** | Accepting or Yielding Right-of-Way | A | TTC § 545.152 | Left turn across traffic: must yield to oncoming straight flow. | **IN PROGRESS** |
| 4 | **L03-T04** | Move Over & Slow Down Law | A | TTC § 545.157 | Vacate lane or slow 20 mph below limit for emergency vehicles. | Queued |
| 5 | **L03-T05** | Passing Stopped Emergency Vehicles | A | TTC § 545.066 | Stop for school bus with flashing red lights; median divider rule. | Queued |
| 6 | **L03-T06** | Legal & Responsible Decisions | C | TTC § 552.003 | Duty to yield to pedestrians in crosswalks and blind individuals. | Queued |
| 7 | **L03-T07** | Defensive Driving — Anticipate & Respond | C | TTC § 544.007 | Defensive scan of intersection quadrants on green before entry. | Queued |"""

new_phase1 = """| # | Lesson ID | Topic Title | Cat | Statutory Anchor | Core Driving Rule | Status |
| :-: | :--- | :--- | :-: | :--- | :--- | :--- | :---: |
| 1 | **L03-T01** | Definition of Right-of-Way | A | TTC § 545.151 | Uncontrolled intersection: yield to vehicle on immediate right. | **APPROVED** |
| 2 | **L03-T02** | Traditional & Non-Traditional Intersections | A | TTC § 545.152 | T-intersection: terminating stem yields to through highway platoon. | **VERIFIED** |
| 3 | **L03-T03** | Accepting or Yielding Right-of-Way | A | TTC § 545.152 | Left turn across traffic: must yield to oncoming straight flow. | **VERIFIED** |
| 4 | **L03-T04** | Move Over & Slow Down Law | A | TTC § 545.157 | Vacate lane or slow 20 mph below limit for emergency vehicles. | **VERIFIED** |
| 5 | **L03-T05** | Passing Stopped Emergency Vehicles | A | TTC § 545.066 | Stop for school bus with flashing red lights; median divider rule. | **VERIFIED** |
| 6 | **L03-T06** | Legal & Responsible Decisions | C | TTC § 552.003 | Duty to yield to pedestrians in crosswalks and blind individuals. | **VERIFIED** |
| 7 | **L03-T07** | Defensive Driving — Anticipate & Respond | C | TTC § 544.007 | Defensive scan of intersection quadrants on green before entry. | **IN PROGRESS** |"""

text = text.replace(old_phase1, new_phase1)
with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Roadmap Phase 1 updated!')
