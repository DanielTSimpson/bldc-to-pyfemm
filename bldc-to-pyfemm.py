# Main script for importing DXF files and getting torque values in FEMM
import femm
import math

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
    print(type(save_array))
    for i in range(1, num_copies + 1):
        x = radius * math.cos(phi_0 + direction * i * angle)
        y = radius * math.sin(phi_0 + direction * i * angle)
        femm.mi_addblocklabel(x, y)
        if save_array:
            save_array.append([x, y])


# Initialize FEMM Magnetic Problem
femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0, 'millimeters', 'planar', 1E-8, 20, 20, 0)
femm.mi_readdxf("Input DXFs/" + FILENAME + ".dxf")
femm.mi_zoomnatural()

# Define the position of the stator, rotor, magnet, and coils
air_position = [0, 2 * STATOR_ID - 1]
stator_position = [0, STATOR_ID / 2 + STATOR_BASE / 2]

rotor_position = [0,
                  STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + MAGNET_STATOR_GAP
                  + MAGNET_THK + ROTOR_THK / 2]

magnet_positions = [[0,
                     STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + MAGNET_STATOR_GAP
                     + MAGNET_THK / 2]]

magnet_angle = 2 * math.pi / POLES

slot_r = STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA / 2
slot_angle = 2 * math.pi / SLOTS
slot_position = [slot_r * math.sin(5 * slot_angle / 2), slot_r * math.cos(5 * slot_angle / 2)]

coil1_positions = [[slot_position[0] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(5 * slot_angle / 2),
                    slot_position[1] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(5 * slot_angle / 2)]]
coil2_positions = [[slot_position[0] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(5 * slot_angle / 2),
                   slot_position[1] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(5 * slot_angle / 2)]]

# Add air position
femm.mi_addblocklabel(air_position[0], air_position[1])

# Add stator base and rotor positions
femm.mi_addblocklabel(stator_position[0], stator_position[1])
femm.mi_addblocklabel(rotor_position[0], rotor_position[1])

# Add magnet positions
femm.mi_addblocklabel(magnet_positions[0][0], magnet_positions[0][1])
circ_pattern([magnet_positions[0][0], magnet_positions[0][1]], magnet_angle, int(POLES) - 1, 1, magnet_positions)

# Add coil1 positions
femm.mi_addblocklabel(coil1_positions[0][0], coil1_positions[0][1])
circ_pattern([coil1_positions[0][0], coil1_positions[0][1]], slot_angle, 5, 1, coil1_positions)

# Add coil2 positions
femm.mi_addblocklabel(coil2_positions[0][0], coil2_positions[0][1])
circ_pattern([coil2_positions[0][0], coil2_positions[0][1]], slot_angle, 5, 1, coil2_positions)

input(0)
