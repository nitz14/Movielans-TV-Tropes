#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

""" This file contains logic of file IN/OUT operations. """

def save_file(content, save_path):
    """ Saving content to a file. """
    file = codecs.open(save_path, "w", "utf-8")
    for line in content:
        file.write(line)
    file.close()