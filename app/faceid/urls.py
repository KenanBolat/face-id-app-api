"""
URL mappings for the faceid app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from faceid import views

router = DefaultRouter()
router.register('faceid', views.FaceIDViewSet)
router.register('foreigner', views.ForeignerViewSet)
"""
URL mappings for the faceid app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from faceid import views

router = DefaultRouter()
router.register('faceid', views.FaceIDViewSet)
router.register('foreigner', views.ForeignerViewSet)


app_name = 'faceid'

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'foreigner'

urlpatterns = [
    path('', include(router.urls)),
]
