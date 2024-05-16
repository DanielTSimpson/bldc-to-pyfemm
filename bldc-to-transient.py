import femm as f

f.openfemm()
f.opendocument("temp.ans")

circ_props = ['Phase A', 'Phase B', 'Phase C']
print(f.mo_getcircuitproperties(circ_props[0]))

input(0)
