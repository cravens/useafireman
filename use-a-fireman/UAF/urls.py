"""UAF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""


from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic.base import TemplateView


from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

class index(TemplateView):
    template_name = "Landing.html"


admin.autodiscover()

urlpatterns = patterns('')

from django.conf import settings
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)

urlpatterns = [
    #url(r'(?P<email>[0-9A-Za-z._%+-]+)/', index.as_view(), name='index'),
    url(r'^email/', 'UAF.views.emailview', name='emailview'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/register/$', 'UAF.views.register', name='register'),
    #url(r'^accounts/register/complete/$', 'UAF.views.registration_complete', name='registration_complete'),
    #url(r'^accounts/', include('allauth.urls')),
    #url(r'^datetime/$', 'UAF.views.current_datetime', name="datetime"),
    url(r'^$', index.as_view(), name='index'),
    url(r'(?P<email>\w+)/', index.as_view(), name='index'),
    #url(r'^email/send/$', template_name="emailtemplate.html", name="sendmail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)