from django.urls import path, include

urlpatterns = [
    path('academic/', include(('api.academy.urls', 'academic'), namespace='academic')),
    path('marketplace/', include(('api.marketplace.urls', 'marketplace'), namespace='marketplace')),
    path('authentication/', include(('api.authentication.urls', 'authentication'), namespace='authentication')),
    path('users/', include(('api.user.urls', 'user'), namespace='user')),
]