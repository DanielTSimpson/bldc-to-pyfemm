
def unit_back_emf(angle, phase):
    """
    Returns trapezoidal back emf unit function
    :param angle: the position of the rotor in degrees
    :param phase: the phase receiving the back emf, either 0, 1, or 2
    """
    if phase == 1:
        angle = angle - 120
    elif phase == 2:
        angle = angle - 240

    magnet_angle = 360 / 38

    angle = angle % 360 % (2*magnet_angle)

    if 0 <= angle < magnet_angle/3:
        return 3 * angle / magnet_angle
    
    elif magnet_angle/3 <= angle < 2*magnet_angle/3:
        return 1
    
    elif 2*magnet_angle/3 <= angle < 4 * magnet_angle / 3:
        return -3 * angle / magnet_angle + 3 
    
    elif 4*magnet_angle/3 <= angle < 5*magnet_angle/3:
        return -1
    
    elif 5*magnet_angle/3 <= angle < 6*magnet_angle/3:
        return 3 * angle / magnet_angle - 6
    
import matplotlib.pyplot as plt

da = 0.25
angle = [da*x for x in range(0, 360)]
signal_a = []
signal_b = []
signal_c = []

for a in angle: 
    signal_a.append(unit_back_emf(a,0))
    signal_b.append(unit_back_emf(a,1))
    signal_c.append(unit_back_emf(a,2))

# Create a figure with three subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 12), constrained_layout=True)

# Plot signal_a
axs[0].plot(angle, signal_a, label='signal_a', color='b')
axs[0].set_xlabel('a')
axs[0].set_ylabel('signal_a')
axs[0].set_title('Plot of signal_a vs a')
axs[0].legend()
axs[0].grid(True)

# Plot signal_b
axs[1].plot(angle, signal_b, label='signal_b', color='r')
axs[1].set_xlabel('a')
axs[1].set_ylabel('signal_b')
axs[1].set_title('Plot of signal_b vs a')
axs[1].legend()
axs[1].grid(True)

# Plot signal_c
axs[2].plot(angle, signal_c, label='signal_c', color='g')
axs[2].set_xlabel('a')
axs[2].set_ylabel('signal_c')
axs[2].set_title('Plot of signal_c vs a')
axs[2].legend()
axs[2].grid(True)

# Show the plot
plt.show()

# Create a figure
plt.figure(figsize=(10, 6))

# Plot signal_a
plt.plot(angle, signal_a, label='signal_a', color='b')

# Plot signal_b
plt.plot(angle, signal_b, label='signal_b', color='r')

# Plot signal_c
plt.plot(angle, signal_c, label='signal_c', color='g')

# Add labels and title
plt.xlabel('Angle')
plt.ylabel('Signals')
plt.title('Plot of signal_a, signal_b, and signal_c vs Angle')

# Add a legend
plt.legend()

# Add a grid
plt.grid(True)

# Show the plot
plt.show()