from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.



class Simbol(models.Model):
    coin_name = models.CharField(max_length=30)
    

class CryptoTransaction(models.Model):
    simbol = models.ForeignKey(Simbol, on_delete=models.CASCADE,)
    volume = models.FloatField()
    count_trades  = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.simbol.coin_name} - {self.volume} - {self.count_trades}'


class BigLimits(models.Model):
    simbol = models.ForeignKey(Simbol, on_delete=models.CASCADE)
    price = models.CharField(max_length= 12)
    is_purchase = models.BooleanField(default=True)
    volume = ArrayField(models.FloatField(), default=list)
    timestamp = ArrayField(models.DateTimeField(), default=list)
    changes = ArrayField(models.FloatField(), default=list)

    def __str__(self):
        return f'{self.simbol.coin_name} - {self.price} - {self.volume}'


class ChatSubId(models.Model):
    chatId = models.IntegerField(unique=True)
    timeEndSub = models.DateTimeField()

    def __str__(self):
        return f'{self.chatId} - {self.timeEndSub}'
    
class BigLimitsEz(models.Model):
    simbol = models.ForeignKey(Simbol, on_delete=models.CASCADE)
    volume = models.FloatField()
    price = models.FloatField(default=0.0)
    is_purchase = models.BooleanField(default=True)
    range = models.FloatField(default=0.0)
    def __str__(self):
        return f'{self.simbol.coin_name} - {self.volume} - {self.price} - {self.is_purchase}'
    
class TableView(models.Model):
    name = models.CharField(max_length=20)
    table = models.JSONField()