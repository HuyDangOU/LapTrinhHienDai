from rest_framework import permissions, views
from rest_framework import viewsets, generics

from ecourseapi import app_permission
from ecourseapi.serializers import CourseSerializer, UserSerializer, CategorySerializer, LessonSerializer, \
    LessonSerializerDetails, CommentSerializer
from ecourseapi.models import Course, User, Category, Lesson, Comment
from ecourseapi.paginators import CoursePaginator, CommentPaginator
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

    @action(methods=['get'], detail=True, url_path="lessons")
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        return Response(data=LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=["get", 'patch'], url_path="current_user", detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__("PATCH"):
            data = request.data
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return Response(self.get_serializer(user).data)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    serializer_class = LessonSerializerDetails
    queryset = Lesson.objects.prefetch_related("tags").filter(active=True)

    def get_permissions(self):
        if self.action in ['comment']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=["post"], url_path="comment", detail=True)
    def comment(self, request, pk):

        user = request.user
        lesson = self.get_object()
        if request.method.__eq__("POST"):
            comment = lesson.comment_set.create(content=request.data.get('content'), user=user)
            return Response(data=CommentSerializer(comment).data, status=status.HTTP_201_CREATED)




    @action(methods=["get"], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.all()
        paginator = CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [app_permission.CommentOwnerPermission]

