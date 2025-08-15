from django.db import models
from django.core.validators import MinValueValidator

import common.table_names as table

class Stock(models.Model):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=20, unique=True)
    margin = models.FloatField(
        default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = table.STOCK

class StockW1(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time = models.IntegerField(validators=[MinValueValidator(0)])
    close = models.FloatField(validators=[MinValueValidator(0)])
    open = models.FloatField(validators=[MinValueValidator(0)])
    low = models.FloatField(validators=[MinValueValidator(0)])
    high = models.FloatField(validators=[MinValueValidator(0)])
    volume = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.stock)

    class Meta:
        db_table = 'W1'  # hoặc table.W1 nếu bạn định nghĩa hằng số table tương tự D1


class StockD1(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time = models.IntegerField(validators=[MinValueValidator(0)])
    close = models.FloatField(validators=[MinValueValidator(0)])
    open = models.FloatField(validators=[MinValueValidator(0)])
    low = models.FloatField(validators=[MinValueValidator(0)])
    high = models.FloatField(validators=[MinValueValidator(0)])
    volume = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.stock

    class Meta:
        db_table = table.D1
        
class StockH1(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time = models.IntegerField(validators=[MinValueValidator(0)])
    close = models.FloatField(validators=[MinValueValidator(0)])
    open = models.FloatField(validators=[MinValueValidator(0)])
    low = models.FloatField(validators=[MinValueValidator(0)])
    high = models.FloatField(validators=[MinValueValidator(0)])
    volume = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.stock

    class Meta:
        db_table = table.H1
        
class StockM15(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time = models.IntegerField(validators=[MinValueValidator(0)])
    close = models.FloatField(validators=[MinValueValidator(0)])
    open = models.FloatField(validators=[MinValueValidator(0)])
    low = models.FloatField(validators=[MinValueValidator(0)])
    high = models.FloatField(validators=[MinValueValidator(0)])
    volume = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.stock

    class Meta:
        db_table = table.M15
        
class StockM5(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time = models.IntegerField(validators=[MinValueValidator(0)])
    close = models.FloatField(validators=[MinValueValidator(0)])
    open = models.FloatField(validators=[MinValueValidator(0)])
    low = models.FloatField(validators=[MinValueValidator(0)])
    high = models.FloatField(validators=[MinValueValidator(0)])
    volume = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.stock

    class Meta:
        db_table = table.M5
        
class StockM1(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time = models.IntegerField(validators=[MinValueValidator(0)])
    close = models.FloatField(validators=[MinValueValidator(0)])
    open = models.FloatField(validators=[MinValueValidator(0)])
    low = models.FloatField(validators=[MinValueValidator(0)])
    high = models.FloatField(validators=[MinValueValidator(0)])
    volume = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.stock

    class Meta:
        db_table = table.M1
