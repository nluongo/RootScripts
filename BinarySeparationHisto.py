import ROOT
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed, kBlue, kGreen, kMagenta, kOrange
from NNDefs import prepared_flat_file_lines
import os

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

# Define and open path to the flat files that we will read from
init_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_AllEtNormSig_Flat.txt')
norm_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_Norm_Predictions.txt')
hidden_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_Norm_Hid_Predictions.txt')
twohidden_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_Norm_2Hid_Predictions.txt')

# Get lists of lines from flat files
init_all_lines = prepared_flat_file_lines(init_file_path)
norm_all_lines = prepared_flat_file_lines(norm_file_path)
hidden_all_lines = prepared_flat_file_lines(hidden_file_path)
twohidden_all_lines = prepared_flat_file_lines(twohidden_file_path)

init_sig_histo = TH1F("Signal", "Signal", 100, 0, 1)
init_back_histo = TH1F("Background", "Background", 100, 0, 1)

norm_sig_histo = TH1F("Signal", "Signal", 100, 0, 1)
norm_back_histo = TH1F("Background", "Background", 100, 0, 1)

hidden_sig_histo = TH1F("Signal", "Signal", 100, 0, 1)
hidden_back_histo = TH1F("Background", "Background", 100, 0, 1)

twohidden_sig_histo = TH1F("Signal", "Signal", 100, 0, 1)
twohidden_back_histo = TH1F("Background", "Background", 100, 0, 1)

for line in init_all_lines:
    init, truth = line.split(',')
    init, truth = float(init), int(truth)
    
    if truth == 0:
        init_back_histo.Fill(init)
    elif truth == 1:
        init_sig_histo.Fill(init)
    else:
        print('Non-binary truth value encountered')
        
for line in norm_all_lines:
    norm, truth = line.split(',')
    norm, truth = float(norm), int(truth)

    if truth == 0:
        norm_back_histo.Fill(norm)
    elif truth == 1:
        norm_sig_histo.Fill(norm)
    else:
        print('Non-binary truth value encountered')

for line in hidden_all_lines:
    norm, truth = line.split(',')
    norm, truth = float(norm), int(truth)

    if truth == 0:
        hidden_back_histo.Fill(norm)
    elif truth == 1:
        hidden_sig_histo.Fill(norm)
    else:
        print('Non-binary truth value encountered')
        
for line in twohidden_all_lines:
    norm, truth = line.split(',')
    norm, truth = float(norm), int(truth)

    if truth == 0:
        twohidden_back_histo.Fill(norm)
    elif truth == 1:
        twohidden_sig_histo.Fill(norm)
    else:
        print('Non-binary truth value encountered')
        


name_prepend = ''
file_name = name_prepend + 'BinClassHistogram.pdf'

leg1 = TLegend(0.7, 0.8, 0.9, 0.9)

leg1.AddEntry(init_back_histo, 'Background', 'l')
leg1.AddEntry(init_sig_histo, 'Signal', 'l')


init_back_histo.Draw()
init_back_histo.SetLineColor(kBlue)
init_back_histo.GetYaxis().SetRangeUser(1,100000)
init_back_histo.SetStats(False)
init_sig_histo.Draw('same')
init_sig_histo.SetLineColor(kRed)
init_back_histo.SetTitle('Normalized Signal vs Background Classification')
leg1.Draw()

c1.SetLogy()
c1.Print(file_name + '(')

norm_back_histo.Draw()
norm_back_histo.SetLineColor(kBlue)
norm_back_histo.GetYaxis().SetRangeUser(1,100000)
norm_back_histo.SetStats(False)
norm_sig_histo.Draw('same')
norm_sig_histo.SetLineColor(kRed)
norm_back_histo.SetTitle('Trained (No Hidden) Signal vs Background Classification')
leg1.Draw()

c1.SetLogy()
c1.Print(file_name)

hidden_back_histo.Draw()
hidden_back_histo.SetLineColor(kBlue)
hidden_back_histo.GetYaxis().SetRangeUser(1,100000)
hidden_back_histo.SetStats(False)
hidden_sig_histo.Draw('same')
hidden_sig_histo.SetLineColor(kRed)
hidden_back_histo.SetTitle('Trained (1 Hidden) Signal vs Background Classification')
leg1.Draw()

c1.SetLogy()
c1.Print(file_name)

twohidden_back_histo.Draw()
twohidden_back_histo.SetLineColor(kBlue)
twohidden_back_histo.GetYaxis().SetRangeUser(1,100000)
twohidden_back_histo.SetStats(False)
twohidden_sig_histo.Draw('same')
twohidden_sig_histo.SetLineColor(kRed)
twohidden_back_histo.SetTitle('Trained (2 Hidden) Signal vs Background Classification')
leg1.Draw()

c1.SetLogy()
c1.Print(file_name + ')')