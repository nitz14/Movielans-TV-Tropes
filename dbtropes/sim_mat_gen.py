#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import logging
import numpy
import sys

from scipy.spatial.distance import pdist

from files import open_file as ofile
from files import save_file as sfile

logger = None

# Availible metrics:
# http://docs.scipy.org/doc/scipy/reference/spatial.distance.html
# Vectors are rows
def create_similarity_matrix(matrix, metric='euclidean'):
    ret_mat = []
    for iterator in range(len(matrix)):
        nxt_row = []
        for jterator in range(iterator):
            nxt_val = pdist([matrix[iterator], matrix[jterator]], metric)[0]
            nxt_row.append(nxt_val)
        ret_mat.append(nxt_row)
        if iterator % 100 == 0:
            #logger.warning(str(iterator) + " movies completed.")
            print str(iterator) + " movies completed."
    return ret_mat

if __name__ == '__main__':
    logger = logging.getLogger('cutter')
    hdlr = logging.FileHandler('log.log')
    formatter = logging.Formatter('%(asctime)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

    metric = 'euclidean'

    try:
        metric = sys.argv[1]
        print metric
    except:
        logger.warning('Unknown metric given as argument!')
        print 'Unknown metric given as argument!'

    logger.warning('Start')
    print 'Start'

    matrix = ofile("matrix-20140601.lst")

    logger.warning('Matrix loaded!')
    print 'Matrix loaded!'

    matrix = zip(*matrix)

    logger.warning('Matrix represented as floats!')
    print 'Matrix represented as floats!'

    # similarity_mtx = create_similarity_matrix(matrix)
    similarity_mtx = pdist(matrix, metric)

    logger.warning('Distances calculated!')
    print 'Distances calculated!'

    numpy.savetxt('similarity.lst', similarity_mtx, fmt="%s")

    logger.warning('Triangle matrix of distances saved.')
    print 'Triangle matrix of distances saved.'
