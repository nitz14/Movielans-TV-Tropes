#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

""" This file contains logic of file IN/OUT operations. """

# def open_file(path):
#     """ Opening a file specified by a path. Returns a file content. """
#     f = open(path, 'r')
#     insides = u""
#     counter = 1
#     for line in f:
#         # Just to see that somthing's happening.
#         if counter % 1000 == 0:
#             print str(counter/10) + " ads loaded."
#         counter += 1
#         insides += line
#     return insides

def save_file(content, save_path):
    """ Saving content to a file. """
    file = codecs.open(save_path, "w", "utf-8")
    for line in content:
        file.write(line)
    file.close()