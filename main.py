#!/usr/bin/env python
"""
@copyright Mikko Tuohimaa 2017
"""
from collections import Counter
from datetime import datetime
import log
import urllib.request

logger = log.get_logger(__file__)

def get_source_data():
    logger.info("Fetching raw data")
    url = 'https://raw.githubusercontent.com/wunderdogsw/wunderpahkina-vol8/master/alastalon_salissa.txt'
    start = datetime.now()
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        return data.decode('utf-8')
    finally:
        logger.info("Data fetching took %s", datetime.now() - start)

def get_dictionary(text):
    logger.info("Composing dictionary")
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
        logger.info("Dictionary composing took %s", datetime.now() - start)

def get_output_lines(dictionary):
    full_output_lines = []
    uneven_output_lines = []
    while dictionary:
        line_words = []
        line_remaining = 80
        try:
            while line_remaining > 0:
                key = get_key(dictionary, max_length=line_remaining)
                word = dictionary[key].pop()
                line_words.append(word)
                line_remaining -= key + 1
                if not dictionary[key]:
                    del dictionary[key]
        except ValueError as err:
            if dictionary:
                logger.warning("Error when parsing: %s", err)
        finally:
            if line_remaining == -1:
                full_output_lines.append(line_words)
            else:
                uneven_output_lines.append(line_words)

    return full_output_lines, uneven_output_lines

def get_key(dictionary, max_length=80):
    keys = dictionary.keys()
    if max_length in dictionary.keys():
        return max_length
    return max(filter(lambda x: x <= max_length, dictionary.keys()))

def print_output_stats(output_lines):
    logger.info("Output lines count: %d", len(output_lines))
    lengths = Counter([len(l) for l in output_lines])
    logger.info("%s", lengths)

def main():
    data = get_source_data()
    output_lines = []
    for _ in range(5):
        dictionary = get_dictionary(data)
        logger.info("Dictionary shape:")
        for key in sorted(dictionary.keys()):
            logger.info("  %d: %d words", key, len(dictionary[key]))

        full_output_lines, uneven_output_lines = get_output_lines(dictionary)
        logger.info("Line count: full=%d, uneven=%d, total=%d", len(full_output_lines), len(uneven_output_lines), len(full_output_lines) + len(uneven_output_lines))

        output_lines += full_output_lines
        data = ' '.join((' '.join(l) for l in uneven_output_lines))

    output_lines += uneven_output_lines
    logger.info(' '.join(uneven_output_lines[0]))

main()