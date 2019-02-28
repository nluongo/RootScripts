import ROOT
from ROOTDefs import build_event_instance, Tree, reco_et_roc_curve
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed, kBlue, kGreen, kMagenta, kOrange
import numpy as np
import os
import math

#temp_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'temp_file.root')
#temp_file = TFile(temp_file_path, 'recreate')

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))

# Values obtained from training network in LayerWeights.py
# None
layer_weights = [3.411339, 1.0414326, 1.3924104, 3.3474362, 1.4786445]
shift_et = 0

# Bias
#layer_weights = [1.4866527, 0.2245883, 0.9129165, 1.7364172, 0.9893436]
#shift_et = 17.115534

# Shift
#layer_weights = [1.8113599, 0.36242402, 0.99382144, 2.0082638, 1.0719023]
#shift_et = 14.227625502888978

tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
tsig.set_adjacent_eta_cells(new_adj_dict)
#tsig.set_reco_et_layer_weights(layer_weights)
sigentries = tsig.entries

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
backentries = tback.entries


#tsig.set_reco_et_layer_weights([-6.31, 3.29, 1.59, -0.84, 1.20])
tsig.get_entry(0)
event = build_event_instance(tsig, 1, 1, 0)

histo_reco = TH1F("Initial", "Reconstructed Et", 100, -100, 100)
histo_reco_weighted = TH1F("Weighted", "Weighted Reconstructed Et", 100, -100, 100)

histo_res = TH1F("Initial", "Et Resolution", 100, -100, 100)
histo_res_weighted = TH1F("Weighted", "Weighted Et Resolution", 100, -100, 100)

sum_et = 0
num = 0

for i in range(sigentries):
    tsig.get_entry(i)
    event = build_event_instance(tsig, 1, 1, 0)
    event.phi_orient()

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

    sum_et += reco_et - true_et
    num += 1

    res_et = reco_et - true_et
    res_et_weighted = reco_et_weighted - true_et

    histo_reco.Fill(reco_et)
    histo_reco_weighted.Fill(reco_et_weighted)

    histo_res.Fill(res_et)
    histo_res_weighted.Fill(res_et_weighted)

print(num)
print(sum_et/num)

file_name = 'EtRes.pdf'

histo_reco.Draw()
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

histo_res.SetTitle('Signal Et Resolution')
histo_res.GetXaxis().SetTitle('Resolution')
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
leg1.AddEntry(histo_res, 'Initial Resolution', 'l')
leg1.AddEntry(histo_res_weighted, 'Network Trained Resolution', 'l')
leg1.Draw()

c1.Print(file_name+')')

#temp_file.Close()
#os.remove(temp_file_path)