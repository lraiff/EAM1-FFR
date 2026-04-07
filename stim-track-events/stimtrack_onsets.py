import os
import mne
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class StimtrackOnsets:
    def __init__(self, root_dir, save_dir, num_expected_peaks, skip_subjects):
        self.root_dir = root_dir
        self.save_dir = save_dir
        self.num_expected_peaks = num_expected_peaks
        self.skip_subjects = skip_subjects

    def list_data_files(self):
        return [d for d in os.listdir(self.root_dir) if d.startswith('sub-')]