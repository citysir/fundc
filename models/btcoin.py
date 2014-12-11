#coding:utf8

from django.db import models

class CnBtCoinMinutelyPrice(models.Model):
    class Meta:
        db_table = "CnBtCoinMinutelyPrice"
    Open = models.FloatField()
    Close = models.FloatField()
    High = models.FloatField()
    Low = models.FloatField()
    Volumn = models.FloatField()
    PriceTime = models.DateTimeField()
    RecordTime = models.DateTimeField()
