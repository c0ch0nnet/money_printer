import time

from djoser.views import User
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from api.models import Manager, InstrumentPlatform


class ManagerTest(APITestCase):
    """
        - создание менежджера
        - создание дубликата менеждера
        - проверка видимости менеджера другим пользователем
        - изменение менеждера владельцем
        - изменения менеждера администратором
        - удаление менежджера владельцем
        - удаление менеджара администратором
    """

    def setUp(self):
        pass
        # self.base_url = reverse("auth")
        self.admin = User.objects.create(username='admin', password='admin', is_staff=True)
        self.user_BTC = User.objects.create(username='user_BTC', password='pass')
        self.user_ETH = User.objects.create(username='user_ETH', password='pass')
        self.instrument_platform = InstrumentPlatform.create(instrument='ETH', platform='moex')

        self.base_url = reverse("managers-list")
        self.put_url = reverse("managers-detail", args=[2])
        data = {
            "instrument": self.instrument_platform,
            "order_spread": 1.0,
            "order_step": 1.0,
            "start_step": 89890.0,
            "order_size": 1.0,
            "grid_depth": 0.5,
            "grid_side": 6.0,
            "user": self.user_ETH,
        }

        self.m = Manager(**data)
        self.m.save()
        print('self.m', self.m)

    def test_1(self):
        data = {
            "instrument": "ETH",
            "order_spread": 1.0,
            "order_step": 1.0,
            "start_step": 89890.0,
            "order_size": 1.0,
            "grid_depth": 0.5,
            "grid_side": 6.0
        }
        print(Manager.objects.all())
        self.client.force_authenticate(user=self.user_ETH)
        response = self.client.post(self.base_url, data=data)
        print(response.json())
        print(self.put_url)
        response = self.client.get(self.put_url)
        print(response.json())
        print(Manager.objects.all())
        print()
        self.client.force_authenticate(user=self.user_BTC)
        response = self.client.get(self.put_url)
        print(response.json())

        print()
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.base_url)
        print(response.json())


    # def test_2(self):
    #     # user = User.objects.create(username='test_user_01', password='ii484801')
    #     # self.client.credentials(username='test_user_01', password='ii484801')
    #     # data = {
    #     #     "username": user.username,
    #     #     "password": user.password,
    #     # }
    #     # response = self.client.post('/auth/token/login/', data=data)
    #     # print(response.json())
    #
    #     # self.client.force_authenticate(user=user)
    #     print('Manager.objects.all()')
    #     print(Manager.objects.all())
    #     data = {
    #         "instrument": "ETH_change",
    #         "order_spread": 1.0,
    #         "order_step": 1.0,
    #         "start_step": 89890.0,
    #         "order_size": 1.0,
    #         "grid_depth": 0.5,
    #         "grid_side": 606.0
    #     }
    #     self.client.force_authenticate(user=self.user_02)
    #     response = self.client.get(self.base_url)
    #     print(response.json())
    #
    #     self.client.force_authenticate(user=self.user_01)
    #     response = self.client.post(self.base_url, data=data)
    #     print(response.json())
    #
    #     response = self.client.get(self.base_url)
    #     print(response.json())
    #
    #     self.client.force_authenticate(user=self.user_02)
    #     response = self.client.get(self.base_url)
    #     print(response.json())



        # data = {
        #     "instrument": "ETH_change",
        # }
        # response = self.client.patch(self.put_url, data=data)
        # print(response.json())
        #
        # response = self.client.get(self.put_url)
        # print(response.json())
        # admin = User.objects.get(username='test_user_01')
        # print(admin)
        #
