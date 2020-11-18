import pandas as pd
from check_order_api_catboost.settings import BASE_DIR
from evaluation.constants import Params
import os
from os import listdir
from os.path import isfile, join
from rest_framework.exceptions import ValidationError
import joblib

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


def get_model(profile_name: str):
    if models.get(profile_name):
        return models[profile_name]
    profile_path = get_full_path(profile_name)
    model = joblib.load(profile_path)

    if 'cat' in profile_name:
        encode = {}
        if model.__class__ == dict:
            if "profile" in model.keys() and str(model["profile"].__class__) == Params.CATBOOST_CLASS_NAME:
                if "encode" in model.keys():
                    encode = model.get('encode')
                model = model["profile"]

        if str(model.__class__) != Params.CATBOOST_CLASS_NAME:
            e = "We expected {} as {} or as dict('profile': {}, '_encode': '...')" . \
                format(profile_name, Params.CATBOOST_CLASS_NAME, Params.CATBOOST_CLASS_NAME)
            raise ValidationError(e)

        model._encode = encode
        model._algorithm_name = 'catboost'
        feature_cat, feature_num = get_cat_num_features_from_catboost(model)
        model._factor_list = sorted(model.feature_names_)
        model._feature_cat = feature_cat
        model._feature_num = feature_num
    models[profile_name] = model
    return model

def get_profile(request):
    config = request.data.get('config')
    profile_name = config.get('profile')
    profile = get_model(profile_name)
    return profile


def get_used_factor_list(request):
    profile = get_profile(request)
    return sorted(profile._factor_list)


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
                    profile = get_model(profile_name)
                    used_factor_list = profile._factor_list
                    diff_column = list(set(used_factor_list) - set(data.keys()))
                    if len(diff_column) > 0:
                        validate = False
                        message['data_error'] = 'Invalid data. {} is required. Algorithm {} expects factors list: {}'. \
                            format(', '.join(diff_column), profile._algorithm_name, ', '.join(used_factor_list))

    return validate, message


def replace_na(dataset: pd.DataFrame, replace_val=-9999) -> pd.DataFrame:
    return dataset.fillna(replace_val)
