Pynormalize
===========


.. image:: https://travis-ci.org/giannisterzopoulos/pynormalize.svg?branch=master
        :target: https://travis-ci.org/giannisterzopoulos/pynormalize
        :alt: Build Status


.. image:: https://badge.fury.io/py/pynormalize.svg
        :target: https://pypi.python.org/pypi/pynormalize
        :alt: PyPI Version


|
| **Command line utility for audio normalization**
|
| It saves the metadata of the original files. Currently supported formats : WAV, FLAC, MP3, OGG, WEBM and MP4.

Usage
-----
- Either select multiple files to normalize : ``pynormalize --files audio1.mp3 /dir/audio2.flac``
- or edit all the audio files in current directory : ``pynormalize --all``

you can also import pynormalize:

.. code-block:: python

    import pynormalize

    Files = ['audio.wav']
    target_dbfs = -13.5

    pynormalize.process_files(
        Audio=Files,
        target_dbfs=target_dbfs,
    )


Installation
------------

Clone it ::

   >> git clone https://github.com/giannisterzopoulos/pynormalize.git
   >> cd pynormalize
   >> pip install .

or install via PyPI : ``pip install pynormalize``


Requirements
------------
| FFmpeg is required for opening and saving non-wav files. Get it from `here`_ and put it in the 
| pynormalize directory (where pynormalize.py is stored) or in your system PATH variable.
| Pynormalize supports **Python 3.4-3.6**

.. _`here`: https://www.ffmpeg.org/
