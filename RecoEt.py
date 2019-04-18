import ROOT
from ROOTDefs import build_event_instance, Tree, apply_tree_cut, reco_et_tree_histogram, set_po_tree_parameters
from NNDefs import get_layer_weights_from_txt
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed
import numpy as np
import os
import math

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'ztt_Output_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))

set_po_tree_parameters(tsig)
sigentries = tsig.entries

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
backentries = tback.entries

temp_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'temp_file.root')
temp_file = TFile(temp_file_path, 'recreate')

tsig = apply_tree_cut(tsig, 'event.true_tau_pt > 20000', temp_file)
set_po_tree_parameters(tsig)
sigentries = tsig.entries

sig_reco_histo = reco_et_tree_histogram(tsig)
back_reco_histo = reco_et_tree_histogram(tback)

# Get layer weights and shift et for given scheme from text file
layer_weights, shift_et = get_layer_weights_from_txt(15)
print(layer_weights)
print(shift_et)

tsig.set_reco_et_layer_weights(layer_weights)
tsig.set_reco_et_shift(shift_et)
tback.set_reco_et_layer_weights(layer_weights)
tback.set_reco_et_shift(shift_et)

sig_reco_histo_weighted = reco_et_tree_histogram(tsig)
back_reco_histo_weighted = reco_et_tree_histogram(tback)

name_prepend = 'Quartic'
file_name = name_prepend + 'RecoEt.pdf'

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
back_reco_histo_weighted.SetTitle(name_prepend + ' Network Trained Reconstructed Et (> 20 GeV True Pt)')
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