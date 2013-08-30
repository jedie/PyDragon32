#!/usr/bin/env python2
# coding: utf-8

"""
    Python dragon 32 converter
    ==========================

    :copyleft: 2013 by Jens Diemer
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from CassetteObjects import Cassette
from PyDC import BitstreamHandler
from wave2bitstream import Wave2Bitstream, Bitstream2Wave
from utils import print_bitlist


__version__ = (0, 1, 0, 'dev')
VERSION_STRING = '.'.join(str(part) for part in __version__)

TITLE_LINE = "PyDC v%s copyleft 2013 by htfx.de - Jens Diemer, GNU GPL v3 or above" % VERSION_STRING


def bas2wav(source_filepath, destination_filepath, cfg):
    # Create a bitstream from a existing .bas file:

    c = Cassette(cfg)

    c.add_from_bas(source_filepath)
    c.print_debug_info()
    bitstream = c.get_as_bitstream()
#     print_bitlist(bitstream)

    bw = Bitstream2Wave(bitstream, cfg)
    bw.write_wave(destination_filepath)


def wav2bas(source_filepath, destination_filepath, cfg):
    # get bitstream generator from WAVE file:
    bitstream = iter(Wave2Bitstream(source_filepath, cfg))

    # store bitstream into python objects
    bh = BitstreamHandler(cfg)
    bh.feed(bitstream)

    # save .bas file
    bh.cassette.save_bas(destination_filepath)



if __name__ == "__main__":
#     import doctest
#     print doctest.testmod(
#         verbose=False
#         # verbose=True
#     )
    print TITLE_LINE

    from configs import Dragon32Config
    cfg = Dragon32Config()

#     wav2bas(
#         "../test_files/HelloWorld1 origin.wav",
#         "../HelloWorld1 origin.bas",
#         cfg
#     )

    bas2wav(
        "../test_files/HelloWorld1.bas",
        "../HelloWorld1 created.wav",
        cfg
    )
    print "\n --- END ---"
