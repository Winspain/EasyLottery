# -- coding utf-8 --
# @Time     2022/5/14 下午10:16
# @Author   dicardo
# @File     lottery_serializer.py
# @Software PyCharm

from rest_framework import serializers

from lottery.models import LotterySelectInfo, LotteryInfo


class LotterySelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotterySelectInfo
        fields = '__all__'


class Lottery500Serializer(serializers.ModelSerializer):
    class Meta:
        model = LotteryInfo
        fields = '__all__'
