# Generated by Django 5.1 on 2025-01-05 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_question_lesson_estimated_time_lesson_points_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='course_thumbnails/'),
        ),
    ]
