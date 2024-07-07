# from src.llm import model

import requests
import json

question = ""
input_text = input("Enter the sentence: ")

configs_list = []
while True:
    config = input("Enter a config: ")
    if config == 'none' or config == 'end':
        break
    configs_list.append(config)

# lang_model = model("large_model")

# if len(question) != 0:
#     input_text = lang_model(question)

# Detection and mitigation on response

racial_bias_api = "http://127.0.0.1:8000/racialBias/"
hate_profanity_api = "http://127.0.0.1:8000/hateprofanity/"

urls = {'racial_bias': racial_bias_api,
        'hate_profanity': hate_profanity_api}

# Detector = detector()
# Mitigator = mitigator()
# result = Detector(reponse)
# if result:
#     final_output = Mitigator(input_ids = inputs)
# else:
#     final_output = reponse

detected = {}

for i in configs_list:
    sentence = {"input_text": input_text}
    headers = {"Content-Type":"application/json"}
    response = requests.post(urls[i], data=json.dumps(sentence), headers=headers)
    print(response.json()['model_verdict'])
    # detected[i] = response.json()['model_verdict']

print(detected)