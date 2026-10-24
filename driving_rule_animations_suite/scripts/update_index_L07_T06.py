import re

def update_index():
    index_path = r"c:\tx_dmv\driving_rule_animations_suite\index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update counter
    content = content.replace("26 of 33", "27 of 33")

    # Add Lesson 26 Card before Lesson 33 Card
    lesson_26_card = """        <!-- LESSON 26 CARD -->
        <div class="rounded-xl bg-[#131720] border border-[#252E3C] p-5 flex flex-col justify-between hover:border-blue-500/50 transition shadow-lg">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 mono">LESSON 26</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-black mono">APPROVED &bull; 100%</span>
            </div>
            <div>
              <h3 class="text-sm font-bold text-white">L07-T06: Responsibilities If Stopped by Law Enforcement</h3>
              <p class="text-xs text-gray-400 mt-1">Texas Community Safety Education Act (Senate Bill 30) &bull; TTC &sect; 545.421 &amp; &sect; 543.005</p>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">
              Demonstrates lawful traffic stop procedures established under the Texas Community Safety Education Act (Senate Bill 30): acknowledging patrol cruiser emergency lights with right turn signal, slowing and safely pulling to the right emergency shoulder, shifting to PARK and setting emergency brake, turning on interior dome light at night, keeping hands visible on steering wheel (10 &amp; 2), verbal notice before reaching for credentials, Texas DPS 2-foot tactical fender offset corridor, statutory Notice to Appear signing compliance under TTC &sect; 543.005, and hazard simulation of abrupt active travel lane halts and furtive movements.
            </p>
          </div>

          <div class="pt-4 mt-4 border-t border-[#1F2633] space-y-2">
            <a href="simulations/L07_T06_police_traffic_stop.html" target="_blank" class="w-full py-2 px-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow transition">
              <span>Launch 60 FPS Simulation &rarr;</span>
            </a>
            <div class="flex justify-between text-[11px] text-gray-400 mono pt-1">
              <span>Senate Bill 30 &bull; Tactical Offset</span>
              <span class="text-emerald-400">Verified</span>
            </div>
          </div>
        </div>

"""
    content = content.replace("<!-- LESSON 33 CARD -->", lesson_26_card + "        <!-- LESSON 33 CARD -->")

    # Add Lesson 26 Table Row before Lesson 33 Table Row
    lesson_26_row = """            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">
              <td class="py-2 px-4 mono text-emerald-400 font-bold">26</td>
              <td class="py-2 px-4 mono font-bold text-white">L07-T06</td>
              <td class="py-2 px-4 font-medium text-blue-300">Responsibilities If Stopped by Law Enforcement &mdash; SB 30 Protocols</td>
              <td class="py-2 px-4 mono text-blue-400">RULE_DEMO</td>
              <td class="py-2 px-4 text-gray-400">TTC &sect; 545.421 &amp; &sect; 543.005 &bull; Senate Bill 30</td>
              <td class="py-2 px-4 text-right mono text-emerald-400 font-semibold">Verified &bull; Ready</td>
            </tr>
"""
    content = content.replace('<tr class="hover:bg-[#181F2B] bg-emerald-500/5">\n              <td class="py-2 px-4 mono text-emerald-400 font-bold">33</td>',
                            lesson_26_row + '            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">\n              <td class="py-2 px-4 mono text-emerald-400 font-bold">33</td>')

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("index.html updated successfully to 27 of 33.")

if __name__ == "__main__":
    update_index()
