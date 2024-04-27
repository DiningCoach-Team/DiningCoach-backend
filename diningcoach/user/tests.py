from django.urls import include, path, reverse

from user.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, URLPatternsTestCase


class UserAPITestCase(APITestCase):
  user1_instance = None
  user1_setup_data = {
    'username': 'test1',
    'email': 'test1@diningcoach.org',
    'password': 'Password1*',
    'platform_type': 'D',
    'platform_id': None,
    'user_agent': 'TEST HTTP USER AGENT',
  }

  signup_url = reverse('signup')
  login_url = reverse('login')

  user1_signup_data = {
    'username': 'test1',
    'email': 'test1@diningcoach.org',
    'password1': 'Password1*',
    'password2': 'Password1*',
  }
  user1_login_data = {
    'username': 'test1',
    'email': 'test1@diningcoach.org',
    'password': 'Password1*',
  }

  user2_signup_data = {
    'username': 'test2',
    'email': 'test2@diningcoach.org',
    'password1': 'Password2*',
    'password2': 'Password2*',
  }
  user2_login_data = {
    'username': 'test2',
    'email': 'test2@diningcoach.org',
    'password': 'Password2*',
  }

  def setUp(self) -> None:
    self.client = APIClient()
    self.user1_instance = User.objects.create_user(**self.user1_setup_data)

  def test_login_success(self) -> None:
    login_success_response = self.client.post(self.login_url, self.user1_login_data, format='json')
    login_success_data = login_success_response.data

    self.assertEqual(login_success_response.status_code, status.HTTP_200_OK)
    self.assertEqual(login_success_data['user']['username'], self.user1_instance.username)
    self.assertEqual(login_success_data['user']['email'], self.user1_instance.email)

  def test_login_fail(self) -> None:
    login_fail_response = self.client.post(self.login_url, self.user2_login_data, format='json')
    login_fail_data = login_fail_response.data

    self.assertEqual(login_fail_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(login_fail_data['error_code'], 400)
    self.assertEqual(login_fail_data['error_message'][0], 'UNKNOWN_ERROR')

  def test_signup_success(self) -> None:
    signup_success_response = self.client.post(self.signup_url, self.user2_signup_data, format='json')
    signup_success_data = signup_success_response.data

    self.assertEqual(signup_success_response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(signup_success_data['user']['username'], self.user2_signup_data['username'])
    self.assertEqual(signup_success_data['user']['email'], self.user2_signup_data['email'])

  def test_signup_fail(self) -> None:
    signup_fail_response = self.client.post(self.signup_url, self.user1_signup_data, format='json')
    signup_fail_data = signup_fail_response.data

    self.assertEqual(signup_fail_response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(signup_fail_data['error_code'], 400)
    self.assertEqual(signup_fail_data['error_message'][0], 'ACCOUNT_ALREADY_EXISTS')
