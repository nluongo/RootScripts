import ROOT
from ROOT import TFile
from ROOTDefs import Tree, prepare_event, set_po_tree_parameters
import os

# Open flat file we will write to
flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification_PO_Flat.txt')
flat_file = open(flat_file_path, 'w')

# Open signal file
sig_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'ztt_Output_formatted.root')
sig_file = ROOT.TFile(sig_path)
sig_tree = Tree(sig_file.Get('mytree'))

# Use below if dealing with a PO file
set_po_tree_parameters(sig_tree)

# Open background file
back_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'output_MB80_formatted.root')
back_file = ROOT.TFile(back_path)
back_tree = Tree(back_file.Get('mytree'))

for i in range(sig_tree.entries):
    event = prepare_event(sig_tree, i, 0, 1, 0)

    # Use below if layer Ets should be calculated based on a reconstructed Et algorithm
    l0_et = str(event.l0_layer.reco_et)
    l1_et = str(event.l1_layer.reco_et)
    l2_et = str(event.l2_layer.reco_et)
    l3_et = str(event.l3_layer.reco_et)
    had_et = str(event.had_layer.reco_et)

    sig_back = '1'

    line = l0_et + ',' + l1_et + ',' + l2_et + ',' + l3_et + ',' + had_et + ',' + sig_back + '\n'

    flat_file.write(line)

for i in range(back_tree.entries):
    event = prepare_event(back_tree, i, 0, 1, 0)

    # Use below if layer Ets should be calculated based on a reconstructed Et algorithm
    l0_et = str(event.l0_layer.reco_et)
    l1_et = str(event.l1_layer.reco_et)
    l2_et = str(event.l2_layer.reco_et)
    l3_et = str(event.l3_layer.reco_et)
    had_et = str(event.had_layer.reco_et)

    sig_back = '0'

    line = l0_et + ',' + l1_et + ',' + l2_et + ',' + l3_et + ',' + had_et + ',' + sig_back + '\n'

    flat_file.write(line)

flat_file.close()
