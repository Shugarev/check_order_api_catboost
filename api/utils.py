import pandas as pd
import numpy as np

import os
from os import listdir
from os.path import isfile, join

import joblib
from torch import Tensor

from rest_framework.exceptions import ValidationError
from check_order_api_catboost.settings import BASE_DIR

models = {}


def get_full_path(name):
    return "{}/media/{}".format(BASE_DIR, name)


def get_model_list():
    media_path = "{}/media/".format(BASE_DIR)
    onlyfiles = [f for f in listdir(media_path) if isfile(join(media_path, f)) and '.' not in f]
    return onlyfiles


def get_cat_num_features_from_catboost(profile):
    cat_indexes = profile.get_cat_feature_indices()
    feature_name = profile.feature_names_
    feature_cat = []
    feature_num = []
    for i in range(len(profile.feature_names_)):
        if i in cat_indexes:
           feature_cat.append(feature_name[i])
        else:
           feature_num.append(feature_name[i])
    return feature_cat, feature_num


def validate_profile_config(profile_config):
    message = {}
    validate = True
    if profile_config.__class__ != dict:
        message['profile_config'] = 'We expected profile_config  as ' \
            'dict("profile": ... , "algorithm_name": ... , "factor_list": ...,"replaced_values": ...)'
        validate = False
    profile_conf_keys = profile_config.keys()
    if profile_config.__class__ == dict:
        if 'profile' not in profile_conf_keys or 'algorithm_name' not in profile_conf_keys or 'factor_list' not in\
                profile_conf_keys or "replaced_values" not in profile_conf_keys:
            message['obligatory_keys'] = ' We expected profile_config  as dict. Keys "profile, "algorithm_name", ' \
                                         '"factor_list", "replaced_values" are obligatory.'
            validate = False

        if profile_config.get('algorithm_name') == 'catboost' and 'numeric_factors' not in profile_conf_keys:
            message['catboost_obligatory_key'] = ' Key "numeric_factors" for catboost model is obligatory'
            validate = False

        if profile_config.get('algorithm_name') == 'torch' and 'scaler_params' not in profile_conf_keys:
            message['torch_obligatory_key'] = ' Key "numeric_factors" for torch model is obligatory'
            validate = False

    if not validate:
        raise ValidationError(message)


def get_model(profile_name: str):
    if models.get(profile_name):
        return models[profile_name]
    profile_path = get_full_path(profile_name)
    profile_config = joblib.load(profile_path)
    validate_profile_config(profile_config)

    models[profile_name] = profile_config
    return profile_config


def get_profile_config(request):
    config = request.data.get('config')
    profile_name = config.get('profile')
    profile_config = get_model(profile_name)
    return profile_config


def get_used_factor_list(request):
    profile_config = get_profile_config(request)
    return sorted(profile_config.get('factor_list'))


def prepare_order_data(order_data, used_factor: list) -> dict:
    return {k: [v] for k, v in order_data.items() if k in used_factor}


def get_data_to_create_order(request):
    order_data = request.data.get('data')
    used_factor = get_used_factor_list(request)
    order_data_convert = prepare_order_data(order_data, used_factor)
    return order_data_convert


def validate_data(request):
    message = {}
    validate = True
    data = request.data.get('data')
    if not data:
        message['data_error'] = 'Data is required'
        validate = False

    config = request.data.get('config')
    if not config:
        message['config_error'] = 'Config is required'
        validate = False
    else:
        profile_name = config.get('profile')
        if not profile_name:
            message['profile_error'] = 'Profile is required in config'
            validate = False
        else:
            profile_path = get_full_path(profile_name)
            if not os.path.isfile(profile_path):
                onlyfiles = get_model_list()
                message['profile_error'] = 'Invalid  profile {}. Expected profiles from list: {}'. \
                    format(profile_name, ', '.join(onlyfiles))
                validate = False
            else:
                if data:
                    profile_config = get_model(profile_name)
                    used_factor_list = profile_config.get('factor_list')
                    diff_column = list(set(used_factor_list) - set(data.keys()))
                    if len(diff_column) > 0:
                        validate = False
                        message['data_error'] = 'Invalid data. {} is required. Algorithm {} expects factors list: {}'. \
                            format(', '.join(diff_column), profile_config.get('algorithm_name'), ', '.join(used_factor_list))

    return validate, message


def get_predict_torch(row: np.array, model):
    # convert row to data
    row = Tensor([row])
    # make prediction
    yhat = model(row)
    # retrieve numpy array
    yhat = yhat.detach().numpy()
    return yhat


def apply_scaler_to_column(series_data: pd.Series, feature: str, profile_config: dict) -> pd.Series:
    series_data = series_data.copy()
    key_factor_min = feature + '_min'
    key_factor_max = feature + '_max'

    scaler_params = profile_config.get('scaler_params')

    x_min = scaler_params[key_factor_min]
    x_max = scaler_params[key_factor_max]

    series_data = (series_data - x_min) / (x_max - x_min)
    series_data = np.where(series_data > 1, 1, series_data)
    series_data = np.where(series_data < 0, 0, series_data)

    return series_data