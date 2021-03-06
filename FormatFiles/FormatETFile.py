import ROOT
from ROOT import TFile, TTree
from ROOTClassDefs import Layer, Event, Tree
import numpy as np
import os

'''
Take raw ET (Eric Torrence) file and create new formatted version
- Keep only Et and Pt information
- Keep only true tau Pt from entire truth Lorentz vector
'''

# Read data from input file
f_in_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Raw Data Files', 'output_MB80.root')
f_in = ROOT.TFile(f_in_path)
t_in = f_in.Get("mytree")
entries_ztt = t_in.GetEntries()

# Create output file
f_out_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'output_MB80_formatted_new.root')
f_out = TFile(f_out_path, 'recreate')
t_out = TTree('mytree', 'Formatted ET File')

l0_cells = np.array([0]*9, dtype=np.float32)
l1_cells = np.array([0]*39, dtype=np.float32)
l2_cells = np.array([0]*39, dtype=np.float32)
l3_cells = np.array([0]*9, dtype=np.float32)
had_cells = np.array([0]*9, dtype=np.float32)
true_tau_pt = np.array([0], dtype=np.float32)
t_out.Branch('L0CellEt', l0_cells, 'L0CellEt[9]/F')
t_out.Branch('L1CellEt', l1_cells, 'L1CellEt[39]/F')
t_out.Branch('L2CellEt', l2_cells, 'L2CellEt[39]/F')
t_out.Branch('L3CellEt', l3_cells, 'L3CellEt[9]/F')
t_out.Branch('HadCellEt', had_cells, 'HadCellEt[9]/F')
if hasattr(t_in, 'mc_visibleTau'):
    t_out.Branch('true_tau_pt', true_tau_pt, 'true_tau_pt/F')

for i in range(entries_ztt):
    t_in.GetEntry(i)
    for i in range(9):
        l0_cells[i] = t_in.L0CellEt[i] / 1000.
        l3_cells[i] = t_in.L3CellEt[i] / 1000.
        had_cells[i] = t_in.HadCellEt[i] / 1000.
    for i in range(39):
        l1_cells[i] = t_in.L1CellEt[i] / 1000.
        l2_cells[i] = t_in.L2CellEt[i] / 1000.
    if hasattr(t_in, 'mc_visibleTau'):
        true_tau_pt[0] = t_in.mc_visibleTau.Pt() / 1000.

    t_out.Fill()

f_out.Write()
f_out.Close()
