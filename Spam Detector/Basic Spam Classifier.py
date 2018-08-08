import nltk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import string

messages = [line.rstrip() for line in open("smsspamcollection/SMSSpamCollection")]

messages = pd.read_csv('smsspamcollection/SMSSpamCollection', sep='\t',names = ['Label','Message'])

from nltk.corpus import stopwords

def text_process(mess):
    '''
    Removing the punctuations
    Removing the common words 
    Returning the cleaned words
    '''
    nopunc = [char for char in mess if char not in string.punctuation]
    
    nopunc = ''.join(nopunc)
    
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

from sklearn.feature_extraction.text import CountVectorizer
bow_transformer = CountVectorizer(analyzer= text_process).fit(messages['Message'])
bow_messages = bow_transformer.transform(messages['Message'])

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from sklearn.cross_validation import train_test_split
msg_train, msg_test, label_train, label_test = train_test_split(messages['Message'], messages['Label'], test_size = 0.25, random_state = 0)


from sklearn.pipeline import Pipeline
#parameters
'''steps : list
    List of (name, transform) tuples (implementing fit/transform) that are
    chained, in the order in which they are chained, with the last object
    an estimator.'''
pipeline = Pipeline([
                    ('bow', CountVectorizer(analyzer= text_process)),
                    ('tfidf', TfidfTransformer()),
                    ('classifier', MultinomialNB())])
    
pipeline.fit(msg_train, label_train)
predictions = pipeline.predict(msg_test)


user_msg = input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nEnter the message text:\n')
user_msg = user_msg.rstrip()
f_user_msg = pd.Series(data= user_msg, index= [len(user_msg)])
result = pipeline.predict(f_user_msg)[0]

if result == 'spam':
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nThe message is a SPAM ')
else:
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nThe message is NOT A SPAM ')



