# Generated by Django 4.1.3 on 2022-11-16 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstaApp', '0007_story'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='static/posts'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(upload_to='static/profilepics'),
        ),
    ]
