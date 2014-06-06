#!/usr/bin/env python

from __future__ import division
from math import sqrt

class MovieLens:

    def __init__(self, movies_dat, ratings_dat):
        self.movies = {}
        self.rated_movies = {}

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
            if values[0] not in self.rated_movies.keys():
                self.rated_movies[values[0]] = []
            movie_and_rating = (self.movies[values[1]], values[2])
            self.rated_movies[values[0]].append(movie_and_rating)

        self.movies = self.movies.values()
 
    def is_rated(self, user_id, title):
        if user_id not in self.rated_movies.keys():
            return False
        if len([i for i, v in enumerate(self.rated_movies[user_id]) if v[0] == title]) == 0:
            return False
        return True


    def get_rating(self, user_id, title):
        if self.is_rated(user_id, title):
            list = [i for i, v in enumerate(self.rated_movies[user_id]) if v[0] == title]
            index = list[0]
            return float(self.rated_movies[user_id][index][1])
        return 0


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

        for i in range(0, len(self.movies)):
            if self.is_rated(x, self.movies[i]) \
               and self.is_rated(y, self.movies[i]):
                x_rating = self.get_rating(x, self.movies[i])
                y_rating = self.get_rating(y, self.movies[i])
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
            if not self.is_rated(id, movie):
                not_seen.append(movie)
    
        corr = {}
        for person in self.rated_movies.keys():
            if person != id:
                corr[person] = self.pcc(id, person)
 
        ratings = []
        for movie in not_seen:
            corr_sum = 0
            rating_sum = 0
            for person in self.rated_movies.keys():
                if self.is_rated(person, movie) and corr[person] > 0:
                    rating_sum += corr[person] * self.get_rating(person, movie)
                    corr_sum += corr[person]
            if corr_sum != 0:
                ratings.append((movie, round((rating_sum / corr_sum), 3)))

        return ratings
