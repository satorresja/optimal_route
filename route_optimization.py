import numpy as np
from sklearn.metrics.pairwise import haversine_distances

class RouteOptimizer:
    
    def __init__(self, data):
        self.data = data
        self.routes = {}
    
    def _compute_tsp_route_manual(self, points):
        """Compute a TSP route for a set of points using the nearest neighbor approximation manually."""
        remaining_points = list(range(len(points)))
        start_point = 0
        route = [start_point]
        remaining_points.remove(start_point)
        
        # Nearest neighbor algorithm
        while remaining_points:
            last_point = route[-1]
            distances = [haversine_distances([points[last_point]], [points[i]])[0][0] for i in remaining_points]
            nearest_point = remaining_points[np.argmin(distances)]
            route.append(nearest_point)
            remaining_points.remove(nearest_point)
        
        # Complete the cycle
        route.append(route[0])
        
        return route
    
    def optimize_routes(self):
        unique_clusters = self.data['cluster'].unique()
        
        for cluster in unique_clusters:
            if cluster != -1:  # Exclude noise
                cluster_points = self.data[self.data['cluster'] == cluster][['LATITUD', 'LONGITUD']].values
                route = self._compute_tsp_route_manual(cluster_points)
                self.routes[cluster] = route
                
        return self.routes
    
    def get_optimized_data(self):
        self.data['optimized_order'] = None
        for cluster, route in self.routes.items():
            cluster_data = self.data[self.data['cluster'] == cluster]
            self.data.loc[cluster_data.index, 'optimized_order'] = [route.index(i) for i in range(len(route)-1)]
        
        return self.data.copy()
