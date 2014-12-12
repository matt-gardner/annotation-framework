from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('annotate.urls')),

    # Login stuff
    (r'accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
)
