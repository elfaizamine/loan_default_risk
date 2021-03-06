import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def one_hot_encoding(df, columns, key, drop_first=True):
    """
    dummies a set of columns

    :param df: dataframe
    :param columns: category columns
    :param key: table primary key generally Loan ID
    :param drop_first: if True drop first column

    :return  dataframe of one hot encoded columns plus key
    """
    df_dummies = pd.get_dummies(df[columns], drop_first=drop_first)
    df_dummies[key] = df[key]

    return df_dummies


def binary_encoding(df, columns):
    """
    binaries columns 

    :param columns: columns to binaries
    :param df: dataframe
    
    :return  dataframe of binary encoded columns plus SK_ID_CURR
    """
    df_binary = df.loc[:, ['SK_ID_CURR'] + columns]
    ordinal_encoder_df = preprocessing.OrdinalEncoder()
    df_binary.loc[:, columns] = ordinal_encoder_df.fit_transform(df_binary.loc[:, columns]).astype('int8')

    return df_binary


def label_encoding(df, col_to_label, col_categories):
    """
    transform category columns to numeric [Monday,...,Sunday] --> [1,...,7]

    :param df: dataframe
    :param col_to_label: dataframe column that should be labeled
    :param col_categories: sorted categories from lower to higher

    :return  dataframe of labeled  columns plus SK_ID_CURR
    """
    df_label = df.loc[:, ['SK_ID_CURR'] + col_to_label]
    for index, col in enumerate(col_to_label):
        df_label[col] = df_label[col].apply(lambda x: col_categories[index].index(x)).astype('int8')

    return df_label


def aggregate_columns_on_col(df, columns_to_aggregate):
    """
    aggregate multiple columns to one by summing values

    :param df: dataframe
    :param columns_to_aggregate: columns to aggregate

    :return  dataframe of aggregated column plus SK_ID_CURR
    """
    df_sum_agg = pd.DataFrame(df.SK_ID_CURR, columns=['SK_ID_CURR'])

    for col_name in columns_to_aggregate:
        df_sum_agg[col_name] = df[columns_to_aggregate[col_name]].sum(axis=1)

    return df_sum_agg


def columns_not_changed(df, col_to_keep):
    """
    insert the clean columns as features without changing the columns

    :param df: dataframe
    :param col_to_keep: columns that are clean and should not be changed

    :return  unchanged columns plus SK_ID_CURR
    """
    df = df.loc[:, ['SK_ID_CURR'] + col_to_keep]
    df.loc[df.DAYS_ID_PUBLISH > 0, :] = np.nan
    col_to_turn_positive = ['DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH']
    df[col_to_turn_positive] = df[col_to_turn_positive].abs()

    return df
