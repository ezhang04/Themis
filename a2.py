from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
from transformers import logging

logging.set_verbosity_error()

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class Model2:
    def __init__(self):
        self.tokenizer2 = AutoTokenizer.from_pretrained("d4data/bias-detection-model")
        self.model2 = TFAutoModelForSequenceClassification.from_pretrained("d4data/bias-detection-model")

        self.classifier = pipeline('text-classification', model=self.model2, tokenizer=self.tokenizer2) # cuda = 0,1 based on gpu availability

    def predict(self, text):
        results = self.classifier(text)
        label = results[0]['label']
        score = results[0]['score']

        if label == 'Biased':
            return score, 1 - score
        else:
            return 1 - score, score