import ROOT
from ROOT import TFile
from ROOTDefs import prepare_event, get_po_signal_et_background_files
import os

flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'RecoEt_ETBack_Flat.txt')
flat_file = open(flat_file_path, 'w')

tsig, fsig, tback, fback = get_po_signal_et_background_files()

for i in range(tback.entries):
    event = prepare_event(tback, i, 0, 1, 0)

    # Use below if layer Ets should be calculated based on a reconstructed Et algorithm
    l0_et = str(event.l0_layer.reco_et)
    l1_et = str(event.l1_layer.reco_et)
    l2_et = str(event.l2_layer.reco_et)
    l3_et = str(event.l3_layer.reco_et)
    had_et = str(event.had_layer.reco_et)

    '''
    # Use below if layer Ets should be the sum of all cells
    l0_et = str(event.l0_layer.total_et)
    l1_et = str(event.l1_layer.total_et)
    l2_et = str(event.l2_layer.total_et)
    l3_et = str(event.l3_layer.total_et)
    had_et = str(event.had_layer.total_et)
    '''

    # Use below if using a PO file where true Pt is provided
    #if event.true_tau_pt < 20000. or event.true_tau_charged != 1 or event.true_tau_neutral != 3:
    #    continue

    # Use below if using an ET file where the true tau Et is provided
    # true_et = str(event.mctau.Et() / 1000.)
    # Use below if using a PO file where the true tau Pt must be used in lieu of Et
    # true_et = str(event.true_tau_pt / 1000.)
    # Use below if using a background file in which 0 is being used for the true Et
    true_et = str(0)

    line = l0_et + ',' + l1_et + ',' + l2_et + ',' + l3_et + ',' + had_et + ',' + true_et + '\n'

    flat_file.write(line)

flat_file.close()
