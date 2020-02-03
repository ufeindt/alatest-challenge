import unittest
import numpy as np

from phonerouting import PhoneOperatorList, PhoneOperator

operatorA = {'1': 0.9,
             '268': 5.1,
             '46': 0.17,
             '4620': 0.0,
             '468': 0.15,
             '4631': 0.15,
             '4673': 0.9,
             '46732': 1.1}

operatorB = {'1': 0.92,
             '44': 0.5,
             '46': 0.2,
             '467': 1.0,
             '48': 1.2}

test_operator_list = PhoneOperatorList(['operatorA', 'operatorB'],
                                       [operatorA, operatorB])


class TestPhoneRouting(unittest.TestCase):
    def test_prices(self):
        test_cases = {'1234567890': ('operatorA', 0.9),
                      '2681234567': ('operatorA', 5.1),
                      '4412345678': ('operatorB', 0.5),
                      '4612345678': ('operatorA', 0.17),
                      '4620123456': ('operatorA', 0.0),
                      '4631123456': ('operatorA', 0.15),
                      '4677077387': ('operatorA', 0.17),
                      '4673123456': ('operatorA', 0.9),
                      '4673212345': ('operatorB', 1.0),
                      '4812345678': ('operatorB', 1.2),
                      '4921517479': (None, np.inf)}

        for number, result in test_cases.items():
            self.assertEqual(test_operator_list.get_price(number), result,
                             msg=f'Tested number: {number}')

    def test_values(self):
        self.assertRaises(TypeError, test_operator_list.get_price, 1234567890)
        self.assertRaises(TypeError, test_operator_list.get_price, 123.4567890)
        self.assertRaises(ValueError, test_operator_list.get_price,
                          '555-GET-LWYR')


class TestPhoneOperator(unittest.TestCase):
    def test_values(self):
        self.assertRaises(TypeError, PhoneOperator, {1: 1.0})
        self.assertRaises(TypeError, PhoneOperator, {'1': '1.0'})
        self.assertRaises(ValueError, PhoneOperator, {'GET': 1.0})
