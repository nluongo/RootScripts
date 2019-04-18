import ROOT
from ROOTDefs import build_event_instance, Tree, reco_et_roc_curve, tree_average_seed_region_et, apply_tree_cut
from ROOT import TGraph, TCanvas, TFile, TLine, TH1F, TGraph2D, TLegend, kRed, kBlue, kGreen, kMagenta, kOrange, TTree
import os

# Define path to unformatted file
raw_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Raw Data Files', 'ztt_Output.root')
raw_file = ROOT.TFile(raw_file_path)
raw_tree = raw_file.Get("tauROI")
raw_entries = raw_tree.GetEntries()

formatted_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
formatted_file = ROOT.TFile(formatted_file_path)
formatted_tree = formatted_file.Get("mytree")

formatted_custom_tree = Tree(formatted_tree)
formatted_custom_tree.set_layer_dim(1, 12, 3)
formatted_custom_tree.set_layer_dim(2, 12, 3)

flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'RecoEt_PO_Flat_30GeV.txt')
flat_file = open(flat_file_path, 'r')

raw_event_num = 1
formatted_event_num = 0

raw_events = raw_tree.GetEntries()
raw_tree.GetEntry(raw_event_num)
print('Raw File')
print('Events: ',raw_events)
print('Layer 0')
for i in range(len(raw_tree.scellsEM0)):
    print(raw_tree.scellsEM0[i])
print('True Pt ', raw_tree.trueTauPt)
print('Eta ', raw_tree.trueTauEta)

formatted_events = formatted_tree.GetEntries()
formatted_tree.GetEntry(formatted_event_num)
print('Formatted File')
print('Events: ', formatted_events)
for i in range(len(formatted_tree.L0CellEt)):
    print(formatted_tree.L0CellEt[i])

formatted_custom_tree.get_entry(formatted_event_num)
event = build_event_instance(formatted_custom_tree, 1, 0, 0)
print(event.l0_layer.cell_et)

raw_file.Close()
formatted_file.Close()
