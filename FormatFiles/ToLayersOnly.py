import ROOT
from ROOT import TTree, AddressOf
from ROOTDefs import get_po_signal_et_background_files, recreate_formatted_root_file, prepare_event
from array import array

'''
Take formatted PO signal file and ET background file and format such that only the total Et of each layer is stored
Default algorithm for determining layer Et is used
For background (ET)
- layer_dim_keys = {0 : [3, 3], 1 : [13, 3], 2 : [13, 3], 3 : [3, 3], 4 : [3, 3]}
- reco_et_def = [[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]]
- seed_region_def = [[4, 8], [1, 1]]
- adjacent_eta_cells = { 4: -1, 5: 0, 6: 0, 7: 0, 8: 1 }
For signal (PO)
- layer_dim_keys = {0 : [3, 3], 1 : [12, 3], 2 : [12, 3], 3 : [3, 3], 4 : [3, 3]}
- reco_et_def = [[1, 2], [5, 2], [5, 2], [3, 2], [3, 2]]
- seed_region_def = [[4, 7], [1, 1]]
- adjacent_eta_cells = { 4: -1, 5: 0, 6: 0, 7: 0, 8: 1 }
'''

# Set up input files and trees
input_signal_tree, input_signal_file, input_background_tree, input_background_file = get_po_signal_et_background_files()
print(input_signal_tree.entries)
print(input_background_tree.entries)

# Set up output signal file and tree
output_signal_file = recreate_formatted_root_file('ztt_LayerEts.root')
output_signal_tree = TTree('mytree', 'Layer Et Signal File')

# Set up output background file and tree
output_background_file = recreate_formatted_root_file('MB80_LayerEts.root')
output_background_tree = TTree('mytree', 'Layer Et Background File')

# Initialize signal variables
signal_l0_layer_et = array('f', [0])
signal_l1_layer_et = array('f', [0])
signal_l2_layer_et = array('f', [0])
signal_l3_layer_et = array('f', [0])
signal_had_layer_et = array('f', [0])
signal_true_tau_pt = array('f', [0])

# Connect signal variables to branches in output signal tree
output_signal_tree.Branch('L0Et', signal_l0_layer_et, 'L0Et/F')
output_signal_tree.Branch('L1Et', signal_l1_layer_et, 'L1Et/F')
output_signal_tree.Branch('L2Et', signal_l2_layer_et, 'L2Et/F')
output_signal_tree.Branch('L3Et', signal_l3_layer_et, 'L3Et/F')
output_signal_tree.Branch('HadEt', signal_had_layer_et, 'HadEt/F')
output_signal_tree.Branch('TrueTauPt', signal_true_tau_pt, 'TrueTauPt/F')

# Load layer Ets from input tree and store in output tree
signal_entries = input_signal_tree.entries
print(signal_entries)
for i in range(signal_entries):
    event = prepare_event(input_signal_tree, i, 1, 1, 0)

    # if i == 0:
    #     print(event.l0_layer.reco_et)
    #     print(event.l1_layer.reco_et)
    #     print(event.l2_layer.reco_et)
    #     print(event.l3_layer.reco_et)
    #     print(event.had_layer.reco_et)

    signal_l0_layer_et[0] = event.l0_layer.reco_et
    signal_l1_layer_et[0] = event.l1_layer.reco_et
    signal_l2_layer_et[0] = event.l2_layer.reco_et
    signal_l3_layer_et[0] = event.l3_layer.reco_et
    signal_had_layer_et[0] = event.had_layer.reco_et
    signal_true_tau_pt[0] = event.true_tau_pt

    output_signal_tree.Fill()

output_signal_file.Write()
output_signal_file.Close()

# Initialize background variables
background_l0_layer_et = array('f', [0])
background_l1_layer_et = array('f', [0])
background_l2_layer_et = array('f', [0])
background_l3_layer_et = array('f', [0])
background_had_layer_et = array('f', [0])

# Connect background variables to branch in output background tree
output_background_tree.Branch('L0Et', background_l0_layer_et, 'L0Et/F')
output_background_tree.Branch('L1Et', background_l1_layer_et, 'L1Et/F')
output_background_tree.Branch('L2Et', background_l2_layer_et, 'L2Et/F')
output_background_tree.Branch('L3Et', background_l3_layer_et, 'L3Et/F')
output_background_tree.Branch('HadEt', background_had_layer_et, 'HadEt/F')

# Load layer Ets from input tree and store in output tree
background_entries = input_background_tree.entries
for i in range(background_entries):
    event = prepare_event(input_background_tree, i, 1, 1, 0)

    background_l0_layer_et[0] = event.l0_layer.reco_et
    background_l1_layer_et[0] = event.l1_layer.reco_et
    background_l2_layer_et[0] = event.l2_layer.reco_et
    background_l3_layer_et[0] = event.l3_layer.reco_et
    background_had_layer_et[0] = event.had_layer.reco_et

    output_background_tree.Fill()

output_background_file.Write()
output_background_file.Close()
