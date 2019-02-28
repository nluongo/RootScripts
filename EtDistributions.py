import ROOT
from ROOT import TCanvas, TGraph2D
from ROOTDefs import tree_average_layer_et_map, Tree, true_pt_tree_histogram, had_seed_tree_histogram, build_event_instance, find_et_seed, get_eta_range, tree_average_seed_region_et, build_2d_index_arrays
import numpy as np
import os

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

# Read data from output_Z80 file
f_z80_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'output_Z80_formatted.root')
f_z80 = ROOT.TFile(f_z80_path)
t_z80 = Tree(f_z80.Get("mytree"))

# Create histograms and average cell Et graphs for each layer
true_et_z80 = true_pt_tree_histogram(t_z80)
l0_graph_z80 = tree_average_layer_et_map(t_z80, 0)
l1_graph_z80 = tree_average_layer_et_map(t_z80, 1)
l2_graph_z80 = tree_average_layer_et_map(t_z80, 2)
l3_graph_z80 = tree_average_layer_et_map(t_z80, 3)
had_graph_z80 = tree_average_layer_et_map(t_z80, 4)
had_cell_z80 = had_seed_tree_histogram(t_z80)

# Read data from ztt_Output file
f_ztt_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'ztt_Output_formatted.root')
f_ztt = ROOT.TFile(f_ztt_path)
t_ztt = Tree(f_ztt.Get("mytree"))
t_ztt.set_layer_dim(1, 12, 3)
t_ztt.set_layer_dim(2, 12, 3)

true_et_ztt = true_pt_tree_histogram(t_ztt)
l0_graph_ztt = tree_average_layer_et_map(t_ztt, 0)
l1_graph_ztt = tree_average_layer_et_map(t_ztt, 1)
l1_graph_seed_ztt = tree_average_seed_region_et(t_ztt, 1, 9, 3)
l2_graph_ztt = tree_average_layer_et_map(t_ztt, 2)
l2_graph_seed_ztt = tree_average_seed_region_et(t_ztt, 2, 9, 3)
l3_graph_ztt = tree_average_layer_et_map(t_ztt, 3)
had_graph_ztt = tree_average_layer_et_map(t_ztt, 4)
had_cell_ztt = had_seed_tree_histogram(t_ztt)


# Create Et maps centered on the seed for layers 1 and 2
sum_l1_cell_et = np.zeros((9,3))

for i in range(t_ztt.entries):
    t_ztt.get_entry(i)
    event = build_event_instance(t_ztt, 0, 0, 0)

    seed_eta, seed_phi = find_et_seed(event.l1_layer,[[3,7],[1,1]])
    if seed_eta < 4 or seed_eta > 7 or seed_phi != 1:
        continue

    min_eta, max_eta = get_eta_range(12, 9, seed_eta)

    new_cell_et = event.l1_layer.cell_et[min_eta:max_eta + 1]
    sum_l1_cell_et += new_cell_et

average_cell_et = sum_l1_cell_et / t_ztt.entries
print(average_cell_et)
eta_values, phi_values = build_2d_index_arrays(average_cell_et.size, len(average_cell_et), len(average_cell_et[0]))
flat_cell_et = average_cell_et.flatten('F')

print(eta_values)
print(phi_values)

l1_seed_graph_ztt = TGraph2D(average_cell_et.size, eta_values, phi_values, flat_cell_et)
l1_seed_graph_ztt.GetXaxis().SetTitle("Eta")
l1_seed_graph_ztt.GetYaxis().SetTitle("Phi")


sum_l2_cell_et = np.zeros((9,3))

for i in range(t_ztt.entries):
    t_ztt.get_entry(i)
    event = build_event_instance(t_ztt, 0, 0, 0)

    seed_eta, seed_phi = find_et_seed(event.l2_layer,[[3,7],[1,1]])
    if seed_eta < 4 or seed_eta > 7 or seed_phi != 1:
        continue

    min_eta, max_eta = get_eta_range(12, 9, seed_eta)

    new_cell_et = event.l2_layer.cell_et[min_eta:max_eta + 1]
    sum_l2_cell_et += new_cell_et

average_cell_et = sum_l2_cell_et / t_ztt.entries
#print(average_cell_et)
eta_values, phi_values = build_2d_index_arrays(average_cell_et.size, len(average_cell_et), len(average_cell_et[0]))
flat_cell_et = average_cell_et.flatten('F')

eta_values = np.array([-0.1, -0.075, -0.05, -0.025, 0, 0.025, 0.05, 0.075, 0.1, -0.1, -0.075, -0.05, -0.025, 0, 0.025, 0.05, 0.075, 0.1, -0.1, -0.075, -0.05, -0.025, 0, 0.025, 0.05, 0.075, 0.1])
phi_values = np.array([-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

l2_seed_graph_ztt = TGraph2D(average_cell_et.size, eta_values, phi_values, flat_cell_et)
l2_seed_graph_ztt.GetZaxis().SetTitle("Et (GeV)")
l2_seed_graph_ztt.GetXaxis().SetTitle("Eta Offset")
l2_seed_graph_ztt.GetYaxis().SetTitle("Phi Offset")



true_et_z80.Draw()
c1.Print("EtDistributions.pdf(")
l0_graph_z80.Draw()
c1.Print("EtDistributions.pdf")
l1_graph_z80.Draw()
c1.Print("EtDistributions.pdf")
l2_graph_z80.Draw()
c1.Print("EtDistributions.pdf")
l3_graph_z80.Draw()
c1.Print("EtDistributions.pdf")
had_graph_z80.Draw()
c1.Print("EtDistributions.pdf")

true_et_ztt.Draw()
true_et_ztt.SetTitle("PO True Tau Pt")
c1.Print("EtDistributions.pdf")
l0_graph_ztt.Draw()
l0_graph_ztt.SetTitle("PO L0 Cell Ets")
c1.Print("EtDistributions.pdf")
l1_graph_ztt.Draw()
l1_graph_ztt.SetTitle("PO L1 Cell Ets")
c1.Print("EtDistributions.pdf")
l1_seed_graph_ztt.Draw()
l1_seed_graph_ztt.SetTitle("PO L1 Seed-Centered Cell Ets")
c1.Print("EtDistributions.pdf")
#l1_graph_seed_ztt.Draw()
#c1.Print("EtDistributions.pdf")
l2_graph_ztt.Draw()
l2_graph_ztt.SetTitle("PO L2 Cell Ets")
c1.Print("EtDistributions.pdf")
l2_seed_graph_ztt.Draw()
l2_seed_graph_ztt.SetTitle("Average Tau Energy Deposition (Layer 2)")
c1.Print("EtDistributions.pdf")
#l2_graph_seed_ztt.Draw()
#c1.Print("EtDistributions.pdf")
l3_graph_ztt.Draw()
l3_graph_ztt.SetTitle("PO L3 Cell Ets")
c1.Print("EtDistributions.pdf")
had_graph_ztt.Draw()
had_graph_ztt.SetTitle("PO Had Cell Ets")
c1.Print("EtDistributions.pdf")
had_cell_z80.Draw()
c1.SetLogy()
c1.Print("EtDistributions.pdf")
had_cell_ztt.Draw()
had_cell_ztt.SetTitle("PO Center Had Cell Et")
c1.Print("EtDistributions.pdf)")