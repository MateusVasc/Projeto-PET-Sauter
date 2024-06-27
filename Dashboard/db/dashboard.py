import streamlit as st
import pandas as pd
from PredictionsManager import PredictionsManager

def plot_prediction(pred_name, pred_manager):
    pred_manager = PredictionsManager('predictions.db')
    
    df_original, df_pred, df_test = pred_manager.get_prediction(pred_name)

    df_original['ds'] = pd.to_datetime(df_original['ds'])
    df_pred['ds'] = pd.to_datetime(df_pred['ds'])
    df_test['ds'] = pd.to_datetime(df_test['ds'])

    df_combined = pd.merge(df_original[['ds', 'y']], df_pred[['ds', 'XGBRegressor']], on='ds', how='outer', suffixes=('_orig', '_pred'))
    df_combined = pd.merge(df_combined, df_test[['ds', 'XGBRegressor']], on='ds', how='outer', suffixes=('', '_test'))

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
