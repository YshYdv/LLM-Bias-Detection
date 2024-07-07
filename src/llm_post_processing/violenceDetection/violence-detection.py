#!/usr/bin/env python
# coding: utf-8

# In[357]:


import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import spacy
import pickle



# In[359]:


data = pd.read_csv("violenceDetection/train.csv")


# In[360]:


data = data.drop("id", axis=1)


# In[361]:


data


# In[480]:


# Positive Sample
s=data["comment_text"][79]


# # Cleaning

# In[363]:


def clean(s):
#     stop_words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    porter = PorterStemmer()
    s = re.sub(r'[^\w\s]','',s)
#     s = " ".join([lemmatizer.lemmatize(w) for w in s.split() if not w in stop_words])
    s = " ".join([lemmatizer.lemmatize(w) for w in s.split()])
    s = " ".join([porter.stem(w) for w in s.split()])
    return s


# In[364]:


import sys
sys.setrecursionlimit(5000)


# In[365]:


X = data["comment_text"].apply(clean).to_list()
y = data["threat"].to_list()


# #### Weighting positive samples

# In[348]:


# n = len(X)
# for j in range(10):
#     for i in range(n):
#         if y[i]==1:
#             X.append(X[i])
#             y.append(y[i])


# In[456]:


vectorizer = CountVectorizer()
X_ = vectorizer.fit_transform(X)


# # Training

# In[457]:


clf = LogisticRegression(max_iter=1000)
clf.fit(X_, y)


# In[411]:


def getThreatSentence(p):
    P = paragraph_to_sentence(p)
    x = vectorizer.transform(P)
    pred = clf.predict_proba(x)
    return P[np.argmax(pred[:,1])]


# In[479]:


k = 1
for i in range(k):

    n = len(X)
    for i in range(n):

        if y[i]==1:
            X.insert(0, getThreatSentence(X[i]))
            y.insert(0, y[i])
            
    vectorizer = CountVectorizer()
    X_ = vectorizer.fit_transform(X)
    
    clf.fit(X_, y)



# In[480]:


file = "model.sav"
pickle.dump(clf, open(file, 'wb'))



# # Testing

# In[476]:


s = "do my work else die"


# In[459]:


def sentence_extraction(token, l, main):
    if token.text in main:
        main.remove(token.text)
    for token_ in token.lefts:
        if token_.dep_[0]!='c':
            sentence_extraction(token_, l, main)
    l.append(token.text)
    for token_ in token.rights:
        if token_.dep_[0]!='c':
            sentence_extraction(token_, l, main)
    return l, main


# In[460]:


def paragraph_to_sentence(p):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(p)

    main_words = []
    for token in doc:
        if token.dep_=="ROOT" or token.pos_=='VERB':
            main_words.append(token.text)
            
    if len(main_words)==0:
        return [doc.text]

    lst = []
    for token in doc:
        if token.text in main_words:
            l, main_words = sentence_extraction(token, [], main_words)
            lst.append(clean(' '.join(l)))

    return lst


# In[481]:


p = paragraph_to_sentence(s)
p


# In[412]:


getThreatSentence(s)


# In[480]:


file = "model.sav"
clf = pickle.load(open(file, 'rb'))



# In[482]:


def checkThreat(p):
    for s in p:
        x = vectorizer.transform([s])
        print(s, clf.predict_proba(x)[0][1])
        if clf.predict(x):
            return 1
    return 0


# In[483]:


checkThreat(p)


# In[ ]:




