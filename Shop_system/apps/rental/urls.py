from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.RentaltList.as_view(),name='rental_list'),
    url(r'^add/$', views.RentalAdd.as_view(),name='rental_add'),
    url(r'^gather/$', views.RentalGather.as_view(),name='rental_gather'),
    url(r'^edit(?P<id>\d+)/$', views.RentalEdit.as_view(),name='rental_edit'),
]