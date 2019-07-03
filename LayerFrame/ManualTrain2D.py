import ROOT
from ROOT import TCanvas, TH1F, TLegend
from NNDefs import build_and_train_class_nn
from LayersDefs import get_signal_and_background_frames, calculate_derived_et_columns, roc_efficiencies, background_eff_at_target_signal_eff
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

#random.seed(7)
#np.random.seed(7)

total_steps = 21

ninety_percent_efficiencies = np.ones([total_steps, total_steps])

signal_frame, background_frame = get_signal_and_background_frames()

calculate_derived_et_columns(signal_frame, background_frame)

# Don't do this unless actually training a network!
# Sample from background frame so there are the same number of signal and background events

for i in range(total_steps):
    for j in range(total_steps):
        print('i = {0}  j = {1}'.format(i, j))
        l0l1_weight = 0.2 * i - 1
        l2l3had_weight = 0.2 * j - 1

        calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1], column_names=['L0Et', 'L1Et'],
                                     output_column_name='L0+L1Et')
        calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1, 1], column_names=['L2Et', 'L3Et', 'HadEt'],
                                     output_column_name='L2+L3+HadEt')
        calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[l0l1_weight, l2l3had_weight], column_names=['L0+L1Et', 'L2+L3+HadEt'],
                                     output_column_name='TotalEt')

        if i == 0 and j == 0:
            print(l0l1_weight)
            print(l2l3had_weight)
            print(signal_frame)

        signal_eff, background_eff = roc_efficiencies(signal_frame[['TotalEt']], background_frame[['TotalEt']], 300, target_90percent_signal=1)
        end_background_efficiency = background_eff_at_target_signal_eff(signal_eff, background_eff)

        ninety_percent_efficiencies[i][j] = end_background_efficiency

print(ninety_percent_efficiencies)

min_eff = float('inf')
for i in range(total_steps):
    for j in range(total_steps):
        if ninety_percent_efficiencies[i][j] == 0:
            continue
        if ninety_percent_efficiencies[i][j] < min_eff:
            min_eff = ninety_percent_efficiencies[i][j]

print(min_eff)
