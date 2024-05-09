# Main script for importing DXF files and getting torque values in FEMM
import femm
femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0,'millimeters','planar',1E-8,20,20,(0))
femm.mi_drawrectangle(0,0,10,10)
femm.mi_addblocklabel(5,5)
femm.mi_selectlabel(4,5)
input(0)

