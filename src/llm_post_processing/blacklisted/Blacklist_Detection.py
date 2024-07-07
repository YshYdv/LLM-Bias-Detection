import pickle
import os
from gensim.corpora import Dictionary
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

print(script_dir)
# Specify the file name
file_name = 'Blacklist_LDA_Dict.pkl'

# Construct the full file path
file_path_dict = os.path.join(script_dir, file_name)

# Load the dictionary
dictionary = Dictionary.load(file_path_dict)

# Load the LDA model
model_file = "Blacklist_LDA.pkl"

# Construct the full file path
file_path_model = os.path.join(script_dir, model_file)
with open(file_path_model, 'rb') as file:
    lda_model = pickle.load(file)

# Preprocess function from Train
stemmer = SnowballStemmer("english")
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

# Tokenize and lemmatize
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result

# Create a dictionary of the identified topics and their contents
topics_dict = {
    0: 'Politics',
    1: 'Geopolitics and Violence',
    2: 'Sports',
    3: 'Ads and Sales',
    4: 'Technology',
    5: 'Space and Science',
    6: 'Automobiles',
    7: 'Religion'
}

unseen_document = input("Enter the LLM generated text: ")
# Data preprocessing step for the unseen document
bow_vector = dictionary.doc2bow(preprocess(unseen_document))

flag = 0
topic = ""
for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score,  topics_dict.get(index,)))
    if(score > 0.5 and (index == 0 or index == 1 or index == 3 or index == 7)):
        flag = 1
        topic = topics_dict[index]
        break
    
if flag == 1:
    print("BLACKLISTED")
else:
    print(unseen_document)