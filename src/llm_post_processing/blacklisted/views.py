from django.shortcuts import render
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from blacklisted.models import InputData

import pickle
import os
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

class BlackListView(APIView):
    def post(self, request):
        sentence = request.data.get('input_text')
        new = InputData.objects.create(input_text=sentence)
        new.save()

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

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

        # Preprocess function from Train
        stemmer = SnowballStemmer("english")

        result=[]
        for token in simple_preprocess(sentence) :
            if token not in STOPWORDS and len(token) > 3:
                result.append(stemmer.stem(WordNetLemmatizer().lemmatize(token, pos='v')))
        bow_vector = dictionary.doc2bow(result)

        flag = 0
        det_topic = ""
        det_score = 0
        for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
            print("Score: {}\t Topic: {}".format(score,  topics_dict.get(index,)))
            if(score > 0.5 and (index == 0 or index == 1 or index == 3 or index == 7)):
                flag = 1
                det_score = score
                det_topic = topics_dict[index]
                break
            
        if flag == 1:
            return Response({"verdict": flag ,"message": "The text contains blacklisted topics. They are as follows: " + det_topic, "topic": det_topic, "score": det_score})
        else:
            return Response({"verdict": flag ,"message": "The text does not contain blacklisted topics.", "response": sentence})