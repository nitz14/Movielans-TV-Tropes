#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

""" This file contains logic of file IN/OUT operations. """

def open_file(path):
    """ Opening a file specified by a path. Returns a file content. """
    f = open(path, 'r')
    return [line for line in f]

def save_file(content, save_path):
    """ Saving content to a file. """
    file = codecs.open(save_path, "w", "utf-8")
    for line in content:
        file.write(line)
    file.close()