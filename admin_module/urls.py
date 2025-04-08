"""
URL configuration for admin_module project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from apps.tour_package import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.user_login.urls', 'user_login'), namespace='user_login')),
    path('', include(('apps.tourism_company.urls', 'tourism_company'), namespace='tourism_company')),
    path('', include(('apps.tour_package.urls', 'tour_package'), namespace='tour_package')),
    path('', include(('apps.Guides.urls', 'Guides'), namespace='Guides')),
    path('', include(('apps.hotelbooking.urls', 'hotelbooking'), namespace='hotelbooking')),
    path('', include(('apps.bookings.urls', 'bookings'), namespace='bookings')),
    path('', include(('apps.reviews.urls', 'reviews'), namespace='reviews')),
    path('', include(('apps.social_community.urls', 'social_community'), namespace='social_community')),
    path('', include(('apps.expense_tracker.urls', 'expense_tracker'), namespace='expense_tracker')),
    path('maps/', include(('apps.maps.urls', 'maps'), namespace='maps')),
    path('social_stories/', include(('apps.social_stories.urls', 'social_stories'), namespace='social_stories')),
]


# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


