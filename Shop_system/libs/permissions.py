"""
@file:   permissions.py
@author: Liu
@date:   2019/06/08
"""

from django.contrib.auth.decorators import user_passes_test


# 定义装饰器，
def admin_required(function=None, common_user_url="/403/"):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_superuser,  # 验证条件
        login_url=common_user_url,  # 不满足条件，跳转路径。不要被login_url语言意义迷惑，它的逻辑其实就判断条件False时的跳转路径
        redirect_field_name=None  # 满足条件
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class AdminRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(AdminRequiredMixin, cls).as_view(**initkwargs)
        return admin_required(view)
