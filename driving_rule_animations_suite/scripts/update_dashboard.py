import os

with open('driving_rule_animations_suite/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update counter
c = c.replace('<span class="text-emerald-400 font-bold text-sm">17 of 33</span>', '<span class="text-emerald-400 font-bold text-sm">18 of 33</span>')

# 2. Add Lesson 17 Card after Lesson 16 Card
target_card = '<!-- LESSON 33 CARD -->'
l17_card = '''        <!-- LESSON 17 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 17</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L05-T08: Adverse Conditions &mdash; Hydroplaning &amp; Texas Flash Flood Barricade Law</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Driver Handbook Ch. 5 &bull; Texas Transportation Code &sect; 472.022</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates hydrodynamic lift dynamics (tire water wedge causing complete 0% traction at &gt;35 MPH) and mandatory throttle-lift recovery (no panic braking). Highlights Texas low-water crossing hazards with authentic MUTCD Type 3 Road Closed barricades, roadside depth gauge metrics (12&quot; floats cars, 24&quot; sweeps trucks), the statutory &quot;Turn Around, Don't Drown&quot; mandate, and the Class B Misdemeanor penalty for barricade bypass.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L05_T08_poor_conditions_flash_floods.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Hydroplaning &bull; Flood Barricades</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
'''

if '<!-- LESSON 17 CARD -->' not in c:
    c = c.replace(target_card, l17_card + target_card)

# 3. Add table rows 14, 15, 16, 17
target_tr = '<tr class="hover:bg-[#181F2B] bg-emerald-500/5">\n              <td class="py-2 px-4 mono text-emerald-400 font-bold">33</td>'
rows_to_add = '''            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">14</td>
              <td class="py-2 px-4 mono font-bold text-white">L05-T05</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Blind Spot Driving &mdash; Mirror Coverage &amp; Mandatory Shoulder Head-Check</td>
              <td class="py-2 px-4 mono text-emerald-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.060</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">15</td>
              <td class="py-2 px-4 mono font-bold text-white">L05-T06</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Safe Following Distances &mdash; The 3-Second Rule &amp; Adverse Condition Multipliers</td>
              <td class="py-2 px-4 mono text-emerald-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.062</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">16</td>
              <td class="py-2 px-4 mono font-bold text-white">L05-T07</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Safe Stopping Distances &mdash; The Perception, Reaction &amp; Braking Curve</td>
              <td class="py-2 px-4 mono text-emerald-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 545.351</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">17</td>
              <td class="py-2 px-4 mono font-bold text-white">L05-T08</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Adverse Conditions &mdash; Hydroplaning &amp; Texas Flash Flood Barricade Law</td>
              <td class="py-2 px-4 mono text-emerald-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 472.022</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
'''

if 'L05-T08</td>' not in c:
    c = c.replace(target_tr, rows_to_add + target_tr)

with open('driving_rule_animations_suite/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Dashboard successfully updated!')
