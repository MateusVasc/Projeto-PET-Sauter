import streamlit as st
import pandas as pd
from PredictionsManager import PredictionsManager

def plot_prediction(pred_name, pred_manager):
    pred_manager = PredictionsManager('predictions.db')
    
    df_original, df_pred = pred_manager.get_prediction(pred_name)

    prediction_model_name = 'AutoARIMA'

    df_combined = pd.merge(df_original[['ds', 'y']], df_pred[['ds', prediction_model_name]], on='ds', how='outer', suffixes=('_orig', '_pred')).set_index('ds')

    df_combined.rename(columns = {'y':'Vendas', prediction_model_name : 'Previsão'}, inplace=True)

    st.line_chart(df_combined, width=0, height=0)

def main():
    st.title("Dashboard")
    st.sidebar.title("Menu")

    pred_manager = PredictionsManager('predictions.db')

    list_dfs = pred_manager.get_df_names()

    option = st.sidebar.selectbox("Selecione uma Base de Dados para previsão", list_dfs)

    plot_prediction(option, pred_manager)

if __name__ == "__main__":
    main()
