class Params:
    BAD_STATUSES = ('true', 1, '1')
    ALGORITHMS = ['adaboost', 'gausnb', 'decisiontree', 'gradientboost', 'logregression', 'linear_sgd', 'xgboost'
        , 'lightgbm', 'kneighbors', 'catboost', 'torch']

    CATBOOST_CLASS_NAME = "<class 'catboost.core.CatBoostClassifier'>"
