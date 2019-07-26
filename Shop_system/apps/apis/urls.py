"""shop_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^operators/$', views.operators, name="operators"),
    url(r'^shops/$', views.shops, name="shops"),
    url(r'^contracts/$', views.contracts, name="contract_load"),
    # url(r'^arrears/$', views.all_arrears, name="all_arrears"),
    # 这个id该是还没有传递到前端的
    url(r'^arrears(?P<contract_id>\d+)/$', views.contract_arrears, name="contract_arrears"),

]
