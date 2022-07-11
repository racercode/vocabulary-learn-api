from django.db import models
from django.contrib.postgres.fields import ArrayField

class categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    vol_list = ArrayField(models.CharField(max_length=1000))
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    

    class Meta:
        ordering = ('-date_added', )

    def __str__(self):
        return self.name

class Sentence(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    word = models.CharField(max_length=1000)
    source = models.CharField(max_length=1000)
    chinese = models.CharField(max_length=1000)
    ans = models.CharField(max_length=1000)
    class Meta:
        ordering = ('word', )

    def __str__(self):
        return self.name