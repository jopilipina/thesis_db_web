from ner import relation_extractor
from .models import Relation

rels = relation_extractor()

for rel in rels:
  Relation.object.create(gene=rel[0], disease=rel[1], relation=rel[2], full_text=rel[3])
