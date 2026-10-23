import re

path = 'C:/tx_dmv/driving_rule_animations_suite/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize CRLF to LF
text = text.replace('\r\n', '\n')

text = text.replace('5 of 33', '6 of 33')
text = text.replace('grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6', 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6')

lesson_6_card = """        <!-- LESSON 6 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 06</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L03-T06: Pedestrians in Crosswalk</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Transportation Code &sect; 552.003</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates advance stop line compliance when a pedestrian enters a crosswalk in either half of the roadway. Includes hazard mode demonstrating prohibited overtaking of a stopped vehicle under TTC § 552.003(c).
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L03_T06_pedestrian_crosswalk.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Dual-Direction Yielding</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
"""

target = '        <!-- LESSON 5 CARD -->'
# Find closing </div> of lesson 5 card
l5_pos = text.find(target)
if l5_pos != -1:
    # find next </section>
    sec_end = text.find('      </div>\n    </section>', l5_pos)
    if sec_end != -1:
        text = text[:sec_end] + lesson_6_card + text[sec_end:]
        print('Lesson 6 card inserted successfully!')

# Update rows 6 and 7 in the table
old_row_6 = """            <tr class="hover:bg-[#181F2B]">
              <td class="py-2 px-4 mono text-gray-500">6</td>
              <td class="py-2 px-4 mono font-bold text-white">L03-T06</td>
              <td class="py-2 px-4 font-medium">Legal &amp; Responsible Decisions (Pedestrians in Crosswalk)</td>
              <td class="py-2 px-4 mono text-amber-400">HAZARD</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code § 552.003</td>
              <td class="py-2 px-4 text-right mono text-gray-500">Queued</td>
            </tr>"""

new_row_6 = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">6</td>
              <td class="py-2 px-4 mono font-bold text-white">L03-T06</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Legal &amp; Responsible Decisions (Pedestrians in Crosswalk)</td>
              <td class="py-2 px-4 mono text-emerald-400">HAZARD</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 552.003</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>"""

old_row_7 = """            <tr class="hover:bg-[#181F2B]">
              <td class="py-2 px-4 mono text-gray-500">7</td>
              <td class="py-2 px-4 mono font-bold text-white">L03-T07</td>
              <td class="py-2 px-4 font-medium">Defensive Driving &mdash; Quadrant Scanning on Green</td>
              <td class="py-2 px-4 mono text-amber-400">HAZARD</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code § 544.007</td>
              <td class="py-2 px-4 text-right mono text-gray-500">Queued</td>
            </tr>"""

new_row_7 = """            <tr class="hover:bg-[#181F2B] bg-amber-500/5">
              <td class="py-2 px-4 mono text-amber-400 font-bold">7</td>
              <td class="py-2 px-4 mono font-bold text-white">L03-T07</td>
              <td class="py-2 px-4 font-medium text-amber-300">Defensive Driving &mdash; Quadrant Scanning on Green</td>
              <td class="py-2 px-4 mono text-amber-400">HAZARD</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 544.007</td>
              <td class="py-2 px-4 text-right mono text-amber-400 font-semibold">In Production</td>
            </tr>"""

text = text.replace(old_row_6, new_row_6)
text = text.replace(old_row_7, new_row_7)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Update complete!')
