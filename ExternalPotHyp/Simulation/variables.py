#In this file, I will define parameters that match number of pixels to distance in microns
#also define variables since it's cleaner to change it in 1 file
import numpy as np
import random

exp_celldia = 10                      # a cell has a diameter of 10 um 
model_celldia = 5                     # want a pixel diamter of at least 3 pixels per cell. 
umperpix = exp_celldia/model_celldia  # microns per pixel

#experimental dimensions in microns (um)
expXdim = 100           
expYdim = expXdim 
expZdim_well = 180            #make the well a bit higher than the max cell blob s.t. there is always medium above
expZdim_cells = 130 #np.random.randint(expXdim, expZdim_well)  # somewhere between 100 and 200 

#model dimensions in pixels
modelXdim = expXdim/umperpix  # umperpix gives how many um fit in 1 pixel. Know the well size, so know the number of pixels of the well.           
modelYdim = modelXdim
modelZdim_well = expZdim_well/umperpix
modelZdim_cells = int(expZdim_cells/umperpix) # do not use this one with the new method

#targetV = 25*5-8*4 #93
targetV = 90
targetS = 170  #if we look at the surface in the warm-up face, when the volume has reached it's target volume, the surface is +/- 170.
# weird thing in how the surface 'develops': overshoot 

warmuptime = 200
relaxationtime = warmuptime + 200

number_of_cells = (np.pi*modelZdim_cells*(modelXdim/2)**2) / targetV  #volume cylinder = pi*h*r^2
#the amount of cells in the simulation is the volume in which the cells can be devided by the volume of 1 cell

#define the x and y dim of the box and let the z-dimension vary. 
cube_xdim = 10
cube_ydim = 10 
cube_zdim = np.round(number_of_cells/(cube_xdim*cube_ydim)) #if volume of 1 cell = 1 pixel, then #cells = x*y*z
#need to round in order to make it a proper number of pixels (cant have a half pixel)

#the box is located in the middel plus or minus half the length of the box
boxmin_x = modelXdim/2-cube_xdim/2
boxmin_y = modelYdim/2-cube_ydim/2
boxmin_z = modelZdim_cells/2-cube_zdim/2

boxmax_x = modelXdim/2+cube_xdim/2
boxmax_y = modelYdim/2+cube_ydim/2
boxmax_z = modelZdim_cells/2+cube_zdim/2

##plot 
sortingpar_plot = 0
volume = 0
volume_hist = 0
volumeEP = 0
count = 0
surface = 0
energyplot = 0
volumez = 0

#output
output = 0
sortingpar_output = 0
outputvolumedifference = 0



    
    
    
    
    
    
    
    
    
    
    
    