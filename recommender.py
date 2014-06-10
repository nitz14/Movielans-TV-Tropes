#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from movie_lens import MovieLens
from dbtropes import tropes_recommend as dbt_rec

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
		alpha = 0.5
		lista = {}
        recommendations = self.movie_lens_recommender.predict_ratings(userID)
        recommendations1 = dbt_rec([name for (name, _) in self.movie_lens_recommender.get_rated_movies(userID)])
		for key in recommendations.keys():
			if key in recommendations1:
				lista[key] = alpha * recommendations[key] + (1 - alpha) * recommendations1[key]
		return lista
		#return self.movie_lens_recommender.predict_ratings(userID)
        # Aby dzialalo - nalezy skopiowac do tego folderu plik movies.lst i wypakowany plik matrix-20140601.lst .
        #slownik_nazwa_filmu_i_ocena = dbt_rec(["Teen Wolf", "Little Darlings", "Tego nie doda, bo to nie film"], nr_of_wanted_recs)

        #return recommendations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="Input user.")
    args = parser.parse_args()

    recommender = Recommender()
    result = recommender.recommend(args.u)
    print result
