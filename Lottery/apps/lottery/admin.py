from django.contrib import admin

# Register your models here.
from lottery.models import LotterySelectInfo, LotteryInfo


class LotterySelectAdmin(admin.ModelAdmin):
    list_display = ['id', 'frontNum1', 'frontNum2', 'frontNum3', 'frontNum4', 'frontNum5', 'backNum1', 'backNum2', 'isDeleted', 'createdTime']


class LotteryInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'drawNum', 'frontNum1', 'frontNum2', 'frontNum3', 'frontNum4', 'frontNum5', 'backNum1', 'backNum2', 'drawTime', 'createdTime']


admin.site.register(LotteryInfo, LotteryInfoAdmin)
admin.site.register(LotterySelectInfo, LotterySelectAdmin)
