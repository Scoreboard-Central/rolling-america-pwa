import re

with open("src/app/app.component.html", "r") as f:
    html = f.read()

with open("generated_map.html", "r") as f:
    svg_map = f.read().strip()
    svg_map = svg_map.replace("\\'", "'")
    svg_map = re.sub(r'<svg.*?>', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 748 408" class="w-full h-full max-h-full">', svg_map)

# Extract Modal
modal_match = re.search(r'<!-- Input Modal \(Overlay\) -->.*', html, re.DOTALL)
modal_html = modal_match.group(0) if modal_match else ""

# Layout
new_html = """<div class="wave-bg h-[100dvh] w-screen overflow-hidden flex flex-row items-center justify-center sm:p-2">
  <div class="w-full h-full flex flex-row bg-white overflow-hidden shadow-2xl sm:border-2 border-slate-300">
    
    <!-- LEFT SIDEBAR -->
    <div class="w-[100px] sm:w-[150px] lg:w-[15%] h-full flex flex-col items-center justify-around px-1 py-4 bg-slate-50 border-r-2 border-slate-200 flex-shrink-0 z-10">
      
      <!-- Title -->
      <div class="flex flex-col items-center text-center px-1">
        <h1 class="text-xs sm:text-base lg:text-xl font-bold tracking-widest text-[#414E69] mb-1 font-['Century_Gothic'] leading-tight">ROLLING<br>AMERICA<sup class="text-[8px] font-normal">&trade;</sup></h1>
      </div>

      <!-- Round -->
      <div class="flex flex-col items-center text-center mt-2">
        <span class="text-slate-500 font-bold tracking-wide text-[9px] mb-1">ROUND</span>
        <div class="flex flex-wrap justify-center border-[2px] border-slate-600 rounded-sm overflow-hidden bg-white w-[50px] sm:w-[65px] lg:w-[90px]">
            @for (r of [1,2,3,4,5,6,7,8]; track r) {
            <div class="w-[20px] h-[20px] sm:w-[30px] sm:h-[30px] lg:w-[40px] lg:h-[40px] flex items-center justify-center border-r-[1px] border-b-[1px] border-slate-600 font-bold text-slate-700 text-[10px] sm:text-sm">
              {{r}}
            </div>
            }
        </div>
      </div>

      <!-- Abilities -->
      <div class="flex flex-col gap-3 sm:gap-6 mt-4">
        <!-- Color Change -->
        <div class="flex flex-col items-center">
          <span class="text-[8px] sm:text-[10px] font-bold text-slate-600 tracking-wide mb-1 lowercase text-center">color change</span>
          <div class="flex gap-0.5 border-[2px] border-slate-600 rounded-sm p-0.5 bg-white">
            @for (i of [1,2,3]; track i) {
            <button class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 border border-slate-400 flex items-center justify-center font-bold text-xs sm:text-sm outline-none hover:bg-slate-100 transition-colors" (click)="openModal('ability', 'colorChange', i-1)">{{ abilities.colorChange[i-1] }}</button>
            }
          </div>
        </div>
        <!-- Guard -->
        <div class="flex flex-col items-center">
          <span class="text-[8px] sm:text-[10px] font-bold text-slate-600 tracking-wide mb-1 lowercase text-center">guard</span>
          <div class="flex gap-0.5 border-[2px] border-slate-600 rounded-sm p-0.5 bg-white">
            @for (i of [1,2,3]; track i) {
            <button class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 border border-slate-400 flex items-center justify-center font-bold text-xs sm:text-sm outline-none hover:bg-slate-100 transition-colors" (click)="openModal('ability', 'guard', i-1)">{{ abilities.guard[i-1] }}</button>
            }
          </div>
        </div>
        <!-- Dupe -->
        <div class="flex flex-col items-center">
          <span class="text-[8px] sm:text-[10px] font-bold text-slate-600 tracking-wide mb-1 lowercase text-center">dupe</span>
          <div class="flex gap-0.5 border-[2px] border-slate-600 rounded-sm p-0.5 bg-white">
            @for (i of [1,2,3]; track i) {
            <button class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8 border border-slate-400 flex items-center justify-center font-bold text-xs sm:text-sm outline-none hover:bg-slate-100 transition-colors" (click)="openModal('ability', 'dupe', i-1)">{{ abilities.dupe[i-1] }}</button>
            }
          </div>
        </div>
      </div>
    </div>

    <!-- MAP AREA (Main Focus) -->
    <div class="flex-grow flex justify-center items-center p-2 sm:p-6 lg:p-12 min-w-0 bg-white">
       __MAP_PLACEHOLDER__
    </div>

    <!-- RIGHT SIDEBAR -->
    <div class="w-[80px] sm:w-[120px] lg:w-[15%] h-full flex flex-col items-center justify-center p-2 bg-slate-50 border-l-2 border-slate-200 flex-shrink-0 z-10">
      <!-- Xs -->
      <div class="flex flex-col items-center">
        <span class="text-[9px] sm:text-[11px] font-bold text-slate-600 tracking-wide mb-2 text-center lowercase">number of <br>Xs</span>
        <button
          class="w-12 h-12 sm:w-16 sm:h-16 lg:w-20 lg:h-20 border-[2px] border-slate-600 flex items-center justify-center font-bold text-2xl sm:text-3xl lg:text-5xl text-slate-800 outline-none hover:bg-slate-100 transition-colors bg-white shadow-sm"
          (click)="openModal('xs', 'xs')">{{ xs }}</button>
      </div>
    </div>

  </div>

  __MODAL_PLACEHOLDER__
</div>
"""

new_html = new_html.replace("__MAP_PLACEHOLDER__", svg_map)
new_html = new_html.replace("__MODAL_PLACEHOLDER__", modal_html)

with open("src/app/app.component.html", "w") as f:
    f.write(new_html)

print("HTML Structure rewritten for side-bars and map focus.")
