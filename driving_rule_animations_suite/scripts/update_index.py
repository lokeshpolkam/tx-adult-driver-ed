import os

index_path = r"c:\tx_dmv\driving_rule_animations_suite\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update counter
content = content.replace("24 of 33", "25 of 33", 1)

# Add Lesson 24 Card
lesson_24_card = """        <!-- LESSON 24 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-orange-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-orange-500/10 text-orange-400 border border-orange-500/20 mono">LESSON 24</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L05-T17: Construction &amp; Work Zone Safety &mdash; Automatic Doubled Fines &amp; Flaggers</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Transportation Code &sect; 542.404 &amp; &sect; 542.501</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates mandatory Texas work zone compliance: advance MUTCD W20-1 diamond warning recognition, early 100-ft continuous turn signaling, smooth 45 MPH merging along retroreflective channelizing barrel tapers, human flagger preemption under TTC &sect; 542.501 (STOP/SLOW paddles overruling roadside signs), safe buffer zones around active highway crews and utility trucks, and an alarming work zone speeding collision demo triggering mandatory automatic 2X fine doubling ($800+) under TTC &sect; 542.404.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L05_T17_work_zones.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-orange-600 hover:bg-orange-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Flaggers &bull; Doubled Fines (&sect; 542.404)</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>
"""

target_card = "        <!-- LESSON 33 CARD -->"
if target_card in content:
    content = content.replace(target_card, lesson_24_card + "\n" + target_card, 1)
    print("Inserted Lesson 24 card.")
else:
    print("Target card not found!")

# Add Lesson 24 Table Row
lesson_24_row = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">24</td>
              <td class="py-2 px-4 mono font-bold text-white">L05-T17</td>
              <td class="py-2 px-4 font-medium text-orange-300">Construction &amp; Work Zone Safety &mdash; Automatic Doubled Fines &amp; Flaggers</td>
              <td class="py-2 px-4 mono text-orange-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">Texas Transportation Code &sect; 542.404 &amp; &sect; 542.501</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
"""

target_row_33 = "mono text-emerald-400 font-bold\">33</td>"
# find the tr tag before this
idx = content.find(target_row_33)
if idx != -1:
    tr_idx = content.rfind("<tr", 0, idx)
    content = content[:tr_idx] + lesson_24_row + content[tr_idx:]
    print("Inserted Lesson 24 row.")
else:
    print("Row 33 not found!")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html updated successfully.")
