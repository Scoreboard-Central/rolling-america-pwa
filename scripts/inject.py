import re

with open('generated_map.html', 'r') as f: new_svg = f.read()

# Add standard tailwind classes and viewBox
# width is W * SIZE = 96 * 12 = 1152
# height is H * SIZE = 48 * 12 = 576
new_svg = new_svg.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg xmlns="http://www.w3.org/2000/svg" class="w-full h-full max-h-full" viewBox="0 0 1152 576"')

with open('../src/app/app.component.html', 'r') as f: html = f.read()

replacement = f"""    <!-- MAP AREA (Main Focus) -->
    <div class="flex-grow flex flex-col justify-center items-center p-1 sm:p-2 lg:p-4 min-w-0 bg-white relative">
      <!-- Title (Centered) -->
      <div class="flex flex-col items-center text-center w-full mb-[-5px] sm:mb-[-15px] z-10">
        <h1
          class="text-lg sm:text-2xl lg:text-4xl font-bold tracking-widest text-[#414E69] mb-0 font-['Century_Gothic'] leading-tight">
          ROLLING AMERICA</h1>
      </div>

{new_svg}

      <!-- Reset Button -->
      <button
        class="absolute bottom-2 left-2 sm:bottom-4 sm:left-4 p-2 text-slate-400 hover:text-slate-700 transition-colors"
        (click)="openResetModal()" title="Reset Game">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor"
          class="w-6 h-6 sm:w-8 sm:h-8">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
        </svg>
      </button>
    </div>

    <!-- RIGHT SIDEBAR -->"""

html = re.sub(r'<!-- MAP AREA \(Main Focus\) -->.*?<!-- RIGHT SIDEBAR -->', replacement, html, flags=re.DOTALL)
with open('../src/app/app.component.html', 'w') as f: f.write(html)
print("Injected map and removed duplicates!")
