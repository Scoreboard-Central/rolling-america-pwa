import re

with open('make_map.py', 'r') as f: code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

H, W = len(grid), max(len(r) for r in grid)
for i in range(H):
    grid[i].extend(['..'] * (W - len(grid[i])))

# R03: NY(24) NY(25) VT(26) VT(27) NH(28) NH(29) NH(30) NH(31)
grid[3][24] = 'NY'; grid[3][25] = 'NY'; grid[3][26] = 'VT'; grid[3][27] = 'VT'
grid[3][28] = 'NH'; grid[3][29] = 'NH'; grid[3][30] = 'NH'; grid[3][31] = 'NH'

# R04: NY(24) NY(25) VT(26) MA(27) MA(28) MA(29) MA(30) RI(31)
grid[4][24] = 'NY'; grid[4][25] = 'NY'; grid[4][26] = 'VT'; grid[4][27] = 'MA'
grid[4][28] = 'MA'; grid[4][29] = 'MA'; grid[4][30] = 'MA'; grid[4][31] = 'RI'

# R05: PA(23) PA(24) NY(25) NY(26) NY(27) CT(28) CT(29) CT(30) RI(31)
grid[5][23] = 'PA'; grid[5][24] = 'PA'; grid[5][25] = 'NY'; grid[5][26] = 'NY'; grid[5][27] = 'NY'
grid[5][28] = 'CT'; grid[5][29] = 'CT'; grid[5][30] = 'CT'; grid[5][31] = 'RI'

# R06: NE(16) NE(17) MO(18) IL(19) IN(20) OH(21) OH(22) PA(23) PA(24) NJ(25) DE(26) DE(27) DE(28) DE(29) .. ..
grid[6][18] = 'MO'; grid[6][19] = 'IL'; grid[6][20] = 'IN'; grid[6][21] = 'OH'; grid[6][22] = 'OH'
grid[6][23] = 'PA'; grid[6][24] = 'PA'; grid[6][25] = 'NJ'; grid[6][26] = 'DE'; grid[6][27] = 'DE'; grid[6][28] = 'DE'; grid[6][29] = 'DE'

# R07: KS(16) KS(17) MO(18) IL(19) KY(20) OH(21) OH(22) WV(23) PA(24) PA(25) PA(26) DE(27) DE(28) DE(29)
grid[7][16] = 'KS'; grid[7][17] = 'KS'; grid[7][18] = 'MO'; grid[7][19] = 'IL'; grid[7][20] = 'KY'
grid[7][21] = 'OH'; grid[7][22] = 'OH'; grid[7][23] = 'WV'; grid[7][24] = 'PA'; grid[7][25] = 'PA'
grid[7][26] = 'PA'; grid[7][27] = 'DE'; grid[7][28] = 'DE'; grid[7][29] = 'DE'

# R08: CO(15) KS(16) KS(17) MO(18) MO(19) KY(20) KY(21) KY(22) WV(23) WV(24) WV(25) MD(26) MD(27) MD(28)
grid[8][15] = 'CO'; grid[8][16] = 'KS'; grid[8][17] = 'KS'; grid[8][18] = 'MO'; grid[8][19] = 'MO'
grid[8][20] = 'KY'; grid[8][21] = 'KY'; grid[8][22] = 'KY'; grid[8][23] = 'WV'; grid[8][24] = 'WV'
grid[8][25] = 'WV'; grid[8][26] = 'MD'; grid[8][27] = 'MD'; grid[8][28] = 'MD'

# R09: OK(16) OK(17) MO(18) MO(19) KY(20) KY(21) VA(22) VA(23) VA(24) VA(25) VA(26) MD(27) .. ..
grid[9][16] = 'OK'; grid[9][17] = 'OK'; grid[9][18] = 'MO'; grid[9][19] = 'MO'; grid[9][20] = 'KY'
grid[9][21] = 'KY'; grid[9][22] = 'VA'; grid[9][23] = 'VA'; grid[9][24] = 'VA'; grid[9][25] = 'VA'
grid[9][26] = 'VA'; grid[9][27] = 'MD'; grid[9][28] = '..'; grid[9][29] = '..'

# R10: TX(15) TX(16) OK(17) OK(18) MO(19) TN(20) TN(21) TN(22) TN(23) TN(24) NC(25) NC(26) NC(27) NC(28) NC(29)
grid[10][15] = 'TX'; grid[10][16] = 'TX'; grid[10][17] = 'OK'; grid[10][18] = 'OK'; grid[10][19] = 'MO'
grid[10][20] = 'TN'; grid[10][21] = 'TN'; grid[10][22] = 'TN'; grid[10][23] = 'TN'; grid[10][24] = 'TN'
grid[10][25] = 'NC'; grid[10][26] = 'NC'; grid[10][27] = 'NC'; grid[10][28] = 'NC'; grid[10][29] = 'NC'
grid[10][30] = '..'

# R11: TX(15) TX(16) TX(17) AR(18) AR(19) AR(20) MS(21) MS(22) AL(23) GA(24) GA(25) GA(26) SC(27) SC(28) SC(29)
grid[11][15] = 'TX'; grid[11][16] = 'TX'; grid[11][17] = 'TX'; grid[11][18] = 'AR'; grid[11][19] = 'AR'
grid[11][20] = 'AR'; grid[11][21] = 'MS'; grid[11][22] = 'MS'; grid[11][23] = 'AL'; grid[11][24] = 'GA'
grid[11][25] = 'GA'; grid[11][26] = 'GA'; grid[11][27] = 'SC'; grid[11][28] = 'SC'; grid[11][29] = 'SC'
grid[11][30] = '..'

# R12: TX(15) TX(16) TX(17) TX(18) LA(19) LA(20) MS(21) MS(22) AL(23) AL(24) ..
grid[12][15] = 'TX'; grid[12][16] = 'TX'; grid[12][17] = 'TX'; grid[12][18] = 'TX'; grid[12][19] = 'LA'
grid[12][20] = 'LA'; grid[12][21] = 'MS'; grid[12][22] = 'MS'; grid[12][23] = 'AL'; grid[12][24] = 'AL'

joined = ",\n    ".join('"' + " ".join(r) + '"' for r in grid)
new_code = code[:m.start(1)] + "\n    " + joined + "\n" + code[m.end(1):]
with open('make_map.py', 'w') as f: f.write(new_code)
print("Finished patching everything!")
