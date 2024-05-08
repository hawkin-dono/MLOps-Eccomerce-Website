"""
DONE:
- To implement the adjusted cosine similarity
- To implement similarities pre-calculation
- To implement the rating prediction based on similarities
- To implement the recommendation system

TODO:
- To refactor
- To optimize
"""

import pandas as pd
import numpy as np
from tqdm import tqdm


class RecommendationSystem(object):
    def __init__(self, similarities_matrix_file=None):
        self.rating_data = None
        self.rating_matrix = None
        self.similarities_matrix_file = similarities_matrix_file
        self.similarities_matrix = None
        self.new_users = None
        self.senior_users = None

    def read_csv(self, file):
        self.rating_data = pd.read_csv(file)

    def matrix_construction(self):
        # Create a pivot table
        pivot_table = pd.pivot_table(self.rating_data, values='rating', index='customer_id', columns='product_id')
        # Only retain users that voted for at least 10 items
        pivot_table['cnt'] = pivot_table.count(axis=1)
        self.senior_users = pivot_table[pivot_table['cnt'] >= 10].index.to_list()
        pivot_table = pivot_table[pivot_table['cnt'] >= 10].drop(columns=['cnt'])
        pivot_table = pivot_table.fillna(0)
        self.rating_matrix = pivot_table
        return pivot_table

    def high_rating(self):
        sum = self.rating_matrix.sum()
        count = (self.rating_matrix > 0).astype(int).sum(axis=0)
        rating = (sum / count).fillna(0).sort_values(ascending=False)
        return rating.head(10).index.to_list()

    def adjusted_cosine(self, item_i, item_j):
        rated_users = self.rating_matrix[
            (self.rating_matrix.iloc[:, item_i] > 0) & (self.rating_matrix.iloc[:, item_j] > 0)]
        numerator = 0
        denominator = 0
        sum_1 = 0
        sum_2 = 0
        for user in rated_users.index:
            user_index = self.senior_users.index(user)
            mean_user_u = self.rating_matrix.iloc[user_index].mean()
            r_ui = self.rating_matrix.iloc[user_index, item_i]
            r_uj = self.rating_matrix.iloc[user_index, item_j]
            numerator += ((r_ui - mean_user_u) * (r_uj - mean_user_u))
            sum_1 += (r_ui - mean_user_u) ** 2
            sum_2 += (r_uj - mean_user_u) ** 2

        denominator = np.sqrt(sum_1) * np.sqrt(sum_2)
        if denominator == 0:
            return 0

        return numerator / denominator

    def similarities(self):
        if self.similarities_matrix_file is not None:
            matrix = pd.read_csv(self.similarities_matrix_file)
            self.similarities_matrix = matrix
            return matrix

        n_items = len(self.rating_matrix.columns)
        print(n_items)
        matrix = np.zeros((n_items, n_items))
        for item_i in tqdm(range(n_items)):
            for item_j in range(n_items):
                matrix[item_i, item_j] = self.adjusted_cosine(item_i, item_j)
        pd.DataFrame(matrix).to_csv('similarities_matrix.csv', index=False)
        return matrix

    def predict(self, uid, item_i):
        if uid not in self.senior_users:
            return None
        user_u = self.senior_users.index(uid)
        user_rating = self.rating_matrix.iloc[user_u]
        numerator = 0
        denominator = 0
        for item_id in user_rating.index:
            if user_rating[item_id] == 0.:
                continue
            numerator += abs(self.similarities_matrix.iloc[item_id, item_i] * user_rating[item_id])
            denominator += abs(self.similarities_matrix.iloc[item_id, item_i])
        if denominator == 0:
            return 0
        return numerator / denominator

    def recommend(self, uid):
        if uid not in self.senior_users:
            print('Nani????')
            return self.high_rating()
        user_u = self.senior_users.index(uid)
        recommend = []
        n_items = len(self.rating_matrix.columns)
        for item_i in range(n_items):
            if self.rating_matrix.iloc[user_u, item_i] == 0:
                recommend.append((self.predict(uid, item_i), item_i))
        recommend.sort(reverse=True)
        recommend = recommend[:10]
        return [rcm[1] for rcm in recommend]


if __name__ == '__main__':
    rcm = RecommendationSystem(similarities_matrix_file='similarities_matrix.csv')
    rcm.read_csv('user_item_rating.csv')
    rcm.matrix_construction()
    rcm.similarities()
    print(rcm.recommend(2))

