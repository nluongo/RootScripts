import ROOT
from ROOT import TFile
from ROOTDefs import prepare_event, get_po_signal_et_background_files, get_temp_root_file, apply_tree_cut, set_po_tree_parameters, \
    get_reco_stats, sigmoid
import os

# Open flat file we will write to
flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_PO_Flat.txt')
flat_file = open(flat_file_path, 'w')

tsig, fsig, tback, fback = get_po_signal_et_background_files()

temp_file = get_temp_root_file('temp_file.root')
tsig = apply_tree_cut(tsig, 'event.true_tau_pt > 20000', temp_file)
set_po_tree_parameters(tsig)

#max_et, min_et, avg_et, stdev_et = get_reco_stats(tsig, tback)
#print(max_et, min_et, avg_et, stdev_et)

#stdev_mult = 10
#stdev_div = stdev_et * stdev_mult

#shift = avg_et / stdev_div

file_info = \
    '********* \n' \
    '** Signal file: ztt_Output_formatted.root \n' \
    '** Background file: output_MB80_formatted.root \n' \
    '** Value 1: L0 Reconstructed Et \n' \
    '** Value 2: L1 Reconstructed Et \n' \
    '** Value 3: L2 Reconstructed Et \n' \
    '** Value 4: L3 Reconstructed Et \n' \
    '** Value 5: Had Reconstructed Et \n' \
    '** Value 6: 1/0 Signal/background bit \n' \
    '** Cuts: Signal True Et > 20 GeV \n' \
    '********* \n'

flat_file.write(file_info)

for i in range(tsig.entries):
    event = prepare_event(tsig, i, 0, 1, 0)

    # Use below if layer Ets should be calculated based on a reconstructed Et algorithm
    l0_et = str(event.l0_layer.reco_et)
    l1_et = str(event.l1_layer.reco_et)
    l2_et = str(event.l2_layer.reco_et)
    l3_et = str(event.l3_layer.reco_et)
    had_et = str(event.had_layer.reco_et)

    # Use below if single event Et should be used
    #norm_et = (event.reco_et / stdev_div) - (avg_et / stdev_div)
    #sigmoid_et = sigmoid(norm_et)
    #all_et = str(sigmoid_et)

    sig_back = '1'

    line = l0_et + ',' + l1_et + ',' + l2_et + ',' + l3_et + ',' + had_et + ',' + sig_back + '\n'
    #line = all_et + ',' + sig_back + '\n'

    flat_file.write(line)

for i in range(tback.entries):
    event = prepare_event(tback, i, 0, 1, 0)

    # Use below if layer Ets should be calculated based on a reconstructed Et algorithm
    l0_et = str(event.l0_layer.reco_et)
    l1_et = str(event.l1_layer.reco_et)
    l2_et = str(event.l2_layer.reco_et)
    l3_et = str(event.l3_layer.reco_et)
    had_et = str(event.had_layer.reco_et)

    # Use below if total event Et should be used
    #norm_et = (event.reco_et / stdev_div) - (avg_et / stdev_div)
    #sigmoid_et = sigmoid(norm_et)
    #all_et = str(sigmoid_et)

    sig_back = '0'

    line = l0_et + ',' + l1_et + ',' + l2_et + ',' + l3_et + ',' + had_et + ',' + sig_back + '\n'
    #line = all_et + ',' + sig_back + '\n'

    flat_file.write(line)

flat_file.close()
temp_file.Close()
