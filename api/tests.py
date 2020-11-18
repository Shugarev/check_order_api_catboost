import os
import shutil
import json
import unittest
from unittest import skip
from django.test import Client
from django.urls import reverse
from check_order_api_catboost.settings import BASE_DIR
from rest_framework import status
from .utils import get_model
# Create your tests here.
from django.test import TestCase

class OrderTesting(TestCase):
    client = Client()

    def copy_files(file_name):
        sourse_path = "{}/data_for_testing/{}".format(BASE_DIR, file_name)
        dest_path = "{}/media/{}".format(BASE_DIR, file_name)
        shutil.copyfile(sourse_path, dest_path)

    @classmethod
    def del_files(cls, file_name):
        del_path = "{}/media/{}".format(BASE_DIR, file_name)
        os.remove(del_path)

    @classmethod
    def setUpClass(cls):
        cls.copy_files('ada-test-model')
        cls.copy_files('xgb-test-model')
        cls.copy_files('lgbm-test-model')
        cls.copy_files('cat-test-model')
        cls.copy_files('cat-dic-test-model')


        cls.valid_ada_order = {
            "config": {
                "profile": "ada-test-model"
            },
            "data": {
                "amount": "25.00",
                "bank_currency": "840",
                "client_hour": "17",
                "day_of_week": "2",
                "hour": "00",
                "is_bank_country_equal_country": "1",
                "is_ip_country_equal_country": "1",
                "latitude": "38.2981",
                "longitude": "-77.4826",
                "bin": "400022"
            }
        }

        cls.valid_xgb_order = {
            "config": {
                "profile": "xgb-test-model"
            },
            "data": {
                "amount": "25.00",
                "bank_currency": "840",
                "client_hour": "17",
                "day_of_week": "2",
                "hour": "00",
                "is_bank_country_equal_country": "1",
                "is_ip_country_equal_country": "1",
                "latitude": "38.2981",
                "longitude": "-77.4826",
                "bin": "400022",
                "phone_2_norm": "01"
            }
        }

        cls.valid_lgbm_order = {
            "config": {
                "profile": "lgbm-test-model"
            },
            "data": {
                "amount": "25.00",
                "bank_currency": "840",
                "client_hour": "17",
                "day_of_week": "2",
                "hour": "00",
                "is_bank_country_equal_country": "1",
                "is_ip_country_equal_country": "1",
                "latitude": "38.2981",
                "longitude": "-77.4826",
                "bin": "400022",
            }
        }

        cls.invalid_factorlist_order = {
            "config": {
                "profile": "xgb-test-model"
            },
            "data": {
                "amount": "25.00",
                "bank_currency": "840",
                "client_hour": "17",
                "day_of_week": "2",
                "hour": "00",
                "is_bank_country_equal_country": "1",
                "is_ip_country_equal_country": "1",
                "latitude": "38.2981",
                "longitude": "-77.4826",
                "phone_2_norm": "01"
            }
        }

        cls.invalid_profile_order = {
            "config": {
                "profile": "xgb2-test-model"
            },
            "data": {
                "amount": "25.00",
                "bank_currency": "840",
                "client_hour": "17",
                "day_of_week": "2",
                "hour": "00",
                "is_bank_country_equal_country": "1",
                "is_ip_country_equal_country": "1",
                "latitude": "38.2981",
                "longitude": "-77.4826",
                "bin": "400022",
                "phone_2_norm": "01"
            }
        }

        cls.valid_cat_order = {
            "config": {
                "profile": "cat-test-model"
            },
            "data": {
                "phone_2_norm": "",
                "bin": "510932.00",
                "amount": "158.85",
                "bank_currency": "840",
                "hour": "00",
                "day_of_week": "2",
                "is_city_resolved": "1",
                "longitude": "-88.5305",
                "latitude": "44.1843",
                "is_gender_undefined": "1",
                "country": "USA"
            }
        }


    def create_web_order(self, order_data):
        return self.client.post(
            reverse('get_order_probability'),
            data=json.dumps(order_data),
            content_type='application/json')

    def test_adaboost_prob(self):
        response = self.create_web_order(self.valid_ada_order)
        self.assertEqual(response.data.get('probability'), 0.49841105097826394,
                         'Probability in adaboost response is incorrect.')

    def test_xgboost_prob(self):
        response = self.create_web_order(self.valid_xgb_order)
        self.assertEqual(response.data.get('probability'), 0.4336259365081787,
                         'Probability xgboost in response is incorrect.')

    def test_lgbm_prob(self):
        response = self.create_web_order(self.valid_lgbm_order)
        self.assertEqual(response.data.get('probability'), 0.021128826009703186,
                         'Probability in lightgbm response is incorrect.')

    def test_adaboost_order_status(self):
        response = self.create_web_order(self.valid_ada_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status-code in adaboost response is incorrect.')

    def test_lgbm_order_status(self):
        response = self.create_web_order(self.valid_lgbm_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status-code in lgbm response is incorrect.')

    def test_xgboost_order_status(self):
        response = self.create_web_order(self.valid_xgb_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status-code in xgboost response is incorrect.')

    def test_xgboost_invalid_field_order(self):
        response = self.create_web_order(self.invalid_factorlist_order)
        self.assertEqual(response.data['data_error'].rsplit('.', 1)[0], "Invalid data. bin is required")

    def test_xgboost_invalid_order_status(self):
        response = self.create_web_order(self.invalid_factorlist_order)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY,
                         'Status-code in invalid order response is incorrect.')

    def test_xgboost_invalid_profile_order(self):
        response = self.create_web_order(self.invalid_profile_order)
        self.assertEqual(response.data['profile_error'].split('.')[0], 'Invalid  profile xgb2-test-model',
                         'Profile check in incorrect response is not working properly.')

    def test_get_model_catboost_factor_list(self):
        profile = get_model('cat-test-model')
        expected = ['amount', 'bank_currency', 'bin', 'country', 'day_of_week', 'hour', 'is_city_resolved', \
                    'is_gender_undefined', 'latitude', 'longitude', 'phone_2_norm']
        self.assertListEqual(expected, profile._factor_list, 'Factor list is not correct')

    def test_get_model_catboost_feature_cat(self):
        profile = get_model('cat-test-model')
        expected = ['bank_currency', 'hour', 'day_of_week', 'is_gender_undefined', 'is_city_resolved', \
                    'phone_2_norm', 'country']
        self.assertListEqual(expected, profile._feature_cat, 'Feature categories are not correct')

    def test_get_model_catboost_feature_num(self):
        profile = get_model('cat-test-model')
        expected = ['bin', 'amount', 'longitude', 'latitude']
        self.assertListEqual(expected, profile._feature_num, 'Feature numerics are not correct')

    def test_get_model_catboost_encode(self):
        profile = get_model('cat-dic-test-model')
        encode = profile._encode
        expected = {'longitude': -97}
        self.assertDictEqual(expected, encode, 'Encode is not correct')

    def test_catboost_prob(self):
        order = self.valid_cat_order.copy()
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'), 0.028897349613769 ,
                         'Probability in catboost response is incorrect.')

    def test_catboost_prob_2(self):
        order = self.valid_cat_order.copy()
        order['data']['longitude'] = "-9999"
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'), 0.04446285010200619,
                         'Probability in catboost response is incorrect.')

    def test_catboost_prob_3(self):
        order = self.valid_cat_order.copy()
        order['data']['longitude'] = "-97"
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'), 0.032601330122430515,
                         'Probability in catboost response is incorrect.')

    def test_catboost_porb_dic(self):
        order = self.valid_cat_order.copy()
        order['config']['profile'] = 'cat-dic-test-model'
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'),  0.028897349613769,
                         'Probability in catboost response is incorrect.')

    def test_catboost_prob_dic_3(self):
        order = self.valid_cat_order.copy()
        order['config']['profile'] = 'cat-dic-test-model'
        order['data']['longitude'] = "undefined"
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'),  0.032601330122430515,
                         'Probability in catboost response is incorrect.')

    @classmethod
    def tearDownClass(cls):
        cls.del_files('ada-test-model')
        cls.del_files('xgb-test-model')
        cls.del_files('lgbm-test-model')
        cls.del_files('cat-test-model')
        cls.del_files('cat-dic-test-model')