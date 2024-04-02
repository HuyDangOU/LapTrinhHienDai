from rest_framework import serializers
from ecourseapi.models import Course, Category, Lesson, User, Tag, Comment


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        pre = super().to_representation(instance)
        pre["image"] = instance.image.url
        return pre


class CourseSerializer(ImageSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "created_date", "image", "category"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tag
        fields = ["id", "name"]

class LessonSerializer(ImageSerializer):
    class Meta:
        model = Lesson
        fields = ["course_id", "id", "content", "image", "created_date"]


class LessonSerializerDetails(LessonSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ["tags"]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',"avatar" ]





class CommentSerializer(serializers.ModelSerializer):
    user  = UserSerializer()
    lesson = LessonSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'lesson', 'user']