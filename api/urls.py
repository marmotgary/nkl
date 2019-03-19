from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<int:pk>', views.user_detail),
    path('teams/', views.team_list),
    path('teams/<int:pk>', views.team_detail),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
