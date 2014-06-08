#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from files import save_file as sfile

if __name__ == '__main__':
    logger = logging.getLogger('cutter')
    hdlr = logging.FileHandler('log.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)

    logger.warning('Start')

    # Create movies list
    movies = []

    # Create tropes list
    tropes_list = []
    tropes_set = set()

    # Create matrix
    not_resolved = dict()
    temp_con_list = []

    f = open("dbtropes-20140601.nt", 'r')
    for line in f:
        # Info about Film names.
        if (("<http://www.w3.org/2000/01/rdf-schema#label>" in line) and ("<http://dbtropes.org/resource/Film/" in line)):
            parts = line[:-1].strip().split()
            movies.append(parts[0] + " @|@ " + parts[2])
        # All film <-> trope connections.. and tropes.
        elif (("<http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature>" in line) and ("<http://dbtropes.org/resource/Film/" in line)):
            name = line[:-1].strip().split()[2].strip()
            tropes_list.append(name)
            not_resolved[name] = line[:-1].strip().split()[0]
        elif "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>" in line:
            names = line[:-1].strip().split()
            name = names[0]
            if name in tropes_list:
                tropes_set.add(names[2].split("/")[5][:-1])
                tropes_list.remove(name)
            if names[0] in not_resolved:
                temp_con_list.append((names[2].split("/")[5][:-1], not_resolved[names[0]]))
                del not_resolved[names[0]]

    movies = sorted(movies)

    logger.warning('Film list created - ' + str(len(movies)) + ' films.')

    save_file('\n'.join(movies), "movies.lst")

    logger.warning('Film list saved.')

    tropes_list = sorted(tropes_set)

    logger.warning('Tropes list created - ' + str(len(tropes_list)) + ' tropes.')

    save_file('\n'.join(tropes_list), "tropes.lst")

    logger.warning('Tropes list saved.')

    connections_list = []
    for elem in sorted(sorted(temp_con_list, key=lambda tup: tup[1]), key=lambda tup: tup[0]):
        connections_list.append(elem[0] + " @|@ " + elem[1])

    logger.warning('Connections list created - ' + str(len(connections_list)) + ' connections.')

    # Removing UNIQUE tropes
    # to_del = []
    # for trope in tropes_list:
    #     if len([trope_ins for trope_ins in connections_list if trope in trope_ins]) <= 1:
    #         to_del += [trope]
    # for trope in to_del:
    #     tropes_list.remove(trope)
    #     connections_list = [connection for connection in connections_list if trope not in connection]

    # logger.warning('Only unique tropes remaining.' + str(len(tropes_list)) + " tropes. " + str(len(connections_list)) + " connections.")

    # # TODO - transform to MATRIX!
    # for elem in connections_list:
    #     print elem

    logger.warning('End.')
