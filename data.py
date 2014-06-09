#!/usr/bin/env python
# -*- coding: utf-8 -*-

from movie_lens import MovieLens
import random

def database():
	lista = []
	n = random.randint(0, 6040)
	lista.append(n)
	comparator = MovieLens.MovieLens("movie_lens/movies.dat", "movie_lens/ratings.dat")
	while(len(lista)<100):
		m = random.randint(0,6040)
		if( not (m in lista) and comparator.pcc(n,m)>0.4 ):
			lista.append(m)
	file = open("nowy.out", 'w')
	for element in lista:
		file.writelines(element)
	file.close()

if __name__ == '__main__':
	database()
