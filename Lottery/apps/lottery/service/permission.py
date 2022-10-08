# -- coding utf-8 --
# @Time     2022/10/8 15:13
# @Author   dicardo
# @File     permission.py
# @Software PyCharm

from rest_framework.permissions import BasePermission


class CeleryPermission(BasePermission):
    def has_permission(self, request, view):
        ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1':
            return True
        return False
