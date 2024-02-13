from django.urls import path, include

urlpatterns = [
    path('marketplace/', include(('api.marketplace.urls', 'marketplace'), namespace='marketplace')),
    path('authentication/', include(('api.authentication.urls', 'authentication'), namespace='authentication')),
    path('users/', include(('api.user.urls', 'user'), namespace='user')),
]