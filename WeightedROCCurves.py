import ROOT
from ROOTDefs import build_event_instance, Tree, reco_et_roc_curve, tree_average_seed_region_et, apply_tree_cut
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed, kBlue, kGreen, kMagenta, kOrange
import numpy as np
import os
import math

temp_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'temp_file.root')
temp_file = TFile(temp_file_path, 'recreate')

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))

tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}

tsig = apply_tree_cut(tsig, 'event.true_tau_pt > 20000.', temp_file)
tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
tsig.set_adjacent_eta_cells(new_adj_dict)

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))

# None
layer_weights = [3.411339, 1.0414326, 1.3924104, 3.3474362, 1.4786445]
shift_et = 0

# Bias
#layer_weights = [1.4866527, 0.2245883, 0.9129165, 1.7364172, 0.9893436]
#shift_et = 17.115534

# Shift
#layer_weights = [1.8113599, 0.36242402, 0.99382144, 2.0082638, 1.0719023]
#shift_et = 14.227625502888978

gr0 = reco_et_roc_curve(tsig, tback)

tsig.set_reco_et_layer_weights(layer_weights)
tback.set_reco_et_layer_weights(layer_weights)
tsig.set_reco_et_shift(shift_et)
tback.set_reco_et_shift(shift_et)

gr1 = reco_et_roc_curve(tsig, tback)

gr0.Draw()
gr0.SetLineColor(kRed)
gr0.SetTitle('Reconstructed Energy ROC Curves')
gr0.GetXaxis().SetTitle('Background Eff')
gr0.GetYaxis().SetTitle('Signal Eff')
gr1.Draw('same')
gr1.SetLineColor(kBlue)

leg1 = TLegend(0.7, 0.1, 0.9, 0.2)
leg1.AddEntry(gr0, 'Initial ROC Curve', 'l')
leg1.AddEntry(gr1, 'Network Trained ROC Curve', 'l')
leg1.SetHeader('Reconstructed Et Definitions')
leg1.Draw()

c1.Print('LayerWeightedROCCurve.pdf')

temp_file.Close()
os.remove(temp_file_path)