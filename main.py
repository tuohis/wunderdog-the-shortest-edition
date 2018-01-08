#!/usr/bin/env python
"""
@copyright Mikko Tuohimaa 2017
"""
import argparse
from datetime import datetime
import urllib.request

import log

def get_source_data(source_file=None):
    if source_file:
        with open(source_file, 'r') as f:
            return f.read()
    else:
        url = 'https://raw.githubusercontent.com/wunderdogsw/wunderpahkina-vol8/master/alastalon_salissa.txt'
        response = urllib.request.urlopen(url)
        data = response.read()
        return data.decode('utf-8')

def get_dictionary(text):
    dictionary = {}
    for word in text.split():
        try:
            word_len = len(word)
            dictionary[word_len].append(word)
        except KeyError:
            dictionary[word_len] = [word]

    return dictionary

class NoSequenceFoundError(ValueError):
    pass

def get_output_lines(dictionary):
    word_count_dict = {key: len(dictionary[key]) for key in dictionary}
    output_lines = []

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
            output_lines.append(' '.join(line_words))

    return output_lines


def get_keys(word_count_dict, max_length=80):
    """
    Input data structure:
    {
        <word length>: <word count>,
        ...
    }
    """
    def get_keys_recursive(word_count_dict, max_length=80):
        keys = sorted(filter(lambda x: x <= max_length, word_count_dict.keys()), reverse=True)
        try:
            keys_max = max(keys)
        except ValueError:
            raise NoSequenceFoundError("Empty dict")

        if max_length <= keys_max and max_length in keys:
            return [max_length]
        else:
            # Find a sequence of keys which add up to max_length
            for biggest_key in keys:
                try:
                    word_count_dict_copy = {key: word_count_dict[key] for key in keys if key <= biggest_key}
                    if word_count_dict_copy[biggest_key] == 1:
                        del word_count_dict_copy[biggest_key]
                    else:
                        word_count_dict_copy[biggest_key] -= 1

                    return [biggest_key] + get_keys_recursive(word_count_dict_copy, max_length - biggest_key - 1)
                except NoSequenceFoundError:
                    pass

        raise NoSequenceFoundError("Couldn't find a sequence")

    try:
        return get_keys_recursive(word_count_dict, max_length)
    except NoSequenceFoundError:
        return [max(filter(lambda k: k <= max_length, word_count_dict))]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str, nargs='?', default=None, help='Source text file name (or omit for fresh download)')
    parser.add_argument('--test', action='store_true', default=False, help='Print output stats instead of full output')
    return parser.parse_args()

def main():
    start = datetime.now()

    args = parse_args()

    data = get_source_data(args.source_file)
    dictionary = get_dictionary(data)

    output_lines = get_output_lines(dictionary)

    if args.test:
        logger = log.AlastaloLogger(__file__, level=log.DEBUG)
        logger.print_dictionary_stats(dictionary)
        logger.print_output_stats(output_lines)

        logger.debug("Script completed in %s", datetime.now() - start)

    else:
        for l in output_lines:
            print(l)

main()
