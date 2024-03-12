# Generated by Django 5.0.3 on 2024-03-12 08:08

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecourseapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('subject', models.CharField(max_length=255)),
                ('content', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(null=True, upload_to='lesson/%Y/%m')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='ecourseapi.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
