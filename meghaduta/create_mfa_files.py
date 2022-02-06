# -*- coding: utf-8 -*-
"""

@author: avinashvarna
"""


import datetime
import os
import sys

import pandas as pd


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

import utils


if __name__ == "__main__":
    _start_time = datetime.datetime.now()

    database = 'meghaduta.csv'
    df = pd.read_csv(database)
    NUM_TRAIN = 260

    audio_dir = 'audio'
    base_url = 'https://archive.org/download/meghadUta-mUlam-vedabhoomi.org'
    audio_files = set(df['filepath'])

    utils.download_files(base_url, audio_files, audio_dir)
    dataset = {
        'train': df.iloc[:NUM_TRAIN],
        'test': df.iloc[NUM_TRAIN:]
    }

    for name, _df in dataset.items():
        utils.split_audio(_df, audio_dir, name)

    # Create .lab files for training dataset
    utils.create_lab_files(dataset['train']['text'], 'train')
    # Create lexicon/dict using entire text
    utils.create_lexicon(df['text'], 'dict.txt')

    _end_time = datetime.datetime.now()
    delta = _end_time - _start_time
    print(f"Took {delta} ({delta.total_seconds()} s)")