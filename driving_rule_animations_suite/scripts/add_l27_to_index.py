import os

def update_index():
    path = 'driving_rule_animations_suite/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Update counter
    c = c.replace('27 of 33', '28 of 33')

    # 2. Insert Card after Lesson 26 Card
    l27_card = '''        <!-- LESSON 27 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-blue-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 mono">LESSON 27</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L07-T08: Aggressive Driving &amp; Road Rage Avoidance</h3>
              <p class="text-xs text-gray-400 mt-1">Defensive De-escalation &bull; TTC &sect; 545.401 &amp; &sect; 545.062</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates defensive de-escalation protocols when confronting aggressive drivers and tailgaters: maintaining emotional composure, signaling right 100 ft in advance (TTC &sect; 545.104) and smoothly yielding the passing lane, avoiding direct eye contact and provocative gestures, and restoring a safe 4-second following cushion (&gt; 250 ft). Includes critical hazard simulations for retaliatory brake-checking and competitive high-speed highway duels.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L07_T08_aggressive_driving_avoidance.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>De-escalation &bull; Buffer Defense</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
'''

    target_card = '<!-- LESSON 33 CARD -->'
    if target_card in c and 'LESSON 27 CARD' not in c:
        c = c.replace(target_card, l27_card + '\n        ' + target_card)

    # 3. Insert Table row
    l27_row = '''            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">27</td>
              <td class="py-2 px-4 mono font-bold text-white">L07-T08</td>
              <td class="py-2 px-4 font-medium text-blue-300">Aggressive Driving &amp; Road Rage Avoidance &mdash; De-escalation &amp; Yielding</td>
              <td class="py-2 px-4 mono text-blue-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">TTC &sect; 545.401 &amp; &sect; 545.062 &bull; Defensive De-escalation</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>\n'''

    if 'L07-T08</td>' not in c:
        idx = c.find('<td class="py-2 px-4 mono text-emerald-400 font-bold">33</td>')
        if idx != -1:
            tr_start = c.rfind('<tr', 0, idx)
            c = c[:tr_start] + l27_row + c[tr_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

    print('Successfully updated index.html with Lesson 27!')

if __name__ == '__main__':
    update_index()
