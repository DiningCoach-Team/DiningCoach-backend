# Generated by Django 4.2 on 2024-03-25 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_alter_processednutrition_processed_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookednutrition',
            name='cooked_food',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='nutrition_info', serialize=False, to='food.cookedfood', verbose_name='조리식품'),
        ),
        migrations.AlterField(
            model_name='customizednutrition',
            name='customized_food',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='nutrition_info', serialize=False, to='food.customizedfood', verbose_name='사용자 추가식품'),
        ),
        migrations.AlterField(
            model_name='freshnutrition',
            name='fresh_food',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='nutrition_info', serialize=False, to='food.freshfood', verbose_name='신선식품'),
        ),
    ]
