
def configure_simulation():
    import variables as v
    import contact_energy as c
    from cc3d.core.XMLUtils import ElementCC3D
    
    CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20200821","Version":"4.2.3"})
    
    MetadataElmnt=CompuCell3DElmnt.ElementCC3D("Metadata")
    
    # Basic properties simulation
    MetadataElmnt.ElementCC3D("NumberOfProcessors",{},4)
    MetadataElmnt.ElementCC3D("DebugOutputFrequency",{},500)
    # MetadataElmnt.ElementCC3D("NonParallelModule",{"Name":"Potts"})
    
    potts=CompuCell3DElmnt.ElementCC3D("Potts")
    # Basic properties of CPM (GGH) algorithm
    potts.ElementCC3D("Dimensions",{"x":v.modelXdim,"y":v.modelYdim,"z":v.modelZdim_well})
    potts.ElementCC3D("Steps",{},         200000)
    potts.ElementCC3D("Temperature",{},   10)
    potts.ElementCC3D("NeighborOrder",{}, 1)  
      
    celltype=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
    celltype.ElementCC3D("CellType",  {"TypeId":"0",   "TypeName":"Medium"    })
    celltype.ElementCC3D("CellType",  {"TypeId":"1",   "TypeName":"Epi_1"     })
    celltype.ElementCC3D("CellType",  {"TypeId":"2",   "TypeName":"PrE_1"     })
    celltype.ElementCC3D("CellType",  {"TypeId":"3",   "TypeName":"Well",   "Freeze":""})
    celltype.ElementCC3D("CellType",  {"TypeId":"4",   "TypeName":"Epi_2"})
    celltype.ElementCC3D("CellType",  {"TypeId":"5",   "TypeName":"PrE_2"})
    celltype.ElementCC3D("CellType",  {"TypeId":"6",   "TypeName":"Epi_3"})
    celltype.ElementCC3D("CellType",  {"TypeId":"7",   "TypeName":"PrE_3"})
    
    volume=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})   
    
    surface=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
    surface.ElementCC3D("SurfaceEnergyParameters" ,{"CellType":"Epi_2","LambdaSurface": 5, "TargetSurface":v.targetS})   
    surface.ElementCC3D("SurfaceEnergyParameters" ,{"CellType":"PrE_2","LambdaSurface": 5, "TargetSurface":v.targetS})    
    surface.ElementCC3D("SurfaceEnergyParameters" ,{"CellType":"Epi_3","LambdaSurface": 5, "TargetSurface":v.targetS})   
    surface.ElementCC3D("SurfaceEnergyParameters" ,{"CellType":"PrE_3","LambdaSurface": 5, "TargetSurface":v.targetS})
    
    COM_Plugin=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
    Tracker_Plugin=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"NeighborTracker"})
    
    
    contact=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
    # warm-up: neutral energies
    contact.ElementCC3D("Energy",{"Type1":"Epi_1",     "Type2":"Epi_1"},     10) 
    contact.ElementCC3D("Energy",{"Type1":"Epi_1",     "Type2":"PrE_1"},     10)
    contact.ElementCC3D("Energy",{"Type1":"PrE_1",     "Type2":"PrE_1"},     10) 
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"Epi_1"},     10)
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"PrE_1"},     10)     
    contact.ElementCC3D("Energy",{"Type1":"Epi_1",     "Type2":"Well"},      10)   
    contact.ElementCC3D("Energy",{"Type1":"PrE_1",     "Type2":"Well"},      10)  
    
    #relaxation: neutral energies
    contact.ElementCC3D("Energy",{"Type1":"Epi_2",     "Type2":"Epi_2"},     10) 
    contact.ElementCC3D("Energy",{"Type1":"Epi_2",     "Type2":"PrE_2"},     10)
    contact.ElementCC3D("Energy",{"Type1":"PrE_2",     "Type2":"PrE_2"},     10) 
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"Epi_2"},     10)
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"PrE_2"},     10) 
    contact.ElementCC3D("Energy",{"Type1":"PrE_2",     "Type2":"Well"},      10) 
    contact.ElementCC3D("Energy",{"Type1":"Epi_2",     "Type2":"Well"},      10)     
    
    #results: non-neutral energies
    contact.ElementCC3D("Energy",{"Type1":"Epi_3",     "Type2":"Epi_3"},     c.J3_ee) 
    contact.ElementCC3D("Energy",{"Type1":"Epi_3",     "Type2":"PrE_3"},     c.J3_ep)
    contact.ElementCC3D("Energy",{"Type1":"PrE_3",     "Type2":"PrE_3"},     c.J3_pp) 
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"Epi_3"},     c.J3_me)
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"PrE_3"},     c.J3_mp) 
    contact.ElementCC3D("Energy",{"Type1":"PrE_3",     "Type2":"Well"},      c.J3_wp) 
    contact.ElementCC3D("Energy",{"Type1":"Epi_3",     "Type2":"Well"},      c.J3_we) 
    
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"Medium"},     0) 
    contact.ElementCC3D("Energy",{"Type1":"Medium",    "Type2":"Well"},       0)  
    contact.ElementCC3D("Energy",{"Type1":"Well",      "Type2":"Well"},       0) 
    contact.ElementCC3D("NeighborOrder",{}, 1)
    
    
    chemotaxis=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Chemotaxis"})
    chemotaxis.ElementCC3D("ChemicalField",{"Name": "externalpotential"})
   

    SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"DiffusionSolverFE"})
    # # Specification of PDE solvers
    diffusionfield=SteppableElmnt.ElementCC3D("DiffusionField",{"Name":"externalpotential"})
    diffusiondata=diffusionfield.ElementCC3D("DiffusionData")                                   #open diffusion data
    diffusiondata.ElementCC3D("FieldName",{},"externalpotential")                               #define de naam van de chemotaxin waarvoor de geldt
    # # diffusiondata.ElementCC3D("Regular") weet niet zeker of dit klopt
    # # diffusiondata.ElementCC3D("GlobalDiffusionConstant",{}, 0)  #or GlobalDiffusionConstant
    diffusiondata.ElementCC3D("InitialConcentrationExpression",{}, "z^2")                         #geen de diffusion eigenschappen: voor mij alleen begin concentratie.
    
    
    #both irrelevant since the gradient is not decaying or diffusing.
    # diffusiondata.ElementCC3D("DoNotDiffuseTo",{},"Well")
    # diffusiondata.ElementCC3D("DoNotDiffuseTo",{},"PrE_3")
    # diffusiondata.ElementCC3D("DoNotDiffuseTo",{},"Epi_3")
    # # "To prevent decay of a chemical in certain cells we use syntax:" https://compucell3dreferencemanual.readthedocs.io/en/latest/flexible_diffusion_solver.html
    # diffusiondata.ElementCC3D("DoNotDecayIn",{},"Well")
    # diffusiondata.ElementCC3D("DoNotDecayIn",{},"PrE_3")
    # diffusiondata.ElementCC3D("DoNotDecayIn",{},"Epi_3")
    
            # DiffusionDataElmnt.ElementCC3D("GlobalDecayConstant",{},"1e-05")
            # Additional options are:
    # DiffusionDataElmnt.ElementCC3D("InitialConcentrationExpression",{},"z">str(v.modelcellheight))
    # DiffusionDataElmnt.ElementCC3D("InitialConcentrationExpression",{},"z>80")
    
            # DiffusionDataElmnt.ElementCC3D("ConcentrationFileName",={},"INITIAL CONCENTRATION FIELD - 
            #   typically a file with path Simulation/NAME_OF_THE_FILE.txt")
            # DiffusionDataElmnt.ElementCC3D("DiffusionCoefficient",{"CellType":"Epi"},"0.1")
            # DiffusionDataElmnt.ElementCC3D("DiffusionCoefficient",{"CellType":"PrE"},"0.1")
            # DiffusionDataElmnt.ElementCC3D("DiffusionCoefficient",{"CellType":"Well"},"0.1")
            # DiffusionDataElmnt.ElementCC3D("DecayCoefficient",{"CellType":"Epi"},"0.0001")
            # DiffusionDataElmnt.ElementCC3D("DecayCoefficient",{"CellType":"PrE"},"0.0001")
            # DiffusionDataElmnt.ElementCC3D("DecayCoefficient",{"CellType":"Well"},"0.0001")
            # # When secretion is defined inside DissufionSolverFE all secretion constants are scaled 
            #   automaticaly to account for the extra calls to the diffusion step when handling large diffusion constants
    
    
   
    
    SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"UniformInitializer"})
    blob=SteppableElmnt.ElementCC3D("Region")
    blob.ElementCC3D("BoxMin",{"x":v.boxmin_x,"y":v.boxmin_y,"z":v.boxmin_z})
    blob.ElementCC3D("BoxMax",{"x":v.boxmax_x,"y":v.boxmax_y,"z":v.boxmax_z})
    blob.ElementCC3D("Width",{}, 1)
    blob.ElementCC3D("Types",{},"Epi_1,PrE_1")

    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)    

    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)


            
from cc3d import CompuCellSetup
        

configure_simulation()            

            

from ExternalPotHypSteppables import ExternalPotHypSteppable

CompuCellSetup.register_steppable(steppable=ExternalPotHypSteppable(frequency=100))


CompuCellSetup.run()
