import ROOT
from ROOT import TCanvas, kRed, kBlue, kGreen, kMagenta, kOrange, TLegend
from ROCCurveDefs import classification_roc_curve
import os

# Define and open path to the flat file that we will write predicted end values to
init_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_AllEt_Flat.txt')

# Define and open path to the flat file that we will write predicted end values to
norm_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_AllEtNorm_Flat.txt')

# Define and open path to the flat file that we will write predicted end values to
sigmoid_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_AllEtNormSig_Flat.txt')

# Define and open path to the flat file that we will write predicted end values to
pred_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_Norm_Predictions.txt')

# Define and open path to the flat file that we will write predicted end values to
hidden_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_Norm_Hid_Predictions.txt')

# Define and open path to the flat file that we will write predicted end values to
twohidden_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_Norm_2Hid_Predictions.txt')

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

# gr0 = classification_roc_curve(init_file_path, 400, -10, 100)
# gr1 = classification_roc_curve(norm_file_path, 400, -1, 4)
gr2 = classification_roc_curve(sigmoid_file_path, 1000, 0, 1)
gr3 = classification_roc_curve(pred_file_path, 1000, 0, 1)
gr4 = classification_roc_curve(hidden_file_path, 1000, 0, 1)
gr5 = classification_roc_curve(twohidden_file_path, 1000, 0, 1)

title = ''

# gr0.Draw()
# gr0.SetLineColor(kRed)
# gr0.SetTitle(title + ' Classifier ROC Curves')
# gr0.GetXaxis().SetTitle('Background Eff')
# gr0.GetXaxis().SetLimits(0, 1.2)
# gr0.GetYaxis().SetTitle('Signal Eff')
# gr0.SetMinimum(0)
# gr0.SetMaximum(1.2)
#
# gr1.Draw('same')
# gr1.SetLineColor(kBlue)

gr2.Draw()
gr2.SetLineColor(kGreen)
gr2.SetTitle(title + ' Classifier ROC Curves')
gr2.GetXaxis().SetTitle('Background Eff')
gr2.GetXaxis().SetLimits(0, 1.2)
gr2.GetYaxis().SetTitle('Signal Eff')
gr2.SetMinimum(0)
gr2.SetMaximum(1.2)

gr3.Draw('same')
gr3.SetLineColor(kMagenta)

gr4.Draw('same')
gr4.SetLineColor(kOrange)

gr5.Draw('same')

leg1 = TLegend(0.7, 0.1, 0.9, 0.3)

# leg1.AddEntry(gr0, 'Reconstructed Et', 'l')
# leg1.AddEntry(gr1, 'Normalized Et', 'l')
leg1.AddEntry(gr2, 'Untrained', 'l')
leg1.AddEntry(gr3, 'Trained No Hidden Layers', 'l')
leg1.AddEntry(gr4, 'Trained One Hidden Layer', 'l')
leg1.AddEntry(gr5, 'Trained Two Hidden Layers', 'l')

leg1.SetHeader('Network Setup')
leg1.Draw()

c1.Print(title + 'ClassROCCurve.pdf(')

# gr0.Draw()
# gr0.SetLineColor(kRed)
# gr0.SetTitle(title + ' Classifier ROC Curves')
# gr0.GetXaxis().SetTitle('Background Eff')
# gr0.GetXaxis().SetLimits(0, 1.2)
# gr0.GetYaxis().SetTitle('Signal Eff')
# gr0.SetMinimum(0.6)
# gr0.SetMaximum(1.1)
#
# gr1.Draw('same')
# gr1.SetLineColor(kBlue)

gr2.Draw()
gr2.SetLineColor(kGreen)
gr2.SetTitle(title + ' Classifier ROC Curves')
gr2.GetXaxis().SetTitle('Background Eff')
gr2.GetXaxis().SetLimits(0, 1.2)
gr2.GetYaxis().SetTitle('Signal Eff')
gr2.SetMinimum(0.6)
gr2.SetMaximum(1.1)

gr3.Draw('same')
gr3.SetLineColor(kMagenta)

gr4.Draw('same')
gr4.SetLineColor(kOrange)

gr5.Draw('same')

leg1 = TLegend(0.7, 0.1, 0.9, 0.3)

# leg1.AddEntry(gr0, 'Reconstructed Et', 'l')
# leg1.AddEntry(gr1, 'Normalized Et', 'l')
leg1.AddEntry(gr2, 'Normalized Et + Sigmoid', 'l')
leg1.AddEntry(gr3, 'No Hidden Layers', 'l')
leg1.AddEntry(gr4, 'One Hidden Layer', 'l')
leg1.AddEntry(gr5, 'Two Hidden Layers', 'l')

leg1.SetHeader('Network Setup')
leg1.Draw()

c1.Print(title + 'ClassROCCurve.pdf)')