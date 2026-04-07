import os
import mne
import mne_bids
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re

from glob import glob
from mne_bids import BIDSPath, read_raw_bids

bids_root = r"C:\Users\Laura\OneDrive - Northwestern University\SoundBrain Lab - EAM2\data-bids"
bids_root_local = r"C:\Users\Laura\Documents\PhD\Soundbrain lab\EAM\EAM2-data\data-bids-local"

print('BIDS root directory:', bids_root)


# outputs
deriv_dir = os.path.join(bids_root_local)
if not os.path.exists(deriv_dir):
    os.makedirs(deriv_dir)
os.listdir(deriv_dir)


# task_list = ['active', 'passive']
task_list = ['passive']
ses = '2'
sub_label = 'pilot1'
sched_list = range(1,3)
event_file_pattern = re.compile(
    rf"sub-{sub_label}.*ses-{ses}.*({'|'.join(task_list)}).*acq-sched(\d+).*run-(\d+).*events\.tsv"
)

bids_files_list = os.listdir(os.path.join(bids_root, f'sub-{sub_label}', f'ses-{ses}', 'eeg'))

bids_path = BIDSPath(root=bids_root, 
                     datatype='eeg',
                     subject='pilot1',
                     task='passive',
                    run=1,
                    acquisition='sched1',
                    session='2')

data = read_raw_bids(bids_path)
data.load_data()

# re-reference data to linked mastoid reference
data_ref = data.set_eeg_reference(ref_channels=['M1', 'M2'])

# filter data
data_filtered = data_ref.copy().filter(l_freq=80, h_freq=2000)

# loading events from Status-channel generated events
events_path = bids_path.copy().update(suffix='events', extension='.tsv')
events_df = pd.read_csv(events_path.fpath, delimiter='\t')
annot = mne.Annotations(onset=events_df.onset, duration=0.170, description=events_df.trial_type)
data_filtered.set_annotations(annot)
events_from_annot, event_dict2 = mne.events_from_annotations(data_filtered)

# initialize an empty dictionary for data
task_evoked_dict = {}
event_evoked_dict = {}

# epoch data based on stimulus events
epochs = mne.Epochs(data_filtered, 
                    events=events_from_annot, 
                    event_id=event_dict2,
                    on_missing='warn',
                    picks=['Cz'],
                    tmin=-0.04, tmax=0.4, 
                    baseline=[-0.04, 0],
                    reject=dict(eeg=75e-6)).drop_bad()


t1 = 16384 * epochs.annotations.onset[0]
t2 = 16384 * epochs.annotations.onset[1]
print('t1:', t1)

mne.viz.set_browser_backend('matplotlib')
data_filtered.plot(events=events_from_annot, event_id=event_dict2, block=True, picks=['Cz'], duration=0.170)

