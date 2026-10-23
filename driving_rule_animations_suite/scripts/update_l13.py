with open('driving_rule_animations_suite/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update counter
content = content.replace(
    '<span class="text-emerald-400 font-bold text-sm">13 of 33</span>',
    '<span class="text-emerald-400 font-bold text-sm">14 of 33</span>'
)

# Insert Lesson 13 card right after Lesson 12 card
l13_card = '''        <!-- LESSON 13 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 13</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L05-T04: Passing Maneuvers &mdash; The 200-Foot Oncoming Return Clearance Rule</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Transportation Code &sect; 545.054, &sect; 545.053 &amp; &sect; 545.056</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates the statutory requirement under TTC &sect; 545.054 to return to the authorized lane of travel before coming within 200 feet of an oncoming vehicle. Highlights mirror apex checks (headlights visible before return), bridge/structure passing prohibition zones (TTC &sect; 545.056), and a critical head-on hazard simulation for late returns.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L05_T04_passing_turning_parking.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>200-Ft Oncoming Clearance</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
'''

target_after_l12 = '          </div>\n        </div>\n        <!-- LESSON 33 CARD -->'
replacement_after_l12 = '          </div>\n        </div>\n' + l13_card + '        <!-- LESSON 33 CARD -->'

content = content.replace(target_after_l12, replacement_after_l12)

# Insert Lesson 13 row in table
l13_row = '''            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">13</td>
              <td class="py-2 px-4 mono font-bold text-white">L05-T04</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Passing, Turning, and Parking &mdash; The 200-Foot Oncoming Return Rule</td>
              <td class="py-2 px-4 mono text-emerald-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.054</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
'''

target_after_row12 = '''              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.104</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>'''

content = content.replace(target_after_row12, target_after_row12 + '\n' + l13_row)

with open('driving_rule_animations_suite/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard index.html successfully updated for Lesson 13!")
