import ROOT
from ROOT import TFile
from ROOTDefs import Tree, build_event_instance, layer_reco_et
import os

#flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'AllEt_Z80_Flat.txt')
flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'RecoEt_PO_Flat_First5.txt')
flat_file = open(flat_file_path, 'w')

#fin_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Raw Data Files', 'output_Z80.root')
fin_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
fin = ROOT.TFile(fin_path)
tin = Tree(fin.Get("mytree"))

# Use below if dealing with a PO file
tin.set_layer_dim(1, 12, 3)
tin.set_layer_dim(2, 12, 3)
tin.set_seed_region(4, 7, 1, 1)
new_adj_dict = {4: -1, 5: 0, 6: 0, 7: 1}
tin.set_adjacent_eta_cells(new_adj_dict)

for i in range(tin.entries):
    tin.get_entry(i)

    event = build_event_instance(tin, 1, 1, 0)

    print(str(layer_reco_et(event.l0_layer, 1, 2, -1, -1, event.adjacent_eta_direction)))

    event.phi_orient()

    #print(event.reco_et)
    print(str(layer_reco_et(event.l0_layer, 1, 2, -1, -1, event.adjacent_eta_direction)))

    # Use below if layer Ets should be calculated based on a reconstructed Et algorithm
    l0_et = str(layer_reco_et(event.l0_layer, 1, 2, -1, -1, event.adjacent_eta_direction))
    l1_et = str(layer_reco_et(event.l1_layer, 5, 2, event.seed_eta, event.seed_phi))
    l2_et = str(layer_reco_et(event.l2_layer, 5, 2, event.seed_eta, event.seed_phi))
    l3_et = str(layer_reco_et(event.l3_layer, 3, 2, -1, -1, event.adjacent_eta_direction))
    had_et = str(layer_reco_et(event.had_layer, 3, 2, -1, -1, event.adjacent_eta_direction))

    # Use below if layer Ets should be the sum of all cells
    '''
    l0_et = str(event.l0_layer.total_et)
    l1_et = str(event.l1_layer.total_et)
    l2_et = str(event.l2_layer.total_et)
    l3_et = str(event.l3_layer.total_et)
    had_et = str(event.had_layer.total_et)
    '''

    if event.true_tau_pt < 20000.:
        continue

    # Use below if using an ET file where the true tau Et is provided
    # true_et = str(event.mctau.Et() / 1000.)
    # Use below if using a PO file where the true tau Pt must be used in lieu of Et
    true_et = str(event.true_tau_pt / 1000.)

    line = l0_et + ',' + l1_et + ',' + l2_et + ',' + l3_et + ',' + had_et + ',' + true_et + '\n'

    flat_file.write(line)

flat_file.close()
