from django.urls import path, include

urlpatterns = [
    path('marketplace/', include(('api.marketplace.urls', 'marketplace'), namespace='marketplace')),
]