from django.urls import path, include
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

admin.site.site_header = 'Администрирование Lotracker'
admin.site.site_title = 'Администрирование Lotracker'

router = DefaultRouter()

router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='API Documentation', permission_classes=[])),
    path('api/v1/', include([
        path('auth/', include(('authentication.urls.mobi', 'authentication'), namespace='authentication')),
        path('auth/', include(router.urls)),
        path('notifier/', include(('notifier.urls.mobi', 'notifier'), namespace='notifier')),
        path('', include(('lotracker.urls.mobi', 'lotracker'), namespace='lotracker')),
    ])),
    path('web/api/v1/', include([
        path('auth/', include(('authentication.urls.web', 'authentication'), namespace='web-authentication')),
        path('notifier/', include(('notifier.urls.web', 'notifier'), namespace='web-notifier')),
        path('', include(('lotracker.urls.web', 'lotracker'), namespace='web-lotracker')),
        path('faq/', include(('faq.urls', 'faq'), namespace='web-faq')),
        path('content/', include(('content.urls', 'content'), namespace='web-content')),
    ])),
]
