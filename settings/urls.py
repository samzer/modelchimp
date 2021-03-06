from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_control


urlpatterns = [
    url(r'^api/', include('modelchimp.api_urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^hq/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns  + static(settings.MEDIA_URL,
                                document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^sw.js', cache_control(max_age=2592000)(TemplateView.as_view(
        template_name="sw.js",
        content_type='application/javascript',
        )), name='sw.js'),
        url(r'^.*', TemplateView.as_view(template_name="index.html"), name="home"),
        ];
