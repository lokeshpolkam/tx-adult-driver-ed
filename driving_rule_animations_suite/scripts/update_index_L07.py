import os

path = 'C:/tx_dmv/driving_rule_animations_suite/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n')

text = text.replace('6 of 33', '7 of 33')

lesson_7_card = """        <!-- LESSON 7 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 07</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L03-T07: Defensive Driving &mdash; Quadrant Scanning</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Transportation Code &sect; 544.007(b)</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates 4-quadrant visual sweep (left-center-right-left) on green signal with a 2-second defensive hold to evade red-light runners. Dual scenario toggle includes Hazard Demo of fatal T-bone side-impact crash.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L03_T07_defensive_quadrant_scanning.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>4-Quadrant Visual Sweep</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
"""

# Insert lesson 7 card after lesson 6 card
target_end = '      </div>\n    </section>'
sec_end = text.find(target_end)
if sec_end != -1:
    text = text[:sec_end] + lesson_7_card + text[sec_end:]
    print('Lesson 7 card inserted!')

old_row_7 = """            <tr class="hover:bg-[#181F2B] bg-amber-500/5">
              <td class="py-2 px-4 mono text-amber-400 font-bold">7</td>
              <td class="py-2 px-4 mono font-bold text-white">L03-T07</td>
              <td class="py-2 px-4 font-medium text-amber-300">Defensive Driving &mdash; Quadrant Scanning on Green</td>
              <td class="py-2 px-4 mono text-amber-400">HAZARD</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 544.007</td>
              <td class="py-2 px-4 text-right mono text-amber-400 font-semibold">In Production</td>
            </tr>"""

new_row_7_and_8 = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">7</td>
              <td class="py-2 px-4 mono font-bold text-white">L03-T07</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Defensive Driving &mdash; Quadrant Scanning on Green</td>
              <td class="py-2 px-4 mono text-emerald-400">HAZARD</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 544.007(b)</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
            <tr class="hover:bg-[#181F2B] bg-amber-500/5">
              <td class="py-2 px-4 mono text-amber-400 font-bold">8</td>
              <td class="py-2 px-4 mono font-bold text-white">L04-T02</td>
              <td class="py-2 px-4 font-medium text-amber-300">Responding to Traffic Control Devices (Flashing Yellow Arrow)</td>
              <td class="py-2 px-4 mono text-amber-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 544.007</td>
              <td class="py-2 px-4 text-right mono text-amber-400 font-semibold">In Production</td>
            </tr>"""

if old_row_7 in text:
    text = text.replace(old_row_7, new_row_7_and_8)
    print('Table rows updated!')
else:
    print('old_row_7 not matched, checking partial match...')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Dashboard update complete!')
