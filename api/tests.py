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
        cls.copy_files('cat_3-75-015_seed_45_2021-01-26')
        cls.copy_files('pytorch_30-09-001_2021-01-26')
        cls.copy_files('xgb_3-80-035_2021-01-26')

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
                "profile": "xgb_3-80-035_2021-01-26"
            },
            "data": {
                "amount": "158.85",
                "bin": "510932",
                "day_of_week": "2",
                "hour": "00",
                "bank_currency": "840",
                "is_city_resolved": "1",
                "latitude": "undef",
                "is_gender_undefined": "1",
                "longitude": "undef",
                "phone_2_norm": "20"
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
                "profile": "cat_3-75-015_seed_45_2021-01-26"
            },
            "data": {
                "amount": "158.85",
                "bank_currency": "840",
                "bin": "510932",
                "day_of_week": "2",
                "hour": "00",
                "is_city_resolved": "1",
                "is_gender_undefined": "1",
                "latitude": "undef",
                "longitude": "undef",
                "phone_2_norm": "20"

            }
        }

        cls.valid_pytorch_order = {
            "config": {
                "profile": "pytorch_30-09-001_2021-01-26"
            },
            "data": {
                "latitude": "undef",
                "bank_currency": "840",
                "bin": "510932",
                "count_months_to_end_card": "19",
                "day_of_week": "2",
                "hour": "00",
                "is_city_resolved": "1",
                "is_gender_undefined": "1",
                "longitude": "undef",
                "amount": "158.85",
                "phone_2_norm": "20"
            }
        }

    def create_web_order(self, order_data):
        return self.client.post(
            reverse('get_order_probability'),
            data=json.dumps(order_data),
            content_type='application/json')

    @skip
    def test_adaboost_prob(self):
        response = self.create_web_order(self.valid_ada_order)
        self.assertEqual(response.data.get('probability'), 0.49841105097826394,
                         'Probability in adaboost response is incorrect.')

    @skip
    def test_lgbm_prob(self):
        response = self.create_web_order(self.valid_lgbm_order)
        self.assertEqual(response.data.get('probability'), 0.021128826009703186,
                         'Probability in lightgbm response is incorrect.')

    @skip
    def test_adaboost_order_status(self):
        response = self.create_web_order(self.valid_ada_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status-code in adaboost response is incorrect.')

    @skip
    def test_lgbm_order_status(self):
        response = self.create_web_order(self.valid_lgbm_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status-code in lgbm response is incorrect.')

    def test_xgboost_prob(self):
        response = self.create_web_order(self.valid_xgb_order)
        self.assertEqual(response.data.get('probability'), 0.24286703765392303,
                         'Probability xgboost in response is incorrect.')

    def test_xgboost_order_status(self):
        response = self.create_web_order(self.valid_xgb_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status-code in xgboost response is incorrect.')

    def test_xgboost_invalid_field_order(self):
        response = self.create_web_order(self.invalid_factorlist_order)
        self.assertEqual(response.data['profile_error'].rsplit('.', 1)[0], "Invalid  profile xgb-test-model")

    def test_xgboost_invalid_order_status(self):
        response = self.create_web_order(self.invalid_factorlist_order)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY,
                         'Status-code in invalid order response is incorrect.')

    def test_xgboost_invalid_profile_order(self):
        response = self.create_web_order(self.invalid_profile_order)
        self.assertEqual(response.data['profile_error'].split('.')[0], 'Invalid  profile xgb2-test-model',
                         'Profile check in incorrect response is not working properly.')

    def test_get_model_catboost_factor_list(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        expected = ['amount', 'bank_currency', 'bin', 'day_of_week', 'hour', 'is_city_resolved',
                    'is_gender_undefined', 'latitude', 'longitude', 'phone_2_norm']
        self.assertListEqual(expected, profile_config['factor_list'], 'Factor list is not correct')

    def test_compare_catboost_factor_list_from_model(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        profile = profile_config['profile']
        expected = profile.feature_names_
        self.assertListEqual(expected, profile_config['factor_list'], 'Factor list is not correct')

    def test_get_model_catboost_feature_cat(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        value = set(profile_config['factor_list'])-set(profile_config['numeric_factors'])
        expected = {'hour', 'day_of_week', 'bank_currency'}
        self.assertSetEqual(expected, value, 'Features categories are not correct')

    def test_compare_catboost_feature_cat_from_model(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        profile = profile_config['profile']
        expected = set(profile_config['factor_list']) - set(profile_config['numeric_factors'])
        value = set(profile.feature_names_[index] for index in profile.get_cat_feature_indices())
        self.assertSetEqual(expected, value, 'Features categories are not correct')

    def test_get_model_catboost_feature_num(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        expected = ['amount', 'longitude', 'phone_2_norm', 'bin', 'latitude', 'is_gender_undefined', 'is_city_resolved']
        self.assertListEqual(expected, profile_config['numeric_factors'], 'Features numeric are not correct')

    def test_compare_catboost_feature_num_from_model(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        profile = profile_config['profile']
        expected = set(profile_config['numeric_factors'])
        value = set(profile.feature_names_[index] for index in range(len(profile.feature_names_)) if index not in
                    profile.get_cat_feature_indices())
        self.assertSetEqual(expected, value, 'Features numeric are not correct')

    def test_get_model_catboost_replaced_values(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        encode = profile_config['replaced_values']
        expected = {'latitude': 36.90237577890762, 'longitude': -92.53325861542274, 'default': -999}
        self.assertDictEqual(expected, encode, 'Encode is not correct')

    def test_catboost_prob(self):
        order = self.valid_cat_order.copy()
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'), 0.02343292704289948,
                         'Probability in catboost response is incorrect.')

    def test_catboost_prob_2(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        order = self.valid_cat_order.copy()
        order['data']['longitude'] = profile_config['replaced_values']['default']
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'), 0.02335825922584818,
                         'Probability in catboost response is incorrect.')

    def test_catboost_prob_3(self):
        profile_config = get_model('cat_3-75-015_seed_45_2021-01-26')
        order = self.valid_cat_order.copy()
        order['data']['longitude'] = 'undef'
        response = self.create_web_order(order)
        self.assertEqual(response.data.get('probability'), 0.02343292704289948,
                         'Probability in catboost response is incorrect.')

    def test_pytorch_prob(self):
        response = self.create_web_order(self.valid_pytorch_order)
        self.assertEqual(response.data.get('probability'), 0.03023967519402504,
                         'Probability pytorch in response is incorrect.')

    def test_pytorch_order_status(self):
        response = self.create_web_order(self.valid_pytorch_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status-code in pytorch response is incorrect.')

    @classmethod
    def tearDownClass(cls):
        cls.del_files('cat_3-75-015_seed_45_2021-01-26')
        cls.del_files('pytorch_30-09-001_2021-01-26')
        cls.del_files('xgb_3-80-035_2021-01-26')
