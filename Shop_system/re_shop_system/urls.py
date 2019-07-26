"""re_shop_system URL Configuration

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
from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',include('apps.index.urls',namespace='index')),
    url(r'^login/',include('apps.login.urls',namespace='login')),
    url(r'^operator/',include('apps.oper.urls',namespace='operator')),
    url(r'^shop/',include('apps.shop.urls',namespace='shop')),
    url(r'^contract/', include('apps.contract.urls',namespace='contract')),
    url(r'^rental/', include('apps.rental.urls',namespace='rental')),
    url(r'^apis/', include('apps.apis.urls',namespace='apis')),
    url(r'^welcome/', include('apps.welcome.urls',namespace='welcome')),
    url(r'^account/', include('apps.account.urls',namespace='account')),

]