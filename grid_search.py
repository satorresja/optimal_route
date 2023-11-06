# grid_search.py

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

import numpy as np

class DBSCANGridSearch:

    def __init__(self, data):
        self.data = np.radians(data[['LATITUD', 'LONGITUD']].values)
        self.best_score = -1
        self.best_params = {'eps': None, 'min_samples': None}

    def search(self, eps_values, min_samples_values):
        for eps in eps_values:
            for min_samples in min_samples_values:
                db = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine').fit(self.data)
                labels = db.labels_

                no_noise_labels = labels[labels != -1]
                no_noise_data = self.data[labels != -1]

                if len(set(no_noise_labels)) < 2:
                    continue

                score = silhouette_score(no_noise_data, no_noise_labels, metric='haversine')

                if score > self.best_score:
                    self.best_score = score
                    self.best_params['eps'] = eps
                    self.best_params['min_samples'] = min_samples

        return self.best_score, self.best_params
