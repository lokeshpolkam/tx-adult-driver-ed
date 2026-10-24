import os

index_path = r"C:\tx_dmv\driving_rule_animations_suite\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n')

# 1. Update counter to 33 of 33 (100% COMPLETE)
assert "32 of 33" in text, "Could not find '32 of 33' in index.html"
text = text.replace("32 of 33", "33 of 33 (100% COMPLETE)")

# 2. Lesson 32 Card
lesson_32_card = """        <!-- LESSON 32 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 32</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L08-T07: Dangers of Driving at Night &mdash; Overdriving Headlights</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Transportation Code &sect; 547.302 &amp; &sect; 547.333</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates the critical physics of overdriving headlights: low-beam 180-foot sightline vs. 312-foot stopping distance at 65 MPH (driving 132 feet blind!). Contrasts safe 45 MPH low-beam speed ceiling with high-beam 420-foot illumination, oncoming 500-foot dimming mandate, white fog line visual anchor to prevent retinal bleaching, and 300-foot rear following dimming rule.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L08_T07_night_driving.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Overdriving Headlights &bull; 500-FT Dimming</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>

"""

# Insert right before LESSON 33 CARD
target_l33_card = '        <!-- LESSON 33 CARD -->'
assert target_l33_card in text, "Could not find LESSON 33 CARD marker"
text = text.replace(target_l33_card, lesson_32_card + target_l33_card)

# 3. Lesson 32 Table Row
lesson_32_row = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">32</td>
              <td class="py-2 px-4 mono font-bold text-white">L08-T07</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Dangers of Driving at Night &mdash; Overdriving Headlights</td>
              <td class="py-2 px-4 mono text-emerald-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">TTC &sect; 547.302 &amp; &sect; 547.333</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
"""

target_l33_row = '<tr class="hover:bg-[#181F2B] bg-emerald-500/5">\n              <td class="py-2 px-4 mono text-emerald-400 font-bold">33</td>'
assert target_l33_row in text, "Could not find LESSON 33 table row marker"
text = text.replace(target_l33_row, lesson_32_row + target_l33_row)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("index.html updated successfully with Lesson 32 (33 of 33 Complete)!")
