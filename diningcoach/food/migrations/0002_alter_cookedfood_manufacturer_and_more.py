# Generated by Django 4.2 on 2024-03-17 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookedfood',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='지역/제조사'),
        ),
        migrations.AlterField(
            model_name='customizedfood',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='지역/제조사'),
        ),
        migrations.AlterField(
            model_name='freshfood',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='지역/제조사'),
        ),
        migrations.AlterField(
            model_name='processedfood',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='지역/제조사'),
        ),
    ]
