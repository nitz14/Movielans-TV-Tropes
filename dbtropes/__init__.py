#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from files import save_file as sfile

if __name__ == '__main__':
    list_of_movies = []
    for line in sys.stdin:
        if len(line[:-1] > 0):
            list_of_movies.append(line[:-1])
