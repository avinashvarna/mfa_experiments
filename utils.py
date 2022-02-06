# -*- coding: utf-8 -*-
"""

@author: avinashvarna
"""


import os
import pandas as pd
from typing import Iterable
from requests_downloader import downloader
from pydub import AudioSegment
from tqdm import tqdm
from indic_transliteration.sanscript import transliterate, DEVANAGARI, SLP1


def download_files(base_url, files, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    for f in files:
        download_path = os.path.join(download_dir, f)
        if not os.path.exists(download_path):
            url = f'{base_url}/{f}'
            downloader.download(url, download_path=download_path)


def split_audio(df, audio_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    audio_files = set(df['filepath'])
    audios = {x:AudioSegment.from_file(os.path.join(audio_dir, x))
              for x in audio_files}
    for i, row in tqdm(df.iterrows()):
        segment = audios[row.filepath][row.start*1000:row.stop*1000]
        segment.export(os.path.join(output_dir, f'{i}.wav'), format='wav')


def make_trans():
    ''' A simple translation table to replace upper case letters in SLP1 with
        the corresponding lower case + 1 '''
    forward = {}
    backward = {}
    for i in range(ord('A'), ord('Z')+1):
        char = chr(i)
        subs = char.lower() + '1'
        forward[char] = subs
        backward[subs] = char
    return forward, backward


forward, backward = make_trans()
forward_table = str.maketrans(forward)


def create_lab_files(text_lines: Iterable[str], output_dir:str):
    ''' Create the transcription files in .lab format for the given data '''
    for i, line in enumerate(text_lines):
        text = transliterate(line, DEVANAGARI, SLP1)
        with open(os.path.join(output_dir, f'{i}.lab'), 'w') as f:
            f.write(f'{text}')


def create_lexicon(text_lines: Iterable[str], output_path):
    ''' Create the lexicon for the Montreal forced aligner '''
    seen = set()
    with open(output_path, 'w') as f:
        for line in text_lines:
            text = transliterate(line, DEVANAGARI, SLP1)
            for word in text.split():
                if word not in seen:
                    pron = ' '.join(word)
                    pron = pron.translate(forward_table)
                    f.write(f'{word} {pron}\n')
                    seen.add(word)