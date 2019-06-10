import ROOT
from ROOT import TCanvas, kRed, kBlue
from ROOTDefs import get_po_signal_et_background_files, sig_and_back_reco_et_histograms
from NNDefs import apply_layer_weights

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

tsig, fsig, tback, fback = get_po_signal_et_background_files()

# Get layer weights and shift et for given scheme from text file
apply_layer_weights(tsig, tback, 19)

unweighted_sig_histo, unweighted_back_histo = sig_and_back_reco_et_histograms(tsig, tback, 110, -10, 100)

unweighted_sig_histo.Draw()
unweighted_sig_histo.SetLineColor(kRed)
unweighted_back_histo.Draw('sames')
unweighted_back_histo.SetLineColor(kBlue)

c1.Prin('')