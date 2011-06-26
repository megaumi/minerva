from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from main.views import ArticleCreateView, ArticleListView, IssueListView
from main.models import Article, MagazineIssue
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minerva.views.home', name='home'),
    # url(r'^minerva/', include('minerva.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

urlpatterns += patterns('main.views',
    #url(r'^$', 'home'),
    url(r'^issues/$', IssueListView.as_view()),
    url(r'^articles/(\d+)/$', ArticleListView.as_view()),
    url(r'^article/add/$', 'add_article'),
    url(r'^article/translate/(?P<article_id>\d+)/$', 'translate_article'),
    url(r'^add_translation/(\d+)/$', 'ajax_add_translation'),
    url(r'^get_comments/(\d+)/$', 'ajax_get_comments'),
    url(r'^translation_history/(\d+)/$', 'get_translation_history'),
)


#urlpatterns += patterns('',
    #url(r'^article/add/', ArticleCreateView.as_view(template_name="add_article.html")),
#)
