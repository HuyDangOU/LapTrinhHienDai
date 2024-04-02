from django.urls import path, include
from rest_framework import routers
from ecourseapi import views
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('users', views.UserViewSet)
router.register('categories', views.CategoryViewSet)
router.register('lesson', views.LessonViewSet)
router.register('comment', views.CommentViewSet)


urlpatterns = [
    path('', include(router.urls))
]