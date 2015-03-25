from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
    url(r'^signup/$', 'user_signup', name='signup'),
    url(r'^login/$', 'user_login', name='login'),
    url(r'^logout/$', 'user_logout', name='logout'),

    url(r'^verification/$', 'user_verification',
        name='user_verification'),
    url(r'^verify/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$', 'user_verify',
        name='user_verify'),

    url(r'^password-reset/$', 'user_password_reset',
        name='password_reset'),
    url(r'^password-reset/done/$', 'user_password_reset_done',
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>.+)/(?P<token>.+)/$',
        'user_password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', 'user_password_reset_complete',
        name='password_reset_complete'),
)
