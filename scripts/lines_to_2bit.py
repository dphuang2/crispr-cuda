"""
This file is for converting a file of lines (guides) into a file of lines in
twobit format.

The file of lines would look like:
ATCATGAC
AGATAGCA
AGACGTAG

And the converted file of twobit format lines would look like this (not
actually a translation of the above example):

0101011101010111
0110010110101011
0101011010101010
"""

from to_2bit import four_bases_to_byte
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file of lines')
    parser.add_argument('file_path', help='file path')
    args = parser.parse_args()

    with open(args.file_path) as fo:
      data = fo.read().split('\n')

    with open("{}.twobit".format(args.file_path), "wb") as fo:
        for i in range(len(data)):
            line = data[i]
            start, end = 0, 4
            translated = bytearray()
            while bool(line[start:end]):
                translated.append(four_bases_to_byte(*line[start:end]))
                start += 4
                end += 4
            fo.write(translated)
            if i < len(data) - 1:
                fo.write('\n')
