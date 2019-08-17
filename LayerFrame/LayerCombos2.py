import ROOT
from ROOT import TCanvas, TH1F, TLegend
from NNDefs import build_and_train_class_nn
from LayersDefs import get_signal_and_background_frames, predict_nn_on_all_frame, calculate_derived_et_columns, roc_curve, \
    background_eff_at_target_signal_eff
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

#random.seed(7)
#np.random.seed(7)

signal_frame, background_frame = get_signal_and_background_frames()

full_background_frame = background_frame.sample(n=len(background_frame))

# Sample from background frame so there are the same number of signal and background events
background_frame = background_frame.sample(n=len(signal_frame))

# Create new columns combining base columns
calculate_derived_et_columns(signal_frame, background_frame)

calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1], column_names=['L0Et', 'L1Et'],
                             output_column_name='L0+L1Et')
calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1], column_names=['L2Et', 'L3Et'],
                             output_column_name='L2+L3Et')

# Calculate 3 Et with minimum weights
calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1.3, 8.4], column_names=['L0+L1Et', 'L2+L3Et', 'HadEt'],
                             output_column_name='3EtWeighted')

# Calculate 5 Et with minimum weights
calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, .3, 3.6], column_names=['L0+L1Et', 'L2+L3Et', 'HadEt'],
                             output_column_name='5EtWeighted')

# Combine signal and background
all_frame = pd.concat([signal_frame, background_frame])

#predicted_signal_frame, predicted_background_frame, _ = predict_nn_on_all_frame(all_frame, ['L0Et', 'L1Et', 'L2Et', 'L3Et', 'HadEt'], ['IsSignal'])
twohidden_predicted_signal_frame, twohidden_predicted_background_frame, twohidden_model = predict_nn_on_all_frame(all_frame, ['L0Et', 'L1Et', 'L2Et', 'L3Et', 'HadEt'], ['IsSignal'], epochs=30, hidden_layers=2)

# Create ROC curves by cutting on total Et and also cutting on trained network classifier value
gr0 = roc_curve(background_frame[['TotalEt']], signal_frame[['TotalEt']], 300)
gr1 = roc_curve(twohidden_predicted_background_frame, twohidden_predicted_signal_frame, 300)
gr2 = roc_curve(background_frame[['3EtWeighted']], signal_frame[['3EtWeighted']], 1000)
gr3 = roc_curve(background_frame[['5EtWeighted']], signal_frame[['5EtWeighted']], 1000)

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

gr0.Draw()
gr0.SetTitle('Training Scenario ROC Curves')
gr0.GetXaxis().SetTitle('Background Efficiency')
gr0.GetYaxis().SetTitle('Signal Efficiency')
gr0.SetMaximum(1)
gr0.SetMinimum(0.8)
gr1.Draw('same')
gr1.SetLineColor(4)
gr2.Draw('same')
gr2.SetLineColor(8)
gr3.Draw('same')
gr3.SetLineColor(2)

leg = TLegend(0.45, 0.1, 0.9, 0.3)
leg.SetHeader('Layer Configuration')
leg.AddEntry(gr0, 'No training')
leg.AddEntry(gr1, 'Network Trained - Two Hidden Layers')
leg.AddEntry(gr2, 'Manually Trained to 90% - L0+L1, L2+L3, Had Layers')
leg.AddEntry(gr3, 'Manaully Trained to 95% - L0+L1, L2+L3, Had Layers')
leg.SetTextSize(0.02)
leg.Draw()

c1.Print('LayerFrame/SelectROCCurves.pdf')