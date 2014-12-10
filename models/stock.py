#coding:utf8

from django.db import models
    
class StockBaseInfo(models.Model):
    class Meta:
        db_table = "StockBaseInfo"
    Code = models.CharField()
    Name = models.CharField()
    Name2 = models.CharField()
    Region = models.IntegerField()
    Tag = models.CharField()

class CnStockDailyPrice(models.Model):
    class Meta:
        db_table = "CnStockDailyPrice"
    Date = models.CharField()
    Code = models.CharField()
    Open = models.FloatField()
    Close = models.FloatField()
    High = models.FloatField()
    Low = models.FloatField()
    AdjClose = models.FloatField()
    
class UsStockDailyPrice(models.Model):
    class Meta:
        db_table = "UsStockDailyPrice"
    Date = models.CharField()
    Code = models.CharField()
    Open = models.FloatField()
    Close = models.FloatField()
    High = models.FloatField()
    Low = models.FloatField()
    AdjClose = models.FloatField()
    
class CnStockGroup(models.Model):
    class Meta:
        db_table = "CnStockGroup"
    Code = models.CharField()
    StockGroup = models.IntegerField()

class UsStockGroup(models.Model):
    class Meta:
        db_table = "UsStockGroup"
    Code = models.CharField()
    StockGroup = models.IntegerField()