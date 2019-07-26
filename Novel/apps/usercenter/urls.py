from django.conf.urls import url
from .views import Profile, ChangePasswd

urlpatterns = [
    url(r'^profile/$', Profile.as_view(), name='profile'),
    url(r'^cgpasswd/$', ChangePasswd.as_view(), name='cgpasswd'),
]