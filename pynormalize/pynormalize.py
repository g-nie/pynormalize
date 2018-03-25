#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=W0612


import argparse
import os
import sys
import warnings
import logging
from datetime import datetime
import mutagen

with warnings.catch_warnings():
    # Silence RuntimeWarning about absence of ffmpeg
    warnings.simplefilter("ignore")
    from pydub import AudioSegment

# Directory to store edited files
DIRECTORY = 'NORMALIZED'

if not os.path.exists(DIRECTORY):  # Create the directory if it doesn't exist
    os.mkdir(DIRECTORY)

Supported = ('.wav', '.flac', '.mp3', '.ogg', '.webm', '.mp4')

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


# Check if given files exist in the file system
def _valid_files(file):
    if not os.path.isfile(file):
        msg = 'File cannot be found : {}'.format(file)
        raise argparse.ArgumentTypeError(msg)
    elif not file.endswith(Supported):
        msg = 'File format is not supported : {}'.format(file)
        raise argparse.ArgumentTypeError(msg)
    else:
        return file


def main():
    parser = argparse.ArgumentParser(description="""Normalize audio files to a specified level of dBs
        \nSupported audio formats : .wav, .flac, .mp3, .ogg, .webm, .mp4""")
    parser.add_argument('-d', '--decibels', help='Decibels to use in normalization', type=float, default='-13.5')
    # Accept only one of these arguments : either --files or --all
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--files', help='Audio files to normalize.', type=_valid_files, nargs='+')
    group.add_argument('-a', '--all', help='Process all the audio files in current directory.', action='store_true')
    args = parser.parse_args()

    target_dbfs = args.decibels
    if args.all:  # User selected --all
        Files = []
        for f in os.listdir():
            if f.endswith(Supported):
                Files.append(f)
        if not Files:
            logger.warning('Current directory has no audio files.')
            sys.exit(1)
    else:  # User selected --files
        Files = args.files
    process_files(Files, target_dbfs)


def process_files(Files, target_dbfs):
    show_message = True
    for count, audio_file in enumerate(Files):
        (dirname, filename) = os.path.split(audio_file)
        (shortname, extension) = os.path.splitext(filename)
        logger.info('Processing file : "%s" (%s of %s)', filename, count + 1, len(Files))

        # Extract metadata information
        tags = mutagen.File(audio_file, easy=True)
        # Export the edited file
        try:
            song = AudioSegment.from_file(audio_file, format=extension[1:])
        except FileNotFoundError:  # Could not locate FFmpeg
            if show_message:
                logger.warning('WARNING: Could not locate FFmpeg, skipping non-wav files.')
                show_message = False
            continue
        change_in_dBFS = target_dbfs - song.dBFS
        dest_file = os.path.join(DIRECTORY, filename)
        normalized_sound = song.apply_gain(change_in_dBFS)
        bitrate = '320k' if 'mp3' in extension else None
        normalized_sound.export(dest_file, format=extension[1:], bitrate=bitrate)
        # Copy metadata to new file (if the original has metadata)
        if tags:
            tags.save(dest_file)


if __name__ == '__main__':
    start = datetime.now()
    main()
    logger.info('Execution time : %s seconds', (datetime.now() - start).seconds)


# TODO : Support more formats
# -----> (Error while importing .wma, error while exporting .m4a, .ape, .aac)
