import femm as f
import numpy as np
import bldc_to_pyfemm
rotor_position = bldc_to_pyfemm.rotor_position
magnet_positions = bldc_to_pyfemm.magnet_positions

dt = 0.1
t = [round(dt * x,  3) for x in range(0, int(10/dt) + 1)]
torque = np.array(0)
omega = 2000
theta_0 = 0
v_0 = [8, 0, 0]
R = 0.08469183967160236 * np.identity(3)

f.openfemm()
f.opendocument("StatorFEMM.fem")
circ_props = ['Phase A', 'Phase B', 'Phase C']

L =  np.zeros((3,3))
k = np.zeros((3,1))

torque[0] = f.mo_gapintegral("slidingBand",0)

for n in [1,2,3]: 
    f.mi_modifycircprop(circ_props[0],1, 3 - 2.5*n + 0.5*n*n)
    f.mi_modifycircprop(circ_props[1],1,-3 + 4*n - n*n)
    f.mi_modifycircprop(circ_props[2],1, 1 - 1.5*n + 0.5*n*n)
    f.mi_analyze()
    f.mi_loadsolution()
    f.mo_hidecontourplot()

    f.mo_selectblock(rotor_position[0], rotor_position[1])
    for j in range(len(magnet_positions)):
        f.mo_selectblock(magnet_positions[j][0], magnet_positions[j][1])

    k[n - 1, 0] = f.mo_blockintegral(22)
    f.mo_clearblock()
    L[n - 1, 0] = f.mo_getcircuitproperties(circ_props[0])[2]
    L[n - 1, 1] = f.mo_getcircuitproperties(circ_props[1])[2]
    L[n - 1, 2] = f.mo_getcircuitproperties(circ_props[2])[2]    
f.mo_close()    

print(L)
print(k)
print(torque)
#dxdt = L\(v_0 - omega*k' - R*x)

#f.mi_setcurrent(circ_props[0], 1)
#f.mi_setcurrent(circ_props[1], 0)
#f.mi_setcurrent(circ_props[2], 0)

input(0)
