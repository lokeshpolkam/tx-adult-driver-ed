import os

path = 'C:/tx_dmv/driving_rule_animations_suite/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n')

text = text.replace('7 of 33', '8 of 33')

lesson_8_card = """        <!-- LESSON 8 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 08</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L04-T02: Traffic Control Devices &mdash; Flashing Yellow Arrow</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Transportation Code &sect; 544.007</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates Texas 4-section signal mast phasing: Flashing Yellow Arrow (permissive turn yielding to oncoming traffic) vs. Steady Green Arrow (protected turn). Includes Hazard Demo of failure to yield on FYA.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L04_T02_flashing_yellow_arrow.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Flashing Yellow vs. Green Arrow</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
"""

# Insert lesson 8 card after lesson 7 card
target_end = '      </div>\n    </section>'
sec_end = text.find(target_end)
if sec_end != -1:
    text = text[:sec_end] + lesson_8_card + text[sec_end:]
    print('Lesson 8 card inserted!')

old_row_8 = """            <tr class="hover:bg-[#181F2B] bg-amber-500/5">
              <td class="py-2 px-4 mono text-amber-400 font-bold">8</td>
              <td class="py-2 px-4 mono font-bold text-white">L04-T02</td>
              <td class="py-2 px-4 font-medium text-amber-300">Responding to Traffic Control Devices (Flashing Yellow Arrow)</td>
              <td class="py-2 px-4 mono text-amber-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 544.007</td>
              <td class="py-2 px-4 text-right mono text-amber-400 font-semibold">In Production</td>
            </tr>"""

new_row_8_and_9 = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">8</td>
              <td class="py-2 px-4 mono font-bold text-white">L04-T02</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Responding to Traffic Control Devices (Flashing Yellow Arrow)</td>
              <td class="py-2 px-4 mono text-blue-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 544.007</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
            <tr class="hover:bg-[#181F2B] bg-amber-500/5">
              <td class="py-2 px-4 mono text-amber-400 font-bold">9</td>
              <td class="py-2 px-4 mono font-bold text-white">L04-T03</td>
              <td class="py-2 px-4 font-medium text-amber-300">Pavement Markings (Solid vs. Broken Lines &amp; Passing Zones)</td>
              <td class="py-2 px-4 mono text-amber-400">SPATIAL</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.055</td>
              <td class="py-2 px-4 text-right mono text-amber-400 font-semibold">In Production</td>
            </tr>"""

if old_row_8 in text:
    text = text.replace(old_row_8, new_row_8_and_9)
    print('Table rows updated!')
else:
    print('old_row_8 not found')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Dashboard update complete!')
