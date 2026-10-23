with open(r'C:\tx_dmv\driving_rule_animations_suite\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Update count
text = text.replace('8 of 33', '9 of 33')

# Card to insert
lesson_9_card = """        <!-- LESSON 9 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 09</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L04-T03: Pavement Markings &mdash; Passing Zones</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Transportation Code &sect; 545.055 &amp; &sect; 545.054</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates legal passing corridor across broken yellow centerline vs. strict double solid yellow line no-passing zone (MUTCD W14-3). Enforces 100-ft signal, 45 MPH overtaking, and &gt;200-ft safe buffer return. Includes Hazard Demo of illegal passing head-on conflict.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L04_T03_pavement_markings_passing.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Solid vs. Broken Yellow Passing</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
"""

idx_card = text.find('Flashing Yellow vs. Green Arrow')
if idx_card != -1:
    end_card = text.find('</div>\n        </div>', idx_card)
    if end_card != -1:
        insert_pos = end_card + len('</div>\n        </div>\n')
        text = text[:insert_pos] + lesson_9_card + text[insert_pos:]
        print('Card inserted!')

# Table update
old_row = """            <tr class="hover:bg-[#181F2B] bg-amber-500/5">
              <td class="py-2 px-4 mono text-amber-400 font-bold">9</td>
              <td class="py-2 px-4 mono font-bold text-white">L04-T03</td>
              <td class="py-2 px-4 font-medium text-amber-300">Pavement Markings (Solid vs. Broken Lines &amp; Passing Zones)</td>
              <td class="py-2 px-4 mono text-amber-400">SPATIAL</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.055</td>
              <td class="py-2 px-4 text-right mono text-amber-400 font-semibold">In Production</td>
            </tr>"""

new_rows = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">9</td>
              <td class="py-2 px-4 mono font-bold text-white">L04-T03</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Pavement Markings (Solid vs. Broken Lines &amp; Passing Zones)</td>
              <td class="py-2 px-4 mono text-emerald-400">SPATIAL</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.055 &amp; &sect; 545.054</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
            <tr class="hover:bg-[#181F2B] bg-amber-500/5">
              <td class="py-2 px-4 mono text-amber-400 font-bold">10</td>
              <td class="py-2 px-4 mono font-bold text-white">L04-T04</td>
              <td class="py-2 px-4 font-medium text-amber-300">Dark / Malfunctioning Signals &mdash; 4-Way Stop Rule</td>
              <td class="py-2 px-4 mono text-amber-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 544.007(x)</td>
              <td class="py-2 px-4 text-right mono text-amber-400 font-semibold">In Production</td>
            </tr>"""

text = text.replace(old_row, new_rows)

with open(r'C:\tx_dmv\driving_rule_animations_suite\index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Dashboard index.html successfully updated!')
