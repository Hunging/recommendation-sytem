import numpy as np
import pandas as pd
import os
import sys
import math
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse    
from sklearn.metrics.pairwise import pairwise_distances 
# sys.append('..')
buy_model = 'static/data/buy_model.xlsx'


def calculate_similarity(data_items):
    """Calculate the column-wise cosine similarity for a sparse
    matrix. Return a new dataframe matrix with similarities.
    """
    data_sparse = sparse.csr_matrix(data_items)
    similarities = cosine_similarity(data_sparse.transpose())
    sim = pd.DataFrame(data=similarities, index= data_items.columns, columns= data_items.columns)
    return sim


def get_recommendation_by_id(id):
    buy_model_dataframe = pd.read_excel (buy_model)
    cols = ['QuoteId']
    buy_model_dataframe.drop(cols, axis=1, inplace=True)
    # total_rows = buy_model_dataframe['CustomerId'].count
    total_rows = len(buy_model_dataframe.index)
    #add value to dataframe
    value_col = np.ones((total_rows, 1))
    buy_model_dataframe['values'] = value_col

    n_users = buy_model_dataframe.groupby('CustomerId').nunique().values.shape[0]
    n_items = buy_model_dataframe.groupby('ModelId').nunique().values.shape[0]
    
    user_item_df = buy_model_dataframe.pivot_table(index='CustomerId', columns='ModelId', values ="values" , aggfunc='max')
    user_item_df.fillna(0, inplace=True)

    data_items = user_item_df.copy()

    # magnitude = sqrt(x2 + y2 + z2 + ...)
    magnitude = np.sqrt(np.square(data_items).sum(axis=1))

    # unitvector = (x / magnitude, y / magnitude, z / magnitude, ...)
    data_items = data_items.divide(magnitude, axis='index')
    data_items_result = calculate_similarity(data_items)
    print(data_items_result.loc[id].nlargest(10))
    return data_items_result.loc[id].nlargest(10)

def normalize_matrix_by_type(user_item_matrix, type='user'):
    normalize_matrix = user_item_matrix.copy()
    axis = 1
    if type == 'user':
        mean = np.nanmean(normalize_matrix, axis = 0)
        for col in range(0, normalize_matrix.shape[0]):
            normalize_matrix[col] = normalize_matrix[col] - mean
    elif type == 'item':
        normalize_matrix = normalize_matrix.T
        mean = np.nanmean(normalize_matrix, axis = 0)
        for col in range(0, normalize_matrix.shape[0]):
            normalize_matrix[col] = normalize_matrix[col] - mean
        normalize_matrix = normalize_matrix.T
    normalize_matrix = np.nan_to_num(normalize_matrix, copy=True, nan=0, posinf=None, neginf=None)
    return normalize_matrix

def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        #We use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred


def get_recommendation_by_list_of_id(id_list):
    buy_model_dataframe = pd.read_excel (buy_model)
    cols = ['QuoteId']
    buy_model_dataframe.drop(cols, axis=1, inplace=True)
    # total_rows = buy_model_dataframe['CustomerId'].count
    total_rows = len(buy_model_dataframe.index)
    fake_user_id = str(-1)
    for i in range(0, len(id_list)):
        buy_model_dataframe.loc[buy_model_dataframe.index.max() + 1]  = [str(fake_user_id),id_list[i]]
    total_rows = len(buy_model_dataframe.index)
    #add value to dataframe
    value_col = np.ones((total_rows, 1))
    buy_model_dataframe['values'] = value_col

    n_users = buy_model_dataframe.groupby('CustomerId').nunique().values.shape[0]
    n_items = buy_model_dataframe.groupby('ModelId').nunique().values.shape[0]
    
    user_item_df = buy_model_dataframe.pivot_table(index='ModelId', columns='CustomerId', values ="values" , aggfunc='max')
    user_item_df.fillna(0, inplace=True)

    items = user_item_df.index.tolist()
    users = user_item_df.columns.tolist()

    user_item_matrix = user_item_df.as_matrix()

    user_normalize_matrix = normalize_matrix_by_type(user_item_matrix, type='user')
    item_normalize_matrix = normalize_matrix_by_type(user_item_matrix, type='item')

    user_pairwise_distances = pairwise_distances(user_normalize_matrix.T, metric='cosine')
    item_pairwise_distances = pairwise_distances(item_normalize_matrix, metric='cosine')

    user_cosine_similarity = cosine_similarity(user_normalize_matrix.T, user_normalize_matrix.T)
    item_cosine_similarity = cosine_similarity(item_normalize_matrix, item_normalize_matrix)

    user_prediction = predict(user_normalize_matrix.T, user_cosine_similarity, type='user')
    item_prediction = predict(item_normalize_matrix.T, item_cosine_similarity, type='item')

    pred_data = pd.DataFrame()
    pred_data = pred_data.append(pd.DataFrame(user_prediction))
    pred_data = pred_data.stack().reset_index(name='values')
    pred_data.columns = ['CustomerId', 'ModelId', 'values']
    pred_data['CustomerId'] = pred_data['CustomerId'].map(lambda value: users[value])
    pred_data['ModelId'] = pred_data['ModelId'].map(lambda value: items[value])
   
    fake_user_df = buy_model_dataframe.loc[buy_model_dataframe['CustomerId'] == fake_user_id]
    fake_user_predict = pred_data.loc[pred_data['CustomerId'] == fake_user_id]
    merged_data = fake_user_df.copy().merge(fake_user_predict, left_on=['CustomerId', 'ModelId'], right_on=['CustomerId', 'ModelId'], how='outer')

    redundancy = []
    for index, row in merged_data.iterrows():
        # access data using column names
        if math.isnan(row['values_x']) == False:
            redundancy.append(index)
    merged_data = merged_data.drop(redundancy)
    # return user_item_df.shape
    top_10 = merged_data.loc[merged_data['CustomerId'] == fake_user_id].nlargest(10, "values_y")
    cols = ['CustomerId', 'values_x']
    top_10.drop(cols, axis=1, inplace=True)
    return top_10