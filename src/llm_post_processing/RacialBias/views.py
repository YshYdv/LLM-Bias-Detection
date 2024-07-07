from django.shortcuts import render
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from RacialBias.models import inputData

import pickle
import numpy as np
import os

class ResultsView(APIView):

    def post(self, request):
        
        sentence = request.data.get('input_text')
        new = inputData.objects.create(input_data = sentence, prediction = 0)
        new.save()
        
        MAX_SEQUENCE_LENGTH = 250

        model_path = os.path.abspath('RacialBias/racial_bias_model.pkl')
        with open(model_path, 'rb') as file:  
            model = pickle.load(file)

        tokenizer_path = os.path.abspath('RacialBias/tokenizer.pkl')
        with open(tokenizer_path, 'rb') as file:
            tokenizer = pickle.load(file)

        pad_sequences_path = os.path.abspath('RacialBias/pad_sequences.pkl')
        with open(pad_sequences_path, 'rb') as file:
            pad_sequences = pickle.load(file)
        
        sent = tokenizer.texts_to_sequences([sentence])
        sent_ = pad_sequences(sent, maxlen=MAX_SEQUENCE_LENGTH)

        y_pred = model.predict(sent_)

        pred = np.argmax(y_pred[0])

        new.prediction = pred
        new.save()

        output = ''
        
        if y_pred[0][pred]>0:
            if pred==0:
                output = 'The text is not racially biased.'
            else:
                output = 'Sorry I cannot process your request as the text is racially biased.'
        else:
            output = 'The text is not racially biased.'

        # mapping = {'No considerable bias': 0,
        #            'No racial bias': 0,
        #            'Racially biased': 1}
        
        return Response({'verdict': pred, 'message': output})