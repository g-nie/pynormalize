#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0612,W0703


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


Supported = ('.wav', '.flac', '.mp3', '.ogg', '.webm', '.mp4')


# Configure logging
def get_logger(mod_name):
    log = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log


logger = get_logger(__name__)


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
    start = datetime.now()
    try:
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
    except KeyboardInterrupt:
        logger.warning('Interrupted.')
        sys.exit()
    else:
        logger.info('Execution time : %s seconds', (datetime.now() - start).seconds)


def process_files(Files, target_dbfs, directory='NORMALIZED'):
    """
    Normalize the audio files, given their paths and the decibels
    relative to full scale (dbfs). Default argument 'directory' can be overwritten.
    """
    Files = [os.path.abspath(f) for f in Files]
    if not os.path.exists(directory):  # Create the directory if it doesn't exist
        os.mkdir(directory)

    show_message = True
    for count, audio_file in enumerate(Files):
        try:
            audio_file = _valid_files(audio_file)
        except argparse.ArgumentTypeError as e:
            logger.error('%s , Skipping...', str(e))
            continue

        (dirname, filename) = os.path.split(audio_file)
        (shortname, extension) = os.path.splitext(filename)
        logger.info('(%s of %s) Processing file : "%s"', count + 1, len(Files), filename)

        # Extract metadata information
        try:
            tags = mutagen.File(audio_file, easy=True)
        except Exception as e:
            logger.error('%s , Skipping...', str(e))
            continue

        # Export the edited file
        try:
            song = AudioSegment.from_file(audio_file, format=extension[1:])
        except FileNotFoundError:  # Could not locate FFmpeg
            if show_message:
                logger.warning('WARNING: Could not locate FFmpeg, skipping non-wav files.')
                show_message = False
            continue
        change_in_dBFS = target_dbfs - song.dBFS
        dest_file = os.path.join(directory, filename)
        normalized_sound = song.apply_gain(change_in_dBFS)
        bitrate = '320k' if 'mp3' in extension else None
        normalized_sound.export(dest_file, format=extension[1:], bitrate=bitrate)
        # Copy metadata to new file (if the original has metadata)
        if tags:
            tags.save(dest_file)


if __name__ == '__main__':
    main()


# TODO : Support more formats
# -----> (Error while importing .wma, error while exporting .m4a, .ape, .aac)
