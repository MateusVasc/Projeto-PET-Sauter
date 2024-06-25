import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PredictionsManager import PredictionsManager

def plot_prediction(pred_name):
    pred_manager = PredictionsManager('predictions.db')
    
    df_original, df_pred = pred_manager.get_prediction(pred_name)

    df_original['ds'] = pd.to_datetime(df_original['ds'])
    df_pred['ds'] = pd.to_datetime(df_pred['ds'])

    df_combined = pd.merge(df_original[['ds', 'y']], df_pred[['ds', 'LinearRegression']], on='ds', how='outer', suffixes=('_orig', '_pred'))

    df_pred.sort_values(by='ds', inplace=True)

    st.line_chart(df_combined.set_index('ds'), width=0, height=0)

def main():
    st.title("User Dashboard")
    st.sidebar.title("Menu")
    
    option = st.sidebar.selectbox("Select a section", ["General", "Hobbies"])
    
    plot_prediction(str.lower(option))

if __name__ == "__main__":
    main()
