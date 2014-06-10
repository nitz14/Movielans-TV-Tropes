#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from files import open_file as ofile

def movies_to_nrs(s_movies):
    movies = ofile("movies.lst")
    counter = 0
    m_counter = 0
    ret_list = []
    for line in movies:
        if s_movies[counter][1] < line[1]:
            counter += 1
        if counter == len(s_movies):
            return ret_list
        if s_movies[counter] == line.split(" @|@ ")[0][1:-1]:
            ret_list.append(m_counter)
            counter += 1
        if counter == len(s_movies):
            return ret_list
        m_counter += 1
    return ret_list

def tropes_recommend(list_of_movies, nr_of_wanted_recs=10):
    logger = logging.getLogger('cutter')
    hdlr = logging.FileHandler('log.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

    movies = movies_to_nrs(sorted(list_of_movies))
    logger.warning('Movies transformed into numbers - ' + str(len(movies)) + ' transformed correctly!')
    print 'Movies transformed into numbers - ' + str(len(movies)) + ' transformed correctly!'

    if len(movies) == 0:
        return dict()

    matrix = ofile("matrix-20140601.lst")
    logger.warning('Matrix loaded!')
    print 'Matrix loaded!'

    row_nr = len(matrix)
    style_vector = []
    for _ in range(row_nr):
        style_vector.append(0)
    for movie in movies:
        for iterat in range(row_nr):
            style_vector[iterat] += int(matrix[iterat][movie])

    logger.warning('Style vector created!')
    print 'Style vector created!'

    movie_list = ofile("movies.lst")
    # matrix_t = zip(*matrix)
    recommended = []
    for movie in range(len(movie_list)):
        if movie not in movies:
            suma = 0
            for iterat in range(row_nr):
                suma += style_vector[iterat] * int(matrix[iterat][movie])
            if suma != 0:
                recommended.append((suma, movie_list[movie]))
        if movie % 100 == 0:
            logger.warning(str(movie) + ' recommendations created!')
            print str(movie) + ' recommendations created!'

    recommended = sorted(recommended, key=lambda tup: tup[0], reverse=True)

    logger.warning('Recommendations created!')
    print 'Recommendations created!'

    if len(recommended) >= nr_of_wanted_recs:
        recommended = recommended[:nr_of_wanted_recs]
    return dict([(movie_str.split(" @|@ ")[0][1:-1], score) for (score, movie_str) in recommended])

if __name__ == '__main__':
    list_of_movies = []
    for line in sys.stdin:
        if len(line[:-1]) > 0:
            list_of_movies.append(line[:-1])
    rec_list = tropes_recommend(list_of_movies)
    for movie in rec_list:
        print movie + " scored " + str(rec_list[movie]) + " points!"
