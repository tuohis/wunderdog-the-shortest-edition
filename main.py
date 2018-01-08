#!/usr/bin/env python3
"""
@copyright Mikko Tuohimaa 2018
"""
import argparse
import urllib.request

import log
from word_packer import WordPacker

def get_source_data(source_file=None):
    if source_file:
        with open(source_file, 'r') as f:
            return f.read()
    else:
        url = 'https://raw.githubusercontent.com/wunderdogsw/wunderpahkina-vol8/master/alastalon_salissa.txt'
        response = urllib.request.urlopen(url)
        data = response.read()
        return data.decode('utf-8')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str, nargs='?', default=None, help='Source text file name (or omit for fresh download)')
    parser.add_argument('--test', action='store_true', default=False, help='Print output stats instead of full output')
    return parser.parse_args()

def main():
    args = parse_args()

    data = get_source_data(args.source_file)
    packer = WordPacker(line_length=80)
    output_lines = packer.pack(data)

    if args.test:
        logger = log.AlastaloLogger(__file__, level=log.DEBUG)
        logger.print_output_stats(output_lines)

        logger.debug("Script completed in %s", datetime.now() - start)

    else:
        for l in output_lines:
            print(l)

main()
