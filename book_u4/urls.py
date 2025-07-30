
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.i18n import set_language

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('',include('book.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('i18n/setlang/', set_language, name='set_language'),
    path('accounts/', include('user.urls')),
    path('pro/', include('page.urls')),
    path('captcha/', include('captcha.urls')),

)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]