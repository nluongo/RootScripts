import ROOT
from ROOTDefs import sig_and_back_reco_et_histograms, get_po_signal_et_background_files
from NNDefs import apply_layer_weights
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, TText, kRed

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

tsig, fsig, tback, fback = get_po_signal_et_background_files()

sig_histo, back_histo = sig_and_back_reco_et_histograms(tsig, tback, 120, -20, 100)

apply_layer_weights(tsig, tback, 21)
sig_histo_weighted, back_histo_weighted = sig_and_back_reco_et_histograms(tsig, tback, 120, -20, 100)

apply_layer_weights(tsig, tback, 22)
sig_histo_bias, back_histo_bias = sig_and_back_reco_et_histograms(tsig, tback, 120, -20, 100)

name_prepend = 'HundredSigAndBack'
file_name = name_prepend + 'RecoEtHisto.pdf'

back_histo.Draw()
back_histo.SetTitle('Reconstructed Et')
back_histo.SetStats(0)
sig_histo.Draw('same')
sig_histo.SetLineColor(kRed)
sig_histo.SetStats(0)
c1.SetLogy()

leg1 = TLegend(0.7, 0.8, 0.9, 0.9)
leg1.AddEntry(back_histo, 'Background', 'l')
leg1.AddEntry(sig_histo, "Signal", "l")
leg1.Draw()

txt1 = TText(0.68, 0.75, 'Signal True Et = 100 GeV')
txt1.SetNDC()
txt1.SetTextFont(43)
txt1.SetTextSize(10)
#txt1.Draw()

txt2 = TText(0.68, 0.7, 'Background True Et = 0 GeV')
txt2.SetNDC()
txt2.SetTextFont(43)
txt2.SetTextSize(10)
#txt2.Draw()

c1.Print(file_name + '(')

back_histo_weighted.Draw()
back_histo_weighted.SetTitle('Network Trained Reconstructed Et')
back_histo_weighted.SetStats(0)
sig_histo_weighted.Draw('same')
sig_histo_weighted.SetLineColor(kRed)
sig_histo_weighted.SetStats(0)
c1.SetLogy()
leg1.Draw()
txt1.Draw()
txt2.Draw()

c1.Print(file_name)

back_histo_bias.Draw()
back_histo_bias.SetTitle('Network Trained (with Bias) Reconstructed Et')
back_histo_bias.SetStats(0)
sig_histo_bias.Draw('same')
sig_histo_bias.SetLineColor(kRed)
sig_histo_bias.SetStats(0)
c1.SetLogy()
leg1.Draw()
txt1.Draw()
txt2.Draw()

c1.Print(file_name + ')')
