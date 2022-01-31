from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'usercart/', views.UserCartView.as_view(), name = 'UserCart'),
    path(r'order/', views.OrderView.as_view(), name = 'Order'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)