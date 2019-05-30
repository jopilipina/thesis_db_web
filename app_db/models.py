from django.db import models

class Entry(models.Model):
  id = models.AutoField(primary_key=True)
  disease = models.CharField(max_length=50)
  gene = models.CharField(max_length=50)
  relation = models.CharField(max_length=50)
  full_text = models.TextField()
  pmid = models.IntegerField(default=None, blank=True, null=True)

  class Meta:
    unique_together = ["gene", "relation", "full_text", "pmid"]

  def __str__(self):
    return self.relation
