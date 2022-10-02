from django.db import models


# Create your models here.

class LotteryInfo(models.Model):
    drawNum = models.CharField(unique=True, max_length=50, verbose_name='开奖期号')
    frontNum1 = models.IntegerField()
    frontNum2 = models.IntegerField()
    frontNum3 = models.IntegerField()
    frontNum4 = models.IntegerField()
    frontNum5 = models.IntegerField()
    backNum1 = models.IntegerField()
    backNum2 = models.IntegerField()
    drawTime = models.DateField(verbose_name='开奖日期')
    isDeleted = models.BooleanField(default=0)
    createdBy = models.CharField(null=True, max_length=100)
    updateBy = models.CharField(null=True, max_length=100)
    createdTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'lottery_info'


class LotterySelectInfo(models.Model):
    frontNum1 = models.IntegerField()
    frontNum2 = models.IntegerField()
    frontNum3 = models.IntegerField()
    frontNum4 = models.IntegerField()
    frontNum5 = models.IntegerField()
    backNum1 = models.IntegerField()
    backNum2 = models.IntegerField()
    selectState = models.CharField(max_length=100)
    isDeleted = models.BooleanField()
    createdBy = models.CharField(max_length=100)
    updateBy = models.CharField(max_length=100)
    createdTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'lottery_select'
