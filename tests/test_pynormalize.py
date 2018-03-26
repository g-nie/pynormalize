#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0413


import warnings
import time
import os
from datetime import datetime
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pynormalize.pynormalize import process_files
with warnings.catch_warnings():
    # Silence RuntimeWarning about absence of ffmpeg
    warnings.simplefilter("ignore")
    from pydub import AudioSegment


STORE = 'NORMALIZED'


def get_modified_time_diff(f):
    mod = time.ctime(os.path.getmtime(f))
    mod_time = datetime.strptime(mod, '%a %b %d %H:%M:%S %Y')
    return (datetime.now() - mod_time).total_seconds()


def cleanup_on_finish(Files, folder):
    delete_dir = True
    for f in Files:
        os.remove(f)
        try:
            os.remove(os.path.join(folder, f))
        except FileNotFoundError:
            delete_dir = False
    if delete_dir:
        os.removedirs(folder)


def test_process_files():
    Files = ['temp.wav']
    target_dbfs = -13.5

    empty_audio = AudioSegment.silent(duration=3000)
    empty_audio.export(Files[0], format='wav')
    process_files(Files, target_dbfs)
    if Files[0] in os.listdir(STORE) and \
            get_modified_time_diff(os.path.join(STORE, Files[0])) < 100:
        assert True
    else:
        assert False
    cleanup_on_finish(Files, STORE)


def test_process_files_different_directory():
    Files = ['temp.wav']
    target_dbfs = -13.5
    EDITED_STORE = '_TEMP'

    empty_audio = AudioSegment.silent(duration=3000)
    empty_audio.export(Files[0], format='wav')
    process_files(Files=Files, target_dbfs=target_dbfs, directory=EDITED_STORE)
    if Files[0] in os.listdir(EDITED_STORE) and \
            get_modified_time_diff(os.path.join(EDITED_STORE, Files[0])) < 100:
        assert True
    else:
        assert False
    cleanup_on_finish(Files, EDITED_STORE)


def test_invalid_files():
    Nonexist = ['temp.wav', 'temp.mp3']
    target_dbfs = -13.5
    process_files(Nonexist, target_dbfs)

    Unsupported = ['audio1.ape', 'audio2.aac']
    for u in Unsupported:
        with open(u, 'w'):
            pass
    process_files(Unsupported, target_dbfs)
    cleanup_on_finish(Unsupported, '/')
