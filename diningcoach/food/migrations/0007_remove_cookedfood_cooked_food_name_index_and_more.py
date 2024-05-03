# Generated by Django 4.2 on 2024-04-29 05:56

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_alter_cookedfood_food_image_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='cookedfood',
            name='cooked_food_name_index',
        ),
        migrations.RemoveIndex(
            model_name='customizedfood',
            name='customized_food_name_index',
        ),
        migrations.RemoveIndex(
            model_name='freshfood',
            name='fresh_food_name_index',
        ),
        migrations.RemoveIndex(
            model_name='processedfood',
            name='processed_food_name_index',
        ),
        migrations.AddIndex(
            model_name='cookedfood',
            index=django.contrib.postgres.indexes.GinIndex(fields=['food_name'], name='cooked_food_name_index', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='customizedfood',
            index=django.contrib.postgres.indexes.GinIndex(fields=['food_name'], name='customized_food_name_index', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='freshfood',
            index=django.contrib.postgres.indexes.GinIndex(fields=['food_name'], name='fresh_food_name_index', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='processedfood',
            index=django.contrib.postgres.indexes.GinIndex(fields=['food_name'], name='processed_food_name_index', opclasses=['gin_trgm_ops']),
        ),
    ]