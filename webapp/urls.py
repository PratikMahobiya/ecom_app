from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'', views.Index, name = 'Index'),
    path(r'checkout/', views.Checkout, name = 'CheckOut'),
    path(r'order/', views.Order, name = 'Orders'),
    path(r'single/', views.single_page, name = 'SingleProduct'),
    path(r'invoice/', views.get_invoice, name = 'Invoice'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)