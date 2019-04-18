import ROOT
from ROOTDefs import build_event_instance, Tree, set_po_tree_parameters, prepare_event
from NNDefs import get_layer_weights_from_txt
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed, kBlue, kGreen, kMagenta, kOrange
import numpy as np
import os
import math

#temp_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'temp_file.root')
#temp_file = TFile(temp_file_path, 'recreate')

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'ztt_Output_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))

# Get layer weights and shift et for given scheme from text file
layer_weights, shift_et = get_layer_weights_from_txt(1)
print(layer_weights)
print(shift_et)

set_po_tree_parameters(tsig)
sigentries = tsig.entries

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
backentries = tback.entries

histo_reco = TH1F("Initial", "Reconstructed Et", 100, -100, 100)
histo_reco_weighted = TH1F("Weighted", "Weighted Reconstructed Et", 100, -100, 100)

histo_res = TH1F("Initial", "Et Resolution", 100, -100, 100)
histo_res_weighted = TH1F("Weighted", "Weighted Et Resolution", 100, -100, 100)

sum_et = 0
num = 0

for i in range(sigentries):
    event = prepare_event(tsig, i, 1, 1, 0)

    reco_et = event.reco_et

    event.set_reco_et_layer_weights(layer_weights)
    event.set_reco_et_shift(shift_et)

    reco_et_weighted = event.reco_et

    if i == 0:
        print(reco_et)
        print(reco_et_weighted)

    true_et = event.true_tau_pt / 1000.

    if true_et < 20.:
        continue

    res_et = reco_et - true_et
    res_et_weighted = reco_et_weighted - true_et

    histo_reco.Fill(reco_et)
    histo_reco_weighted.Fill(reco_et_weighted)

    histo_res.Fill(res_et)
    histo_res_weighted.Fill(res_et_weighted)

name_prepend = ''
file_name = name_prepend + 'EtRes.pdf'

histo_reco.Draw()

histo_reco.SetTitle(name_prepend + ' Reconstructed Et')
histo_reco.GetYaxis().SetRange(0, 450)
histo_reco.GetXaxis().SetTitle('Reconstructed Et')
histo_reco.GetYaxis().SetTitle('Events')
histo_reco.SetLineColor(kRed)
histo_reco.SetAxisRange(0, 450, 'Y')
histo_reco_weighted.Draw('sames')
c1.Update()
histo_reco_weighted.SetLineColor(kBlue)
st = histo_reco_weighted.FindObject('stats')
st.SetY1NDC(.6)
st.SetY2NDC(.75)

leg0 = TLegend(0.1, 0.8, 0.4, 0.9)
leg0.AddEntry(histo_reco, 'Initial Reconstructed Et', 'l')
leg0.AddEntry(histo_reco_weighted, 'Network Trained Reconstructed Et', 'l')
leg0.Draw()

c1.Print(file_name+'(')

histo_res.Draw()

histo_res.SetTitle(name_prepend + ' Signal Reco - True Et')
histo_res.GetXaxis().SetTitle('Reco - True Et')
histo_res.GetYaxis().SetTitle('Events')
histo_res.SetLineColor(kRed)
histo_res.SetAxisRange(0, 625, 'Y')
histo_res_weighted.Draw('sames')
c1.Update()
histo_res_weighted.SetLineColor(kBlue)
st = histo_res_weighted.FindObject('stats')
st.SetY1NDC(.6)
st.SetY2NDC(.75)

leg1 = TLegend(0.1, 0.8, 0.4, 0.9)
leg1.AddEntry(histo_res, 'Initial Reco - True Et', 'l')
leg1.AddEntry(histo_res_weighted, 'Network Trained Reco - True Et', 'l')
leg1.Draw()

c1.Print(file_name+')')

#temp_file.Close()
#os.remove(temp_file_path)