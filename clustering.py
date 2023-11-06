import numpy as np
from math import radians
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import haversine_distances
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

class LocationClusterer:
    
    def __init__(self, data):
        self.data = data
        self.coords = self.data[['LATITUD', 'LONGITUD']].values
        self.labels = None
        
    def cluster_locations(self, eps, min_samples):
        db = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine').fit(np.radians(self.coords))
        self.labels = db.labels_
        self.data['cluster'] = self.labels
        return self.labels
    
    def evaluate_clusters(self):
        if self.labels is None:
            raise ValueError("You need to perform clustering first.")
        
        # Filter out noise
        filtered_data = self.coords[self.labels != -1]
        filtered_labels = self.labels[self.labels != -1]
        
        silhouette_val = silhouette_score(filtered_data, filtered_labels, metric='haversine')
        calinski_harabasz_val = calinski_harabasz_score(filtered_data, filtered_labels)
        davies_bouldin_val = davies_bouldin_score(filtered_data, filtered_labels)
        
        return {
            'silhouette_score': silhouette_val,
            'calinski_harabasz_score': calinski_harabasz_val,
            'davies_bouldin_score': davies_bouldin_val
        }


    def get_distance_statistics(self, sample_size=100):
        """
        Calculate and return distance statistics for a sample of the data.
        
        Parameters:
        - sample_size: int. Size of the sample to be used. Default is 100.
        
        Returns:
        - tuple. Mean, median, minimum, and maximum distance in meters.
        """
        # Convert latitude and longitude to radians
        data_radians = np.radians(self.data[['LATITUD', 'LONGITUD']].values)
        
        # Take a representative sample of points to calculate distances
        sample_indices = np.random.choice(data_radians.shape[0], sample_size, replace=False)
        sample = data_radians[sample_indices]
        
        # Calculate distances between sample points using the Haversine formula
        distances = haversine_distances(sample, sample) * 6371000  # Convert to meters
        
        # Get the distribution of distances
        mean_distance = np.mean(distances)
        median_distance = np.median(distances)
        min_distance = np.min(distances)
        max_distance = np.max(distances)
        
        return mean_distance, median_distance, min_distance, max_distance
    
    def meters_to_radians(self, meters):
        """
        Convert a distance value in meters to radians based on Earth's radius.
        
        Parameters:
        - meters: float. Distance in meters.
        
        Returns:
        - float. Distance in radians.
        """
        earth_radius_meters = 6371008.8  # Earth's average radius in meters
        return meters / earth_radius_meters
    
    def calculate_eps(self, distance_meters):
        """
        Calculate eps value for DBSCAN clustering based on desired distance in meters.
        
        Parameters:
        - distance_meters: float. Desired distance in meters.
        
        Returns:
        - float. Eps value in radians.
        """
        return self.meters_to_radians(distance_meters)
    
    def get_clustered_data(self):
        return self.data.copy()
