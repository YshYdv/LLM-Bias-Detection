from django.shortcuts import render
from rest_framework.views import APIView
from blacklisted.views import BlackListView
from Hate_profanity.views import CommentViewSet
from PII.views import anonymizeView
from RacialBias.views import ResultsView
from violenceDetection.views import InputTextViewSet
from rest_framework.response import Response
from rest_framework import status
import requests

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

import sys
sys.path.insert(0, '..')
from llm import model as flant5_model

# Create your views here.

class MainView(APIView):
    def get(self, request, format=None):
        
        input_text = request.query_params.get('input_text')
        llm = request.query_params.get('llm')
        
        print('11111111111111111111111111111111111111111111111111111')
        
        if llm == 'flant5':
            generator = flant5_model("google/flan-t5-small")
            generated_text = generator(input_text, min_length=256, max_new_tokens=512,
                                    length_penalty=2, num_beams=16, no_repeat_ngram_size=2, early_stopping=True)
        
        elif llm == 'gpt2':
            model_name = 'gpt2'
            tokenizer = GPT2Tokenizer.from_pretrained(model_name)

            # Load the pre-trained GPT-2 model
            model = GPT2LMHeadModel.from_pretrained(model_name, pad_token_id = tokenizer.eos_token_id)

            # Tokenize and encode the input text
            inputs = tokenizer.encode(
                input_text,
                max_length=512,
                return_tensors='pt'
            )

            # Perform the question-answering inference
            with torch.no_grad():
                output = model.generate(inputs, max_length=256, num_beams = 5, no_repeat_ngram_size=3, early_stopping = True, do_sample=True, top_k=10, top_p=0.95, temperature=1.0)

            generated_text = tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces = True)
            
            generated_text = generated_text.replace(input_text, ' ')
            generated_text = generated_text.replace('\n', ' ')
        
        
        return Response(generated_text, status=status.HTTP_200_OK)
        # messages = [{"role": "user", "content": input_text}]
        # model="gpt-3.5-turbo"
        # openai.api_key = "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"
        # response = openai.ChatCompletion.create(
        #     model=model,
        #     messages=messages,
        #     temperature=0,
        # )
        # generated_text = response.choices[0].message["content"]
        # print(generated_text)
        
        
    def post(self, request, format=None):
        # blacklist_result = BlackListView.as_view()(request).render().content
        # hate_profanity_result = CommentViewSet.as_view()(request).render().content
        # pii_result = anonymizeView.as_view()(request).render().content
        # racial_bias_result = ResultsView.as_view()(request).render().content
        # violence_result = InputTextViewSet.as_view()(request).render().content

        config = request.data.get('config')
        
        # print('22222222222222222222222222222222')
        # print(config)
        
        result = {'verdict': []}
        
        if config['blacklisted']:
            result['blacklist_response'] = requests.post('http://127.0.0.1:8000/blacklisted/', data=request.data).json()
            if result['blacklist_response']['verdict']: 
                result['verdict'].append('blacklisted topics')

        if config['hate_profanity']:
            result['hate_profanity_response'] = requests.post('http://127.0.0.1:8000/hateprofanity/', data=request.data).json()
            if result['hate_profanity_response']['verdict']:
                result['verdict'].append('hate speech')

        if config['pii']:
            result['pii_response'] = requests.post('http://127.0.0.1:8000/anonymize_text/', data=request.data).json()
            if result['pii_response']['verdict']:
                result['verdict'].append('personally identifiable information')

        if config['racial_bias']:
            result['racial_bias_response'] = requests.post('http://127.0.0.1:8000/racialBias/', data=request.data).json()
            if result['racial_bias_response']['verdict']:
                result['verdict'].append('raciall biased text')

        if config['violence']:
            result['violence_response'] = requests.post('http://127.0.0.1:8000/violenceDetection/', data=request.data).json()
            if result['violence_response']['verdict']:
                result['verdict'].append('violent text')

        if not bool(result):
            result['error'] = {'message': 'No post processors were selected! Please select at least one post-processor to get results.'}


        # blacklist_data = blacklist_response.json()
        # hate_profanity_data = hate_profanity_response.json()
        # pii_data = pii_response.json()
        # racial_bias_data = racial_bias_response.json()
        # violence_data = violence_response.json()

        return Response(result, status=status.HTTP_200_OK)
