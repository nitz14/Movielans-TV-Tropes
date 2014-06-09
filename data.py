#!/usr/bin/env python
# -*- coding: utf-8 -*-

from movie_lens import MovieLens, pcc
import random

class data:
	def database():
		lista = []
		n = random.randint(0, 6040)
		lista.append(n)
		while(len(lista)<100):
			m = random.randint(0,6040)
			if( not (m in lista) and pcc(n,m)>0.4 ):
				lista.append(m)
		file = open(nowy, 'w')
		for element in lista:
			file.writelines(element)
		file.close()