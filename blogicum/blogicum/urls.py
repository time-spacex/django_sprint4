from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar


handler404 = 'core.views.page_not_found'
handler403 = 'core.views.csrf_failure'
handler500 = 'core.views.server_error'


urlpatterns: list = [
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(())
    urlpatterns.append()'''
