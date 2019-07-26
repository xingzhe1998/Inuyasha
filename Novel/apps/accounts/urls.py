from django.conf.urls import url
from .views import Register, Login, logout, PasswordForget, PasswordReset
urlpatterns = [
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^forget/$', PasswordForget.as_view(), name='forget'),
    url(r'^reset/$', PasswordReset.as_view(), name='reset'),
]