import logging
from datetime import date, timedelta
from unittest.mock import ANY
from rest_framework.test import RequestsClient
import uuid
from django.test import TransactionTestCase
from coupon.models import Coupon
from member.models import Member

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

URI = 'http://localhost:8000'


class APIEndpointsTest(TransactionTestCase):
    def setUp(self):
        self.client = RequestsClient()

    def test_get_main_page_should_return_200(self):
        response = self.client.get(URI)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'Tem um cupom e quer fazer seu cadastro? ->': 'http://localhost:8000/register/',
                          'Já é cadastrado e quer indicar alguem? ->': 'http://localhost:8000/coupon/',
                          'Pesquisar um membro': 'http://localhost:8000/search/member/',
                          'Pesquisar um cupom': 'http://localhost:8000/search/coupon/',
                          })

    def test_create_coupon_should_return_200(self):
        member = Member.objects.create(cpf='72488335096')
        coupon = {'source': member.cpf, 'target': '98739184005'}

        response = self.client.post(f'{URI}/coupon/', coupon)
        self.assertEqual(response.status_code, 200)

    def test_create_member_should_return_200(self):
        member = Member.objects.create(cpf='72488335096')
        coupon = Coupon.objects.create(source=member.cpf, target='98739184005',
                                       coupon=uuid.uuid4())
        new_member = {'cpf': '98739184005', 'coupon': coupon.coupon}
        response = self.client.post(f'{URI}/register/', new_member)
        self.assertEqual(response.status_code, 200)

    def test_get_member_should_return_200(self):
        member = Member.objects.create(cpf='72488335096')
        response = self.client.get(f'{URI}/member/72488335096')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'cpf': '72488335096', 'name': ANY, 'email': ANY, 'address': ANY,
                          'phone': ANY, 'points': ANY, 'zipcode': ANY, 'created': ANY})

    def test_coupon_expired_should_return_400(self):
        date_expired = date.today() - timedelta(days=31)
        member = Member.objects.create(cpf='72488335096')
        coupon = Coupon.objects.create(source=member.cpf, target='98739184005',
                                       coupon=uuid.uuid4(), created=date_expired)
        new_member = {'cpf': '98739184005', 'coupon': coupon.coupon}
        response = self.client.post(f'{URI}/register/', new_member)
        self.assertEqual(response.status_code, 400)

    def test_create_coupon_for_cpf_already_invited_should_return_400(self):
        url1 = '/coupon/'
        date_expired = date.today() - timedelta(days=29)

        member = Member.objects.create(cpf='72488335096')
        coupon1 = {'source': member.cpf, 'target': '98739184005', 'created': date_expired}
        response1 = self.client.post(URI + url1, coupon1)

        member2 = Member.objects.create(cpf='14387361000')
        coupon2 = {'source': member2.cpf, 'target': '98739184005', 'created': date.today()}
        response1 = self.client.post(URI + url1, coupon2)

        self.assertEqual(response1.status_code, 400)

    def test_create_coupon_for_cpf_already_member_shoud_return_400(self):
        member = Member.objects.create(cpf='72488335096')
        member2 = Member.objects.create(cpf='14387361000')

        coupon = {'source': member2.cpf, 'target': '72488335096', }
        response1 = self.client.post(f'{URI}/coupon/', coupon)
        self.assertEqual(response1.status_code, 400)

    def test_create_coupon_target_source_equal_should_return_400(self):
        member = Member.objects.create(cpf='72488335096')
        coupon = {'source': member.cpf, 'target': member.cpf, }
        response1 = self.client.post(f'{URI}/coupon/', coupon)
        self.assertEqual(response1.status_code, 400)

    def test_get_coupon_target_to_source_should_return_200(self):
        member = Member.objects.create(cpf='72488335096')
        coupon = {'source': member.cpf, 'target': '98739184005'}

        response = self.client.post(f'{URI}/coupon/', coupon)
        response2 = self.client.get(f'{URI}/{member.cpf}/coupon-to/{coupon["target"]}')

        self.assertEqual(response.status_code, 200)
