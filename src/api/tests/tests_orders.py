from djoser.views import User
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from api.models import Manager


class OrderTest(APITestCase):
    """
    - нулевая позиция, нет ордеров
    - нулевая позиция, есть ордер
    - нулевая позиция, нет ордеров, цена ушла против грида
    - нулевая позиция, есть ордер, цена ушла против грида
    - не нулевая позиция, нет ордеров
    - не нулевая позиция, есть ордер
    - не нулевая позиция, нет ордеров, цена ушла против грида
    - не нулевая позиция, есть ордер, цена ушла против грида
    - время за интервалом
    """