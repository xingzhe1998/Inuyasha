from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile$', views.AccProfile.as_view(),name='profile'),
    url(r'^change_passwd/$', views.ChangePasswd.as_view(),name='change_passwd'),
    url(r'^user_list/$', views.UserList.as_view(),name='user_list'),
    url(r'^reset_passwd(?P<id>\d+)/$', views.ResetPasswd.as_view(),name='reset_passwd'),
    url(r'^user_add/$', views.UserAdd.as_view(),name='user_add'),
    url(r'^user_logout/$', views.Logout.as_view(),name='user_logout'),
    url(r'^user/(\d+)/$', views.Memberedit.as_view(), name='member_edit'),
]