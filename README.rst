Pynormalize
===========
Command line utility for audio normalization. It saves the metadata of the original files.
MP3 and FLAC files are currently supported.

How to use it
-------------
- Either select multiple files to normalize : ``pynormalize.py -f audio1.mp3 /dir/audio2.flac``
- or edit all the audio files in current directory : ``pynormalize.py -a``

Requirements
------------
- Python 3.4+
- pydub 0.21.0+
- mutagen 1.40.0+
- FFmpeg 3.4+ is also required for opening and saving non-wav files. Get it from `here`_

.. _`here`: https://www.ffmpeg.org/
