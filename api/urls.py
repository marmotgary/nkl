from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter
from api import views

urlpatterns = [
    path('docs', views.schema_view)
]

router = SimpleRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'matches', views.MatchViewSet)
urlpatterns = router.urls + urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
