"""
Zenboard main urls config
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from zenboard import views as zenboard_views


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^$', zenboard_views.HomeView.as_view(), name='home'),

    url(r'^boards/', include('boards.urls', namespace='boards')),
    url(r'^webhooks/', include('webhooks.urls', namespace='webhooks')),

    # Auth
    url(r'^login/$', zenboard_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', zenboard_views.LogoutView.as_view(), name='logout'),

    # API
    url(r'^api/', include([
        url(r'^', include('zenboard.api_urls', namespace='api')),
        url(r'^docs/', include_docs_urls(title='Zenboard API')),
        url(r'^schema/$', get_schema_view(title='Zenboard API')),
    ])),

    # Django Admin
    url(r'^django_admin/', admin.site.urls),
]
