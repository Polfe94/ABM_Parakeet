import numpy as np

class Lattice:

    def __init__(self, width, height, scale = 150):

        # Create squared lattice
        self.grid = np.zeros((width, height), dtype = int)
        i = np.indices((width, height))
        x = np.concatenate(i[0]).ravel().tolist()
        y = np.concatenate(i[1]).ravel().tolist()
        self.coords = list(zip(x, y))
        self.x, self.y = np.meshgrid(np.linspace(0, height, width), np.linspace(0, height, height))
        
        # number of units (meters) per pixel in the grid
        self.scale = scale 
        
class Continuum:
    
    def __init__(self, coord_list):
        
        
        self.coords = {}
        for xy in coord_list:
            if xy in self.coords:
                self.coords[xy] += 1
            else:
                self.coords[xy] = 1
                
 