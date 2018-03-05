import argparse
import os
import sys
from datetime import datetime
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.flac import FLAC


TARGET_DBFS = -13.5  # dBs for the new files
DIRECTORY = '_NORMALIZED'  # Directory for the edited files


# Check if given files exist in the system and are supported
def valid_files(arg):
    if os.path.isfile(arg):
        if arg.endswith('.mp3') or arg.endswith('.flac'):
            return arg
        else:
            msg = 'File type is not supported : {}'.format(arg)
            raise argparse.ArgumentTypeError(msg)
    else:
        msg = 'File cannot be found : {}'.format(arg)
        raise argparse.ArgumentTypeError(msg)


start = datetime.now()

if not os.path.exists(DIRECTORY):  # Create the directory if it doesn't exist
    os.mkdir(DIRECTORY)

# Accept only one of the arguments : either --files or --all
parser = argparse.ArgumentParser(description='Normalize audio files to a specified level of dBs (supports .mp3 and .flac)')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--files', help='Audio files to normalize.', type=valid_files, nargs='+')
group.add_argument('-a', '--all', help='Process all the audio files in current directory.', action='store_true')
args = parser.parse_args()

if args.all:  # User selected --all
    Audio = []
    for f in os.listdir():
        if f.endswith('.mp3') or f.endswith('.flac'):
            Audio.append(f)
    if not Audio:
        print('Current directory has no audio files.')
        sys.exit(1)
else:  # User selected --files
    Audio = args.files

for file in Audio:
    if os.sep in file:
        filename = file[file.rfind(os.sep) + 1:]
    else:
        filename = file
    extension = file[file.rfind('.') + 1:]
    # Extract metadata information
    if extension == 'mp3':
        form = 'mp3'
        title = MP3(file).tags.get('TIT2', '')
        artist = MP3(file).tags.get('TPE1', '')
        album = MP3(file).tags.get('TALB', '')
        tracknumber = MP3(file).tags.get('TRCK', '')
    else:
        form = 'flac'
        title = FLAC(file).get('title')[0] if FLAC(file).get('title') else ''
        artist = FLAC(file).get('artist')[0] if FLAC(file).get('artist') else ''
        album = FLAC(file).get('album')[0] if FLAC(file).get('album') else ''
        tracknumber = FLAC(file).get('tracknumber')[0] if FLAC(file).get('tracknumber') else ''
    # Export the edited file
    song = AudioSegment.from_file(file, format=form)
    change_in_dBFS = TARGET_DBFS - song.dBFS
    dest_file = os.path.join(DIRECTORY, filename)
    normalized_sound = song.apply_gain(change_in_dBFS)
    normalized_sound.export(dest_file, format=form)

    # Write metadata in new file
    if extension == 'mp3':
        audio = MP3(dest_file)
    else:
        audio = FLAC(dest_file)
    audio["title"] = title
    audio["artist"] = artist
    audio["album"] = album
    audio["tracknumber"] = tracknumber
    audio.save()

print('Execution time : {} seconds'.format((datetime.now() - start).seconds))
