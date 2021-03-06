#!/usr/bin/env python

import unittest
import MovieLens as ML

class TestMovieLens(unittest.TestCase):
    
    def setUp(self):
        self.movie_lens = ML.MovieLens('test_movies.dat', 'test_ratings.dat')

    def test_rated_movies(self):
         self.assertEqual(len(self.movie_lens.get_rated_movies('Asia')), 6)
         
    def test_correlation(self):
        self.assertEqual(self.movie_lens.pcc('Asia', 'Genia'), 0.991)
        self.assertEqual(self.movie_lens.pcc('Czarek', 'Czarek'), 1.0)
        self.assertEqual(self.movie_lens.pcc('Czarek', 'Genia'), -1.0)
        self.assertEqual(self.movie_lens.pcc('Ewa', 'Czarek'), -0.258)
        self.assertEqual(self.movie_lens.pcc('Czarek', 'Ewa'), -0.258)

    def test_recommendations(self):
        expected = [('Szczeki', 2.846),
                    ('Terminator', 2.531),
                    ('Rocky', 3.325)
        ]
        self.assertEqual(len(self.movie_lens.predict_ratings("Genia")), 3)
        self.assertEqual(self.movie_lens.predict_ratings("Genia"), expected)

if __name__ == "__main__":
    unittest.main()
