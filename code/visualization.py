import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import numpy as np
# from IPython import display


""" IDEAS FOR VISUALIZATION """
# plot the grid cells at each step
# plot a dot in the center of each occupied cell
# the color of the dot is the mean age in the spot
# the size of the dot is the number of agents in the spot

def gif(model):
    
    x, y = model.environment.x, model.environment.y
    zmin, zmax = -1, max([np.max(model.frames[i]) for i in range(len(model.frames))])
    
    for i in range(len(model.frames)):
        z = model.frames[i]
        fig, ax = plt.subplots()
        c = ax.pcolormesh(x, y, z, cmap = 'viridis', vmin = zmin, vmax = zmax)
        plt.savefig('../results/frame_%s.png' % i)
    
    

'''
def gif(model):
    
    def update(frame):

        plot.set_data(model.frames[frame])
        return plot

    fig, ax = plt.subplots()
    plot = ax.matshow(model.frames[0])
    # plt.colorbar(plot)

    animation = FuncAnimation(fig, update, frames = len(model.frames), interval = 25)

    # video = animation.to_html5_video()
    # html = display.HTML(video)
    # display.display(html)

    return animation
    # plt.close()
'''

    
