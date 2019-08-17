import ROOT
from ROOT import TCanvas, TH1F, TLegend, TGraph
from LayersDefs import get_signal_and_background_frames, predict_nn_on_all_frame, calculate_derived_et_columns, roc_curve, \
    background_eff_at_target_signal_eff, roc_cuts
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
#calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, .3, 3.6], column_names=['L0+L1Et', 'L2+L3Et', 'HadEt'],
#                             output_column_name='5EtWeighted')

# Break frames into one whose events have zero hadronic energy and one whose events have nonzero hadronic energy
no_had_sig = signal_frame[signal_frame['HadEt'] == 0].copy()
no_had_back = background_frame[background_frame['HadEt'] == 0].copy()

some_had_sig = signal_frame[signal_frame['HadEt'] != 0].copy()
some_had_back = background_frame[background_frame['HadEt'] != 0].copy()

# Calculate derived weighted Et column with minimum weight applied
calculate_derived_et_columns(no_had_sig, no_had_back, layer_weights=[1, 1.3], column_names=['L0+L1Et', 'L2+L3Et'], output_column_name='NoHadWeighted')

# Combine signal and background
all_frame = pd.concat([signal_frame, background_frame])

#predicted_signal_frame, predicted_background_frame, _ = predict_nn_on_all_frame(all_frame, ['L0Et', 'L1Et', 'L2Et', 'L3Et', 'HadEt'], ['IsSignal'])
twohid_pred_sig, twohid_pred_back, twohid_model = predict_nn_on_all_frame(all_frame, ['L0Et', 'L1Et', 'L2Et', 'L3Et', 'HadEt'], ['IsSignal'], epochs=50, hidden_layers=2)


# Apply cuts on weighted Et column, returning event counts instead of efficiencies
sig_had_cuts, back_had_cuts = roc_cuts(no_had_sig[['NoHadWeighted']], no_had_back[['NoHadWeighted']], netcuts=500, return_efficiencies=False)
sig_had_noweight, back_had_noweight = roc_cuts(no_had_sig[['TotalEt']], no_had_back[['TotalEt']], netcuts=500, return_efficiencies=False)

# Add back in some had events to get total event counts after cutting on only no had
sig_all_cuts = [i + len(some_had_sig) for i in sig_had_cuts]
back_all_cuts = [i + len(some_had_back) for i in back_had_cuts]

sig_all_noweight = [i + len(some_had_sig) for i in sig_had_noweight]
back_all_noweight = [i + len(some_had_back) for i in back_had_noweight]

# Divide by total number of events to get overall efficiencies
sig_all_eff = np.array([i / len(signal_frame) for i in sig_all_cuts])
back_all_eff = np.array([i / len(background_frame) for i in back_all_cuts])

sig_all_noweight_eff = np.array([i / len(signal_frame) for i in sig_all_noweight])
back_all_noweight_eff = np.array([i / len(background_frame) for i in back_all_noweight])

# Create ROC curves by cutting on total Et and also cutting on trained network classifier value
gr0 = roc_curve(background_frame[['TotalEt']], signal_frame[['TotalEt']], 300)
gr1 = roc_curve(twohid_pred_back, twohid_pred_sig, 1000)
gr2 = roc_curve(background_frame[['3EtWeighted']], signal_frame[['3EtWeighted']], 1000)
#gr3 = roc_curve(background_frame[['5EtWeighted']], signal_frame[['5EtWeighted']], 1000)

gr4 = TGraph(len(sig_all_eff), back_all_eff, sig_all_eff)
gr5 = TGraph(len(sig_all_noweight_eff), back_all_noweight_eff, sig_all_noweight_eff)

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
#gr3.Draw('same')
#gr3.SetLineColor(2)
gr4.Draw('same')
gr4.SetLineColor(6)
gr5.Draw('same')
gr5.SetLineColor(36)

leg = TLegend(0.45, 0.1, 0.9, 0.3)
leg.SetHeader('Layer Configuration')
leg.AddEntry(gr0, 'No training')
leg.AddEntry(gr1, 'Network Trained - Two Hidden Layers')
leg.AddEntry(gr2, 'Manually Trained to 90% - L0+L1, L2+L3, Had Layers')
#leg.AddEntry(gr3, 'Manaully Trained to 95% - L0+L1, L2+L3, Had Layers')
leg.AddEntry(gr4, 'Manually Trained to 90%, Zero Had - L0+L1, L2+L3 Layers')
leg.AddEntry(gr5, 'No training - Zero Had')
leg.SetTextSize(0.02)
leg.Draw()

c1.Print('SelectROCCurves.pdf')