from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Currencies(models.Model):
    #name = models.CharField(max_length=100)
    currency = models.CharField(max_length=3, primary_key=True)
    symbol = models.CharField(max_length=3)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.currency


class Denominations(models.Model):
    #denominationID = models.AutoField(primary_key=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    denomination = models.IntegerField()
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.denomination

class Money_Scan(models.Model):
    scanId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    image = models.ImageField(upload_to='./mediafiles')
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT)
    denomination = models.IntegerField()
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.result



