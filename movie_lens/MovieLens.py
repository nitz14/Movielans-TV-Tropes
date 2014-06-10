#!/usr/bin/env python

from __future__ import division
from math import sqrt

class MovieLens:

    def __init__(self, movies_dat, ratings_dat):
        self.movies = {}
        self.rated_movies = {}
        self.ratings = {}

        """
        Movie information is contained in the file movies_dat 
        Each line of this file represents one movie, 
        and has the following format:
            MovieID::Title::Genres
        """
        movies_file = open(movies_dat, 'r')

        for line in movies_file:
            values = line.split("::")
            self.movies[values[0]] = values[1]

        """
        All ratings are contained in the file ratings_dat 
        Each line of this file represents one rating of one 
        movie by one user, and has the following format:
            UserID::MovieID::Rating::Timestamp
        """
        ratings_file = open(ratings_dat, 'r')
        for line in ratings_file:
            values = line.split("::")
            if values[0] not in self.ratings.keys():
                self.ratings[values[0]] = {}
                for key in self.movies.keys():
                    self.ratings[values[0]][self.movies[key]] = 0
            self.ratings[values[0]][self.movies[values[1]]] = float(values[2])

        self.movies = self.movies.values()
 

    def get_rated_movies(self, user_id):
        rated_movies = []
        for movie in self.movies:
            if self.ratings[user_id][movie] != 0:
                rated_movies.append((movie, self.ratings[user_id][movie]))
        return rated_movies

    """
    This function calculates Pearson product-moment correlation coefficient.
    x and y parameters are users IDs.
    """
    def pcc(self, x, y):
        result = 0
        m = 0
        sum_of_mult = 0
        sum_of_x = 0
        sum_of_y = 0
        sum_of_x_sq = 0
        sum_of_y_sq = 0
        n = len(self.movies)

        for i in range(0, n):
            if self.ratings[x][self.movies[i]] != 0 \
               and self.ratings[y][self.movies[i]] != 0:
                x_rating = self.ratings[x][self.movies[i]]
                y_rating = self.ratings[y][self.movies[i]]
                sum_of_mult += x_rating * y_rating
                sum_of_x += x_rating
                sum_of_x_sq += x_rating ** 2
                sum_of_y += y_rating
                sum_of_y_sq += y_rating ** 2
                m += 1
    
        if m == 0:
            return -1

        top = sum_of_mult - ((sum_of_x * sum_of_y) / m)
        bottom_1 = sum_of_x_sq - ((sum_of_x ** 2) / m)
        bottom_2 = sum_of_y_sq - ((sum_of_y ** 2) / m)
    
        if bottom_1 == 0 or bottom_2 == 0:
            return -1;

        result = top / sqrt(bottom_1 * bottom_2)

        return round(result, 3)


    """
    This function predicts ratings of movies not seen yet by a given person. 
    Predicted ratings are based on correlation between persons' ratings.
    """
    def predict_ratings(self, id):
        not_seen = []
        for movie in self.movies:
            if self.ratings[id][movie] == 0:
                not_seen.append(movie)
    
        corr = {}
        for person in self.ratings.keys():
            if person != id:
                corr[person] = self.pcc(id, person)

        pred_ratings = []
        for movie in not_seen:
            corr_sum = 0
            rating_sum = 0
            for person in self.ratings.keys():
                if self.ratings[person][movie] != 0 and corr[person] > 0:
                    rating_sum += corr[person] * self.ratings[person][movie]
                    corr_sum += corr[person]
            if corr_sum != 0:
                pred_ratings.append((movie, round((rating_sum / corr_sum), 3)))

        return pred_ratings
