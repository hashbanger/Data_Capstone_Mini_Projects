# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 00:37:32 2018

@author: prash
"""

import pandas as pd
import numpy as np
import seaborn as sns

column_names = ['user_id','item_id','rating','timestamp']
df = pd.read_csv('u.data',names = column_names, delimiter= '\t')

movie_titles = pd.read_csv('Movie_Id_Titles')

df = df.merge(movie_titles, on= 'item_id')

# Exploratory Analysis------------------------------------------------------------------

sns.set_style('whitegrid')
#Looking at highest rated movies
df.groupby('title')['rating'].mean().sort_values(ascending = False)

#Looking at most rated movies
df.groupby('title')['rating'].count().sort_values(ascending = False)

#Forming a DataFrame with Movie Titles with their Ratings and Number of Ratings
rating = pd.DataFrame(df.groupby('title')['rating'].mean())

rating['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())

#Visualising number of ratings
'''plt.figure(figsize= (10,6))
sns.distplot(rating['num of ratings'], bins = 70, kde = False, color= 'black')

plt.figure(figsize= (10,6))
sns.distplot(rating['rating'], bins = 70, kde = False, color= 'black')

sns.jointplot(rating['rating'], rating['num of ratings'], color = 'green')

'''
#Recommending Movies-----------------------------------------------------------------------
#Creating a matrix having user ids on one axis and the movie title on another axis.  
#And the data being the corresponding rating.

moviemat = df.pivot_table(values = 'rating', index = 'user_id', columns= 'title')

rating.sort_values('num of ratings', ascending = False)
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('prashant.brahmbhatt32@outlook.com')
print('----------------------------------------------')
print('Movie Recommendation System')
print('----------------------------------------------')
user_movie = input('Enter the movie you like: ')
user_movie_ratings = moviemat[user_movie] 

similar_to_user_movie = moviemat.corrwith(user_movie_ratings)

corr_user_movie = pd.DataFrame(similar_to_user_movie,columns= ['Correlation'])
corr_user_movie.dropna(inplace = True)

corr_user_movie.sort_values('Correlation',ascending = False)

'''We can observe that some movies have perfect correlation with the chosen movies.
This is due to some movies have been rated by only a few people with high rating.

So we can filter out movies with number of rating less than a certain number.
'''

corr_user_movie = corr_user_movie.join(rating['num of ratings'])

movies = corr_user_movie[corr_user_movie['num of ratings'] > 100].sort_values('Correlation',ascending = False).head(6)
movies.reset_index(inplace = True)


top5s = np.array(movies.title)
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('\n')
print('Top 5 movies that you may like:')
print('\n')

i = 0
for movie in top5s:
    i = i+1
    if i == 1:
        continue
    else:
        print(movie)

print('\n')
print('\n')
print('\n')
