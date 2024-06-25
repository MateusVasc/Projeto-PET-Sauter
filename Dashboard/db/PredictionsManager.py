import sqlite3
import pandas as pd

class PredictionsManager:
    def __init__(self, db_path):
        try:
            self.db = sqlite3.connect(db_path)
            print(f'Banco de dados conectado: {db_path}')
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.db = None
    
    def save_predictions(self, df_pred):
        if self.db is None:
            print("Conexão com o banco de dados não está estabelecida.")
            return

        table_names = df_pred['unique_id'].unique()

        try:
            for name in table_names:
                curr_pred = df_pred[df_pred['unique_id'] == name]

                curr_pred.to_sql(name, self.db, index=False, if_exists='replace')
            
            print(f'Todas as previsões foram salvas em tabelas chamadas: {table_names}')
        except sqlite3.Error as e:
            print(f"Erro ao salvar previsões: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    def get_prediction(self, series_name):
        if self.db is None:
            print("Conexão com o banco de dados não está estabelecida.")
            return None
        
        query_string = f'SELECT * FROM {series_name}'

        try:
            series_pred = pd.read_sql_query(query_string, self.db)
            series_pred['ds'] = pd.to_datetime(series_pred['ds'])
            print(f'Previsões recuperadas com sucesso para: {series_name}')
            return series_pred
        except pd.io.sql.DatabaseError as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None

    def close_connection(self):
        if self.db:
            try:
                self.db.close()
                print('Conexão fechada')
            except sqlite3.Error as e:
                print(f"Erro ao fechar a conexão: {e}")
        else:
            print('Nenhuma conexão para fechar')
