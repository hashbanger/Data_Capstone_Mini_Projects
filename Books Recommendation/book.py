import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

books = pd.read_csv('BX-Books.csv', error_bad_lines= False, sep= ';', encoding= 'iso-8859-1')
books.head()

ratings = pd.read_csv('BX-Book-Ratings.csv',sep = ';', error_bad_lines= False, encoding= 'iso-8859-1')
ratings.head()

users = pd.read_csv('BX-Users.csv', sep = ';', error_bad_lines= False, encoding= 'iso-8859-1')
users.head()

books.drop(labels = ['Image-URL-S','Image-URL-M','Image-URL-L'], axis = 1, inplace = True)

print('Total Unique Values: '+str(books['Year-Of-Publication'].nunique()))

x = books['Publisher'].unique()
pd.set_option('display.max_colwidth', -1) #setting appropriate width

books[books['Year-Of-Publication'] == 'DK Publishing Inc']
books.iloc[209538]['Year-Of-Publication'] = 2000
books.iloc[209538]['Book-Author'] = 'Michael Teitelbaum'
books.iloc[209538]['Publisher'] = 'DK Publishing Inc'
books.iloc[209538]['Book-Title'] = 'DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)'

books.iloc[221678]['Year-Of-Publication'] = 2000
books.iloc[221678]['Book-Author'] = 'James Buckley'
books.iloc[221678]['Publisher'] = 'DK Publishing Inc'
books.iloc[221678]['Book-Title'] = 'DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)'

books.iloc[220731]['Year-Of-Publication'] = 2003
books.iloc[220731]['Book-Author'] = 'Jean-Marie Gustave Le Clézio'
books.iloc[220731]['Publisher'] = 'Gallimard'
books.iloc[220731]['Book-Title'] = 'Peuple du ciel, suivi de Les Bergers'

books['Year-Of-Publication'] = pd.to_numeric(books['Year-Of-Publication'])

books[(books['Year-Of-Publication'] == 0) | (books['Year-Of-Publication'] > 2004)] = np.nan

books['Year-Of-Publication'].fillna(round(books['Year-Of-Publication'].mean()), inplace = True)

books['Year-Of-Publication'] = books['Year-Of-Publication'].astype(np.int32)

books.dropna(axis=0, how='all', subset=['ISBN','Book-Title'], inplace= True)

users[(users['Age'] < 7) | (users['Age'] > 100)] = np.nan

users['Age'].fillna(users['Age'].mean(),inplace = True)
users['Age'] = users['Age'].astype(np.int32)

users.dropna(axis=0, how='all', subset=['User-ID','Location'], inplace= True)

ratings_new = ratings[ratings['ISBN'].isin(books['ISBN'])]
ratings_new = ratings[ratings['User-ID'].isin(users['User-ID'])]

ratings_zero = ratings.loc[ratings['Book-Rating'] == 0]
ratings_nonzero = ratings.loc[ratings['Book-Rating'] > 0]

rating_count = ratings_new.groupby('ISBN')['Book-Rating'].count()
rating_count = rating_count.sort_values(ascending = False)

rating_count = pd.DataFrame(rating_count)
rating_count.reset_index(inplace= True)

most_rated_books = pd.merge(rating_count, books, on= 'ISBN')
rating_avg = pd.DataFrame(ratings_new.groupby('ISBN')['Book-Rating'].mean())
rating_avg.head()

average_rating = pd.DataFrame(ratings_new.groupby('ISBN')['Book-Rating'].mean())
average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['Book-Rating'].count())
average_rating.sort_values('ratingCount', ascending=False).head()

countOfUsers1 = pd.DataFrame(ratings_new['User-ID'].value_counts())
countOfUsers1.reset_index(inplace= True)
countOfUsers1.rename(columns= {'index': 'counts'},inplace= True)

ratings_new = ratings_new[ratings_new['User-ID'].isin(countOfUsers1[countOfUsers1['counts'] >= 200].index)]

countOfBooks = pd.DataFrame(ratings_new['ISBN'].value_counts())

countOfBooks.reset_index(inplace= True)
countOfBooks.rename(columns= {'index': 'ISBN', 'ISBN': 'counts'},inplace= True)

countOfBooks = ratings_new['Book-Rating'].value_counts()
ratings_final = ratings_new[ratings_new['Book-Rating'].isin(countOfBooks[countOfBooks >= 100].index)]
ratings_final.head()

ca = ratings_final.iloc[0:40000,:]

cc = ca.pivot_table(index= 'User-ID', columns= 'ISBN', values= 'Book-Rating')

userID = cc.index
ISBN = cc.columns
print(cc.shape)

#----------------------------------------------------------------------------------------------------
#-------------------------------RUN ONLY ONCE---------------------------------------------------------
#------------------------------------------------------------------------------------------------------


print("ENter the ISBN on the Book you want to look recommendations for:")
input_ISBN = input()
print("Enter the name of the book: ")
input_book = input()
item_ratings = cc[input_ISBN]
name_of_book = input_book
similar_to_item = cc.corrwith(item_ratings)
corr_item = pd.DataFrame(similar_to_item, columns=['pearsonR'])
corr_item.dropna(inplace=True)
corr_summary = corr_item.join(average_rating['ratingCount'])
similars = []

similars = corr_summary[corr_summary['ratingCount']>=300].sort_values('pearsonR', ascending=False).head(10)
similars.reset_index(inplace= True)  
books_corr_to_item = pd.DataFrame(similars['ISBN'], 
                                  index=np.arange(len(similars['ISBN'])), columns=['ISBN'])
corr_books = pd.merge(books_corr_to_item, books, on='ISBN')

print('Recommendations for '+name_of_book)
print(corr_books)