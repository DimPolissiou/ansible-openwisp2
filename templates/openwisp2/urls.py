from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django_netjsonconfig.admin_theme.admin import admin, openwisp_admin

openwisp_admin()

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='devices_home', permanent=True), name='index'),
    url(r'^devices/', include('devices.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login$', login, name='cas_ng_login'),
    url(r'^accounts/logout$', logout, name='cas_ng_logout'),
    url(r'^accounts/callback$', callback, name='cas_ng_proxy_callback'),
    url(r'^collectd_rest/', include('collectd_rest.urls')),
    
    # controller URLs
    # used by devices to download/update their configuration
    # keep the namespace argument unchanged
    url(r'^', include('django_netjsonconfig.controller.urls', namespace='controller')),
    # common URLs
    # shared among django-netjsonconfig components
    # keep the namespace argument unchanged
    url(r'^', include('django_netjsonconfig.urls', namespace='netjsonconfig')),
    # django-x509 urls
    # keep the namespace argument unchanged
    url(r'^', include('django_x509.urls', namespace='x509')),
]

urlpatterns += staticfiles_urlpatterns()
