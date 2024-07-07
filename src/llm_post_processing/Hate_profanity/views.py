# import nltk
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response  # Import this for Response
from rest_framework import status, viewsets  # Import this for Status
from .serializers import CommentSerializer
from detoxify import Detoxify
import pandas as pd
# from hateRemoval.DPhate import DPhate

# nltk.download('averaged_perceptron_tagger')

# Create your views here.


class CommentViewSet(APIView):
    serializer_class = CommentSerializer

    def post(self, request):
        input_text = request.data['input_text']
        results = Detoxify('original').predict(input_text)
        tox = results['toxicity']
        # toxCategory = "not toxic"
        
        if (tox > 0.5):
            # toxCategory = "toxic"
            return Response({'verdict': 1, 'message': 'Sorry I cannot process your request as the text you entered contains toxic content.'})
        else:
            return Response({'verdict': 0, 'message': 'The text does not contain toxic content.'})
