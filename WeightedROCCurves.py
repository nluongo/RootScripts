import ROOT
from ROOTDefs import get_po_signal_et_background_files
from ROCCurveDefs import et_roc_curve
from NNDefs import apply_layer_weights
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, TText, kRed, kBlue, kGreen, kMagenta, kOrange

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

tsig, fsig, tback, fback = get_po_signal_et_background_files()

gr0 = et_roc_curve(tsig, tback, 120, -20, 100)

# Get layer weights and shift et for given scheme from text file and apply to signal and background trees
apply_layer_weights(tsig, tback, 19)
gr1 = et_roc_curve(tsig, tback, 120, -20, 100)

apply_layer_weights(tsig, tback, 20)
gr2 = et_roc_curve(tsig, tback, 120, -20, 100)

title = 'RealSigAndBack'

gr0.Draw()
gr0.SetLineColor(kRed)
gr0.SetTitle('Reconstructed Energy ROC Curves')
gr0.GetXaxis().SetTitle('Background Eff')
gr0.GetYaxis().SetTitle('Signal Eff')

gr1.Draw('same')
gr1.SetLineColor(kBlue)

gr2.Draw('same')
gr2.SetLineColor(kGreen)

txt1 = TText(0.8, 0.3, 'Signal True Et = NTuple Value')
txt1.SetTextFont(43)
txt1.SetTextSize(10)
txt1.Draw()

txt2 = TText(0.8, 0.25, 'Background True Et = 0 GeV')
txt2.SetTextFont(43)
txt2.SetTextSize(10)
txt2.Draw()

leg1 = TLegend(0.65, 0.1, 0.9, 0.25)
leg1.AddEntry(gr0, 'Initial ROC Curve', 'l')
leg1.AddEntry(gr1, 'Trained Weights ROC Curve', 'l')
leg1.AddEntry(gr2, 'Trained Weights+Bias ROC Curve', 'l')
leg1.SetHeader('Reconstructed Et Definitions')
leg1.Draw()

c1.Print(title + 'WeightedROCCurve.pdf')
