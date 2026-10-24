with open('driving_rule_animations_suite/scripts/build_L07_T03.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = """<text id="lbl-zone-front" x="0" y="0" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="900" text-anchor="middle">FRONT NO-ZONE (20 FT)</text>"""
replacement1 = """<g id="badge-front-nozone" transform="translate(0, 0)">
            <rect x="-55" y="-7" width="110" height="14" rx="7" fill="#450A0A" stroke="#EF4444" stroke-width="1" />
            <text x="0" y="3" fill="#FCA5A5" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="900" text-anchor="middle">FRONT NO-ZONE (20 FT)</text>
          </g>"""

target2 = """<text id="lbl-zone-left" x="0" y="0" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="900" text-anchor="middle">LEFT NO-ZONE</text>"""
replacement2 = """<g id="badge-left-nozone" transform="translate(0, 0)">
            <rect x="-42" y="-7" width="84" height="14" rx="7" fill="#451A03" stroke="#F59E0B" stroke-width="1" />
            <text x="0" y="3" fill="#FDE68A" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="900" text-anchor="middle">LEFT NO-ZONE</text>
          </g>"""

if target1 in text:
    text = text.replace(target1, replacement1, 1)
    print("Replaced target 1.")
else:
    print("Target 1 not found!")

if target2 in text:
    text = text.replace(target2, replacement2, 1)
    print("Replaced target 2.")
else:
    print("Target 2 not found!")

with open('driving_rule_animations_suite/scripts/build_L07_T03.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("build_L07_T03.py updated.")
