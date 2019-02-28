import ROOT
from ROOTDefs import build_event_instance, Tree, reco_et_roc_curve, apply_tree_cut
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

#tsig.set_layer_dim(1, 12, 3)
#tsig.set_layer_dim(2, 12, 3)
#tsig.set_seed_region(4, 7, 1, 1)
#new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
#tsig.set_adjacent_eta_cells(new_adj_dict)
#tsig.set_reco_et_layer_weights([2.610375, 1.1629673, 1.4250076, 2.9280183, 1.490009])
print('Signal before cuts: ', tsig.entries)

tsig = apply_tree_cut(tsig, 'event.true_tau_pt > 20000', temp_file)
#tsig = apply_tree_cut(tsig, 'event.reco_et > 20000', temp_file)

tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
tsig.set_adjacent_eta_cells(new_adj_dict)
#tsig.set_reco_et_layer_weights([2.610375, 1.1629673, 1.4250076, 2.9280183, 1.490009])
sigentries = tsig.entries
print('Signal after cuts: ', sigentries)

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))

print('Background before cuts: ', tback.entries)

#tback = apply_tree_cut(tback, 'event.reco_et > 20', temp_file)
backentries = tback.entries

print('Background after cuts: ', backentries)

tsig.set_reco_et_def([[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]])
tback.set_reco_et_def([[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]])
gr0 = reco_et_roc_curve(tsig, tback)

tsig.set_reco_et_def([[3, 3], [9, 3], [9, 3], [3, 3], [3, 3]])
tback.set_reco_et_def([[3, 3], [9, 3], [9, 3], [3, 3], [3, 3]])
gr1 = reco_et_roc_curve(tsig, tback)

tsig.set_reco_et_def([[1, 2], [3, 2], [3, 2], [1, 2], [1, 2]])
tback.set_reco_et_def([[1, 2], [3, 2], [3, 2], [1, 2], [1, 2]])
gr2 = reco_et_roc_curve(tsig, tback)

tsig.set_reco_et_def([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]])
tback.set_reco_et_def([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]])
gr3 = reco_et_roc_curve(tsig, tback)

gr0.Draw()
gr0.SetLineColor(kRed)
gr0.SetTitle('Reconstructed Energy ROC Curves (True Tau Pt > 20 GeV)')
gr0.GetXaxis().SetTitle("Background Eff")
gr0.GetYaxis().SetTitle("Signal Eff")
gr1.Draw('same')
gr1.SetLineColor(kBlue)
gr2.Draw('same')
gr2.SetLineColor(kGreen)
gr3.Draw('same')
gr3.SetLineColor(kMagenta)

leg1 = TLegend(0.7, 0.1, 0.9, 0.2)
leg1.AddEntry(gr3, '(1x1, 1x1, 1x1, 1x1, 1x1)', 'l')
leg1.AddEntry(gr2, '(1x2, 3x2, 3x2, 1x2, 1x2)', 'l')
leg1.AddEntry(gr0, '(1x2, 5x2, 5x2, 3x2, 3x2)', 'l')
leg1.AddEntry(gr1, '(3x3, 9x3, 9x3, 3x3, 3x3)', 'l')
leg1.SetHeader('Reconstruced Et Definitions')
leg1.Draw()

c1.Print('NewWeightedROC.pdf')

temp_file.Close()
os.remove(temp_file_path)