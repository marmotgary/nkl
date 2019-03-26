from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter
from api import views

urlpatterns = [
    path('docs/', views.schema_view),
    path('csrf/', views.csrf),
    path('ping/', views.ping),
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('register/', views.RegistrationAPI.as_view())
]

router = SimpleRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'matches', views.MatchViewSet)
urlpatterns = router.urls + urlpatterns

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),

#     ] + urlpatterns
