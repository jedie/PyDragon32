#!/usr/bin/env python2
# coding: utf-8

"""
    base commandline interface
    ==========================

    :copyleft: 2013 by Jens Diemer
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import argparse
import logging
import sys


def get_log_levels():
    levels = [5] # FIXME
    levels += [level for level in logging._levelNames if isinstance(level, int)]
    return levels

LOG_LEVELS = get_log_levels()


class Base_CLI(object):
    LOG_NAME = None
    DESCRIPTION = None
    EPOLOG = None
    VERSION = None
    DEFAULT_LOG_FORMATTER = "%(message)s"

    def __init__(self):
        self.logfilename = None
        self.log = logging.getLogger(self.LOG_NAME)

        arg_kwargs = {}
        if self.DESCRIPTION is not None:
            arg_kwargs["description"] = self.DESCRIPTION
        if self.EPOLOG is not None:
            arg_kwargs["epilog"] = self.EPOLOG
        if self.VERSION is not None:
            arg_kwargs["version"] = self.VERSION

        self.parser = argparse.ArgumentParser(**arg_kwargs)

        self.parser.add_argument(
            "--verbosity", type=int, choices=LOG_LEVELS, default=logging.WARNING,
            help=(
                "verbosity level to stdout (lower == more output!)"
                " (default: %s)" % logging.INFO
            )
        )
        self.parser.add_argument(
            "--logfile", type=int, choices=LOG_LEVELS, default=logging.INFO,
            help=(
                "verbosity level to log file (lower == more output!)"
                " (default: %s)" % logging.DEBUG
            )
        )
        self.parser.add_argument(
            "--log_format", default=self.DEFAULT_LOG_FORMATTER,
            help=(
                "see: http://docs.python.org/2/library/logging.html#logrecord-attributes"
            )
        )

    def parse_args(self):
        if self.DESCRIPTION is not None:
            print
            print self.DESCRIPTION, self.VERSION
            print "-"*79
            print

        args = self.parser.parse_args()
        return args

    def setup_logging(self, args):
        self.verbosity = args.verbosity
        self.logfile = args.logfile

        formatter = logging.Formatter(args.log_format)

        if self.logfile > 0 and self.logfilename:
            handler = logging.FileHandler(self.logfilename, mode='w', encoding="utf8")
            handler.level = self.logfile
            handler.setFormatter(formatter)
            self.log.addHandler(handler)

        if self.verbosity > 0:
            handler = logging.StreamHandler()
            handler.level = self.verbosity
            handler.setFormatter(formatter)
            self.log.addHandler(handler)

        highest_level = min([self.logfile, self.verbosity])
        self.log.setLevel(highest_level)

        self.log.debug(" ".join(sys.argv))

        verbosity_level_name = logging.getLevelName(self.verbosity)
        self.log.info("Verbosity log level: %s" % verbosity_level_name)

        logfile_level_name = logging.getLevelName(self.logfile)
        self.log.info("logfile log level: %s" % logfile_level_name)


if __name__ == "__main__":
    import doctest
    print doctest.testmod(
        verbose=False
        # verbose=True
    )

    # test via CLI:

    import sys, subprocess

    # bas -> wav
    subprocess.Popen([sys.executable, "../PyDC_cli.py", "--verbosity=10",
#         "--log_format=%(module)s %(lineno)d: %(message)s",
        "../test_files/HelloWorld1.bas", "../test.wav"
    ])

    # wav -> bas
    subprocess.Popen([sys.executable, "../PyDC_cli.py", "--verbosity=10",
#         "--log_format=%(module)s %(lineno)d: %(message)s",
#         "../test.wav", "../test.bas",
        "../test_files/HelloWorld1 origin.wav", "../test_files/HelloWorld1.bas",
    ])
