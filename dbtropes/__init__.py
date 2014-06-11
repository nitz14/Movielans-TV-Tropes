#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from files import open_file as ofile

def get_similarity(sim_matrix, movie, rated, size):
    if movie < rated:
        right = movie
        left = rated
    else:
        right = rated
        left = movie
    return (1.0/(1.0 + float(sim_matrix[sum(range(left - 1)) + right])))

def movies_to_nrs(s_movies):
    movies = ofile("movies.lst")
    counter = 0
    m_counter = 0
    ret_list = []
    for line in movies:
        if s_movies[counter][0][1] < line[1]:
            counter += 1
        if counter == len(s_movies):
            return ret_list
        if s_movies[counter][0] == line.split(" @|@ ")[0][1:-1]:
            ret_list.append((m_counter, s_movies[counter][1]))
            counter += 1
        if counter == len(s_movies):
            return ret_list
        m_counter += 1
    return ret_list

def tropes_recommend(list_of_movies, nr_of_wanted_recs=10):
    logger = logging.getLogger('cutter')
    hdlr = logging.FileHandler('log.log')
    formatter = logging.Formatter('%(asctime)s  %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

    movies = movies_to_nrs(sorted([(title, score) for (title, score) in list_of_movies]))
    movies_set = set(movie for (movie, _) in movies)
    logger.warning('Movies transformed into numbers - ' + str(len(movies)) + ' transformed correctly!')
    # print 'Movies transformed into numbers - ' + str(len(movies)) + ' transformed correctly!'

    if len(movies) == 0:
        return dict()

    matrix = ofile("matrix-20140601.lst")
    logger.warning('Matrix loaded!')
    # print 'Matrix loaded!'

    sim_matrix = ofile("similarity.lst")
    logger.warning('Similarity matrix loaded!')
    # print 'Similarity matrix loaded!'

    movie_list = ofile("movies.lst")
    weight_sum = sum(float(score) for (_, score) in movies)
    recommended = []
    for movie in range(len(movie_list)):
        if movie not in movies_set:
            suma = 0.0
            sum_of_sim = 0.0
            for rated in movies:
                sim = get_similarity(sim_matrix, movie, rated[0], len(movie_list))
                sum_of_sim += sim
                suma += sim * (float(rated[1]) - 2.5)
            if sum_of_sim > 0.0:
                suma = (suma / (sum_of_sim))
                if suma > -1.0:
                    recommended.append((suma + 2.5, movie_list[movie]))
        # if movie % 100 == 0:
        #     logger.warning(str(movie) + ' recommendations created!')
            # print str(movie) + ' recommendations created!'

    recommended = sorted(recommended, key=lambda tup: tup[0], reverse=True)

    logger.warning('Recommendations created!')
    # print 'Recommendations created!'

    if len(recommended) >= nr_of_wanted_recs:
        recommended = recommended[:nr_of_wanted_recs]
    return dict([(movie_str.split(" @|@ ")[0][1:-1], round(score)) for (score, movie_str) in recommended])

if __name__ == '__main__':
    list_of_movies = []
    for line in sys.stdin:
        if len(line[:-1]) > 0:
            list_of_movies.append(line[:-1].split(" @|@ "))
    rec_list = tropes_recommend(list_of_movies)
    for movie in rec_list:
        print movie + " scored " + str(rec_list[movie]) + " points!"
