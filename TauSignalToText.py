import ROOT
import numpy as np
import json
from ROOTDefs import resize_root_layer_to_array

textfile = open("TauEts.txt", "w+")

fsig = ROOT.TFile("~/TauTrigger/output_Z80.root")
tsig = fsig.Get("mytree")
sigentries = tsig.GetEntries()

#Initialize arrays that will hold the cell Ets
L0_Sig_Et = np.zeros((3,3), dtype=float)
L1_Sig_Et = np.zeros((13,3), dtype=float)
L2_Sig_Et = np.zeros((13,3), dtype=float)
L3_Sig_Et = np.zeros((3,3), dtype=float)
Had_Sig_Et = np.zeros((3,3), dtype=float)

#This will hold one element for each event, each element will be an array with the total Et found in each layer
Layer_Event_Et = []
Total_Event_Et = []
All_Et = []

for i in range(sigentries):
    tsig.GetEntry(i)

    #CellEt variables are loaded as a flat 1-D array so this converts them to 2-D arrays, list conversion is necessary
    # for some reason
    L0_Sig_Et = resize_root_layer_to_array(tsig.L0CellEt, 3, 3)
    L0_Sig_Et = np.resize(np.asarray(list(tsig.L0CellEt)), (3,3))
    L1_Sig_Et = np.resize(np.asarray(list(tsig.L1CellEt)), (13, 3))
    L2_Sig_Et = np.resize(np.asarray(list(tsig.L2CellEt)), (13, 3))
    L3_Sig_Et = np.resize(np.asarray(list(tsig.L3CellEt)), (3, 3))
    Had_Sig_Et = np.resize(np.asarray(list(tsig.HadCellEt)), (3, 3))

    #These variables will hold the total Et contained each layer for a given event
    L0_Et = 0
    L1_Et = 0
    L2_Et = 0
    L3_Et = 0
    Had_Et = 0
    Total_Et = 0

    #Loop over all cells and add the corresponding cell to total layer Et where appropriate
    #j = eta, k = phi
    for j in range(13):
        for k in range(3):
            if j < 3 and k < 3:
                L0_Et += L0_Sig_Et[j][k]
                L1_Et += L1_Sig_Et[j][k]
                L2_Et += L2_Sig_Et[j][k]
                L3_Et += L3_Sig_Et[j][k]
                Had_Et += Had_Sig_Et[j][k]
                Total_Et += L0_Sig_Et[j][k]
                Total_Et += L1_Sig_Et[j][k]
                Total_Et += L2_Sig_Et[j][k]
                Total_Et += L3_Sig_Et[j][k]
                Total_Et += Had_Sig_Et[j][k]
            else:
                L1_Et += L1_Sig_Et[j][k]
                L2_Et += L2_Sig_Et[j][k]
                Total_Et += L1_Sig_Et[j][k]
                Total_Et += L2_Sig_Et[j][k]

    #Package total Et for each layer into an array for each event
    Layer_Et = [L0_Et, L1_Et, L2_Et, L3_Et, Had_Et]

    #Append each event array to array holding one element per event
    Layer_Event_Et.append(Layer_Et)
    Total_Event_Et.append(Total_Et)

#Package layer et and total et together in one array to be jsoned
All_Et.append(Layer_Event_Et)
All_Et.append(Total_Event_Et)

#json it and write to text file
json.dump(All_Et, textfile)


#Close connection to file
textfile.close()
