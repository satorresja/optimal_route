import pandas as pd
import pyodbc

class DatabaseConnector:
    
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        
    def _connect(self):
        # Crear la cadena de conexión a la base de datos
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        # Establecer la conexión
        self.conn = pyodbc.connect(conn_str)
        
    def fetch_data(self, query):
        # Establecer conexión si no está activa
        if not self.conn:
            self._connect()
        
        # Cargar los datos en un DataFrame utilizando Pandas
        df = pd.read_sql_query(query, self.conn)
        return df
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
