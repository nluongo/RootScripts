import ROOT
from ROOT import TGraph, TCanvas, TH1F, kRed, kBlue, TLegend
from ROOTDefs import get_po_signal_et_background_files, get_temp_root_file, apply_tree_cut, set_po_tree_parameters, \
    prepare_event, et_roc_curve, get_reco_stats, sigmoid
import math
import numpy as np

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

tsig, fsig, tback, fback = get_po_signal_et_background_files()

temp_file = get_temp_root_file('temp_file.root')

tsig = apply_tree_cut(tsig, 'event.true_tau_pt > 20000', temp_file)
set_po_tree_parameters(tsig)

sig_entries = tsig.entries
back_entries = tback.entries

all_entries = sig_entries + back_entries

all_ets = []

max_et, min_et, avg_et, stdev_et = get_reco_stats(tsig, tback)

print(max_et, min_et, avg_et, stdev_et)

st_dev_mult = 10
layer_weights = [1/(st_dev_mult*stdev_et), 1/(st_dev_mult*stdev_et), 1/(st_dev_mult*stdev_et), 1/(st_dev_mult*stdev_et),
                 1/(st_dev_mult*stdev_et)]
shift = -avg_et / (st_dev_mult*stdev_et)

print(layer_weights)
print(shift)

# Define histograms for reco and sigmoid Et
sig_reco_histo = TH1F("Signal", "Signal", 100, -10, 100)
back_reco_histo = TH1F("Background", "Background", 100, -10, 100)

sig_norm_histo = TH1F("Signal", "Signal", 100, -10, 10)
back_norm_histo = TH1F("Background", "Background", 100, -10, 10)

sig_sigmoid_histo = TH1F("Signal", "Signal", 100, 0, 1)
back_sigmoid_histo = TH1F("Background", "Background", 100, 0, 1)

for i in range(sig_entries):
    event = prepare_event(tsig, i, 0, 1, 0)

    print(event.reco_et)

    sig_reco_histo.Fill(event.reco_et)
    all_ets.append(event.reco_et)

    event.set_reco_et_layer_weights(layer_weights)
    event.set_reco_et_shift(shift)

    print(event.reco_et)
    print(exit())

    sig_norm_histo.Fill(event.reco_et)
    sig_sigmoid_histo.Fill(sigmoid(event.reco_et))


for i in range(back_entries):
    event = prepare_event(tback, i, 0, 1, 0)

    #if i < 5:
    #    print(event.reco_et)
    #    print(sigmoid(event.reco_et))

    back_reco_histo.Fill(event.reco_et)
    all_ets.append(event.reco_et)

    event.set_reco_et_layer_weights(layer_weights)
    event.set_reco_et_shift(shift)

    back_norm_histo.Fill(event.reco_et)
    back_sigmoid_histo.Fill(sigmoid(event.reco_et))

    #if i < 5:
    #    print(event.reco_et)
    #    print(sigmoid(event.reco_et))

    #if sigmoid(event.reco_et) < 0.44:
    #    print(sigmoid(event.reco_et))


all_sigmoids = [sigmoid(x) for x in all_ets]

all_ets = np.array(all_ets)
all_sigmoids = np.array(all_sigmoids)

print('Reco ROC')

reco_roc_curve = et_roc_curve(tsig, tback, 110, -10, 100, 0)

tsig.set_reco_et_layer_weights(layer_weights)
tback.set_reco_et_layer_weights(layer_weights)
tsig.set_reco_et_shift(shift + 0.25)
tback.set_reco_et_shift(shift)

print('Sigmo ROC')

sigmoid_roc_curve = et_roc_curve(tsig, tback, 100, 0, 1, 0, sigmoid)

#exit()

file_name = 'SigmoidEtScatter.pdf'

gr = TGraph(all_entries, np.array(all_ets), np.array(all_sigmoids))
gr.Draw('AP')
gr.SetTitle('Sigmoid vs Reco Et')

c1.Print(file_name + '(')

back_reco_histo.Draw()
sig_reco_histo.Draw('same')
sig_reco_histo.SetLineColor(kRed)
c1.SetLogy()

c1.Print(file_name)

back_norm_histo.Draw()
sig_norm_histo.Draw('same')
sig_norm_histo.SetLineColor(kRed)
c1.SetLogy()

c1.Print(file_name)

back_sigmoid_histo.Draw()
sig_sigmoid_histo.Draw('same')
sig_sigmoid_histo.SetLineColor(kRed)
c1.SetLogy()

c1.Print(file_name)

c2 = TCanvas("c2", "Graph Draw Options", 200, 10, 600, 400)

c2.cd()

reco_roc_curve.Draw('AC*')
reco_roc_curve.SetLineColor(kBlue)
sigmoid_roc_curve.Draw('same')
sigmoid_roc_curve.SetLineColor(kRed)

leg1 = TLegend(0.7, 0.2, 0.9, 0.3)
leg1.AddEntry(reco_roc_curve, 'Reconstructed Et', 'l')
leg1.AddEntry(sigmoid_roc_curve, "Sigmoid Et", "l")
leg1.Draw()

c2.Print(file_name + ')')

temp_file.Close()