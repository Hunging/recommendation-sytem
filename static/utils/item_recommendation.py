import numpy as np
import pandas as pd
import os
import sys
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
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

    return data_items_result.loc[id].nlargest(10)
