"""
Simple User Interface
"""
from movielens import *
from sklearn.cluster import KMeans

import numpy as np
import pickle
import random
import sys
import time

user = []
item = []

d = Dataset()
d.load_users("data/u.user", user)
d.load_items("data/u.item", item)

n_users = len(user)
n_items = len(item)

utility_matrix = pickle.load( open("utility_matrix.pkl", "rb") )

# Find the average rating for each user and stores it in the user's object
for i in range(0, n_users):
    x = utility_matrix[i]
    user[i].avg_r = sum(a for a in x if a > 0) / sum(a > 0 for a in x)

# Find the Pearson Correlation Similarity Measure between two users
def pcs(x, y, ut):
    num = 0
    den1 = 0
    den2 = 0
    A = ut[x - 1]
    B = ut[y - 1]
    num = sum((a - user[x - 1].avg_r) * (b - user[y - 1].avg_r) for a, b in zip(A, B) if a > 0 and b > 0)
    den1 = sum((a - user[x - 1].avg_r) ** 2 for a in A if a > 0)
    den2 = sum((b - user[y - 1].avg_r) ** 2 for b in B if b > 0)
    den = (den1 ** 0.5) * (den2 ** 0.5)
    if den == 0:
        return 0
    else:
        return num / den

# Perform clustering on items
movie_genre = []
for movie in item:
    movie_genre.append([movie.unknown, movie.action, movie.adventure, movie.animation, movie.childrens, movie.comedy,
                        movie.crime, movie.documentary, movie.drama, movie.fantasy, movie.film_noir, movie.horror,
                        movie.musical, movie.mystery, movie.romance, movie.sci_fi, movie.thriller, movie.war, movie.western])

movie_genre = np.array(movie_genre)
cluster = KMeans(n_clusters=19)
cluster.fit_predict(movie_genre)

ask = random.sample(item, 10)
new_user = np.zeros(19)

print "Please rate the following movies (1-5):"

for movie in ask:
	print movie.title + ": "
	a = int(input())
	if new_user[cluster.labels_[movie.id - 1]] != 0:
		new_user[cluster.labels_[movie.id - 1]] = (new_user[cluster.labels_[movie.id - 1]] + a) / 2
	else:
		new_user[cluster.labels_[movie.id - 1]] = a

utility_new = np.vstack((utility_matrix, new_user))

user.append(User(944, 21, 'M', 'student', 110018))

pcs_matrix = np.zeros(n_users)

print "Finding users which have similar preferences."
for i in range(0, n_users + 1):
    if i != 943:
        pcs_matrix[i] = pcs(944, i + 1, utility_new)

user_index = []
for i in user:
	user_index.append(i.id - 1)
user_index = user_index[:943]
user_index = np.array(user_index)

top_5 = [x for (y,x) in sorted(zip(pcs_matrix, user_index), key=lambda pair: pair[0], reverse=True)]
top_5 = top_5[:5]

top_5_genre = []

for i in range(0, 5):
	maxi = 0
	maxe = 0
	for j in range(0, 19):
		if maxe < utility_matrix[top_5[i]][j]:
			maxe = utility_matrix[top_5[i]][j]
			maxi = j
	top_5_genre.append(maxi)

print "Movie genres you'd like:"

for i in top_5_genre:
	if i == 0:
		print "unknown"
	elif i == 1:
		print "action"
	elif i == 2:
		print "adventure"
	elif i == 3:
		print "animation"
	elif i == 4:
		print "childrens"
	elif i == 5:
		print "comedy"
	elif i == 6:
		print "crime"
	elif i == 7:
		print "documentary"
	elif i == 8:
		print "drama"
	elif i == 9:
		print "fantasy"
	elif i == 10:
		print "film_noir"
	elif i == 11:
		print "horror"
	elif i == 12:
		print "musical"
	elif i == 13:
		print "mystery"
	elif i == 14:
		print "romance"
	elif i == 15:
		print "science fiction"
	elif i == 16:
		print "thriller"
	elif i == 17:
		print "war"
	else:
		print "western"