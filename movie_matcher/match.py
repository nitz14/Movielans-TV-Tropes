#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trie_program
import argparse
import operator

def read_movies(match_with_file):
    movies_file = open(match_with_file, 'r')
    movies = [line.split("@|@")[0][1:-2] for line in movies_file]
    return movies

def read_match_file(file_to_match):
    movies_file = open(file_to_match, 'r')
    movies = dict()
    for line in movies_file:
        line_data = line.split("::")        
        movie_name = line_data[1][:-7]
        if movie_name.endswith(", The"):
            movie_name = "The " + movie_name[:-5]
        movies[line_data[0]] = movie_name
    return movies

def update_match_file(file_to_match, movies_matched):
    movies_file = open(file_to_match, 'r')
   
    replaced_lines = []
    for line in movies_file:
        line_data = line.split("::")        
        line_data[1] = movies_matched[line_data[0]]
        replaced_lines.append("::".join(line_data))
    return replaced_lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="File to match (will be updated).")
    parser.add_argument("-v", help="File to match with")
    args = parser.parse_args()

    movies = read_movies(args.v)
    trie_program.initDict(movies)

    movies_to_match = read_match_file(args.f)

    for movie_key in movies_to_match.keys():
        movie = movies_to_match[movie_key]
        databaseMatches = trie_program.search(movie, 3)
        databaseMatches.sort(key=operator.itemgetter(1))
        if len(databaseMatches)!=0:
            movies_to_match[movie_key] = databaseMatches[0][0] 
    new_lines = update_match_file(args.f, movies_to_match)
    print "".join(new_lines)