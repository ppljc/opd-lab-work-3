# Python модули
import unittest


# Локальные модули
from app import app, get_exchange_rates

import app as appn


# Класс тестов
class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.original_get_exchange_rates = get_exchange_rates
        appn.get_exchange_rates = lambda: {
            "USD": 1.0,
            "EUR": 0.9,
            "RUB": 75.0
        }

    def test_empty_input(self):
        response = self.app.post('/', data={
            'amount': '',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ошибка ввода данных'.encode('utf-8'), response.data)

    def test_no_amount_field(self):
        response = self.app.post('/', data={
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ошибка ввода данных'.encode('utf-8'), response.data)

    def test_valid_conversion(self):
        response = self.app.post('/', data={
            'amount': '100',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'90.0 EUR', response.data)

    def test_negative_amount(self):
        response = self.app.post('/', data={
            'amount': '-100',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'-90.0 EUR', response.data)

    def test_decimal_amount(self):
        response = self.app.post('/', data={
            'amount': '100.50',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'90.45 EUR', response.data)

    def test_invalid_number_format(self):
        response = self.app.post('/', data={
            'amount': '100,50',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ошибка ввода данных'.encode('utf-8'), response.data)

    def test_letters_in_amount(self):
        response = self.app.post('/', data={
            'amount': '100abc',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ошибка ввода данных'.encode('utf-8'), response.data)

    def test_special_characters(self):
        response = self.app.post('/', data={
            'amount': '100$#@',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ошибка ввода данных'.encode('utf-8'), response.data)

    def test_zero_amount(self):
        response = self.app.post('/', data={
            'amount': '0',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0.0 EUR', response.data)

    def test_large_number(self):
        response = self.app.post('/', data={
            'amount': '1000000000',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'900000000.0 EUR', response.data)


# Запуск тестов
if __name__ == '__main__':
    unittest.main()