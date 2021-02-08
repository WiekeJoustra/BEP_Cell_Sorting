
from cc3d.core.PySteppables import *
import variables as v
import contact_energy as c
import os.path

class ExternalPotHypSteppable(SteppableBasePy):

    def __init__(self,frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        numCells   =  1000  #number of cells in the circle
        global xMid
        xMid=self.dim.x/2 
                        
        cellTypeMList = ["self.MEDIUM"]
        newCellM = self.new_cell(eval((cellTypeMList[numCells %len(cellTypeMList)])))
        
        cellTypeWList=["self.WELL"]
        newCellW= self.new_cell(eval((cellTypeWList[numCells %len(cellTypeWList)])))
        
        for x in range(self.dim.x): 
            for y in range(self.dim.y): 
                for z in range(self.dim.z): 
                    # if ((x-xMid)**2 +(y-xMid)**2) >= xMid**2: 
                        # self.cell_field[x, y, z] = newCellM
                    if ((x-xMid)**2 +(y-xMid)**2) < (xMid)**2 and ((x-xMid)**2 +(y-xMid)**2) >= (xMid-1)**2: 
                        self.cell_field[x, y, z] = newCellW
                        
                        
        newCellM.targetVolume = newCellM.volume
        newCellM.lambdaVolume = 1000
        
        newCellW.targetVolume = newCellW.volume
        newCellW.lambdaVolume = 1000

     #make the bottom    
        newCellW = self.new_cell(eval(cellTypeWList[numCells %len(cellTypeWList)]))
        self.cell_field[0:self.dim.x, 0:self.dim.y, 0] = newCellW
        
        # field = self.field.externalpotential

        # for y in range(int(v.modelZdim_cells), int(v.modelZdim_well), 1):
            # field[:, :, y] = 8
            
        for cell in self.cellList:
            cell.targetVolume = v.targetV
            if cell.type == self.EPI_1 or cell.type == self.PRE_1: 
                cell.lambdaVolume = 100
            else: 
                cell.lambdaVolume = 0.15
            
        if v.sortingpar_plot: 
            self.plot_sorting = self.add_new_plot_window(
                title='sorting parameter each MCS',
                x_axis_title='MSC',
                y_axis_title='Sorting parameter', 
                grid=False)  
            self.plot_sorting.add_plot('SortingParameter', style='dot', color='blue', size=5)
           
            
        if v.volume_hist: 
            #make a histogram for volum chech
            self.plot_Vhist = self.add_new_plot_window(
                title='volume of every cell each MCS',
                x_axis_title='Volumn in pixel number',
                y_axis_title='Number', 
                grid=False)                                   
            self.plot_Vhist.add_histogram_plot(plot_name = 'cell volume', color='green')
        
        if v.volume:
            #make plot of average volumn 
            self.plot_V = self.add_new_plot_window(
                title='Average Cell Volume of each MCS',
                x_axis_title='MCS', 
                y_axis_title='Average volumn of each MCS',
                grid=False)                                   
            self.plot_V.add_plot('AverageVol', style='dot', color='green', size=5)        
            
        if v.volumeEP:
            self.plot_volEP = self.add_new_plot_window(
                title='Average Cell Volume of PRE and EPI cells each MCS',
                x_axis_title='MCS', 
                y_axis_title='Average volume',
                grid=False)                                   
            self.plot_volEP.add_plot('volE', style='dot', color='red', size=5)
            self.plot_volEP.add_plot('volP', style='dot', color='blue', size=5)
           
        if v.count:
            self.plot_count = self.add_new_plot_window(
                title='number of EPI and PRE cells each MCS',
                x_axis_title='MCS', 
                y_axis_title='number of cells',
                grid=False)                                   
            self.plot_count.add_plot('NumCel', style='dot', color='yellow', size=5)
            
        if v.surface:
            self.plot_surEP = self.add_new_plot_window(
                title='Average Cell Surface of PRE (blue) and EPI (red) cells each MCS',
                x_axis_title='MCS', 
                y_axis_title='Average volume',
                grid=False)                                   
            self.plot_surEP.add_plot('surE', style='dot', color='red', size=5)
            self.plot_surEP.add_plot('surP', style='dot', color='blue', size=5)
        
        if v.energyplot: 
            self.plot_Energy = self.add_new_plot_window(
                title='system energy',
                x_axis_title='MCS', 
                y_axis_title='energy',
                grid=False)                                   
            self.plot_Energy.add_plot('Energy', style='dot', color='yellow', size=5)
            
        if v.volumez: 
            self.plot_Vz = self.add_new_plot_window(
                title='Cell volume in z direction',
                x_axis_title='MCS', 
                y_axis_title='energy',
                grid=False)                                   
            self.plot_Vz.add_plot('volz1', style='dot', color='yellow', size=5)
            self.plot_Vz.add_plot('volz2', style='dot', color='red', size=5)
        
        global mu
        # mu = 0.5
        if  {{run}} == 1 or {{run}} == 2 or {{run}} == 3 or {{run}} == 4 or {{run}} == 5:
            mu = 0.01
        elif {{run}} == 6 or {{run}} == 7 or {{run}} == 8 or {{run}} == 9 or {{run}} == 10:
            mu = 0.03
        elif {{run}} == 11 or {{run}} == 12 or {{run}} == 13 or {{run}} == 14 or {{run}} == 15:
            mu = 0.05  
        elif {{run}} == 16 or {{run}} == 17 or {{run}} == 18 or {{run}} == 19 or {{run}} == 20:
            mu = 0.1 
        elif {{run}} == 21 or {{run}} == 22 or {{run}} == 23 or {{run}} == 24 or {{run}} == 25:
            mu = 0.5 
            
        # run = {{run}}
        if v.output: 
            # save_path = r'\\tudelft.net\student-homes\J\wajoustra\My Documents\cell_sorting_with_cc3d\Final_Results'
            save_path = r'\\tudelft.net\student-homes\J\wajoustra\My Documents\Final_Results_Per_Day\donotsafe'
            
            file_name = os.path.join(save_path, "run" + str(run) + "_numberPcells_mu" + str(mu) + "_gamma" + str(c.gamma_ep_3) + ".csv")
            global f                #think this is not a very neat way to do this
            f=open(file_name, 'w+')
            f.write('MCS; cellid; COM_X; COM_Y; COM_Z \n')
            
            file_name = os.path.join(save_path, "run" + str(run) + "_numberEcells_mu" + str(mu) + "_gamma" + str(c.gamma_ep_3) + ".csv") 
            global g 
            g=open(file_name, 'w+')
            g.write('MCS; cellid; COM_X; COM_Y; COM_Z \n')
        
            file_name = os.path.join(save_path, "run" + str(run) + "_vsEcells_mu"+ str(mu) + "_gamma" + str(c.gamma_ep_3) + ".csv")
            global e             
            e=open(file_name, 'w+')
            e.write('MCS; volumeEPI; surfaceEPI \n')
                       
            file_name = os.path.join(save_path, "run" + str(run) + "_vsPcells_mu" + str(mu) + "_gamma" + str(c.gamma_ep_3) + ".csv")
            global p               
            p=open(file_name, 'w+')
            p.write('MCS; volumePRE; surfacePRE \n')

            file_name = os.path.join(save_path, "run" + str(run) + "_energy_mu" + str(mu) + "_gamma" + str(c.gamma_ep_3) + ".csv")
            global qq
            qq=open(file_name, 'w+')
            qq.write('MCS; energy \n')
        
        if v.sortingpar_output:   
            file_name = os.path.join(save_path, "run" + str(run) + "_sortingpar_mu" + str(mu) + "_gamma" + str(c.gamma_ep_3) + ".csv")
            global rr
            rr=open(file_name, 'w+')
            rr.write('MCS; sortingpar \n')
        
        # mu = 0.01
        if v.outputvolumedifference: 
            save_path = r'\\tudelft.net\student-homes\J\wajoustra\My Documents\cell_sorting_with_cc3d\Final_Results\volume_difference'
            file_name = os.path.join(save_path, "volumedifference_mu" + str(mu) + "_gamma" + str(c.gamma_ep_3) + ".csv")
            global jjj
            jjj=open(file_name, 'w+')
            jjj.write('lowerhalf; upperhalf \n')
            

    def step(self,mcs):
              
        def change_cell_type(initialE, finalE, initialP, finalP):
            for cell in self.cell_list_by_type(initialE): 
                cell.type = finalE
            for cell in self.cell_list_by_type(initialP): 
                cell.type = finalP 
                
        if mcs == v.warmuptime:
            change_cell_type(self.EPI_1, self.EPI_2, self.PRE_1, self.PRE_2)
        if mcs == v.relaxationtime: 
            change_cell_type(self.EPI_2, self.EPI_3, self.PRE_2, self.PRE_3)
            
          #  global mu
                
            for cell in self.cell_list_by_type(self.PRE_3):       
                cd = self.chemotaxisPlugin.addChemotaxisData(cell, "externalpotential")
                cd.setLambda(mu)
                cd.setType('DiffusionSolverFE')
                cd.assignChemotactTowardsVectorTypes([self.MEDIUM, self.PRE_3, self.EPI_3])
                #cell experiences chemotaxis when it touches cell types listed in assignChemotactTowardsVectorTypes function
                #dus dat 'betekent' dat de potential in het medium zit.
                # break  
                
                # if cell.type ==  self.EPI_3:
                        # cd = self.chemotaxisPlugin.addChemotaxisData(cell, "externalpotential")
                        # cd.setLambda(-500)
                        # cd.setType('DiffusionSolverFE')
                        # cd.assignChemotactTowardsVectorTypes([self.MEDIUM, self.PRE_3, self.EPI_3])    

                
        def orderparameter_function(celltypeA, celltypeB): 
            orderparameter = []
            for cell in self.cell_list_by_type(celltypeA, celltypeB): 
                neighbor_list = self.get_cell_neighbor_data_list(cell) #this stores much more data than only neighbor type
                neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
                orderparameter.append(neighbor_count_by_type_dict[cell.type]/sum(neighbor_count_by_type_dict.values()))
                av_orderparameter = np.mean(orderparameter) #mean order par of this MCS
            if v.sortingpar_plot:
                self.plot_sorting.add_data_point('SortingParameter', mcs, av_orderparameter)
            elif v.sortingpar_output: 
                rr.write('{} {} \n' .format(mcs, av_orderparameter))
        
        def volumeplot_function(celltypeA, celltypeB): 
            volume = 0
            if v.volume_hist: 
                volume_array = [] 
            for cell in self.cell_list_by_type(celltypeA, celltypeB):
                volume += cell.volume
                if v.volume_hist: 
                    volume_array.append(cell.volume) 
            if v.volume_hist:        
                self.plot_Vhist.add_histogram(plot_name= 'cell volume', value_array=volume_array, number_of_bins=50)
            volume /= len(self.cell_list_by_type(celltypeA, celltypeB))              
            #this gives the average volumn of each MCS individually
            self.plot_V.add_data_point('AverageVol', mcs, volume) 
    
        def volumeAB_function(celltypeA, celltypeB):
            volumeE = 0
            volumeP = 0
            for cell in self.cell_list_by_type(celltypeA):
                volumeE += cell.volume  
            for cell in self.cell_list_by_type(celltypeB):
                volumeP += cell.volume

            volumeE /= len(self.cell_list_by_type(celltypeA))
            volumeP /= len(self.cell_list_by_type(celltypeB))              
            #this gives the average volumn of each MCS individually
            self.plot_volEP.add_data_point('volE', mcs, volumeE)
            self.plot_volEP.add_data_point('volP', mcs, volumeP)
        
        def countAB_function(celltypeA, celltypeB): 
            counter = len(self.cell_list_by_type(celltypeA)) + len(self.cell_list_by_type(celltypeB)) 
            self.plot_count.add_data_point('NumCel', mcs, counter)
            
        def surfaceAB_function(celltypeA, celltypeB):
            surfaceE = 0
            surfaceP = 0
            for cell in self.cell_list_by_type(celltypeA):
                surfaceE += cell.surface  
            for cell in self.cell_list_by_type(celltypeB):
                surfaceP += cell.surface

            surfaceE /= len(self.cell_list_by_type(celltypeA))
            surfaceP /= len(self.cell_list_by_type(celltypeB))              
            #this gives the average volumn of each MCS individually
            self.plot_surEP.add_data_point('surE', mcs, surfaceE)
            self.plot_surEP.add_data_point('surP', mcs, surfaceP)
            
        def outputfunction(celltype, filezcom, filevs):
            volume = 0 
            surface = 0 
            for cell in self.cell_list_by_type(celltype):
                volume += cell.volume
                surface += cell.surface
                if cell.id % 5 == 0: 
                    filezcom.write('{} {} {} {} {} \n' .format(mcs, cell.id, cell.xCOM, cell.yCOM, cell.zCOM))
            volume /= len(self.cell_list_by_type(celltype))
            surface /= len(self.cell_list_by_type(celltype)) 
                
            filevs.write('{} {} {} \n' .format(mcs, volume, surface))
        
        if mcs < v.warmuptime: 
            A = self.EPI_1
            B = self.PRE_1
        elif v.warmuptime <= mcs < v.relaxationtime: 
            A = self.EPI_2
            B = self.PRE_2
        else: 
            A = self.EPI_3
            B = self.PRE_3
            
            for cell in self.cell_list_by_type(self.PRE_3, self.EPI_3):

                cell.targetVolume = v.targetV + (v.targetV - cell.volume) #het nieuwe volume wordt het target volume plus het verschil tussen het huidige volume en target V
                if cell.targetVolume < 0: 
                    cell.targetVolume = 0
                cell.lambdaVolume = 100*mu
                   
                if cell.type == self.PRE_3: # or self.EPI_3:
                    cd = self.chemotaxisPlugin.getChemotaxisData(cell, "externalpotential")
                    
            if v.output and mcs % 1000 == 0:  
                outputfunction(A, g, e) 
                outputfunction(B, f, p)
                
            if v.volumez: 
                tellerone = 0; volumeone = 0; tellertwo = 0; volumetwo = 0
                for cell in self.cell_list: 
                    if cell.type == self.PRE_3 or self.EPI_3: 
                        if cell.zCOM < 35: 
                            tellerone += 1
                            volumeone += cell.volume
                        else: 
                            tellertwo += 1
                            volumetwo += cell.volume
                average_volumeone = volumeone/tellerone
                average_volumetwo = volumetwo/tellertwo
                self.plot_Vz.add_data_point('volz1', mcs, average_volumeone) 
                self.plot_Vz.add_data_point('volz2', mcs, average_volumetwo) 
              
            if mcs == 199000:  
                if v.outputvolumedifference: 
                    tellerone = 0; volumeone = 0; tellertwo = 0; volumetwo = 0
                    for cell in self.cell_list: 
                        if cell.type == self.PRE_3 or self.EPI_3: 
                            if cell.zCOM < 35: #de cellen komen in praktijk tot een hoogte van ongeveer 35, dus dit is de helft.
                                tellerone += 1
                                volumeone += cell.volume
                            else: 
                                tellertwo += 1
                                volumetwo += cell.volume
                    average_volumeone = volumeone/tellerone
                    average_volumetwo = volumetwo/tellertwo
                    
                    jjj.write('{} {} \n' .format(average_volumeone, average_volumetwo))
                
            
        if v.output and mcs % 1000 == 0:         
            E2 = self.potts.getEnergy()
            qq.write('{} {} \n' .format(mcs, E2))
            # self.plot_Energy.add_data_point('Energy', mcs, E2)
        
        if v.sortingpar_plot or v.sortingpar_output:   
            orderparameter_function(A, B)
        if v.volume: 
            volumeplot_function(A, B)
        if v.volumeEP: 
            volumeAB_function(A, B)
        if v.count: 
            countAB_function(A, B)
        if v.surface: 
            surfaceAB_function(A, B)

                    
                    
        
    def finish(self):
        print('end')
        
        if v.output: 
            f.close()
            g.close()
            e.close()
            p.close()
            qq.close()
          
            
        if v.sortingpar_output: 
            rr.close()
            
        if v.outputvolumedifference: 
            jjj.close()
 
    def on_stop(self):
        # this gets called each time user stops simulation
        return


        