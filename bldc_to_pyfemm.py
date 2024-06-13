# Main script for importing DXF files and getting torque values in FEMM
import femm as f
import math

### Get program properties
config_file = open('config.txt')
params = config_file.read().split("\n")

AIR = params[0].split(',')[1][1:]
MAGNET = params[1].split(',')[1][1:]
ROTOR = params[2].split(',')[1][1:]
STATOR = params[3].split(',')[1][1:]
COIL = params[4].split(',')[1][1:]
PHASE_A = params[5].split(',')[1][1:]
PHASE_B = params[6].split(',')[1][1:]
PHASE_C = params[7].split(',')[1][1:]

### Get BLDC dimensions
FILENAME = "36_38_20_122_4_0.9_2_1.5_3_10_3_0.75_3_slidingband"
properties = FILENAME.split("_")

SLOTS = int(properties[0])
POLES = int(properties[1])
NUMBER_WINDINGS = int(properties[2])
STATOR_ID = float(properties[3])
STATOR_BASE = float(properties[4])
WIRE_DIA = float(properties[5])
TOOTH_HEIGHT = float(properties[6])
TOOTH_OVERHANG = float(properties[7])
TOOTH_WIDTH = float(properties[8])
MAGNET_WIDTH = float(properties[9])
MAGNET_THK = float(properties[10])
AIR_GAP = float(properties[11])
ROTOR_THK = float(properties[12])

### Name global params
circ_names = ['Phase A', 'Phase B', 'Phase C']
bc_properties = ['A = 0', 'slidingBand', 'periodic1', 'periodic2', 'periodic3', 'periodic4']

def circ_pattern(start_pos: list, angle: float, num_copies: int, direction: int, save_array: list = None):
    """
    Adds block labels in a circular pattern
    :param start_pos: a point [x,y] in space. [0,0] is the center of rotation
    :param angle: the angle between copies
    :param num_copies: the number of copies
    :param direction: the direction of the circular pattern. +1 for clockwise, -1 for counterclockwise
    :param save_array: optional list to save block label positions to
    :param start_angl: the starting angle for the circular pattern
    """
    radius = math.pow(math.pow(start_pos[0], 2) + math.pow(start_pos[1], 2), 0.5)
    phi_0 = math.acos(start_pos[0] / radius)
    for i in range(1, num_copies + 1):
        x = radius * math.cos(phi_0 + direction * i * angle)
        y = radius * math.sin(phi_0 + direction * i * angle)
        f.mi_addblocklabel(x, y)
        if save_array:
            save_array.append([x, y])

def setup_magnets(positions: list, magnet_angl: float):
    """
    Sets the direction of each rotor magnet
    :param positions: a list of magnet positions
    :param magnet_angl: the angle between rotor magnets
    :param start_angl: the starting angle for the pattern
    """
    for i in range(len(positions)):
        f.mi_selectlabel(positions[i][0], positions[i][1])
        phi = math.degrees(-math.atan(positions[i][0]/positions[i][1]))
        if i % 2 == 0:
            f.mi_setblockprop(MAGNET, 1, 0, '', 90 + phi)
        else:
            f.mi_setblockprop(MAGNET, 1, 0, '', -90 + phi)
        f.mi_clearselected()

def setup_coils(coilA_positions: list, coilB_positions: list, circ_prop: list):
    polarity = 0
    for i in range(len(coilA_positions)):
        if i % 4 == 0 or i % 4 == 3:
            polarity = 1
        elif i % 4 == 1 or i % 4 == 2:
            polarity = -1

        if i % 6 == 0 or i % 6 == 1:
            f.mi_selectlabel(coilA_positions[i][0], coilA_positions[i][1])
            f.mi_setblockprop(COIL, 1, 0, circ_prop[0], 0, 0, polarity * NUMBER_WINDINGS)
            f.mi_clearselected()
            f.mi_selectlabel(coilB_positions[i][0], coilB_positions[i][1])
            f.mi_setblockprop(COIL, 1, 0, circ_prop[0], 0, 0, -polarity * NUMBER_WINDINGS)
            f.mi_clearselected()
        elif i % 6 == 2 or i % 6 == 3:
            f.mi_selectlabel(coilA_positions[i][0], coilA_positions[i][1])
            f.mi_setblockprop(COIL, 1, 0, circ_prop[1], 0, 0, polarity * NUMBER_WINDINGS)
            f.mi_clearselected()
            f.mi_selectlabel(coilB_positions[i][0], coilB_positions[i][1])
            f.mi_setblockprop(COIL, 1, 0, circ_prop[1], 0, 0, -polarity * NUMBER_WINDINGS)
            f.mi_clearselected()
        elif i % 6 == 4 or i % 6 == 5:
            f.mi_selectlabel(coilA_positions[i][0], coilA_positions[i][1])
            f.mi_setblockprop(COIL, 1, 0, circ_prop[2], 0, 0, polarity * NUMBER_WINDINGS)
            f.mi_clearselected()
            f.mi_selectlabel(coilB_positions[i][0], coilB_positions[i][1])
            f.mi_setblockprop(COIL, 1, 0, circ_prop[2], 0, 0, -polarity * NUMBER_WINDINGS)
            f.mi_clearselected()

def setup_model():  
    # Initialize FEMM Magnetic Problem
    f.openfemm()
    print("Running...")
    f.newdocument(0)
    f.mi_probdef(0, 'millimeters', 'planar', 1E-8, 20, 18)
    f.mi_readdxf("Input DXFs/" + FILENAME + ".dxf")
    f.mi_zoomnatural()

    # Setup Materials
    f.mi_getmaterial(AIR)
    f.mi_getmaterial(MAGNET)
    f.mi_getmaterial(ROTOR)
    f.mi_getmaterial(STATOR)
    f.mi_getmaterial(COIL)

    f.mi_addcircprop(circ_names[0], PHASE_A, 1)
    f.mi_addcircprop(circ_names[1], PHASE_B, 1)
    f.mi_addcircprop(circ_names[2], PHASE_C, 1)

    # Setup Boundaries
    f.mi_addboundprop(bc_properties[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    f.mi_addboundprop(bc_properties[1], 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0)
    # note: additional periodic bcs are setup in setup_periodic_bcs()

def define_positions():
    # Define the position of the stator, rotor, magnet, and coils
    magnet_angle = 2 * math.pi / POLES
    slot_r = STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA / 2
    slot_angle = 2 * math.pi / SLOTS

    outer_air_position = [0, STATOR_ID - 1]
    stator_air_position = [0, STATOR_ID / 2 + STATOR_BASE + NUMBER_WINDINGS * WIRE_DIA + TOOTH_HEIGHT]
    rotor_air_position = [0, STATOR_ID / 2 + STATOR_BASE + NUMBER_WINDINGS * WIRE_DIA + TOOTH_HEIGHT + AIR_GAP]
    no_mesh_position = [0, STATOR_ID / 2 + STATOR_BASE + NUMBER_WINDINGS * WIRE_DIA + TOOTH_HEIGHT + AIR_GAP / 2]
    
    stator_position = [0, STATOR_ID / 2 + STATOR_BASE / 2]
    rotor_position = [0, STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + AIR_GAP + MAGNET_THK + ROTOR_THK / 2]

    r_magnet = STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + AIR_GAP + MAGNET_THK / 2
    phi0_magnet = -3*magnet_angle*0
    magnet_positions = [[r_magnet * math.sin(phi0_magnet), r_magnet * math.cos(phi0_magnet)]]
    
    slot_position = [-slot_r * math.sin(5 * slot_angle / 2), slot_r * math.cos(5 * slot_angle / 2)]
    coil1_positions = [[slot_position[0] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(5 * slot_angle / 2),
                        slot_position[1] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(5 * slot_angle / 2)]]
    coil2_positions = [[slot_position[0] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(5 * slot_angle / 2),
                        slot_position[1] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(5 * slot_angle / 2)]]
    return outer_air_position, rotor_air_position, stator_air_position, no_mesh_position, stator_position, rotor_position, magnet_angle, magnet_positions, slot_angle, coil1_positions, coil2_positions
    
def setup_positions():
    # Add air position & set material
    f.mi_addblocklabel(outer_air_position[0], outer_air_position[1])
    f.mi_addblocklabel(rotor_air_position[0], rotor_air_position[1])
    f.mi_addblocklabel(stator_air_position[0], stator_air_position[1])
    f.mi_selectlabel(outer_air_position[0], outer_air_position[1])
    f.mi_selectlabel(rotor_air_position[0], rotor_air_position[1])
    f.mi_selectlabel(stator_air_position[0], stator_air_position[1])
    f.mi_setblockprop(AIR)
    f.mi_clearselected()

    # Add outer perimeter boundary condition
    f.mi_selectarcsegment(outer_air_position[0], outer_air_position[1])
    f.mi_selectarcsegment(outer_air_position[0], -outer_air_position[1])
    f.mi_setarcsegmentprop(0, bc_properties[0], 0, 0)
    f.mi_clearselected()

    # Add sliding band boundary condition
    f.mi_selectarcsegment(rotor_air_position[0], rotor_air_position[1]+1)
    f.mi_selectarcsegment(rotor_air_position[0], rotor_air_position[1]-1)
    f.mi_setarcsegmentprop(0, bc_properties[1], 0, 0)
    f.mi_clearselected()

    f.mi_selectarcsegment(rotor_air_position[0], -rotor_air_position[1]+1)
    f.mi_selectarcsegment(rotor_air_position[0], -rotor_air_position[1]-1)
    f.mi_setarcsegmentprop(0, bc_properties[1], 0, 0)
    f.mi_clearselected()

    # Add & set no mesh zone
    f.mi_addblocklabel(no_mesh_position[0], no_mesh_position[1])
    f.mi_selectlabel(no_mesh_position[0], no_mesh_position[1])
    f.mi_setblockprop("<No Mesh>")
    f.mi_clearselected()

    # Add stator base position and modify & set materials
    f.mi_addblocklabel(stator_position[0], stator_position[1])
    f.mi_modifymaterial(STATOR, 9, 0)  # Set lamination in plane
    f.mi_modifymaterial(STATOR, 8, 0.98)  # Set lamination fill fraction
    f.mi_modifymaterial(STATOR, 6, 0.635)  # Set lamination thickness
    f.mi_selectlabel(stator_position[0], stator_position[1])
    f.mi_setblockprop(STATOR)
    f.mi_clearselected()

    # Add rotor positions & set materials
    f.mi_addblocklabel(rotor_position[0], rotor_position[1])
    f.mi_selectlabel(rotor_position[0], rotor_position[1])
    f.mi_setblockprop(ROTOR)
    f.mi_clearselected()

    # Add magnet positions
    f.mi_addblocklabel(magnet_positions[0][0], magnet_positions[0][1])
    circ_pattern([magnet_positions[0][0], magnet_positions[0][1]], magnet_angle, 38, -1, magnet_positions)
    setup_magnets(magnet_positions, magnet_angle)

    # Add coil1 positions
    f.mi_addblocklabel(coil1_positions[0][0], coil1_positions[0][1])
    circ_pattern([coil1_positions[0][0], coil1_positions[0][1]], slot_angle, 5, -1, coil1_positions)

    # Add coil2 positions
    f.mi_addblocklabel(coil2_positions[0][0], coil2_positions[0][1])
    circ_pattern([coil2_positions[0][0], coil2_positions[0][1]], slot_angle, 5, -1, coil2_positions)

    # Set up the coils
    setup_coils(coil1_positions, coil2_positions, circ_names)
    return magnet_positions, rotor_position

def setup_periodic_bcs():
    # Establish Periodic BCs
    f.mi_addboundprop(bc_properties[2], 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0)
    f.mi_addboundprop(bc_properties[3], 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0)
    f.mi_addboundprop(bc_properties[4], 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0)
    f.mi_addboundprop(bc_properties[5], 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0)
    
    partl_angl = 3.5*magnet_angle

    # Setup periodic boundary condition 1
    f.mi_selectsegment(stator_air_position[0] - stator_air_position[1] * math.sin(partl_angl), stator_air_position[1] * math.cos(partl_angl))
    f.mi_selectsegment(stator_air_position[0] + stator_air_position[1] * math.sin(partl_angl), stator_air_position[1] * math.cos(partl_angl))
    f.mi_setsegmentprop(bc_properties[2], 0, 0, 0, 0)
    f.mi_clearselected()

    # Setup periodic boundary condition 2
    f.mi_selectsegment(rotor_air_position[0] - rotor_air_position[1] * math.sin(partl_angl), rotor_air_position[1] * math.cos(partl_angl))
    f.mi_selectsegment(rotor_air_position[0] + rotor_air_position[1] * math.sin(partl_angl), rotor_air_position[1] * math.cos(partl_angl))
    f.mi_setsegmentprop(bc_properties[3], 0, 0, 0, 0)
    f.mi_clearselected()

    # Setup periodic boundary condition 3
    f.mi_selectsegment(rotor_position[0] - rotor_position[1] * math.sin(partl_angl), rotor_position[1] * math.cos(partl_angl))
    f.mi_selectsegment(rotor_position[0] + rotor_position[1] * math.sin(partl_angl), rotor_position[1] * math.cos(partl_angl))
    f.mi_setsegmentprop(bc_properties[4], 0, 0, 0, 0)
    f.mi_clearselected()

    # Setup periodic boundary condition 4
    f.mi_selectsegment(outer_air_position[0] - outer_air_position[1] * math.sin(partl_angl), outer_air_position[1] * math.cos(partl_angl))
    f.mi_selectsegment(outer_air_position[0] + outer_air_position[1] * math.sin(partl_angl), outer_air_position[1] * math.cos(partl_angl))
    f.mi_setsegmentprop(bc_properties[5], 0, 0, 0, 0)
    f.mi_clearselected()

#Set up the model
setup_model()
outer_air_position, rotor_air_position, stator_air_position, no_mesh_position, stator_position, rotor_position, magnet_angle, magnet_positions, slot_angle, coil1_positions, coil2_positions = define_positions()
setup_positions()
#setup_periodic_bcs()

# Run the simulation    
f.mi_saveas('temp.fem')
f.mi_analyze()
f.mi_loadsolution()

# Setup post processor
f.mo_hidecontourplot()
f.mo_zoom(-STATOR_ID, -STATOR_ID, STATOR_ID, STATOR_ID)
f.mo_showdensityplot(1, 0, 2, 0, 'bmag')

#Select blocks for Torque
f.mo_selectblock(rotor_position[0], rotor_position[1])
for j in range(len(magnet_positions)):
    f.mo_selectblock(magnet_positions[j][0], magnet_positions[j][1])
torque = f.mo_blockintegral(22)
print("Torque is {:2.4f} N-m ".format(torque)) 
f.mo_clearblock()
#print("for {:.1f} degrees\n".format(i))
input(0)
f.mo_close()
f.mi_close()