import os
import time
from random import randint
from locust import HttpUser, task, between


class UserAccountAPITestUser(HttpUser):
  BASE_URL = '/api/user/account'
  wait_time = between(1, 3)

  @task(3)
  def login_simulate(self):
    login_url = os.path.join(self.BASE_URL, 'login', '')

    num = randint(1, 100)
    login_data = {
      'username': f'test{num}',
      'email': f'test{num}@diningcoach.org',
      'password': f'Password{num}*',
    }
    self.client.post(login_url, json=login_data)

    # for i in range(20):
    #   num = str(i+1)
    #   self.client.post(login_url, json=login_data)
    #   time.sleep(2)

  @task(2)
  def signup_simulate(self):
    signup_url = os.path.join(self.BASE_URL, 'signup', '')

    num = randint(1, 100)
    signup_data = {
      'username': f'test{num}',
      'email': f'test{num}@diningcoach.org',
      'password1': f'Password{num}*',
      'password2': f'Password{num}*',
    }
    self.client.post(signup_url, json=signup_data)

    # for i in range(20):
    #   num = str(i+1)
    #   self.client.post(signup_url, json=signup_data)
    #   time.sleep(2)
