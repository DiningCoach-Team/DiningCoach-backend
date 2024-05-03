import os

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from user.models import User
from diary.models import MealDiary, MealFood, MealImage

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken


class DiaryAPITestCase(APITestCase):
  # Class constants
  BASE_PATH = '/Users/hglee/Documents'
  IMAGE_NAME = '알레르기 정보 표시.jpg'

  # Class variables
  client = None
  access_token = None
  food_image = None

  @classmethod
  def setUpTestData(cls) -> None:
    cls.client = APIClient()

    # Set up food image
    with open(os.path.join(cls.BASE_PATH, cls.IMAGE_NAME), 'rb') as image_file:
      cls.food_image = SimpleUploadedFile(name=cls.IMAGE_NAME, content=image_file.read(), content_type='image/jpeg')

    # Set up user
    user_setup_data = {
      'username': 'test-diary',
      'email': 'test-diary@diningcoach.org',
      'password': 'Password1*',
      'platform_type': 'D',
      'platform_id': None,
      'user_agent': 'TEST HTTP USER AGENT',
    }
    user = User.objects.create_user(**user_setup_data)
    cls.access_token = AccessToken.for_user(user=user)
    cls.client.credentials(HTTP_AUTHORIZATION=f'Bearer {cls.access_token}')

    # Set up meal diary
    diary_write_url = reverse('diary_write')
    diary_write_data = {
      'date': '2024-05-01',
      'meal_type': 'B',
      'content': '식단일기 테스트입니다.',
      'is_favourite': False,
      'is_public': False,
      'is_deleted': False,
      'meal_image[0]image_url': cls.food_image,
      'meal_food[0]food_code': 'P000006-ZZ-AVG',
      'meal_food[0]food_name': '찹쌀 약과',
      'meal_food[0]food_type': 'P',
      'meal_food[0]portion': 1.0,
    }
    cls.client.post(diary_write_url, diary_write_data, format='multipart')

  def setUp(self) -> None:
    with open(os.path.join(self.BASE_PATH, self.IMAGE_NAME), 'rb') as image_file:
      self.food_image = SimpleUploadedFile(name=self.IMAGE_NAME, content=image_file.read(), content_type='image/jpeg')
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

  ##### Success Test Case #####
  def test_diary_write_success(self) -> None:
    diary_write_url = reverse('diary_write')
    diary_write_input = {
      'date': '2024-05-02',
      'meal_type': 'L',
      'content': '식단일기 테스트입니다.',
      'is_favourite': False,
      'is_public': False,
      'is_deleted': False,
      'meal_image[0]image_url': self.food_image,
      'meal_food[0]food_code': 'P000006-ZZ-AVG',
      'meal_food[0]food_name': '찹쌀 약과',
      'meal_food[0]food_type': 'P',
      'meal_food[0]portion': 1.0,
    }
    diary_write_response = self.client.post(diary_write_url, diary_write_input, format='multipart')
    diary_write_output = diary_write_response.data

    self.assertEqual(diary_write_response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(diary_write_output['date'], '2024-05-02')
    self.assertEqual(diary_write_output['meal_type'], 'L')

  def test_diary_read_success(self) -> None:
    diary_read_edit_delete_url = reverse('diary_read_edit_delete', kwargs={'date': '2024-05-01', 'meal_type': 'B'})
    diary_read_response = self.client.get(diary_read_edit_delete_url)
    diary_read_output = diary_read_response.data

    self.assertEqual(diary_read_response.status_code, status.HTTP_200_OK)
    self.assertEqual(diary_read_output['date'], '2024-05-01')
    self.assertEqual(diary_read_output['meal_type'], 'B')

  def test_diary_edit_success(self) -> None:
    diary_read_edit_delete_url = reverse('diary_read_edit_delete', kwargs={'date': '2024-05-01', 'meal_type': 'B'})
    diary_edit_input = {
      'date': '2024-05-01',
      'meal_type': 'B',
      'content': '식단일기 테스트 도중 수정된 내용입니다.',
      'is_favourite': False,
      'is_public': False,
      'is_deleted': False,
      'meal_image[0]image_url': self.food_image,
      'meal_food[0]food_code': 'P000006-ZZ-AVG',
      'meal_food[0]food_name': '찹쌀 약과',
      'meal_food[0]food_type': 'P',
      'meal_food[0]portion': 1.0,
    }
    diary_edit_response = self.client.put(diary_read_edit_delete_url, diary_edit_input, format='multipart')
    diary_edit_output = diary_edit_response.data

    self.assertEqual(diary_edit_response.status_code, status.HTTP_200_OK)
    # self.assertEqual(diary_edit_output['date'], '2024-05-01')
    # self.assertEqual(diary_edit_output['meal_type'], 'B')
    self.assertEqual(diary_edit_output['content'], '식단일기 테스트 도중 수정된 내용입니다.')

  def test_diary_delete_success(self) -> None:
    diary_read_edit_delete_url = reverse('diary_read_edit_delete', kwargs={'date': '2024-05-01', 'meal_type': 'B'})
    diary_delete_response = self.client.delete(diary_read_edit_delete_url)
    diary_delete_output = diary_delete_response.data

    self.assertEqual(diary_delete_response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(diary_delete_response.status_text, 'No Content')
    self.assertEqual(diary_delete_output['message'], '식단일기가 성공적으로 삭제되었습니다.')

  def test_diary_share_success(self) -> None:
    diary_share_url = reverse('diary_share', kwargs={'date': '2024-05-01', 'meal_type': 'B'})
    diary_share_response = self.client.patch(diary_share_url)
    diary_share_output = diary_share_response.data

    self.assertEqual(diary_share_response.status_code, status.HTTP_200_OK)
    self.assertEqual(diary_share_response.status_text, 'OK')
    self.assertEqual(diary_share_output['message'], '식단일기가 공개로 전환되었습니다.')

  ##### Fail Test Case #####
  def test_diary_write_fail(self) -> None:
    diary_write_url = reverse('diary_write')
    diary_write_input = {
      'date': '2024-05-01',
      'meal_type': 'B',
      'content': '식단일기 테스트입니다.',
      'is_favourite': False,
      'is_public': False,
      'is_deleted': False,
      'meal_image[0]image_url': self.food_image,
      'meal_food[0]food_code': 'P000006-ZZ-AVG',
      'meal_food[0]food_name': '찹쌀 약과',
      'meal_food[0]food_type': 'P',
      'meal_food[0]portion': 1.0,
    }
    diary_write_response = self.client.post(diary_write_url, diary_write_input, format='multipart')
    diary_write_output = diary_write_response.data

    self.assertEqual(diary_write_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(diary_write_output['error_message'][0], 'D7')
    self.assertEqual(diary_write_output['error_code'], 400)

  def test_diary_read_fail(self) -> None:
    diary_read_edit_delete_url = reverse('diary_read_edit_delete', kwargs={'date': '2024-05-02', 'meal_type': 'B'})
    diary_read_response = self.client.get(diary_read_edit_delete_url)
    diary_read_output = diary_read_response.data

    self.assertEqual(diary_read_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(diary_read_output['error_message'][0], 'D8')
    self.assertEqual(diary_read_output['error_code'], 400)

  def test_diary_edit_fail(self) -> None:
    diary_read_edit_delete_url = reverse('diary_read_edit_delete', kwargs={'date': '2024-05-02', 'meal_type': 'B'})
    diary_edit_input = {
      'date': '2024-05-02',
      'meal_type': 'B',
      'content': '식단일기 테스트 도중 수정된 내용입니다.',
      'is_favourite': False,
      'is_public': False,
      'is_deleted': False,
      'meal_image[0]image_url': self.food_image,
      'meal_food[0]food_code': 'P000006-ZZ-AVG',
      'meal_food[0]food_name': '찹쌀 약과',
      'meal_food[0]food_type': 'P',
      'meal_food[0]portion': 1.0,
    }
    diary_edit_response = self.client.put(diary_read_edit_delete_url, diary_edit_input, format='multipart')
    diary_edit_output = diary_edit_response.data

    self.assertEqual(diary_edit_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(diary_edit_output['error_message'][0], 'D8')
    self.assertEqual(diary_edit_output['error_code'], 400)

  def test_diary_delete_fail(self) -> None:
    diary_read_edit_delete_url = reverse('diary_read_edit_delete', kwargs={'date': '2024-05-02', 'meal_type': 'B'})
    diary_delete_response = self.client.delete(diary_read_edit_delete_url)
    diary_delete_output = diary_delete_response.data

    self.assertEqual(diary_delete_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(diary_delete_output['error_message'][0], 'D8')
    self.assertEqual(diary_delete_output['error_code'], 400)

  def test_diary_share_fail(self) -> None:
    diary_share_url = reverse('diary_share', kwargs={'date': '2024-05-02', 'meal_type': 'B'})
    diary_share_response = self.client.patch(diary_share_url)
    diary_share_output = diary_share_response.data

    self.assertEqual(diary_share_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(diary_share_output['error_message'][0], 'D8')
    self.assertEqual(diary_share_output['error_code'], 400)
