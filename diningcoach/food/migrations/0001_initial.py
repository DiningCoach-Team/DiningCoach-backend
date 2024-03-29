# Generated by Django 4.2 on 2024-03-17 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookedFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_code', models.CharField(max_length=50, unique=True, verbose_name='식품코드')),
                ('food_name', models.CharField(max_length=255, verbose_name='식품명')),
                ('country_origin', models.CharField(blank=True, max_length=50, null=True, verbose_name='제조국가')),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True, verbose_name='지역/제조사')),
                ('category_main', models.CharField(max_length=50, verbose_name='식품대분류')),
                ('category_sub', models.CharField(max_length=50, verbose_name='식품상세분류')),
                ('food_image', models.TextField(blank=True, null=True, verbose_name='식품 이미지')),
                ('allergy_info', models.TextField(blank=True, null=True, verbose_name='알레르기 정보')),
                ('storage_info', models.TextField(blank=True, null=True, verbose_name='보관방법 정보')),
                ('product_type', models.CharField(max_length=50, verbose_name='상용제품')),
            ],
            options={
                'verbose_name': '조리식품',
                'verbose_name_plural': '조리식품',
                'db_table': 'cooked_food',
            },
        ),
        migrations.CreateModel(
            name='CustomizedFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_code', models.CharField(max_length=50, unique=True, verbose_name='식품코드')),
                ('food_name', models.CharField(max_length=255, verbose_name='식품명')),
                ('country_origin', models.CharField(blank=True, max_length=50, null=True, verbose_name='제조국가')),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True, verbose_name='지역/제조사')),
                ('category_main', models.CharField(max_length=50, verbose_name='식품대분류')),
                ('category_sub', models.CharField(max_length=50, verbose_name='식품상세분류')),
                ('food_image', models.TextField(blank=True, null=True, verbose_name='식품 이미지')),
                ('allergy_info', models.TextField(blank=True, null=True, verbose_name='알레르기 정보')),
                ('storage_info', models.TextField(blank=True, null=True, verbose_name='보관방법 정보')),
            ],
            options={
                'verbose_name': '사용자 추가식품',
                'verbose_name_plural': '사용자 추가식품',
                'db_table': 'customized_food',
            },
        ),
        migrations.CreateModel(
            name='FreshFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_code', models.CharField(max_length=50, unique=True, verbose_name='식품코드')),
                ('food_name', models.CharField(max_length=255, verbose_name='식품명')),
                ('country_origin', models.CharField(blank=True, max_length=50, null=True, verbose_name='제조국가')),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True, verbose_name='지역/제조사')),
                ('category_main', models.CharField(max_length=50, verbose_name='식품대분류')),
                ('category_sub', models.CharField(max_length=50, verbose_name='식품상세분류')),
                ('food_image', models.TextField(blank=True, null=True, verbose_name='식품 이미지')),
                ('allergy_info', models.TextField(blank=True, null=True, verbose_name='알레르기 정보')),
                ('storage_info', models.TextField(blank=True, null=True, verbose_name='보관방법 정보')),
                ('harvest_time', models.CharField(max_length=50, verbose_name='채취시기')),
            ],
            options={
                'verbose_name': '신선식품',
                'verbose_name_plural': '신선식품',
                'db_table': 'fresh_food',
            },
        ),
        migrations.CreateModel(
            name='ProcessedFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_code', models.CharField(max_length=50, unique=True, verbose_name='식품코드')),
                ('food_name', models.CharField(max_length=255, verbose_name='식품명')),
                ('country_origin', models.CharField(blank=True, max_length=50, null=True, verbose_name='제조국가')),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True, verbose_name='지역/제조사')),
                ('category_main', models.CharField(max_length=50, verbose_name='식품대분류')),
                ('category_sub', models.CharField(max_length=50, verbose_name='식품상세분류')),
                ('food_image', models.TextField(blank=True, null=True, verbose_name='식품 이미지')),
                ('allergy_info', models.TextField(blank=True, null=True, verbose_name='알레르기 정보')),
                ('storage_info', models.TextField(blank=True, null=True, verbose_name='보관방법 정보')),
                ('barcode_no', models.CharField(max_length=50, verbose_name='유통바코드')),
            ],
            options={
                'verbose_name': '가공식품',
                'verbose_name_plural': '가공식품',
                'db_table': 'processed_food',
            },
        ),
        migrations.CreateModel(
            name='CookedNutrition',
            fields=[
                ('amount_per_serving', models.FloatField(blank=True, default=0.0, null=True, verbose_name='1회제공량(g)')),
                ('calorie', models.FloatField(blank=True, default=0.0, null=True, verbose_name='칼로리(kcal)')),
                ('carbohydrate', models.FloatField(blank=True, default=0.0, null=True, verbose_name='탄수화물(g)')),
                ('sugar', models.FloatField(blank=True, default=0.0, null=True, verbose_name='당류(g)')),
                ('protein', models.FloatField(blank=True, default=0.0, null=True, verbose_name='단백질(g)')),
                ('fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='지방(g)')),
                ('cholesterol', models.FloatField(blank=True, default=0.0, null=True, verbose_name='콜레스테롤(mg)')),
                ('sodium', models.FloatField(blank=True, default=0.0, null=True, verbose_name='나트륨(mg)')),
                ('saturated_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='포화지방(g)')),
                ('trans_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='트랜스지방(g)')),
                ('cooked_food', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='food.cookedfood', verbose_name='조리식품')),
            ],
            options={
                'verbose_name': '조리식품 영양정보',
                'verbose_name_plural': '조리식품 영양정보',
                'db_table': 'cooked_nutrition',
            },
        ),
        migrations.CreateModel(
            name='CustomizedMetadata',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('customized_food', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='food.customizedfood', verbose_name='사용자 추가식품')),
                ('food_type', models.CharField(choices=[(1, 'Processed Food'), (2, 'Fresh Food'), (3, 'Cooked Food')], max_length=50, verbose_name='식품 종류')),
                ('additional_info', models.TextField(blank=True, null=True, verbose_name='추가정보')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
            ],
            options={
                'verbose_name': '사용자 추가식품 메타데이터',
                'verbose_name_plural': '사용자 추가식품 메타데이터',
                'db_table': 'customized_metadata',
            },
        ),
        migrations.CreateModel(
            name='CustomizedNutrition',
            fields=[
                ('amount_per_serving', models.FloatField(blank=True, default=0.0, null=True, verbose_name='1회제공량(g)')),
                ('calorie', models.FloatField(blank=True, default=0.0, null=True, verbose_name='칼로리(kcal)')),
                ('carbohydrate', models.FloatField(blank=True, default=0.0, null=True, verbose_name='탄수화물(g)')),
                ('sugar', models.FloatField(blank=True, default=0.0, null=True, verbose_name='당류(g)')),
                ('protein', models.FloatField(blank=True, default=0.0, null=True, verbose_name='단백질(g)')),
                ('fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='지방(g)')),
                ('cholesterol', models.FloatField(blank=True, default=0.0, null=True, verbose_name='콜레스테롤(mg)')),
                ('sodium', models.FloatField(blank=True, default=0.0, null=True, verbose_name='나트륨(mg)')),
                ('saturated_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='포화지방(g)')),
                ('trans_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='트랜스지방(g)')),
                ('customized_food', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='food.customizedfood', verbose_name='사용자 추가식품')),
            ],
            options={
                'verbose_name': '사용자 추가식품 영양정보',
                'verbose_name_plural': '사용자 추가식품 영양정보',
                'db_table': 'customized_nutrition',
            },
        ),
        migrations.CreateModel(
            name='FreshNutrition',
            fields=[
                ('amount_per_serving', models.FloatField(blank=True, default=0.0, null=True, verbose_name='1회제공량(g)')),
                ('calorie', models.FloatField(blank=True, default=0.0, null=True, verbose_name='칼로리(kcal)')),
                ('carbohydrate', models.FloatField(blank=True, default=0.0, null=True, verbose_name='탄수화물(g)')),
                ('sugar', models.FloatField(blank=True, default=0.0, null=True, verbose_name='당류(g)')),
                ('protein', models.FloatField(blank=True, default=0.0, null=True, verbose_name='단백질(g)')),
                ('fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='지방(g)')),
                ('cholesterol', models.FloatField(blank=True, default=0.0, null=True, verbose_name='콜레스테롤(mg)')),
                ('sodium', models.FloatField(blank=True, default=0.0, null=True, verbose_name='나트륨(mg)')),
                ('saturated_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='포화지방(g)')),
                ('trans_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='트랜스지방(g)')),
                ('fresh_food', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='food.freshfood', verbose_name='신선식품')),
            ],
            options={
                'verbose_name': '신선식품 영양정보',
                'verbose_name_plural': '신선식품 영양정보',
                'db_table': 'fresh_nutrition',
            },
        ),
        migrations.CreateModel(
            name='ProcessedNutrition',
            fields=[
                ('amount_per_serving', models.FloatField(blank=True, default=0.0, null=True, verbose_name='1회제공량(g)')),
                ('calorie', models.FloatField(blank=True, default=0.0, null=True, verbose_name='칼로리(kcal)')),
                ('carbohydrate', models.FloatField(blank=True, default=0.0, null=True, verbose_name='탄수화물(g)')),
                ('sugar', models.FloatField(blank=True, default=0.0, null=True, verbose_name='당류(g)')),
                ('protein', models.FloatField(blank=True, default=0.0, null=True, verbose_name='단백질(g)')),
                ('fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='지방(g)')),
                ('cholesterol', models.FloatField(blank=True, default=0.0, null=True, verbose_name='콜레스테롤(mg)')),
                ('sodium', models.FloatField(blank=True, default=0.0, null=True, verbose_name='나트륨(mg)')),
                ('saturated_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='포화지방(g)')),
                ('trans_fat', models.FloatField(blank=True, default=0.0, null=True, verbose_name='트랜스지방(g)')),
                ('processed_food', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='food.processedfood', verbose_name='가공식품')),
            ],
            options={
                'verbose_name': '가공식품 영양정보',
                'verbose_name_plural': '가공식품 영양정보',
                'db_table': 'processed_nutrition',
            },
        ),
        migrations.AddIndex(
            model_name='processedfood',
            index=models.Index(fields=['food_code'], name='processed_food_code_index'),
        ),
        migrations.AddIndex(
            model_name='processedfood',
            index=models.Index(fields=['food_name'], name='processed_food_name_index'),
        ),
        migrations.AddIndex(
            model_name='processedfood',
            index=models.Index(fields=['category_main', 'category_sub'], name='processed_food_category_index'),
        ),
        migrations.AddIndex(
            model_name='processedfood',
            index=models.Index(fields=['barcode_no'], name='processed_food_barcode_index'),
        ),
        migrations.AddIndex(
            model_name='freshfood',
            index=models.Index(fields=['food_code'], name='fresh_food_code_index'),
        ),
        migrations.AddIndex(
            model_name='freshfood',
            index=models.Index(fields=['food_name'], name='fresh_food_name_index'),
        ),
        migrations.AddIndex(
            model_name='freshfood',
            index=models.Index(fields=['category_main', 'category_sub'], name='fresh_food_category_index'),
        ),
        migrations.AddField(
            model_name='customizedfood',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='회원'),
        ),
        migrations.AddIndex(
            model_name='cookedfood',
            index=models.Index(fields=['food_code'], name='cooked_food_code_index'),
        ),
        migrations.AddIndex(
            model_name='cookedfood',
            index=models.Index(fields=['food_name'], name='cooked_food_name_index'),
        ),
        migrations.AddIndex(
            model_name='cookedfood',
            index=models.Index(fields=['category_main', 'category_sub'], name='cooked_food_category_index'),
        ),
        migrations.AddIndex(
            model_name='customizedfood',
            index=models.Index(fields=['food_code'], name='customized_food_code_index'),
        ),
        migrations.AddIndex(
            model_name='customizedfood',
            index=models.Index(fields=['food_name'], name='customized_food_name_index'),
        ),
        migrations.AddIndex(
            model_name='customizedfood',
            index=models.Index(fields=['category_main', 'category_sub'], name='customized_food_category_index'),
        ),
    ]
