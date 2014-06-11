#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import random
from recommender import Recommender 

def read_ratings(users_file):
    ratings_file = open(users_file, 'r')
    ratings = {}

    for line in ratings_file:
        values = line.split("::")
        if values[0] not in ratings:
            ratings[values[0]] = [line]
        else:
            ratings[values[0]].append(line)

    return ratings

def remove_some_scores(ratings, users, scores):
    users_wanted_recommendations = {}

    # losuj użytkowników
    for i in range(users):
        random_user = random.choice(ratings.keys())
        # # losuj oceny
        for j in range(scores):
            random_score = random.randint(0, len(ratings[random_user]) -1)
            if random_user not in users_wanted_recommendations:
                users_wanted_recommendations[random_user] = []
            users_wanted_recommendations[random_user].append(ratings[random_user][random_score])
            del ratings[random_user][random_score]
    return users_wanted_recommendations


def save_removed_scores_to_file(ratings):
    pass

def run_training(users_file, iterations, users, scores):
    alphas = [x * (1.0/iterations) for x in range(iterations)]
    ratings = read_ratings(users_file)
    users_wanted_recommendations = remove_some_scores(ratings, users, scores)
    users_recommended = {}

    file_path = save_removed_scores_to_file(ratings)

    recommender = Recommender() # tutaj podać ścieżke do oliwerowo zapisanego pliku


    for alpha in alphas:
        users_recommended[alpha] = {}
        for user in users_wanted_recommendations.keys():
            recommendations = recommender.recommend(users_wanted_recommendations.keys()[0])
            users_recommended[alpha][user] = recommendations

    # teraz porównać trzeba users_wanted_recommendations i users_recommended (rozne struktury danych!!) - porówanie zrobic dla kazdego alfa i sprawdzic wyniki!
    for alpha in users_recommended.keys():
        user_recom = users_recommended[alpha]
        # teraz masz slwonik {user : recomendacje jakie uzyskał w formacie [(,)(,)]}
        # trzeba go porownac z users_wanted_recomendations: {user : [nazwy filmow]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="Number of users to test.")
    parser.add_argument("-s", help="Number of scores to remove for each user.")
    parser.add_argument("-n", help="Number of iterations to test.")
    parser.add_argument("-f", help="File with users' scores.")
    args = parser.parse_args()

    run_training(args.f, int(args.n), int(args.u), int(args.s))

    # wczytaj dane oliwera
    # wylosuj n uzytkownikow
    # usun z nich y ocen i zapamietaj
    # wywolaj na niekompletnych danych recommender (dla kazdego uzytkownika)
    # sprawdz wyniki
    # policz precyzje i recall
