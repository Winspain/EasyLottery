from django.contrib import admin

# Register your models here.
from lottery.models import LotterySelectInfo, LotteryInfo, LotteryWebhookInfo


class LotterySelectAdmin(admin.ModelAdmin):
    list_display = ['id', 'frontNum1', 'frontNum2', 'frontNum3', 'frontNum4', 'frontNum5', 'backNum1', 'backNum2', 'isDeleted', 'createdTime']

    def add_view(self, request, form_url='', extra_context=None):
        data = request.POST.copy()
        data['createdBy'] = request.user.id
        request.POST = data
        return super(LotterySelectAdmin, self).add_view(request, form_url='', extra_context=extra_context)


class LotteryInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'drawNum', 'frontNum1', 'frontNum2', 'frontNum3', 'frontNum4', 'frontNum5', 'backNum1', 'backNum2', 'drawTime', 'createdTime']


class LotteryWebhookAdmin(admin.ModelAdmin):
    list_display = ['id', 'hookUrl', 'isDeleted', 'createdTime']


admin.site.register(LotteryInfo, LotteryInfoAdmin)
admin.site.register(LotterySelectInfo, LotterySelectAdmin)
admin.site.register(LotteryWebhookInfo, LotteryWebhookAdmin)
