from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.OperatorList.as_view(),name='operator_list'),
    url(r'^operator_edit(?P<id>\d+)/$', views.OperatorEdit.as_view(),name='operator_edit'),
    url(r'^operator_add/$', views.AddOperator.as_view(),name='operator_add'),
]