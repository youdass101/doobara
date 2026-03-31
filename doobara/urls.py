"""doobara URL Configuration

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
from django.views.generic import TemplateView
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from .sitemaps import CategorySitemap, ProductSitemap, StaticViewSitemap

def trigger_error(request):
    division_by_zero = 1 / 0

sitemaps = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "products": ProductSitemap,
}

urlpatterns = [
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots_txt',
    ),
    path('hamzeadmin/', admin.site.urls),
    path("", include("shop.urls")),
    path("", include("cart.urls")),
    path("", include("users.urls")),
    path("", include("blog.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]


if settings.DEBUG:
    # Keep Sentry's intentional crash route strictly in debug environments.
    urlpatterns += [path('sentry-debug/', trigger_error)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
