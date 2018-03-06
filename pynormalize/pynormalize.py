import argparse
import os
import sys
import warnings
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

start = datetime.now()

Supported = ('.wav', '.flac', '.mp3', '.ogg', '.webm', '.mp4')


# Check if given files exist in the file system
def valid_files(arg):
    if not os.path.isfile(arg):
        msg = 'File cannot be found : {}'.format(arg)
        raise argparse.ArgumentTypeError(msg)
    elif not arg.endswith(Supported):
        msg = 'File format is not supported : {}'.format(arg)
        raise argparse.ArgumentTypeError(msg)
    else:
        return arg


parser = argparse.ArgumentParser(description="""Normalize audio files to a specified level of dBs
    (supports .mp3 and .flac) \nSupported audio formats : .wav, .flac, .mp3, .ogg, .webm, .mp4""")
parser.add_argument('-d', '--decibels', help='Decibels to use in normalization', type=float, default='-13.5')
# Accept only one of these arguments : either --files or --all
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--files', help='Audio files to normalize.', type=valid_files, nargs='+')
group.add_argument('-a', '--all', help='Process all the audio files in current directory.', action='store_true')
args = parser.parse_args()

target_dbfs = args.decibels
if args.all:  # User selected --all
    Audio = []
    for f in os.listdir():
        if f.endswith(Supported):
            Audio.append(f)
    if not Audio:
        print('Current directory has no audio files.')
        sys.exit(1)
else:  # User selected --files
    Audio = args.files

show_message = True
for file in Audio:
    (dirname, filename) = os.path.split(file)
    (shortname, extension) = os.path.splitext(filename)

    # Extract metadata information
    tags = mutagen.File(file, easy=True)
    # Export the edited file
    try:
        song = AudioSegment.from_file(file, format=extension[1:])
    except FileNotFoundError:  # Could not locate FFmpeg
        if show_message:
            print('WARNING : Could not locate FFmpeg, skipping non-wav files.')
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

print('Execution time : {} seconds'.format((datetime.now() - start).seconds))

# TODO : SUPPORT MORE FORMATS (ERROR IMPORTING .WMA - ERROR EXPORTING .M4A, .APE, .AAC)
# TODO : USE LOGGING
