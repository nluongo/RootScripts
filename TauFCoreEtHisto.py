import ROOT
from ROOT import TGraph, TH1F, TLorentzVector, TCanvas, TLine, TLegend, kRed, kBlue, kGreen
from ROOTDefs import build_event_instance, find_histo_percent_bin, Tree
import numpy as np
import os
'''
fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))
tsig.set_layer_dim(1, 12, 3)
tsig.set_layer_dim(2, 12, 3)
tsig.set_seed_region(4, 7, 1, 1)
sig_adjacent_eta_cells = {4: -1, 5: 0, 6: 0, 7: 1}
tsig.set_adjacent_eta_cells(sig_adjacent_eta_cells)
sigentries = tsig.entries
'''
fsig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_Z80_formatted.root')
fsig = ROOT.TFile(fsig_path)
tsig = Tree(fsig.Get("mytree"))
tsig.set_seed_region(4, 8, 1, 1)
sig_adjacent_eta_cells = {4: -1, 5: 0, 6: 0, 7: 0, 8: 1}
tsig.set_adjacent_eta_cells(sig_adjacent_eta_cells)
sigentries = tsig.entries

fback_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_MB80_formatted.root')
fback = ROOT.TFile(fback_path)
tback = Tree(fback.Get("mytree"))
tback.set_seed_region(4, 8, 1, 1)
back_adjacent_eta_cells = {4: -1, 5: 0, 6: 0, 7: 0, 8: 1}
tback.set_adjacent_eta_cells(back_adjacent_eta_cells)
backentries = tback.entries

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

fcore_sig_histo = TH1F("fcore_sig_histo", "PO Signal + Background FCore (5x2, 9x3, L2);FCore;Entries", 100, 0, 1)
fcore_back_histo = TH1F("fcore_back_histo", "PO Signal + Background FCore:FCore:Entries", 100, 0, 1)

back_pre_histo = TH1F("back_pre_histo", "", 100, 0, 100)
back_post_histo = TH1F("back_post_histo", "", 100, 0, 100)

signal_95_percent_bin = np.zeros(100)

# Create FCore signal histogram
'''
for j in range(100):
    print(j)
    # Reset the histogram so that we can calculate a new histogram
    fcore_sig_histo.Reset("ICESM")

    for i in range(sigentries):
        tsig.get_entry(i)

        event = build_event_instance(tsig, 1)
        event.phi_orient()

        # Don't use events with true Et less than 20 GeV
        if event.true_tau_pt < (j * 1000):
            continue

        # Don't use events with reco Et less than 20 GeV
        if event.reco_et < j:
            continue

        fcore_sig_histo.Fill(event.fcore)

    signal_95_percent_bin[j] = find_histo_percent_bin(fcore_sig_histo, 95)
'''

# This array of FCore values for > i GeV cut is the result of the code block above, hardcoding to save time calculating each time
 # Z80
signal_95_percent_bin = [38., 39., 39., 39., 40., 41., 41., 42., 42., 43., 44., 44., 45., 45., 46., 47., 47., 47.,
 48., 48., 49., 50., 51., 52., 53., 53., 54., 54., 55., 55., 55., 55., 56., 56., 57., 57.,
 57., 58., 59., 59., 59., 60., 60., 60., 60., 60., 60., 60., 60., 62., 62., 61., 64., 64.,
 64., 64., 64., 64., 66., 66., 66., 67., 67., 68., 68., 68., 67., 67., 66., 67., 66., 67.,
 69., 71., 73., 71., 71., 71., 73., 73., 75., 78., 76., 78., 78., 78., 79., 80., 79., 80.,
 80., 80., 80., 80., 79., 79., 79., 80., 80., 80.]
'''
 # ztt values
signal_95_percent_bin = [55., 56., 58., 59., 59., 59., 60., 61., 61., 62., 62., 62., 62., 62., 62., 62., 62., 61.,
 62., 62., 62., 62., 62., 63., 63., 64., 63., 65., 63., 63., 63., 63., 63., 63., 63., 63.,
 63., 65., 65., 65., 63., 66., 63., 66., 66., 62., 62., 62., 66., 66., 62., 62., 62., 61.,
 61., 61., 61., 61., 61., 58., 58., 61., 62., 62., 62., 62., 62., 58., 58., 58., 58., 58.,
 58., 58., 62., 62., 58., 58., 58., 58., 58., 58., 58., 58., 58., 58., 58., 58., 58., 58.,
 58., 58., 58., 58., 58., 58., 58., 58., 58., 58.,]
'''
print(signal_95_percent_bin)

# These arrays hold number of events before and after the FCore cut which was retuned for each Et cut
events_before_fcore = np.zeros(100)
events_after_tuned_fcore = np.zeros(100)
events_after_20gev_fcore = np.zeros(100)

# Create FCore background histogram
for i in range(backentries):
    #if i%1000 == 0:
    #    print(i)
    tback.get_entry(i)

    event = build_event_instance(tback)
    event.phi_orient()

    # Loop through all possible Et cuts, cut on that reco Et, then increment counters for events before and after FCore cut
    for j in range(0, 100):
        if event.reco_et > j:
            events_before_fcore[j] += 1

            if event.fcore > signal_95_percent_bin[j] / 100:
                events_after_tuned_fcore[j] += 1

            if event.fcore > signal_95_percent_bin[20]/100:
                events_after_20gev_fcore[j] += 1

    if event.reco_et < 20:
        continue

    fcore_back_histo.Fill(event.fcore)

    back_pre_histo.Fill(event.reco_et)
    if event.fcore > signal_95_percent_bin[20]/100:
        back_post_histo.Fill(event.reco_et)

eff_20gev = [events_after_20gev_fcore[i] / events_before_fcore[i] for i in range(0,100,10)]
eff_tuned = [events_after_tuned_fcore[i] / events_before_fcore[i] for i in range(0,100,10)]

print(events_before_fcore)
print(events_after_20gev_fcore)
print(events_after_tuned_fcore)
#print(eff_20gev)
print(eff_tuned)

collision_rate = 30000000
events_in_sample = 5500
sample_time = events_in_sample / collision_rate

tuned_ets = np.zeros(100)
single_tau_before = np.zeros(100)
single_tau_tuned_after = np.zeros(100)
single_tau_20gev_after = np.zeros(100)
di_tau_before = np.zeros(100)
di_tau_tuned_after = np.zeros(100)
di_tau_20gev_after = np.zeros(100)

for i in range(100):
    tuned_ets[i] = int(i)
    single_tau_before[i] = int(events_before_fcore[i] / sample_time)
    single_tau_tuned_after[i] = int(events_after_tuned_fcore[i] / sample_time)
    single_tau_20gev_after[i] = int(events_after_20gev_fcore[i] / sample_time)
    di_tau_before[i] = single_tau_before[i]**2 / collision_rate
    di_tau_tuned_after[i] = (single_tau_tuned_after[i] ** 2) / collision_rate
    di_tau_20gev_after[i] = (single_tau_20gev_after[i] ** 2) / collision_rate

print(single_tau_before)
print(single_tau_tuned_after)
print(single_tau_20gev_after)

gr0 = TGraph(100, tuned_ets, single_tau_before)
gr0.SetTitle("Single Tau Trigger Rate (Tuned FCore)")
gr0.GetXaxis().SetTitle("Visible Et (GeV)")
gr0.GetYaxis().SetTitle("Single Tau Rate (Hz)")

gr1 = TGraph(100, tuned_ets, single_tau_tuned_after)
gr1.SetTitle("Single Tau Trigger Rate (Tuned FCore)")
gr1.GetXaxis().SetTitle("Visible Et (GeV)")
gr1.GetYaxis().SetTitle("Single Tau Rate (Hz)")

gr2 = TGraph(100, tuned_ets, single_tau_20gev_after)
gr2.SetTitle("Single Tau Trigger Rate (20 GeV FCore)")
gr2.GetXaxis().SetTitle("Visible Et (GeV)")
gr2.GetYaxis().SetTitle("Single Tau Rate (Hz)")

gr3 = TGraph(100, tuned_ets, di_tau_before)
gr3.SetTitle("Di Tau Trigger Rate")
gr3.GetXaxis().SetTitle("Visible Et (GeV)")
gr3.GetYaxis().SetTitle("Di Tau Rate (Hz)")

gr4 = TGraph(100, tuned_ets, di_tau_tuned_after)
gr4.SetTitle("Di Tau Trigger Rate (Tuned FCore)")
gr4.GetXaxis().SetTitle("Visible Et (GeV)")
gr4.GetYaxis().SetTitle("Di Tau Rate (Hz)")

gr5 = TGraph(100, tuned_ets, di_tau_20gev_after)
gr5.SetTitle("Di Tau Trigger Rate (20 GeV FCore)")
gr5.GetXaxis().SetTitle("Visible Et (GeV)")
gr5.GetYaxis().SetTitle("Di Tau Rate (Hz)")


fcore_sig_histo.Draw("hist")
if fcore_sig_histo.GetEntries() != 0:
    fcore_sig_histo.Scale(1/fcore_sig_histo.GetEntries())
fcore_sig_histo.SetLineColor(kRed)
fcore_back_histo.Draw("hist same")
if fcore_back_histo.GetEntries() != 0:
    fcore_back_histo.Scale(1/fcore_back_histo.GetEntries())
fcore_back_histo.SetLineColor(kBlue)
line1 = TLine(signal_95_percent_bin[20] * 0.01, 0, signal_95_percent_bin[20] * 0.01, fcore_sig_histo.GetMaximum())
line1.Draw()
fcoreleg = TLegend(0.7, 0.1, 0.9, 0.2)
fcoreleg.AddEntry(fcore_sig_histo, "Signal", "l")
fcoreleg.AddEntry(fcore_back_histo, "Background", "l")
fcoreleg.Draw()
c1.Print("PyTauFCoreEtHisto.pdf")


grleg = TLegend(0.6, 0.7, 0.9, 0.9)
line1 = TLine(10, 20000, 50, 20000);


# Print single tau with tuned FCore
gr1.Draw("AP")
gr1.GetYaxis().SetRangeUser(50000, 50000000)
gr1.GetXaxis().SetRangeUser(10, 50)
gr1.SetMarkerStyle(3)
gr1.SetMarkerColor(kGreen)
gr0.Draw("same P")
gr0.SetMarkerStyle(2)
gr0.GetXaxis().SetRangeUser(10, 50)
grleg.AddEntry(gr0, "No FCore Cut", "p")
grleg.AddEntry(gr1, "With 95% FCore Cut", "p")
grleg.AddEntry(line1, '20 kHz Level 1 Trigger Rate', 'l')
grleg.Draw("same")

c1.SetLogy()
c1.Print("PyTauFCoreEtHisto.pdf(")

# Print di tau with tuned FCore
gr4.Draw("AP")
gr4.GetYaxis().SetRangeUser(100, 50000000)
gr4.GetXaxis().SetRangeUser(10, 50)
gr4.SetMarkerStyle(3)
gr4.SetMarkerColor(kGreen)
gr3.Draw("same P")
gr3.SetMarkerStyle(2)
gr3.GetXaxis().SetRangeUser(10, 50)
grleg.Draw("same")
line1.Draw("same")
c1.Print("PyTauFCoreEtHisto.pdf")

# Print single tau with 20 GeV FCore
gr2.Draw("AP")
gr2.GetYaxis().SetRangeUser(50000, 50000000)
gr2.GetXaxis().SetRangeUser(10, 50)
gr2.SetMarkerStyle(3)
gr2.SetMarkerColor(kGreen)
gr0.Draw("same P")
gr0.SetMarkerStyle(2)
gr0.GetXaxis().SetRangeUser(10, 50)
grleg.Draw("same")
c1.Print("PyTauFCoreEtHisto.pdf")

# Print di tau with 20 GeV FCore
gr5.Draw("AP")
gr5.GetYaxis().SetRangeUser(100, 50000000)
gr5.GetXaxis().SetRangeUser(10, 50)
gr5.SetMarkerStyle(3)
gr5.SetMarkerColor(kGreen)
gr3.Draw("same P")
gr3.SetMarkerStyle(2)
gr3.GetXaxis().SetRangeUser(10, 50)
grleg.Draw("same")
line1.Draw("same")
c1.Print("PyTauFCoreEtHisto.pdf)")
