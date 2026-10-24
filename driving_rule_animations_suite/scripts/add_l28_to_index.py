import os

def update_index():
    path = 'driving_rule_animations_suite/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Update counter
    c = c.replace('28 of 33', '29 of 33')

    # 2. Insert Card after Lesson 27 Card
    l28_card = '''        <!-- LESSON 28 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-blue-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 mono">LESSON 28</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L07-T12: Operating Near Oversize Vehicles &amp; Wide Convoys</h3>
              <p class="text-xs text-gray-400 mt-1">TxDMV Permitted Oversize Loads &bull; TTC &sect; 623.001 &amp; &sect; 545.062</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates lawful navigation near permitted oversize and overweight transport convoys: detecting lead pilot escort vehicles with amber flashing strobes and "OVERSIZE LOAD" banners, maintaining a protective 200+ foot following cushion outside the rear No-Zone, respecting 14-foot wide deck lane straddling, executing brisk multi-lane passing via outer Lane 3, and requiring interior rearview mirror confirmation of both pilot headlights before returning to the travel lane (TTC &sect; 545.053). Includes narrow bridge bottleneck pinch and premature cut-in 400+ foot stopping deficit hazard simulations.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L07_T12_oversize_vehicles.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Pilot Strobes &bull; 14-FT Wide Deck</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
'''

    target_card = '<!-- LESSON 33 CARD -->'
    if target_card in c and 'LESSON 28 CARD' not in c:
        c = c.replace(target_card, l28_card + '\n        ' + target_card)

    # 3. Insert Table row
    l28_row = '''            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">28</td>
              <td class="py-2 px-4 mono font-bold text-white">L07-T12</td>
              <td class="py-2 px-4 font-medium text-blue-300">Operating Near Oversize Vehicles &mdash; Convoys, Pilot Strobes &amp; Chokepoints</td>
              <td class="py-2 px-4 mono text-blue-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">TTC &sect; 623.001 &amp; &sect; 545.062 &bull; TxDMV Permits</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>\n'''

    if 'L07-T12</td>' not in c:
        idx = c.find('<td class="py-2 px-4 mono text-emerald-400 font-bold">33</td>')
        if idx != -1:
            tr_start = c.rfind('<tr', 0, idx)
            c = c[:tr_start] + l28_row + c[tr_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

    print('Successfully updated index.html with Lesson 28!')

if __name__ == '__main__':
    update_index()
