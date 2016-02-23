from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^', include('annotate.urls')),

    # Login stuff
    url(r'accounts/login/$',
        login,
        {'template_name': 'login.html'}),
]
