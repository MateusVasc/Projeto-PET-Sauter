import sqlite3
import pandas as pd

class PredictionsManager:
    def __init__(self, db_path):
        try:
            self.db = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.db = None
    
    def save_predictions(self, df, df_pred, df_test):
        if self.db is None:
            print("Conexão com o banco de dados não está estabelecida.")
            return

        table_names = df_pred['unique_id'].unique()

        try:
            for name in table_names:
                curr_df = df[df['unique_id'] == name]
                curr_test = df_test[df_test['unique_id'] == name]
                curr_pred = df_pred[df_pred['unique_id'] == name]

                curr_df.to_sql(name, self.db, index=False, if_exists='replace')
                curr_test.to_sql(f'test_{name}', self.db, index=False, if_exists='replace')
                curr_pred.to_sql(f'pred_{name}', self.db, index=False, if_exists='replace')
            
            print(f'Todas as previsões foram salvas em tabelas chamadas: {table_names}')
        except sqlite3.Error as e:
            print(f"Erro ao salvar previsões: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    def get_prediction(self, series_name):
        if self.db is None:
            print("Conexão com o banco de dados não está estabelecida.")
            return None
        
        pred_name = f'pred_{series_name}'
        test_name = f'test_{series_name}'

        query_string = f'SELECT * FROM {series_name}'
        query_string_pred = f'SELECT * FROM {pred_name}'
        query_string_test = f'SELECT * FROM {test_name}'

        try:
            series = pd.read_sql_query(query_string, self.db)
            series['ds'] = pd.to_datetime(series['ds'])
            
            series_pred = pd.read_sql_query(query_string_pred, self.db)
            series_pred['ds'] = pd.to_datetime(series_pred['ds'])

            series_test = pd.read_sql_query(query_string_test, self.db)
            series_test['ds'] = pd.to_datetime(series_test['ds'])
            
            return series, series_pred, series_test
        
        except pd.io.sql.DatabaseError as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None

    def get_df_names(self):
        cursor = self.db.cursor() 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        names = cursor.fetchall() 

        table_names = [name[0] for name in names if not (name[0].startswith('test_') or name[0].startswith('pred'))]
        
        return table_names 

    def close_connection(self):
        if self.db:
            try:
                self.db.close()
                print('Conexão fechada')
            except sqlite3.Error as e:
                print(f"Erro ao fechar a conexão: {e}")
        else:
            print('Nenhuma conexão para fechar')

    def add_table(self, df, table_name):
        if self.db is None:
            print("Conexão com o banco de dados não está estabelecida.")
            return
        
        try:
            df.to_sql(table_name, self.db, index=False, if_exists='replace')
            print(f"Tabela '{table_name}' adicionada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao adicionar a tabela: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_table(self, table_name):
        if self.db is None:
            print("Conexão com o banco de dados não está estabelecida.")
            return None
        
        query_string = f'SELECT * FROM {table_name}'
        
        try:
            df = pd.read_sql_query(query_string, self.db)
            return df
        except pd.io.sql.DatabaseError as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None
