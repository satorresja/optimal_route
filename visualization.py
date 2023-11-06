import folium

class ClusterVisualizer:
    
    def __init__(self, data):
        self.data = data
        
    def visualize_clusters(self, output_html):
        # Create a base map
        m = folium.Map(location=[self.data['LATITUD'].mean(), self.data['LONGITUD'].mean()], zoom_start=12)
        
        # Color mapping
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 
                  'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen']
        
        # Add points to the map
        for index, row in self.data.iterrows():
            if row['cluster'] != -1:
                folium.CircleMarker(
                    location=(row['LATITUD'], row['LONGITUD']),
                    radius=5,
                    popup=f"Cluster: {row['cluster']}, Order: {row['optimized_order']}",
                    fill=True,
                    color=colors[int(row['cluster']) % len(colors)],
                    fill_color=colors[int(row['cluster']) % len(colors)],
                ).add_to(m)
        
        m.save(output_html)
        return output_html
