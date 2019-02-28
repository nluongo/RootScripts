import ROOT
from ROOTDefs import build_event_instance, Tree, event_reco_et, layer_reco_et, fcore_tree_histogram, apply_tree_cut, reco_et_tree_histogram
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed
import numpy as np
import os
import math

temp_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'temp_file.root')
temp_file = TFile(temp_file_path, 'recreate')

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

#fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_Z80_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))
#tsig.set_layer_dim(1, 12, 3)
#tsig.set_layer_dim(2, 12, 3)
#tsig.set_seed_region(4, 7, 1, 1)
#new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
#tsig.set_adjacent_eta_cells(new_adj_dict)
tsig.set_fcore_def([[3, 2], [13, 3]])
#tsig = apply_tree_cut(tsig, 'event.reco_et > 20. and event.true_tau_pt > 20000.', temp_file)
tsig = apply_tree_cut(tsig, 'event.reco_et > 20.', temp_file)

#tsig.set_layer_dim(1, 12, 3)
#tsig.set_layer_dim(2, 12, 3)
#tsig.set_seed_region(4, 7, 1, 1)
#new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
#tsig.set_adjacent_eta_cells(new_adj_dict)
tsig.set_fcore_def([[3, 2], [13, 3]])
sigentries = tsig.entries
print(sigentries)

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
tback = apply_tree_cut(tback, 'event.reco_et > 20.', temp_file)
backentries = tback.entries
print(backentries)

sig_histo = fcore_tree_histogram(tsig)
sig_histo.Draw()
#c1.Print('TestPlot.pdf(')

back_histo = fcore_tree_histogram(tback)
back_histo.Draw("same")
back_histo.SetLineColor(kRed)
c1.Print('TestPlot.pdf')

temp_file.Close()
os.remove(temp_file_path)