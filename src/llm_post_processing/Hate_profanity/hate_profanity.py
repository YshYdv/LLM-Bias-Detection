from detoxify import Detoxify
import pandas as pd

input_text = input("Enter")
results = Detoxify('original').predict(input_text)
tox = results['toxicity']
toxCategory = 0
if (tox > 0.5):
    toxCategory = 1

print(toxCategory)
