from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Course, Lesson


class LessonAdmin(admin.ModelAdmin):

    list_display = [ 'subject', 'created_date', 'course', "active"]
    readonly_fields = ['this_image']
    def this_image(self, lesson):
        if lesson.image:
            return mark_safe(f'<img "src=/static/{lesson.image.name}" width ="120"/>')

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
