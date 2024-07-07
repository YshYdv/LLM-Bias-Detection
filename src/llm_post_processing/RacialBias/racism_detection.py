# -*- coding: utf-8 -*-

import re
import numpy as np
import pandas as pd
# import nlpaug.augmenter.word as naw
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit

from pprint import pprint
from collections import Counter
from itertools import chain 
# from wordcloud import WordCloud
import matplotlib.pyplot as plt
import logging

from keras.models import Sequential
from keras.layers import SpatialDropout1D, LSTM, Dense, Embedding, Dropout
from keras.callbacks import EarlyStopping
from keras.utils import pad_sequences

import pickle
"""#Read Dataset"""


# df_ = pd.read_csv('dataset_racism.csv', sep=',')

df = pd.read_csv('llm_post_processing/RacialBias/twitter_text.csv', sep=',')
# df = df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

df = df.drop('id', axis=1)

labels = df['label']
df = df.drop('label', axis=1)
# labels

df['label'] = labels

df.rename(columns = {'tweet':'tweets'}, inplace = True)

"""#Data Preprocessing"""

def preprocessing(str):
    #lowercase string
    str = str.lower()
    #remove rt, mention and link
    str = re.sub('rt |@[a-z]*|http([a-z]|[0-9]|/|:|.)*|pic.twitter.com/([a-z]|[0-9])*', '', str)
    #remove punctuation and emoticon
    str = re.sub('[^a-z0-9]+', ' ', str)
    #remove extra white spaces
    str = ' '.join(str.split())
    #tokenization
    # str = str.split()
    # if str == []:
        # return float('NaN')
    return str

df['preprocessed'] = df.tweets.apply(preprocessing)
df.preprocessed = df.preprocessed.apply(str)

# df.head()

"""#Data Analysis"""

df_R = df[df.label == 1]
df_NonR = df[df.label == 0]

label_count = df['label'].value_counts()
print('Class Non-Racist :', label_count[0])
print('Class Racist     :', label_count[1])

# label_count.plot(kind='bar', title='Count (label)',rot=0)

# df

df['preprocessed'][df.label == 1].iloc[0]

# def generateWordCloud(df_tweets):
#   # split texts by whitespace and turn them to array
#   tweets = df_tweets.str.split(" ").tolist()

#   # flatten the 2d array to 1d array
#   tweets = list(chain.from_iterable(tweets))

#   # count most common 20 racist words
#   common_words = dict(Counter(tweets).most_common(20))
#   # print(common_words)

#   # set wordcloud values
#   wordcloud = WordCloud(background_color="white",width=1500,height=1500,relative_scaling=0.5,min_font_size=10).generate_from_frequencies(common_words)

#   return wordcloud

# generate wordcloud racist
# wc_R = generateWordCloud(df[df['label'] == 1]['preprocessed'])

# # plot the WordCloud image                        
# plt.figure(figsize = (6, 6), facecolor = None) 
# plt.imshow(wc_R) 
# plt.axis("off") 
# plt.tight_layout(pad = 0)

# generate wordcloud non-racist
# wc_NonR = generateWordCloud(df[df['label'] == 0]['preprocessed'])

# # plot the WordCloud image                        
# plt.figure(figsize = (6, 6), facecolor = None) 
# plt.imshow(wc_NonR) 
# plt.axis("off") 
# plt.tight_layout(pad = 0)

"""# LSTM"""

# for i in df['preprocessed']:
    

from tensorflow.keras.preprocessing.text import Tokenizer
# The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 50000

# Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 250

# This is fixed.
EMBEDDING_DIM = 100

tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
tokenizer.fit_on_texts(df['preprocessed'].values)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

# get key from word index dictionary
def get_key(val): 
    for key, value in word_index.items(): 
         if val == value: 
             return key 

    return "key doesn't exist"
  
# get_key(922)

with open('llm_post_processing/RacialBias/pad_sequences.pkl', 'wb') as file:
    pickle.dump(pad_sequences, file)

X = tokenizer.texts_to_sequences(df['preprocessed'].values)
X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)
print('Shape of data tensor:', X.shape)

with open('llm_post_processing/RacialBias/tokenizer.pkl', 'wb') as file:  
    pickle.dump(tokenizer, file)

Y = pd.get_dummies(df['label']).values
print('Shape of label tensor:', Y.shape)

df['preprocessed'].iloc[0]

sent = tokenizer.texts_to_sequences([""])
sent_ = pad_sequences(sent, maxlen=MAX_SEQUENCE_LENGTH)
# sent_[0]

# Split dataset
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.10, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

model = Sequential()
model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X_train.shape[1]))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

epochs = 5
batch_size = 64

history = model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size,validation_split=0.1,callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)])


with open('llm_post_processing/RacialBias/racial_bias_model.pkl', 'wb') as file:  
    pickle.dump(model, file)

# y_pred = model.predict(sent_)

# # y_pred

# preds = np.zeros(len(y_pred))
# for i in range(len(y_pred)):
#     preds[i] = int(np.argmax(y_pred[i]))
# preds

# accr = model.evaluate(X_test, Y_test)
# print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))

# plt.title('model train vs validation loss')
# plt.plot(history.history['loss'], label='train')
# plt.plot(history.history['val_loss'], label='test')
# plt.legend()
# plt.show()

# plt.title('Accuracy')
# plt.plot(history.history['accuracy'], label='train')
# plt.plot(history.history['val_accuracy'], label='test')
# plt.legend()
# plt.show()