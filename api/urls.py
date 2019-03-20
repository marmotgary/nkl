from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('teams/', views.TeamList.as_view()),
    path('teams/<int:pk>', views.TeamDetail.as_view()),
    path('matches/', views.MatchList.as_view()),
    path('matches/<int:pk>', views.MatchDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns) # Allows e.g. /api/users/3.json

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),

#     ] + urlpatterns
