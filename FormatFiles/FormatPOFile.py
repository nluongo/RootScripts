import ROOT
from ROOT import TFile, TTree
from ROOTDefs import Layer, Event
import numpy as np
import os

def po_3x3_cells_to_array(formatted_array, po_vector):
    formatted_array[0] = po_vector[0]
    formatted_array[3] = po_vector[1]
    formatted_array[6] = po_vector[2]
    formatted_array[1] = po_vector[3]
    formatted_array[4] = po_vector[4]
    formatted_array[7] = po_vector[5]
    formatted_array[2] = po_vector[6]
    formatted_array[5] = po_vector[7]
    formatted_array[8] = po_vector[8]

def po_12x3_cells_to_array(formatted_array, po_vector):
    formatted_array[0] = po_vector[0]
    formatted_array[3] = po_vector[1]
    formatted_array[6] = po_vector[2]
    formatted_array[9] = po_vector[3]
    formatted_array[12] = po_vector[4]
    formatted_array[15] = po_vector[5]
    formatted_array[18] = po_vector[6]
    formatted_array[21] = po_vector[7]
    formatted_array[24] = po_vector[8]
    formatted_array[27] = po_vector[9]
    formatted_array[30] = po_vector[10]
    formatted_array[33] = po_vector[11]
    formatted_array[1] = po_vector[12]
    formatted_array[4] = po_vector[13]
    formatted_array[7] = po_vector[14]
    formatted_array[10] = po_vector[15]
    formatted_array[13] = po_vector[16]
    formatted_array[16] = po_vector[17]
    formatted_array[19] = po_vector[18]
    formatted_array[22] = po_vector[19]
    formatted_array[25] = po_vector[20]
    formatted_array[28] = po_vector[21]
    formatted_array[31] = po_vector[22]
    formatted_array[34] = po_vector[23]
    formatted_array[2] = po_vector[24]
    formatted_array[5] = po_vector[25]
    formatted_array[8] = po_vector[26]
    formatted_array[11] = po_vector[27]
    formatted_array[14] = po_vector[28]
    formatted_array[17] = po_vector[29]
    formatted_array[20] = po_vector[30]
    formatted_array[23] = po_vector[31]
    formatted_array[26] = po_vector[32]
    formatted_array[29] = po_vector[33]
    formatted_array[32] = po_vector[34]
    formatted_array[35] = po_vector[35]

# Read data from ztt_Output file
f_ztt_in_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Raw Data Files', 'ztt_Output.root')
f_ztt_in = ROOT.TFile(f_ztt_in_path)
t_ztt_in = f_ztt_in.Get("tauROI")
entries_ztt = t_ztt_in.GetEntries()

f_ztt_out_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
f_ztt_out = TFile(f_ztt_out_path, 'recreate')
t_ztt_out = TTree('mytree', 'Formatted PO File')

l0_cells = np.array([0]*9, dtype=np.float32)
l1_cells = np.array([0]*36, dtype=np.float32)
l2_cells = np.array([0]*36, dtype=np.float32)
l3_cells = np.array([0]*9, dtype=np.float32)
had_cells = np.array([0]*9, dtype=np.float32)
true_tau_pt = np.array([0], dtype=np.float32)
true_tau_eta = np.array([0], dtype=np.float32)
true_tau_charged = np.array([0], dtype=np.int32)
true_tau_neutral = np.array([0], dtype=np.int32)
t_ztt_out.Branch('L0CellEt', l0_cells, 'L0CellEt[9]/F')
t_ztt_out.Branch('L1CellEt', l1_cells, 'L1CellEt[36]/F')
t_ztt_out.Branch('L2CellEt', l2_cells, 'L2CellEt[36]/F')
t_ztt_out.Branch('L3CellEt', l3_cells, 'L3CellEt[9]/F')
t_ztt_out.Branch('HadCellEt', had_cells, 'HadCellEt[9]/F')
t_ztt_out.Branch('true_tau_pt', true_tau_pt, 'true_tau_pt/F')
t_ztt_out.Branch('true_tau_eta', true_tau_eta, 'true_tau_eta/F')
t_ztt_out.Branch('true_tau_charged', true_tau_charged, 'true_tau_charged/I')
t_ztt_out.Branch('true_tau_neutral', true_tau_neutral, 'true_tau_neutral/I')

for i in range(entries_ztt):
    t_ztt_in.GetEntry(i)
    if t_ztt_in.trueTauEta < -1.4 or t_ztt_in.trueTauEta > 1.4:
        continue

    # All layers except HAD are sliced because those layers have the seed cell copied at the beginning of the vector
    po_3x3_cells_to_array(l0_cells, t_ztt_in.scellsEM0[1:])
    po_12x3_cells_to_array(l1_cells, t_ztt_in.scellsEM1[1:])
    po_12x3_cells_to_array(l2_cells, t_ztt_in.scellsEM2[1:])
    po_3x3_cells_to_array(l3_cells, t_ztt_in.scellsEM3[1:])
    po_3x3_cells_to_array(had_cells, t_ztt_in.scellsHAD)
    true_tau_pt[0] = t_ztt_in.trueTauPt
    true_tau_eta[0] = t_ztt_in.trueTauEta
    true_tau_charged[0] = t_ztt_in.trueTauNCharged
    true_tau_neutral[0] = t_ztt_in.trueTauNNeutrals

    t_ztt_out.Fill()

f_ztt_in.Close()

f_ztt_out.Write()
f_ztt_out.Close()
