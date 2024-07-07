from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from PII.models import inputData
from PII.anonymizer import PII_anonymize


class anonymizeView(APIView):

    def post(self, request):
        text = request.data.get('input_text')
        new = inputData.objects.create(input_text = text)
        new.save()
        anonymizer = PII_anonymize()
        anonymized_text = anonymizer(text)
        
        if text == anonymized_text:
            return Response({'verdict':0, 'message': 'The text does not contain any personal information.'})
        else:
            # return Response({'verdict':1, 'message': 'The text contains personal information.\n The filtered text is as follows: ' + anonymized_text})
            return Response({'verdict':1, 'message': anonymized_text})
            