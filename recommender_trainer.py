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
    file_name = 'temp.dat'
    f = open(file_name,'w')
    for user in ratings.keys():
        for rating in ratings[user]:  
            f.write(rating) 
    f.close()
    return file_name

def retrieve_recommendations(alphas, removed_scores_file_path, users_wanted_recommendations):
    users_recommended = {}
    print "Initializing recommender..."
    recommender = Recommender("movie_matcher/new_oliwer_data.txt", removed_scores_file_path, 0.5)
    print "Recommender initialization done."

    for alpha in alphas:
        print "Current alfa: ", alpha
        recommender.set_alpha(alpha)
        users_recommended[alpha] = {}
        for user in users_wanted_recommendations.keys():
            print "Recommending for user: ", users_wanted_recommendations.keys()[0]
            recommendations = recommender.recommend(users_wanted_recommendations.keys()[0])
            users_recommended[alpha][user] = recommendations
    print "Recommendations done."
    return users_recommended

def get_movies_list(path):
    movies_file = open(path, 'r')
    movies = {} 
  
    for line in movies_file:
        line_data = line.split("::")        
        movies[line_data[0]] = line_data[1]
    return movies

def print_precision_and_recall_result(alpha, precision, recall):
    print "Alpha: ", alpha
    print "Average precision: ", precision
    print "Average recall: ", recall

def run_training(users_file, iterations, users, scores):
    alphas = [x * (1.0/iterations) for x in range(iterations)]
    ratings = read_ratings(users_file)
    file_path = save_removed_scores_to_file(ratings)
    movies = get_movies_list("movie_matcher/new_oliwer_data.txt")

    users_wanted_recommendations = remove_some_scores(ratings, users, scores)
    users_recommended = retrieve_recommendations(alphas, file_path, users_wanted_recommendations)

    precisions = {}
    recalls = {}

    print "Counting precision and recall"
    for alpha in users_recommended.keys():
        user_recom = users_recommended[alpha]
        precision_sum = 0.0
        recall_sum = 0.0
        for user in user_recom:
            relevant_documents = 0
            for recommendation in users_wanted_recommendations[user]:
                if movies[recommendation.split("::")[1]] in user_recom[user]:
                    relevant_documents += 1
            user_precision = float(relevant_documents) / float(len(user_recom[user]))
            user_recall = float(relevant_documents) / (float(len(users_wanted_recommendations[user])))
            precision_sum += user_precision
            recall_sum += user_recall
        precisions[alpha] = precision_sum / float(len(user_recom))
        recalls[alpha] = recall_sum / float(len(user_recom))        
        print_precision_and_recall_result(alpha, precisions[alpha], recalls[alpha])
    print "Counting precision and recall is done."
    print "Summary: "
    for alpha in precisions.keys():
        print_precision_and_recall_result(alpha, precisions[alpha], recalls[alpha])


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
