# Generated by Django 5.1 on 2025-01-05 19:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0002_initial'),
        ('gamification', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievement',
            name='badge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.badge'),
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='completed_lessons',
            field=models.ManyToManyField(blank=True, to='courses.lesson'),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userprogress',
            unique_together={('user', 'course')},
        ),
    ]
