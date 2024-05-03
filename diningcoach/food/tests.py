from django.db import connection
from django.urls import reverse

from food.models import ProcessedFood, ProcessedNutrition

from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class FoodAPITestCase(APITestCase):
  # @classmethod
  # def setUpClass(cls) -> None:
  #   with connection.cursor() as cursor:
  #     cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
  #   super().setUpClass()

  @classmethod
  def setUpTestData(cls) -> None:
    cls.client = APIClient()

    processed_food5_data = {
      'id': 5,
      'food_code': 'P000006-ZZ-AVG',
      'food_name': '찹쌀 약과',
      'country_origin': '대한민국',
      'manufacturer': '성진식품',
      'category_main': '과자',
      'category_sub': '한과류',
      'food_image': None,
      'allergy_info': None,
      'storage_info': None,
      'barcode_no': '8809647020763',
    }
    processed_food5_instance = ProcessedFood.objects.create(**processed_food5_data)

    processed_nutrition5_data = {
      'amount_per_serving': 40.0,
      'calorie': 155.0,
      'carbohydrate': 0.0,
      'sugar': 10.0,
      'protein': 0.0,
      'fat': 0.0,
      'cholesterol': 0.0,
      'sodium': 11.0,
      'saturated_fat': 1.0,
      'trans_fat': 0.0,
      'processed_food': processed_food5_instance,
    }
    ProcessedNutrition.objects.create(**processed_nutrition5_data)

    processed_food20_data = {
      'id': 20,
      'food_code': 'P000021-ZZ-AVG',
      'food_name': '통밀 뻥튀기',
      'country_origin': '대한민국',
      'manufacturer': '우주통상',
      'category_main': '과자',
      'category_sub': '기타과자',
      'food_image': None,
      'allergy_info': None,
      'storage_info': None,
      'barcode_no': '8809647026270',
    }
    processed_food20_instance = ProcessedFood.objects.create(**processed_food20_data)

    processed_nutrition20_data = {
      'amount_per_serving': 30.0,
      'calorie': 115.0,
      'carbohydrate': 0.0,
      'sugar': 1.0,
      'protein': 0.0,
      'fat': 0.0,
      'cholesterol': 0.0,
      'sodium': 46.0,
      'saturated_fat': 0.1,
      'trans_fat': 0.0,
      'processed_food': processed_food20_instance,
    }
    ProcessedNutrition.objects.create(**processed_nutrition20_data)

  def test_scan_barcode_success(self) -> None:
    scan_barcode_url = reverse('scan_barcode', kwargs={'barcode_no': '8809647020763'})
    scan_barcode_response = self.client.get(scan_barcode_url)
    scan_barcode_data = scan_barcode_response.data[0]

    self.assertEqual(scan_barcode_response.status_code, status.HTTP_200_OK)
    self.assertEqual(scan_barcode_data['id'], 5)
    self.assertEqual(scan_barcode_data['food_name'], '찹쌀 약과')

  def test_scan_barcode_fail(self) -> None:
    scan_barcode_url = reverse('scan_barcode', kwargs={'barcode_no': 'kk'})
    scan_barcode_response = self.client.get(scan_barcode_url)
    scan_barcode_data = scan_barcode_response.data

    self.assertEqual(scan_barcode_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(scan_barcode_data['error_message'][0], 'F1')
    self.assertEqual(scan_barcode_data['error_code'], 400)

  def test_search_processed_success(self) -> None:
    search_processed_url = '?'.join([reverse('search_processed'), 'id=20'])
    search_processed_response = self.client.get(search_processed_url)
    search_processed_data = search_processed_response.data[0]

    self.assertEqual(search_processed_response.status_code, status.HTTP_200_OK)
    self.assertEqual(search_processed_data['id'], 20)
    self.assertEqual(search_processed_data['food_name'], '통밀 뻥튀기')

  def test_search_processed_fail(self) -> None:
    search_processed_url = '?'.join([reverse('search_processed'), 'id=0'])
    search_processed_response = self.client.get(search_processed_url)
    search_processed_data = search_processed_response.data

    self.assertEqual(search_processed_response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(search_processed_data['error_message'][0], 'F2')
    self.assertEqual(search_processed_data['error_code'], 404)

  def test_detail_processed_success(self) -> None:
    detail_processed_url = reverse('detail_processed', kwargs={'id': '20'})
    detail_processed_response = self.client.get(detail_processed_url)
    detail_processed_data = detail_processed_response.data

    self.assertEqual(detail_processed_response.status_code, status.HTTP_200_OK)
    self.assertEqual(detail_processed_data['id'], 20)
    self.assertEqual(detail_processed_data['food_name'], '통밀 뻥튀기')

  def test_detail_processed_fail(self) -> None:
    detail_processed_url = reverse('detail_processed', kwargs={'id': '0'})
    detail_processed_response = self.client.get(detail_processed_url)
    detail_processed_data = detail_processed_response.data

    self.assertEqual(detail_processed_response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(detail_processed_data['error_message'].title(), 'Not Found.')
    self.assertEqual(detail_processed_data['error_code'], 404)
