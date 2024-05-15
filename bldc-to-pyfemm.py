# Main script for importing DXF files and getting torque values in FEMM
import femm
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
FILENAME = "36_38_20_122_4_0.9_2_1.5_3_10_3_0.75_3"
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
MAGNET_STATOR_GAP = float(properties[11])
ROTOR_THK = float(properties[12])


def circ_pattern(start_pos: list, angle: float, num_copies: int, direction: int, save_array: list = None):
    """
    Adds block labels in a circular pattern
    :param start_pos: a point [x,y] in space. [0,0] is the center of rotation
    :param angle: the angle between copies
    :param num_copies: the number of copies
    :param direction: the direction of the circular pattern. +1 for clockwise, -1 for counterclockwise
    :param save_array: optional list to save block label positions to
    """
    radius = math.pow(math.pow(start_pos[0], 2) + math.pow(start_pos[1], 2), 0.5)
    phi_0 = math.acos(start_pos[0] / radius)
    for i in range(1, num_copies + 1):
        x = radius * math.cos(phi_0 + direction * i * angle)
        y = radius * math.sin(phi_0 + direction * i * angle)
        femm.mi_addblocklabel(x, y)
        if save_array:
            save_array.append([x, y])


def setup_magnets(positions: list, magnet_angl: float):
    for i in range(len(positions)):
        femm.mi_selectlabel(positions[i][0], positions[i][1])
        if i % 2 == 0:
            femm.mi_setblockprop(MAGNET, 1, 0, '', 90 + i * (magnet_angl * 180 / math.pi))
        else:
            femm.mi_setblockprop(MAGNET, 1, 0, '', 270 + i * (magnet_angl * 180 / math.pi))
        femm.mi_clearselected()


def setup_coils(coilA_positions: list, coilB_positions: list, circ_prop: list):
    polarity = 0
    for i in range(len(coilA_positions)):
        if i % 4 == 0 or i % 4 == 3:
            polarity = 1
        elif i % 4 == 1 or i % 4 == 2:
            polarity = -1

        if i % 6 == 0 or i % 6 == 1:
            femm.mi_selectlabel(coilA_positions[i][0], coilA_positions[i][1])
            femm.mi_setblockprop(COIL, 1, 0, circ_prop[0], 0, 0, polarity*NUMBER_WINDINGS)
            femm.mi_clearselected()
            femm.mi_selectlabel(coilB_positions[i][0], coilB_positions[i][1])
            femm.mi_setblockprop(COIL, 1, 0, circ_prop[0], 0, 0, -polarity*NUMBER_WINDINGS)
            femm.mi_clearselected()
        elif i % 6 == 2 or i % 6 == 3:
            femm.mi_selectlabel(coilA_positions[i][0], coilA_positions[i][1])
            femm.mi_setblockprop(COIL, 1, 0, circ_prop[1], 0, 0, polarity*NUMBER_WINDINGS)
            femm.mi_clearselected()
            femm.mi_selectlabel(coilB_positions[i][0], coilB_positions[i][1])
            femm.mi_setblockprop(COIL, 1, 0, circ_prop[1], 0, 0, -polarity*NUMBER_WINDINGS)
            femm.mi_clearselected()
        elif i % 6 == 4 or i % 6 == 5:
            femm.mi_selectlabel(coilA_positions[i][0], coilA_positions[i][1])
            femm.mi_setblockprop(COIL, 1, 0, circ_prop[2], 0, 0, polarity*NUMBER_WINDINGS)
            femm.mi_clearselected()
            femm.mi_selectlabel(coilB_positions[i][0], coilB_positions[i][1])
            femm.mi_setblockprop(COIL, 1, 0, circ_prop[2], 0, 0, -polarity*NUMBER_WINDINGS)
            femm.mi_clearselected()


# Initialize FEMM Magnetic Problem
femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0, 'millimeters', 'planar', 1E-8, 20, 30)
femm.mi_readdxf("Input DXFs/" + FILENAME + ".dxf")
femm.mi_zoomnatural()

# Setup Materials
femm.mi_getmaterial(AIR)
femm.mi_getmaterial(MAGNET)
femm.mi_getmaterial(ROTOR)
femm.mi_getmaterial(STATOR)
femm.mi_getmaterial(COIL)
circ_props = ['Phase A', 'Phase B', 'Phase C']
femm.mi_addcircprop(circ_props[0], PHASE_A, 1)
femm.mi_addcircprop(circ_props[1], PHASE_B, 1)
femm.mi_addcircprop(circ_props[2], PHASE_C, 1)

# Setup Boundaries
bc_properties = ['A = 0']
femm.mi_addboundprop(bc_properties[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

# Define the position of the stator, rotor, magnet, and coils
magnet_angle = 2 * math.pi / POLES
slot_r = STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA / 2
slot_angle = 2 * math.pi / SLOTS

air_position = [0, 2 * STATOR_ID - 1]
stator_position = [0, STATOR_ID / 2 + STATOR_BASE / 2]
rotor_position = [0,
                  STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + MAGNET_STATOR_GAP
                  + MAGNET_THK + ROTOR_THK / 2]
magnet_positions = [[0,
                     STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + MAGNET_STATOR_GAP
                     + MAGNET_THK / 2]]
slot_position = [-slot_r * math.sin(5 * slot_angle / 2), slot_r * math.cos(5 * slot_angle / 2)]
coil1_positions = [[slot_position[0] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(5 * slot_angle / 2),
                    slot_position[1] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(5 * slot_angle / 2)]]
coil2_positions = [[slot_position[0] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(5 * slot_angle / 2),
                    slot_position[1] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(5 * slot_angle / 2)]]

# Add air position & set material
femm.mi_addblocklabel(0, 0)
femm.mi_addblocklabel(air_position[0], air_position[1])
femm.mi_selectlabel(air_position[0], air_position[1])
femm.mi_selectlabel(0, 0)
femm.mi_setblockprop(AIR)
femm.mi_clearselected()
femm.mi_selectarcsegment(air_position[0], air_position[1])
femm.mi_selectarcsegment(air_position[0], -air_position[1])
femm.mi_setarcsegmentprop(0, bc_properties[0], 0, 0)
femm.mi_clearselected()

# Add stator base position and modify & set materials
femm.mi_addblocklabel(stator_position[0], stator_position[1])
femm.mi_modifymaterial(STATOR, 9, 0)  # Set lamination in plane
femm.mi_modifymaterial(STATOR, 8, 0.98)  # Set lamination fill fraction
femm.mi_modifymaterial(STATOR, 6, 0.635)  # Set lamination thickness
femm.mi_selectlabel(stator_position[0], stator_position[1])
femm.mi_setblockprop(STATOR)
femm.mi_clearselected()

# Add rotor positions & set materials
femm.mi_addblocklabel(rotor_position[0], rotor_position[1])
femm.mi_selectlabel(rotor_position[0], rotor_position[1])
femm.mi_setblockprop(ROTOR)
femm.mi_clearselected()

# Add magnet positions
femm.mi_addblocklabel(magnet_positions[0][0], magnet_positions[0][1])
circ_pattern([magnet_positions[0][0], magnet_positions[0][1]], magnet_angle, int(POLES) - 1, 1, magnet_positions)
setup_magnets(magnet_positions, magnet_angle)

# Add coil1 positions
femm.mi_addblocklabel(coil1_positions[0][0], coil1_positions[0][1])
circ_pattern([coil1_positions[0][0], coil1_positions[0][1]], slot_angle, 5, -1, coil1_positions)

# Add coil2 positions
femm.mi_addblocklabel(coil2_positions[0][0], coil2_positions[0][1])
circ_pattern([coil2_positions[0][0], coil2_positions[0][1]], slot_angle, 5, -1, coil2_positions)

# Set up the coils
setup_coils(coil1_positions, coil2_positions, circ_props)

# Run the simulation
femm.mi_saveas('temp.fem')
femm.mi_analyze()
femm.mi_loadsolution()

# Setup post processor
femm.mo_hidecontourplot()
femm.mo_zoom(-STATOR_ID, -STATOR_ID, STATOR_ID, STATOR_ID)
femm.mo_showdensityplot(1, 0, 2, 0, 'bmag')

# Calculate Torque
femm.mo_selectblock(rotor_position[0],rotor_position[1])
for i in range(len(magnet_positions)):
    femm.mo_selectblock(magnet_positions[i][0], magnet_positions[i][1])
a = femm.mo_blockintegral(22)
femm.mo_clearblock()
print("Torque is " + str(a) + " N-m")

input(0)
