import re

with open('src/App.jsx', 'r') as f:
    content = f.read()

# 1. Replace all standard "border border-neutral-800" with "border panel-glow"
content = content.replace('border border-neutral-800', 'border panel-glow')

# 2. Replace "border border-neutral-800/80" with "border panel-glow"
content = content.replace('border border-neutral-800/80', 'border panel-glow')

# 3. Add panel-glow-hover to specific interactive elements:
# Interactive history card
content = content.replace('className="bg-[#111] border panel-glow rounded-xl p-4 sm:p-5 shadow-sm"', 'className="bg-[#111] border panel-glow panel-glow-hover rounded-xl p-4 sm:p-5 shadow-sm"')

# Interactive docs item
content = content.replace('className="bg-[#111] border panel-glow rounded-lg p-3.5 shadow-sm flex items-center justify-between gap-3"', 'className="bg-[#111] border panel-glow panel-glow-hover rounded-lg p-3.5 shadow-sm flex items-center justify-between gap-3"')

# Inputs (Agent, Eval, Settings, Login) - they already have input-glow for focus, let's add panel-glow-hover to them too so they glow on hover.
content = content.replace('input-glow', 'input-glow panel-glow-hover')

with open('src/App.jsx', 'w') as f:
    f.write(content)

print("Done replacing glows in App.jsx")
