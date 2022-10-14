from django.db import models

# Create your models here.
from common.constant.number_choice import FRONT_CHOICE, BACK_CHOICE


class LotteryInfo(models.Model):
    drawNum = models.CharField(unique=True, max_length=50, verbose_name='开奖期号')
    frontNum1 = models.CharField(max_length=50)
    frontNum2 = models.CharField(max_length=50)
    frontNum3 = models.CharField(max_length=50)
    frontNum4 = models.CharField(max_length=50)
    frontNum5 = models.CharField(max_length=50)
    backNum1 = models.CharField(max_length=50)
    backNum2 = models.CharField(max_length=50)
    drawTime = models.DateField(verbose_name='开奖日期')
    isDeleted = models.BooleanField(default=0)
    createdBy = models.CharField(null=True, max_length=100)
    updateBy = models.CharField(null=True, max_length=100)
    createdTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'lottery_info'


class LotterySelectInfo(models.Model):
    frontNum1 = models.CharField(max_length=50, choices=FRONT_CHOICE)
    frontNum2 = models.CharField(max_length=50, choices=FRONT_CHOICE)
    frontNum3 = models.CharField(max_length=50, choices=FRONT_CHOICE)
    frontNum4 = models.CharField(max_length=50, choices=FRONT_CHOICE)
    frontNum5 = models.CharField(max_length=50, choices=FRONT_CHOICE)
    backNum1 = models.CharField(max_length=50, choices=BACK_CHOICE)
    backNum2 = models.CharField(max_length=50, choices=BACK_CHOICE)
    selectState = models.CharField(null=True, max_length=100)
    isDeleted = models.BooleanField()
    createdBy = models.CharField(null=True, max_length=100)
    updateBy = models.CharField(null=True, max_length=100)
    createdTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'lottery_select'


class LotteryWebhookInfo(models.Model):
    hookUrl = models.TextField()
    isDeleted = models.BooleanField()
    createdBy = models.CharField(null=True, max_length=100)
    updateBy = models.CharField(null=True, max_length=100)
    createdTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'lottery_webhook'
