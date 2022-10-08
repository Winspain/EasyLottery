from django.contrib import admin

# Register your models here.
from lottery.models import LotterySelectInfo


class LotteryAdmin(admin.ModelAdmin):
    list_display = ['frontNum1', 'frontNum2', 'frontNum3', 'frontNum4', 'frontNum5', 'backNum1', 'backNum2', 'isDeleted', 'createdTime']


admin.site.register(LotterySelectInfo, LotteryAdmin)
