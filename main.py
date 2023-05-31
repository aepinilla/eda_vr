# import mne
import pandas as pd
# Load the NeuroKit package and other useful packages
import neurokit2 as nk
import matplotlib.pyplot as plt
from pathlib import Path
from os import walk
from pathlib import Path
import os
import shutil

participants_codes = ["%.2d" % i for i in range(1, 37)]
removed = ['03', '08', '14', '16', '17', '24', '30']

for r in removed:
    participants_codes.remove(r)

for p in participants_codes:
    data_path = 'data/raw/' + str(p) + '/'
    filenames_scd = next(walk(data_path), (None, None, []))[2]  # [] if no file

    # Get name list of files
    for f in filenames_scd:
        if '.scd' in f:
            pre, ext = os.path.splitext(f)
            os.rename(data_path + f, data_path + pre + '.txt')

    filenames_txt = next(walk(data_path), (None, None, []))[2]  # [] if no file

    names_dict = {
        'f2f_rest': 'F2F_Rest',
        'f2f_therapy': 'F2F_Therapy',
        'vr_rest': 'VR_Rest',
        'vr_therapy': 'VR_Therapy',
        # 'hr': 'HR'
    }

    participant_data = {}
    for k, v in names_dict.items():
        for f in filenames_txt:
            if v in f:
                data = pd.read_csv(data_path + f)
                data = data.iloc[:, :-1]
                data.rename(columns={data.columns[0]: "scl",
                                         data.columns[1]: "scr"}, inplace=True)
                data['scl'] = data['scl'] / 50 # Transform voltage to microsiemens - 50 millivolts per microsiemen
                participant_data[k] = data

        eda_signal = participant_data[k].scl.values

        # signals, info = nk.eda_process(eda_signal, sampling_rate=10) #Sampling rate taken from the data files
        # cleaned = signals["EDA_Clean"]
        # features = [info["SCR_Onsets"], info["SCR_Peaks"], info["SCR_Recovery"]]
        # plot = nk.events_plot(features, cleaned, color=['red', 'blue', 'orange'])
        # plt.show()

        data = nk.eda_phasic(nk.standardize(eda_signal), sampling_rate=10)
        plot = data.plot()
        fig = plot.get_figure()
        fig.savefig("reports/figures/eda_raw/eda_raw_%s_%s.png" % (p, k))
