#!/usr/bin/env python
"""
@copyright Mikko Tuohimaa 2017
"""
from collections import Counter
from datetime import datetime
import log
import urllib.request

LOGLEVEL = log.INFO
logger = log.get_logger(__file__, level=LOGLEVEL)

def get_source_data():
    logger.debug("Fetching raw data")
    url = 'https://raw.githubusercontent.com/wunderdogsw/wunderpahkina-vol8/master/alastalon_salissa.txt'
    start = datetime.now()
    try:
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
    full_output_lines = []
    uneven_output_lines = []
    while dictionary:
        line_words = []
        line_remaining = 80
        try:
            while line_remaining > 0:
                keys = get_keys(dictionary, max_length=line_remaining)
                for key in keys:
                    word = dictionary[key].pop()
                    line_words.append(word)
                    line_remaining -= key + 1
                    if not dictionary[key]:
                        del dictionary[key]
        except ValueError as err:
            if dictionary:
                #logger.warning("Error when parsing: %s", err)
                pass
        finally:
            if line_remaining == -1:
                full_output_lines.append(line_words)
            else:
                uneven_output_lines.append(line_words)

    return full_output_lines, uneven_output_lines

def get_keys(dictionary, max_length=80):
    keys = sorted(filter(lambda x: x <= max_length, dictionary.keys()), reverse=True)
    keys_max = max(keys)

    if max_length <= keys_max and max_length in keys:
        return [max_length]
    elif max_length >= 2 * keys_max:
        return [keys_max]
    else:
        # Find a sequence of keys which add up to max_length
        key_iter = iter(keys)
        while True:
            try:
                biggest_key = next(key_iter)
                new_keys = [biggest_key] + get_keys(dictionary, max_length - biggest_key - 1)
                return new_keys
            except ValueError:
                pass
            except StopIteration:
                break
        return keys[0:1]

def print_output_stats(output_lines):
    logger.info("Output lines count: %d", len(output_lines))
    lengths = Counter([len(l) for l in output_lines])
    logger.info("%s", lengths)

def print_dictionary_stats(dictionary):
    logger.debug("Dictionary shape:")
    for key in sorted(dictionary.keys()):
        logger.debug("  %d: %d words", key, len(dictionary[key]))

def main():
    data = get_source_data()
    dictionary = get_dictionary(data)
    print_dictionary_stats(dictionary)

    full_output_lines, uneven_output_lines = get_output_lines(dictionary)

    output_lines = [' '.join(l) for l in full_output_lines + uneven_output_lines]
    print_output_stats(output_lines)

    dictionary = get_dictionary(' '.join([' '.join(l) for l in uneven_output_lines]))
    print_dictionary_stats(dictionary)

main()