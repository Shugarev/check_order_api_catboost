import pandas as pd
from api.utils import replace_na


class DatasetTester:

    @classmethod
    def run_one_order(cls, profile, order_data: dict = None) -> float:
        test = pd.DataFrame.from_dict(order_data, dtype=str)
        used_factor_list = sorted(profile._factor_list)
        test = test[used_factor_list]
        test = cls.test_dataset(test,  profile)
        return test.probability.values[0]

    @classmethod
    def test_dataset(cls, test: pd.DataFrame, profile) -> pd.DataFrame:
        algorithm_name = profile._algorithm_name
        test = test.copy()
        if algorithm_name == 'catboost':
            return cls.test_dataset_by_catboost(test, profile)

        test_modified = test.apply(pd.to_numeric, errors="coerce")
        if algorithm_name != 'xgboost':
            test_modified = replace_na(test_modified)
        test_matrix = test_modified.values
        test_pred = profile.predict_proba(test_matrix)
        test["probability"] = test_pred[:, 1]
        return test

    @classmethod
    def test_dataset_by_catboost(cls, test: pd.DataFrame, profile) -> pd.DataFrame:
        encode_na = profile._encode if hasattr(profile, '_encode') else {}
        numeric_feature_names = profile._feature_num
        feature_names = profile.feature_names_
        test = test[feature_names]

        for feature in numeric_feature_names:
            replaced_na = encode_na.get(feature) or -9999
            test.loc[:, feature] = test.loc[:, feature].apply(pd.to_numeric, errors="coerce")
            test.loc[:, feature] = test.loc[:, feature].fillna(replaced_na)

        test_pred = profile.predict_proba(test)
        test["probability"] = test_pred[:, 1]
        return test
