import ROOT
from ROOT import TCanvas, TH1F, TLegend
from NNDefs import build_network
from LayersDefs import get_signal_and_background_frames, predict_nn_on_all_frame
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from tensorflow import keras

#random.seed(7)
#np.random.seed(7)

signal_frame, background_frame = get_signal_and_background_frames()

# Combine signal and background
all_frame = pd.concat([signal_frame, background_frame])

pred_signal, pred_background, _ = predict_nn_on_all_frame(all_frame, ['L0Et'], ['IsSignal'])