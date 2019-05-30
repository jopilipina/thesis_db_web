from django.shortcuts import render
from django.db.models import Q
from django.db.models.functions import Lower
from .ner import relation_extractor
from .models import *

def home(request):

  # Uncomment to populate database and then comment again so it doesn't run everytime

  # rels = relation_extractor()

  # for rel in rels:
  #   if rel['entity1'] != rel['entity2']:
  #     if rel['entity1'] == 'disease':
  #       try:
  #         new = Entry.objects.create(gene=rel['entity2_value'], disease=rel['entity1_value'], relation=rel['relation_type'], full_text=rel['fulltext'], pmid=rel['pmid'])
  #       except:
  #         pass
  #     else:
  #       try:
  #         new = Entry.objects.create(gene=rel['entity1_value'], disease=rel['entity2_value'], relation=rel['relation_type'], full_text=rel['fulltext'], pmid=rel['pmid'])
  #       except:
  #         pass

  rels1 = Entry.objects.all()
  return render(request, 'app_db/home.html')


def search(request):
  query = request.GET.get('query')

  results = Entry.objects.filter(Q(gene__icontains=query)).order_by(Lower('gene'), 'relation', 'disease', 'full_text', 'pmid')

  formatted_results = []

  j = ''
  k = ''
  l = ''

  for i in results:
    if j.casefold()==i.gene.casefold():
      temp = {'gene': '', 'relation': i.relation, 'disease': i.disease, 'full_text': i.full_text, 'pmid': i.pmid}
      if k==i.relation:
        temp['relation'] = ''
      else:
        k = i.relation
    else:
      j = i.gene
      k = i.relation
      temp = {'gene': i.gene, 'relation': i.relation, 'disease': i.disease, 'full_text': i.full_text, 'pmid': i.pmid}
    
    formatted_results.append(temp)

  return render(request, 'app_db/search.html', {'results': formatted_results})