"""testsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

# Add URL maps to redirect the base URL to app
from django.views.generic import TemplateView, RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='/getRoute/', permanent=True)),
    # path('getRoute/templates',
    #      TemplateView.as_view(template_name='base.html'),
    #      name='home')
    url(r'^$', TemplateView.as_view(template_name="getRoute/default.html"),
        name='home'),
]

# Use include() to add paths from the getRoute app
urlpatterns += [
    url(r'', include('getRoute.urls')),
    # path('getRoute/', include('getRoute.urls')),
]

# Use Static() to add url mapping to serve static files during development (only)
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
