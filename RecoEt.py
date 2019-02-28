import ROOT
from ROOTDefs import build_event_instance, Tree, apply_tree_cut, reco_et_tree_histogram
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed
import numpy as np
import os
import math

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))
tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
sigentries = tsig.entries

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
backentries = tback.entries

temp_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'temp_file.root')
temp_file = TFile(temp_file_path, 'recreate')

tsig_cut = apply_tree_cut(tsig, 'event.true_tau_pt > 20000', temp_file)
tsig_cut.set_layer_dim(1, 12, 3)
tsig_cut.set_layer_dim(2, 12, 3)
tsig_cut.set_seed_region(4, 7, 1, 1)

sig_reco_histo = reco_et_tree_histogram(tsig_cut)
back_reco_histo = reco_et_tree_histogram(tback)

# None
layer_weights = [3.411339, 1.0414326, 1.3924104, 3.3474362, 1.4786445]
shift_et = 0

# Bias
#layer_weights = [1.4866527, 0.2245883, 0.9129165, 1.7364172, 0.9893436]
#shift_et = 17.115534

#Shift
#layer_weights = [1.8113599, 0.36242402, 0.99382144, 2.0082638, 1.0719023]
#shift_et = 14.227625502888978

tsig_cut.set_reco_et_layer_weights(layer_weights)
tsig_cut.set_reco_et_shift(shift_et)
tback.set_reco_et_layer_weights(layer_weights)
tback.set_reco_et_shift(shift_et)

sig_reco_histo_weighted = reco_et_tree_histogram(tsig_cut)
back_reco_histo_weighted = reco_et_tree_histogram(tback)

file_name = 'RecoEt.pdf'

back_reco_histo.Draw()
back_reco_histo.SetTitle('Reconstructed Et (> 20 GeV True Pt)')
sig_reco_histo.Draw('same')
sig_reco_histo.SetLineColor(kRed)
c1.SetLogy()

leg1 = TLegend(0.7, 0.1, 0.9, 0.2)
leg1.AddEntry(back_reco_histo, 'Background', 'l')
leg1.AddEntry(sig_reco_histo, "Signal", "l")
leg1.Draw()

c1.Print(file_name + '(')

back_reco_histo_weighted.Draw()
back_reco_histo_weighted.SetTitle('Network Trained Reconstructed Et (> 20 GeV True Pt)')
sig_reco_histo_weighted.Draw('same')
sig_reco_histo_weighted.SetLineColor(kRed)
c1.SetLogy()

#leg1 = TLegend(0.7, 0.1, 0.9, 0.2)
#leg1.AddEntry(back_reco_histo, 'Background', 'l')
#leg1.AddEntry(sig_reco_histo, "Signal", "l")
leg1.Draw()

c1.Print(file_name + ')')

temp_file.Close()
os.remove(temp_file_path)