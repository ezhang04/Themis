import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel, BertTokenizer

from model import SentimentClassifier

class Model:
    def __init__(self):
        MODEL_NAME = 'bert-base-cased'

        # Build a BERT based tokenizer
        self.tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
        self.bert_model = BertModel.from_pretrained(MODEL_NAME)

        self.model = SentimentClassifier(3)

        state_dict = torch.load('sentiment_model_weights.pth', map_location=torch.device('cpu'))
        self.model.load_state_dict(state_dict)

        self.tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    def predict(self, text):
        encoding = self.tokenizer(
            text,
            return_tensors='pt',        # return PyTorch tensors
            padding='max_length',       # pad to max_length
            truncation=True,            # truncate if too long
            max_length=128              # or whatever you choose
        )

        input_ids = encoding['input_ids']       # shape: [1, seq_len]
        attention_mask = encoding['attention_mask']  # shape: [1, seq_len]


        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)

        outputs

        probs = F.softmax(outputs, dim=1)

        # 1st is biased, 2nd is inconclusive, 3rd is unbiased
        return(probs[0][0].item(), probs[0][2].item())