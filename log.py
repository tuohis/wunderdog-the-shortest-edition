"""
@copyright Mikko Tuohimaa 2018
"""

from collections import Counter
import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING

class AlastaloLogger(logging.Logger):
    def __init__(self, name, level=WARNING):
        super().__init__(logging.getLogger(name))
        self.setLevel(level)

        # create console handler and set level to info
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def print_output_stats(self, output_lines):
        self.info("Output lines count: %d", len(output_lines))
        lengths = Counter([len(l) for l in output_lines])
        self.info("Line lengths count: %s", lengths)

    def print_dictionary_stats(self, dictionary):
        self.debug("Dictionary shape:")
        for key in sorted(dictionary.keys()):
            self.debug("  %d: %d words", key, len(dictionary[key]))
