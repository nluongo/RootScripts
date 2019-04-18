import os
import numpy as np
import ROOT
from ROOT import TFile, TGraph2D
from ROOTDefs import prepare_event, Tree

fin_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'NTuples', 'ztt_Output_formatted.root')
fin = ROOT.TFile(fin_path)
tin = Tree(fin.Get("mytree"))

# Use below if dealing with a PO file
tin.set_layer_dim(1, 12, 3)
tin.set_layer_dim(2, 12, 3)

mode_nums = np.zeros([6, 6])
print(mode_nums)
for i in range(tin.entries):
    event = prepare_event(tin, i, 1, 0, 0)

    for i in range(6):
        for j in range(6):
            if event.true_tau_charged == i and event.true_tau_neutral == j:
                mode_nums[i][j] += 1
print(mode_nums)
mode_nums = np.array(mode_nums.flatten())
print(mode_nums)

charged_values = np.array([0]*6 + [1]*6 + [2]*6 + [3]*6 + [4]*6 + [5]*6)
neutral_values = np.array([0, 1, 2, 3, 4, 5]*6)
print(charged_values)
print(neutral_values)
charged_values = np.array([float(i) for i in charged_values])
neutral_values = np.array([float(i) for i in neutral_values])
mode_nums = np.array([float(i) for i in mode_nums])

graph = TGraph2D(36, neutral_values, charged_values, mode_nums)
#graph = TGraph2D(2, [1, 2], [1, 2], [1, 2])
graph.Draw()
a = input('something')
