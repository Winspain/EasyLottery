# -- coding utf-8 --
# @Time     2021/6/27 21:40
# @Author   dicardo
# @File     api_router.py
# @Software PyCharm

"""drf路由"""
from rest_framework.routers import DefaultRouter

from lottery.views.lottery_view import MyLotteryView
from users.views.example_views import ExampleView

router = DefaultRouter()
urlpatterns = router.urls
router.register('example/v1/celery', ExampleView, basename='ExampleView')
router.register('easyLottery/v1/myLottery', MyLotteryView, basename='MyLotteryView')
