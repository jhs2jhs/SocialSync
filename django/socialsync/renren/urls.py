from django.conf.urls import patterns, include, url

urlpatterns = patterns('renren.views',
    url(r'^test', 'test'),
    url(r'oauth_request', 'oauth_request'),
    url(r'oauth_redirect', 'oauth_redirect'),
    #url(r'oauth_response', 'oauth_response'),
)
