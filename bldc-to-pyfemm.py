# Main script for importing DXF files and getting torque values in FEMM
import femm

FILENAME = "36_38_20_122_0.9_2_1.5_3_10_3_0.75_3.dxf"
properties = FILENAME.split("_")
SLOTS = properties[0]
POLES = properties[1]
NUMBER_WINDINGS = properties[2]
STATOR_ID = properties[3]
WIRE_DIA = properties[4]
TOOTH_HEIGHT = properties[5]
TOOTH_OVERHANG = properties[6]
MAGNET_WIDTH = properties[7]
MAGNET_THK = properties[8]
MAGNET_STATOR_GAP = properties[9]
ROTOR_THK = properties[10]

femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0, 'millimeters', 'planar', 1E-8, 20, 20, 0)
femm.mi_readdxf("Input DXFs/" + FILENAME)
femm.mi_zoomnatural()

# femm.mi_addblocklabel(5,5)
# femm.mi_selectlabel(4,5)

input(0)
