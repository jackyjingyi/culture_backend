from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, SurveyViewSet

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'', SurveyViewSet, basename='survey')

urlpatterns = [
    path('', include(router.urls))

]
