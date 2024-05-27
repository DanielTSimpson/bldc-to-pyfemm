import femm as f

f.openfemm()
f.opendocument("StatorTestFEMM.fem")
input(0)

circ_props = ['Phase A', 'Phase B', 'Phase C']
print(f.mo_getcircuitproperties(circ_props[0]))
print(f.mo_getcircuitproperties(circ_props[1]))
print(f.mo_getcircuitproperties(circ_props[2]))

input(0)
