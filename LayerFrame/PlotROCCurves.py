import ROOT
from ROOT import TCanvas, TLine, TLegend
from ROOTDefs import tau_formatted_root_directory
from LayersDefs import calculate_derived_et_column, calculate_derived_et_columns, roc_curve, background_eff_at_target_signal_eff, get_signal_and_background_frames
import numpy as np
import pandas as pd
import os
import uproot
from tqdm import tqdm

c1 = TCanvas("c1", "Graph Draw Options", 200, 10, 600, 400)

signal_frame, background_frame = get_signal_and_background_frames()

l0_weight_range = [i*0.1 - 2 for i in range(41)]

efficiencies = []

netcuts = 100

# Calculate with unity weights
calculate_derived_et_columns(signal_frame, background_frame)

gr0 = roc_curve(background_frame[['TotalEt']], signal_frame[['TotalEt']], netcuts, target_90percent_signal=1)

# Calculate combined Et columns
calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1], column_names=['L0Et', 'L1Et'],
                             output_column_name='L0+L1Et')
calculate_derived_et_columns(signal_frame, background_frame, layer_weights=[1, 1, 1], column_names=['L2Et', 'L3Et', 'HadEt'],
                             output_column_name='L2+L3+HadEt')



gr1 = roc_curve(background_frame[['WeightedEt']], signal_frame[['WeightedEt']], netcuts, target_90percent_signal=1)

line = TLine(0, .9, 1, .9)

gr0.Draw()
gr0.SetTitle('ROC Curves')
gr0.GetXaxis().SetTitle('Background Efficiency')
gr0.GetYaxis().SetTitle('Signal Efficiency')
gr0.SetMaximum(1)
gr0.SetMinimum(0.8)
gr1.Draw('same')
gr1.SetLineColor(4)
line.Draw()

leg = TLegend(0.7, 0.1, 0.9, 0.3)
leg.SetHeader('Layer Configuration')
leg.AddEntry(gr0, '2 Layer')
leg.AddEntry(gr1, 'Minimized 2 Layer')
# leg.AddEntry(gr2, 'L0+L1, L2+L3, Had Layers')
# leg.AddEntry(gr3, 'L0+L1, L2+L3+Had Layers')
leg.Draw()

c1.Print('ROCCurves2LayerWeighted0.pdf')

