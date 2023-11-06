from decouple import config
from database_connector import DatabaseConnector
from data_processing import DataProcessor
from clustering import LocationClusterer
from route_optimization import RouteOptimizer
from visualization import ClusterVisualizer

# Configuración de la base de datos

DB_CONFIG = {
    'server': config('SERVER'),
    'database': config('DATABASE'),
    'username': config('USERNAME'),
    'password': config('PASSWORD')
}

# Definir tu consulta SQL
SQL_QUERY = "SELECT [EMPRESA_ID],[CLIENTE_ID],[UBICACION_ID],[NOMBRE_UBICACION],[DIRECCION],[LATITUD],[LONGITUD],[PAIS_ID],[NOMBRE_PAIS],[DEPARTAMENTO_ID],[NOMBRE_DEPARTAMENTO],[CIUDAD_ID],[NOMBRE_CIUDAD],[ZONA_ID],[NOMBRE_ZONA],[BARRIO],[REGION_ID],[NOMBRE_REGION],[ES_PUNTO_VISITA],[ES_PUNTO_ENVIO],[REVALID_DIAS_VISITAS],[REVALID_FREC_VISITAS],[REVALID_SEM_VISITAS],[ESTADO_ACTIVO] FROM [EasySalesBI].[dbo].[VW_BI_UBICACION] where [EMPRESA_ID] = 295 and [ESTADO_ACTIVO] = 1 and [LATITUD] is not null and [LATITUD] != 0"

if __name__ == "__main__":
    # 1. Fetch Data from Database
    db_connector = DatabaseConnector(**DB_CONFIG)
    df = db_connector.fetch_data(SQL_QUERY)
    db_connector.close_connection()
    
    # 2. Data Processing
    data_processor = DataProcessor(df)
    processed_data = data_processor.get_data()
    
    # 3. Clustering
    clusterer = LocationClusterer(processed_data)
    # Calculate distance statistics
    mean_dist, median_dist, min_dist, max_dist = clusterer.get_distance_statistics()
    print(f"Mean Distance: {mean_dist} meters")
    print(f"Median Distance: {median_dist} meters")
    print(f"Min Distance: {min_dist} meters")
    print(f"Max Distance: {max_dist} meters")
    eps_value = clusterer.calculate_eps(mean_dist)  # Calculate eps for 500 meters
    clusterer.cluster_locations(eps=eps_value, min_samples=5)
    clustered_data = clusterer.get_clustered_data()
    
    # 4. Route Optimization
    optimizer = RouteOptimizer(clustered_data)
    optimizer.optimize_routes()
    optimized_data = optimizer.get_optimized_data()
    
    # Add Cluster and Route Order to the original DataFrame
    df["Cluster"] = optimized_data["cluster"]
    df["Route_Order"] = optimized_data["optimized_order"]
    
    # 5. Visualization
    visualizer = ClusterVisualizer(optimized_data)
    visualizer.visualize_clusters("clustered_map.html")

    # 6. Descargar el df
    output_file = "final_output.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Data saved to {output_file}")
