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


def circ_pattern(start_pos: list, angle: float, num_copies: int, direction: int):
    """
    Adds block labels in a circular pattern
    :param start_pos: the point from the center of the motor. the center of the motor is the center of rotation
    :param angle: the angle between copies
    :param num_copies: the number of copies
    :param direction: the direction of the circular pattern. +1 for clockwise, -1 for counterclockwise
    """
    radius = math.pow(math.pow(start_pos[0], 2) + math.pow(start_pos[1], 2), 0.5)
    for i in range(1, num_copies + 1):
        dx = radius * direction * math.sin(i * angle)
        cot = math.tan(math.pi / 2 - i * angle / 2) and (1 / math.tan(math.pi / 2 - i * angle / 2)) or 2 / math.sin(
            i * angle)
        dy = radius * math.sin(i * angle) * cot
        femm.mi_addblocklabel(start_pos[0] + dx, start_pos[1] - dy)


# Initialize FEMM Magnetic Problem
femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0, 'millimeters', 'planar', 1E-8, 20, 20, 0)
femm.mi_readdxf("Input DXFs/" + FILENAME + ".dxf")
femm.mi_zoomnatural()

# Define the position of the stator, rotor, magnet, and coils
stator_position = [0, STATOR_ID / 2 + STATOR_BASE / 2]

rotor_position = [0,
                  STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + MAGNET_STATOR_GAP
                  + MAGNET_THK + ROTOR_THK / 2]

magnet_position = [0,
                   STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA + TOOTH_HEIGHT + MAGNET_STATOR_GAP
                   + MAGNET_THK / 2]
magnet_angle = 2 * math.pi / POLES

tooth_r = STATOR_ID / 2 + STATOR_BASE + float(NUMBER_WINDINGS) * WIRE_DIA / 2
tooth_angle = 2 * math.pi / SLOTS
tooth_position = [tooth_r * math.sin(tooth_angle / 2), tooth_r * math.cos(tooth_angle / 2)]
coil1_position = [tooth_position[0] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(tooth_angle / 2),
                  tooth_position[1] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(tooth_angle / 2)]
coil2_position = [tooth_position[0] + (TOOTH_WIDTH + WIRE_DIA) / 2 * math.cos(tooth_angle / 2),
                  tooth_position[1] - (TOOTH_WIDTH + WIRE_DIA) / 2 * math.sin(tooth_angle / 2)]

# Add stator base and rotor positions
femm.mi_addblocklabel(stator_position[0], stator_position[1])
femm.mi_addblocklabel(rotor_position[0], rotor_position[1])

# Add magnet positions
femm.mi_addblocklabel(magnet_position[0], magnet_position[1])
circ_pattern(magnet_position, magnet_angle, int(POLES / 2), 1)
circ_pattern(magnet_position, magnet_angle, int(POLES / 2), -1)

# Add coil1 positions
femm.mi_addblocklabel(coil1_position[0], coil1_position[1])
circ_pattern(coil1_position, tooth_angle, int(SLOTS / 2), 1)
circ_pattern(coil1_position, tooth_angle, int(SLOTS / 2), -1)

# Add coil2 positions
femm.mi_addblocklabel(coil2_position[0], coil2_position[1])
circ_pattern(coil2_position, tooth_angle, int(SLOTS / 2), 1)
circ_pattern(coil2_position, tooth_angle, int(SLOTS / 2), -1)

# femm.mi_selectlabel(4,5)

input(0)
