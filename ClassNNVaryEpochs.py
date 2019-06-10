import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import random
from NNDefs import prepared_flat_file_lines, train_test_split, build_and_train_class_nn
from ROOTDefs import get_po_signal_et_background_files, get_reco_stats, increment_roc_counter, roc_efficiencies_from_cuts
import ROOT
from ROOT import TGraph, TCanvas, TMultiGraph

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

# Define and open path to the flat file that we are reading Et information from
flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Flat Files', 'Classification', 'Classification_PO_Flat.txt')

tsig, fsig, tback, fback = get_po_signal_et_background_files()

max_et, min_et, avg_et, stdev_et = get_reco_stats(tsig, tback)
print(max_et, min_et, avg_et, stdev_et)
stdev_mult = 10
stdev_div = stdev_et * stdev_mult
shift = -avg_et / stdev_div

cell_ets = []
sig_back = []

all_lines = prepared_flat_file_lines(flat_file_path)

# Convert each line from comma-delimited string to list
all_lines = [line.split(',') for line in all_lines]

# Shuffle signal and background events together
random.shuffle(all_lines)

# Split all_lines into a list for layer ets and a list for signal/background identifier
for line in all_lines:
    floats = [(float(et) / stdev_div) - (float(shift) / stdev_div) for et in line[0:5]]
    cell_ets.append(floats)
    sig_back.append([int(line[5])])

# Split et and identifier lists into training (80%) and test (20%) samples
train_ets, test_ets = train_test_split(cell_ets)
train_sig_back, test_sig_back = train_test_split(sig_back)

# Convert Et lists to numpy arrays for use with tensorflow
cell_ets = np.array(cell_ets)
sig_back = np.array(sig_back)

np.random.seed(6)

netcuts = 200
scaler = float(1)/200
min_value = 0

mg = TMultiGraph()
gr = []

for i in range(10, 100, 10):
    print(i)

    model = build_and_train_class_nn(train_ets, train_sig_back, test_ets, test_sig_back, epochs=i)

    predicted_values = model.predict(cell_ets)

    class_sig_cuts = np.zeros(netcuts)
    class_back_cuts = np.zeros(netcuts)

    for j in range(len(predicted_values)):

        pred = predicted_values[j][0]
        truth = sig_back[j][0]

        #print(pred)
        #print(truth)

        if truth == 1:
            increment_roc_counter(pred, class_sig_cuts, scaler, min_value)
        elif truth == 0:
            increment_roc_counter(pred, class_back_cuts, scaler, min_value)

    class_sig_eff, class_back_eff = roc_efficiencies_from_cuts(class_sig_cuts, class_back_cuts, netcuts)

    gr.append(TGraph(netcuts, class_back_eff, class_sig_eff))

for i, graph in enumerate(gr):
    if i == 0:
        gr[i].Draw()
        gr[i].SetTitle('Classifier ROC Curves')
        gr[i].GetXaxis().SetTitle('Background Eff')
        gr[i].GetXaxis().SetLimits(0, 1.2)
        gr[i].GetYaxis().SetTitle('Signal Eff')
        gr[i].SetMinimum(0)
        gr[i].SetMaximum(1.2)
    else:
        gr[i].Draw('same')
        gr[i].SetLineColor(i+1)

c1.Print('VaryEpoch.pdf')
