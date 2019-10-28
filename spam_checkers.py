#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json, codecs, os
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

all_adverts_classifier = None

def train_spam_texts():
  # Reading dataset file
  dataset_lang = "ru"
  dataset_file = codecs.open(os.path.abspath(os.curdir) + "/assets/spam_texts.json", "r", "utf_8_sig")
  dataset_data = json.load(dataset_file)

  # Preparing adverts spam dataset
  prepared_dataset = []
  for idx, item in enumerate(dataset_data[dataset_lang]["adverts"]):
    prepared_dataset.append({
      "text": item["text"],
      "category": "adverts"
    })
  
  # Training
  # (Will be replaced by another library soon)
  advertsTrainer = Trainer(tokenizer)
  for one_dataset_item in prepared_dataset:
    advertsTrainer.train(one_dataset_item["text"], one_dataset_item["category"])
  adverts_classifier = Classifier(advertsTrainer.data, tokenizer)

  # Usage
  # classification = adverts_classifier.classify("any spam text")

  # return adverts_classifier
  global all_adverts_classifier
  all_adverts_classifier = adverts_classifier

def is_msg_spam(msg_obj):
  pass