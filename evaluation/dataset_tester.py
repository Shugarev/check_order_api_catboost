import pandas as pd


class DatasetTester:

    @classmethod
    def run_one_order(cls, profile_config, order_data: dict = None) -> float:
        test = pd.DataFrame.from_dict(order_data, dtype=str)
        used_factor_list = sorted(profile_config.get('factor_list'))
        test = test[used_factor_list]
        test = cls.test_dataset(test, profile_config)
        return test.probability.values[0]

    @classmethod
    def test_dataset(cls, test: pd.DataFrame, profile_config) -> pd.DataFrame:
        algorithm_name = profile_config.get('algorithm_name')
        test_modified = cls.get_modified_test(test, profile_config)
        if algorithm_name == 'catboost':
            return cls.test_dataset_by_catboost(test_modified, profile_config)

        if algorithm_name == 'torch':
            return cls.test_dataset_by_torch(test_modified, profile_config)

        profile = profile_config['profile']
        test_matrix = test_modified.values
        test_pred = profile.predict_proba(test_matrix)
        test["probability"] = test_pred[:, 1]
        return test

    @classmethod
    def get_modified_test(cls, test: pd.DataFrame, profile_config) -> pd.DataFrame:
        test = test.copy()
        encode_na = profile_config.get('replaced_values') or {}
        feature_names = profile_config['factor_list']
        numeric_feature_names = profile_config.get('numeric_factors')
        algorithm_name = profile_config.get('algorithm_name')
        for feature in feature_names:
            if algorithm_name != 'catboost' or (algorithm_name == 'catboost' and feature in numeric_feature_names):
                test.loc[:, feature] = test.loc[:, feature].apply(pd.to_numeric, errors="coerce")
                replaced_na = encode_na.get(feature) or encode_na.get('default')
                if replaced_na:
                    test.loc[:, feature] = test.loc[:, feature].fillna(replaced_na)
        return test

    @classmethod
    def test_dataset_by_catboost(cls, test_modified: pd.DataFrame, profile_config) -> pd.DataFrame:
        profile = profile_config['profile']
        test_pred = profile.predict_proba(test_modified)
        test_modified["probability"] = test_pred[:, 1]
        return test_modified

    @classmethod
    def test_dataset_by_torch(cls, test: pd.DataFrame, profile_config) -> pd.DataFrame:
        pass