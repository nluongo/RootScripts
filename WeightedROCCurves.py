import ROOT
from ROOTDefs import build_event_instance, Tree, reco_et_roc_curve, tree_average_seed_region_et, apply_tree_cut
from NNDefs import get_layer_weights_from_txt
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed, kBlue, kGreen, kMagenta, kOrange
import numpy as np
import os
import math

temp_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'temp_file.root')
temp_file = TFile(temp_file_path, 'recreate')
temp_file_path_2 = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'temp_file_2.root')
temp_file_2 = TFile(temp_file_path_2, 'recreate')

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'ztt_Output_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))

tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}

tsig = apply_tree_cut(tsig, 'event.true_tau_pt > 20000. and event.true_tau_charged == 1 and event.true_tau_neutral == 0', temp_file)
tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
tsig.set_adjacent_eta_cells(new_adj_dict)

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
#tback = apply_tree_cut(tback, 'event.reco_et > 20.', temp_file_2)

# Get layer weights and shift et for given scheme from text file
layer_weights, shift_et = get_layer_weights_from_txt(11)
print(layer_weights)
print(shift_et)

gr0 = reco_et_roc_curve(tsig, tback)

tsig.set_reco_et_layer_weights(layer_weights)
tback.set_reco_et_layer_weights(layer_weights)
tsig.set_reco_et_shift(shift_et)
tback.set_reco_et_shift(shift_et)

gr1 = reco_et_roc_curve(tsig, tback)

title = '1C0N'
gr0.Draw()
gr0.SetLineColor(kRed)
gr0.SetTitle(title + ' Reconstructed Energy ROC Curves')
gr0.GetXaxis().SetTitle('Background Eff')
gr0.GetYaxis().SetTitle('Signal Eff')
gr1.Draw('same')
gr1.SetLineColor(kBlue)

leg1 = TLegend(0.7, 0.1, 0.9, 0.2)
leg1.AddEntry(gr0, 'Initial ROC Curve', 'l')
leg1.AddEntry(gr1, 'Network Trained ROC Curve', 'l')
leg1.SetHeader('Reconstructed Et Definitions')
leg1.Draw()

c1.Print(title + 'WeightedROCCurve.pdf')

temp_file.Close()
os.remove(temp_file_path)