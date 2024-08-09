from django.test import TestCase, Client
from rest_framework.test import APIClient

from .models import Account, Transaction


class AccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_accounts(self):
        self.account1 = Account.objects.create(username="Alex", balance=0.0)
        self.account2 = Account.objects.create(username="Hellen", balance=0.0) 

        response = self.client.get(f"/accounts/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Alex", response.data[0]["username"])
        self.assertEqual("Hellen", response.data[1]["username"])

    
class TransactionTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(username="Alex", balance=1000.0)
        self.account2 = Account.objects.create(username="Hellen", balance=0.0) 
        self.client = APIClient()

    def test_deposit_funds(self):
        data = {
            "transaction_type": "deposit",
            "amount": 1000,
            "source": self.account1.id
        }
        response = self.client.post(f"/deposit/", data=data, format="json")

        self.assertEqual(response.status_code, 200)
        self.account1.refresh_from_db()
        self.assertEqual(2000.0, self.account1.balance)

    def test_withdraw_funds_with_insufficient_funds(self):
            data = {
                "transaction_type": "withdraw",
                "amount": 1000,
                "source": self.account2.id
            }

            response = self.client.post(f"/withdraw/", data=data, format="json")

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.data['non_field_errors'])

    def test_withdraw_funds(self):
        data = {
            "transaction_type": "withdraw",
            "amount": 500,
            "source": self.account1.id
        }

        response = self.client.post(f"/withdraw/", data=data, format="json")

        self.assertEqual(response.status_code, 200)
        self.account1.refresh_from_db()
        self.assertEqual(500.0, self.account1.balance)

    def test_send_funds_with_insufficient_funds(self):
        data = {
            "transaction_type": "send",
            "amount": 1000,
            "source": self.account2.id
        }

        response = self.client.post(f"/send/", data=data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data['non_field_errors'])

    def test_send_funds(self):
        data = {
            "transaction_type": "send",
            "amount": 200,
            "source": self.account1.id,
            "target": self.account2.id
        }

        response = self.client.post(f"/send/", data=data, format="json")

        self.assertEqual(response.status_code, 200)
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(800.0, self.account1.balance)
        self.assertEqual(200.0, self.account2.balance)