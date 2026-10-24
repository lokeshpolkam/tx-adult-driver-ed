index_path = r"c:\tx_dmv\driving_rule_animations_suite\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update counter
content = content.replace("25 of 33", "26 of 33", 1)

# Add Lesson 25 Card
lesson_25_card = """        <!-- LESSON 25 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-blue-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 mono">LESSON 25</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L07-T03: Laws for Sharing the Road &mdash; Commercial Trucks &amp; The 4 No-Zones</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Driver Handbook Ch. 7 &bull; TTC &sect; 545.062 &amp; &sect; 545.054 &amp; &sect; 545.101</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates critical commercial motor vehicle (CMV) safety protocols: identifying the 4 No-Zones (Front 20 ft, Rear 200 ft, Left 1 lane, and treacherous Right 2 lanes), lawful passing and inside rearview mirror confirmation of the entire truck cab before return under TTC &sect; 545.054, kinetic stopping distance disparities between an 80,000 lb semi (400+ ft) and a sedan (190 ft) under TTC &sect; 545.062, and a catastrophic &quot;Right-Turn Squeeze&quot; collision simulation from trailer off-tracking under TTC &sect; 545.101.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L07_T03_commercial_vehicles.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>4 No-Zones &bull; Right-Turn Squeeze</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
"""

target_card = "        <!-- LESSON 33 CARD -->"
if target_card in content:
    content = content.replace(target_card, lesson_25_card + "\n" + target_card, 1)
    print("Inserted Lesson 25 card.")
else:
    print("Target card not found!")

# Add Lesson 25 Table Row
lesson_25_row = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">25</td>
              <td class="py-2 px-4 mono font-bold text-white">L07-T03</td>
              <td class="py-2 px-4 font-medium text-blue-300">Laws for Sharing the Road &mdash; Commercial Trucks &amp; The 4 No-Zones</td>
              <td class="py-2 px-4 mono text-blue-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Driver Handbook Ch. 7 &bull; TTC &sect; 545.062 &amp; &sect; 545.054</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
"""

target_row_33 = "mono text-emerald-400 font-bold\">33</td>"
idx = content.find(target_row_33)
if idx != -1:
    tr_idx = content.rfind("<tr", 0, idx)
    content = content[:tr_idx] + lesson_25_row + content[tr_idx:]
    print("Inserted Lesson 25 row.")
else:
    print("Row 33 not found!")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html updated successfully.")
