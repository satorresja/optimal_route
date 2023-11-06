import pandas as pd

class DataProcessor:
    
    def __init__(self, data_input):
        if isinstance(data_input, pd.DataFrame):
            self.data = data_input
        else:
            self.data = pd.read_csv(data_input)
        self._clean_data()
        
    def _clean_data(self):
        # Convertir LATITUD y LONGITUD a formato numérico
        self.data['LATITUD'] = pd.to_numeric(self.data['LATITUD'], errors='coerce')
        self.data['LONGITUD'] = pd.to_numeric(self.data['LONGITUD'], errors='coerce')
        # Eliminar filas con valores nulos en LATITUD o LONGITUD
        self.data.dropna(subset=['LATITUD', 'LONGITUD'], inplace=True)
        
    def get_data(self):
        return self.data.copy()
