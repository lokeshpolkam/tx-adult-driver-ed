with open('driving_rule_animations_suite/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update counter
c = c.replace('<span class="text-emerald-400 font-bold text-sm">18 of 33</span>', '<span class="text-emerald-400 font-bold text-sm">19 of 33</span>')

# 2. Add Lesson 18 Card after Lesson 17 Card
target_card = '<!-- LESSON 33 CARD -->'
l18_card = '''        <!-- LESSON 18 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-emerald-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mono">LESSON 18</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L05-T10: Vehicle Lights &mdash; High Beam Dimming &amp; Sight Distance</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Driver Handbook Ch. 5 &bull; Texas Transportation Code &sect; 547.333</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates mandatory statutory headlight dimming rules: switching to low beams within 500 feet of an oncoming vehicle (TTC &sect; 547.333(c)(1)) and within 300 feet when following another vehicle from behind (&sect; 547.333(c)(2)). Features dynamic SVG beam polygons, night illumination envelopes (500 FT high beam vs. 180 FT low beam), mirror reflection glare vectors, and a critical hazard simulation of 50,000+ candela retinal flash blindness causing involuntary centerline drift.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L05_T10_vehicle_lights.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>High Beam Dimming &bull; Glare Hazards</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
'''

if '<!-- LESSON 18 CARD -->' not in c:
    c = c.replace(target_card, l18_card + target_card)

# 3. Add table row 18
target_tr = '<tr class="hover:bg-[#181F2B] bg-emerald-500/5">\n              <td class="py-2 px-4 mono text-emerald-400 font-bold">33</td>'
row_18 = '''            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">18</td>
              <td class="py-2 px-4 mono font-bold text-white">L05-T10</td>
              <td class="py-2 px-4 font-medium text-emerald-300">Vehicle Lights &mdash; High Beam Dimming (500 FT / 300 FT Rules)</td>
              <td class="py-2 px-4 mono text-emerald-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 547.333</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
'''

if 'L05-T10</td>' not in c:
    c = c.replace(target_tr, row_18 + target_tr)

with open('driving_rule_animations_suite/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Dashboard updated for Lesson 18!')
