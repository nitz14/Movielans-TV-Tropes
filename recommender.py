#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from movie_lens import MovieLens

"""
Jak to powinno działać:

dla każdego filmu f policz score(f) = SUMA PO WSZYSTKICH FILMACH f2 ( średni_score(f2) * odleglosc(f,f2) ) 

odleglosc(f,f2) = waga1 * odleglosc_ocenowa(f,f2) + waga2 + 1 / (1 + odleglosc_tropowa(f,f2))

"""


class RecommendationWeights:

    def __init__(self, score_weight, trope_weight):
        self.score_weight = score_weight
        self.trope_weight = trope_weight


class Recommender:
    def __init__(self):
        self.movie_lens_recommender = MovieLens.MovieLens("movie_lens/test_movies.dat", "movie_lens/test_ratings.dat")

    def recommend(self, userID):
        global EXAMPLE_TROPE_RECOMMENDATION, EXAMPLE_SCORE_RECOMMENDATION

        recommendations = self.movie_lens_recommender.predict_ratings(userID)
        return recommendations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="Input user.")
    args = parser.parse_args()

    recommender = Recommender()
    result = recommender.recommend(args.u)
    print result