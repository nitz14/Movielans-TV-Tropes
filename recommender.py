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

class Recommender:
    def __init__(self, movies = "movie_lens/movies.dat", ratings = "movie_lens/ratings.dat", alpha=0.5):
        self.movie_lens_recommender = MovieLens.MovieLens(movies, ratings)
        self.alpha = alpha

    def recommend(self, userID):
        lista = {}
        recommendations = self.movie_lens_recommender.predict_ratings(userID)
        recommendations1 = dbt_rec([name for (name, _) in self.movie_lens_recommender.get_rated_movies(userID)])

        for recommendation in recommendations:
            if recommendation[0] in recommendations1:
                lista[recommendation[0]] = self.alpha * recommendation[1] + (1 - self.alpha) * recommendations1[recommendation[0]]
                del recommendations1[recommendation[0]]
            else:
                lista[recommendation[0]] = self.alpha * recommendation[1]

        for recommendation in recommendations1.keys():
            lista[recommendation] = (1 - self.alpha) * recommendations1[recommendation]
        return lista
        #return self.movie_lens_recommender.predict_ratings(userID)
        # Aby dzialalo - nalezy skopiowac do tego folderu plik movies.lst i wypakowany plik matrix-20140601.lst .
        #slownik_nazwa_filmu_i_ocena = dbt_rec(["Teen Wolf", "Little Darlings", "Tego nie doda, bo to nie film"], nr_of_wanted_recs)

        #return recommendations

    def set_alpha(self, alpha):
        self.alpha = alpha

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="Input user.")
    parser.add_argument("--i", help="Run program in interactive mode", action="store_true")
    args = parser.parse_args()

    print "Wczytuje dane..."
    recommender = Recommender()
    print "Program jest gotowy do działania!"

    if args.i:
        print "Wpisz exit() aby zatrzymać program."
        while True:
            print "Pytanie:"
            s = raw_input()
            if "exit()" in s:
                exit()
        result = recommender.recommend(s)
        print result
    else:
        result = recommender.recommend(args.u)
        print result
