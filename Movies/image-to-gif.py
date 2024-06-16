import imageio
images = []
for i in range(0,100):
    images.append(imageio.imread("Frame{}.png".format(i)))
imageio.mimsave('movie.gif', images)