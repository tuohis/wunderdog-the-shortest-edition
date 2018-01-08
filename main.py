#!/usr/bin/env python
"""
@copyright Mikko Tuohimaa 2017
"""
import argparse
from collections import Counter
from datetime import datetime
import urllib.request

import log

LOGLEVEL = log.WARNING
logger = log.get_logger(__file__, level=LOGLEVEL)

def get_source_data(source_file=None):
    start = datetime.now()
    try:
        if source_file:
            with open(source_file, 'r') as f:
                return f.read()
        else:
            logger.debug("Fetching raw data")
            url = 'https://raw.githubusercontent.com/wunderdogsw/wunderpahkina-vol8/master/alastalon_salissa.txt'
            response = urllib.request.urlopen(url)
            data = response.read()
            return data.decode('utf-8')
    finally:
        logger.debug("Data fetching took %s", datetime.now() - start)

def get_dictionary(text):
    logger.debug("Composing dictionary")
    start = datetime.now()
    try:
        dictionary = {}
        for word in text.split():
            try:
                word_len = len(word)
                dictionary[word_len].append(word)
            except KeyError:
                dictionary[word_len] = [word]

        return dictionary
    finally:
        logger.debug("Dictionary composing took %s", datetime.now() - start)

def get_output_lines(dictionary):
    word_count_dict = {key: len(dictionary[key]) for key in dictionary}
    full_output_lines = []
    uneven_output_lines = []
    while dictionary:
        line_words = []
        line_remaining = 80
        try:
            while line_remaining > 0:
                keys = get_keys(word_count_dict, max_length=line_remaining)
                for key in keys:
                    word = dictionary[key].pop()
                    line_words.append(word)
                    line_remaining -= key + 1
                    if not dictionary[key]:
                        del dictionary[key]
                        del word_count_dict[key]
                    else:
                        word_count_dict[key] -= 1

        except ValueError:
            pass
        finally:
            if line_remaining == -1:
                full_output_lines.append(line_words)
            else:
                uneven_output_lines.append(line_words)

    return full_output_lines, uneven_output_lines


def get_keys(word_count_dict, max_length=80, recursion_depth=0):
    """
    Input data structure:
    {
        <word length>: <word count>,
        ...
    }
    """
    keys = sorted(filter(lambda x: x <= max_length, word_count_dict.keys()), reverse=True)
    keys_max = max(keys)

    if max_length <= keys_max and max_length in keys:
        return [max_length]
    else:
        # Find a sequence of keys which add up to max_length
        key_iter = iter(keys)
        while True:
            try:
                biggest_key = next(key_iter)
            except StopIteration:
                if recursion_depth == 0:
                    return keys[0:1]
                else:
                    raise ValueError("Couldn't find a sequence")

            try:
                word_count_dict_copy = {key: word_count_dict[key] for key in keys if key <= biggest_key}
                if word_count_dict_copy[biggest_key] == 1:
                    del word_count_dict_copy[biggest_key]
                else:
                    word_count_dict_copy[biggest_key] -= 1

                return [biggest_key] + get_keys(word_count_dict_copy, max_length - biggest_key - 1, recursion_depth + 1)
            except ValueError:
                pass

def print_output_stats(output_lines):
    logger.info("Output lines count: %d", len(output_lines))
    lengths = Counter([len(l) for l in output_lines])
    logger.info("%s", lengths)

def print_dictionary_stats(dictionary):
    logger.debug("Dictionary shape:")
    for key in sorted(dictionary.keys()):
        logger.debug("  %d: %d words", key, len(dictionary[key]))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str, nargs='?', default=None, help='Source text file name (or omit for fresh download)')
    parser.add_argument('--test', action='store_true', default=False, help='Print output stats instead of full output')
    return parser.parse_args()

def main():
    start = datetime.now()

    args = parse_args()
    if args.test:
        logger = log.get_logger(__file__, level=log.DEBUG)

    data = get_source_data(args.source_file)
    dictionary = get_dictionary(data)

    full_output_lines, uneven_output_lines = get_output_lines(dictionary)

    output_lines = [' '.join(l) for l in full_output_lines + uneven_output_lines]

    if args.test:
        print_dictionary_stats(dictionary)
        print_output_stats(output_lines)

        logger.debug("Script completed in %s", datetime.now() - start)

    else:
        for l in output_lines:
            print(l)

main()
