from django.shortcuts import render
from rest_framework import viewsets, generics
from ecourseapi.serializers import CourseSerializer, UserSerializer, CategorySerializer, LessonSerializer, \
    LessonSerializerDetails
from ecourseapi.models import Course, User, Category, Lesson
from ecourseapi.paginators import CoursePaginator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.filter(active=True)
    pagination_class = CoursePaginator

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get("q")
        if q:
            queryset = queryset.filter(name__icontains=q)
        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @action(methods=['get'], detail=True,  url_path="lessons")
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        return Response(data=LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    serializer_class = LessonSerializerDetails
    queryset = Lesson.objects.prefetch_related("tags").filter(active=True)
