# Generated by Django 4.2 on 2024-04-11 11:34

import diary.models
import diningcoach.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_alter_mealdiary_user_alter_mealfood_meal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealimage',
            name='image_url',
            field=models.ImageField(storage=diningcoach.storage.FileSystemOverwriteStorage(), upload_to=diary.models.meal_image_path, verbose_name='이미지 주소'),
        ),
    ]