"""
URL configuration for DOcument project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView

# Только на период разработки
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Используйте include() чтобы добавлять URL из каталога приложения

# urlpatterns += [
#      path('catalog/', include('catalog.urls')),
# ]


# # Добавьте URL соотношения, чтобы перенаправить запросы с корневого URL, на URL приложения

# # urlpatterns += [
# #     path('', RedirectView.as_view(url='/catalog/', permanent=True)),
# # ]


# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.DATA_FILE_URL, document_root=settings.DATA_FILE_ROOT)
