import spacy
import json
import kindred
import argparse
import os

# Scispacy
def entity_tagger():
  nlp1 = spacy.load('en_ner_bionlp13cg_md')

  lines = [line.rstrip('\n') for line in open('app_db/ner-input.txt','r')]

  fcounter = 1
  for i in range(0, len(lines)):
    if lines[i] == "TEST":
      docx1 = nlp1(lines[i+1])
      entities = []
      count = 1
      gene_list = []
      disease_list = []
      for token in docx1.ents:
        if token.label_ == "GENE_OR_GENE_PRODUCT":
          obj = "gene"
          if token.text not in gene_list:
            gene_list.append(token.text)
            dict1 = {"id": "T{}".format(count), "obj": obj, "span": {"begin": token.start_char, "end": token.end_char}}
            entities.append(dict1)
            count = count + 1
        elif (token.label_ == "CANCER"):
          obj = "disease"
          if token.text not in disease_list:
            disease_list.append(token.text)
            dict1 = {"id": "T{}".format(count), "obj": obj, "span": {"begin": token.start_char, "end": token.end_char}}
            entities.append(dict1)
            count = count + 1

      dict2 = {"text":lines[i+1], "denotations":entities}

      with open("app_db/ner-dump/{}.json".format(fcounter), "w") as f:
        print(json.dumps(dict2), file=f)
      fcounter = fcounter + 1


# Kindred
# 5 classes
def relation_extractor():

  entity_tagger()

  lines_pmid = [line.rstrip('\n') for line in open('app_db/pmids.txt','r')]

  trainCorpus = kindred.load(dataFormat='json',path='app_db/train')
  devCorpus = kindred.load(dataFormat='json',path='app_db/ner-dump')

  predictionCorpus = devCorpus.clone()

  classifier = kindred.RelationClassifier()
  classifier.train(trainCorpus)
  classifier.predict(predictionCorpus)

  f1score = kindred.evaluate(devCorpus, predictionCorpus, metric='f1score')

  output = []
  count = 0
  for i in predictionCorpus.documents:
    for j in (i.relations):
      rel = {
        'entity1': j.entities[0].entityType,
        'entity1_value': j.entities[0].text,
        'entity2': j.entities[1].entityType,
        'entity2_value': j.entities[1].text,
        'relation_type': j.relationType,
        'fulltext': i.text,
        'pmid': lines_pmid[count]
      }
      output.append(rel)
    count = count + 1
  
  return output
