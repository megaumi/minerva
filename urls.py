from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minerva.views.home', name='home'),
    # url(r'^minerva/', include('minerva.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('main.views',
    url(r'^article/add/', 'main.views.add_article'),
    url(r'^article/translate/(\d+)', 'main.views.translate_article'),
)
