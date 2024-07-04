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

    df_combined.set_index('ds', inplace=True)

    st.line_chart(df_combined, width=0, height=0)

def bar_chart_states(pred_manager):
    st.title('Vendas totais por estado')

    df = pred_manager.get_table('tabela_estados')
    df = df.set_index('state_id')

    st.bar_chart(df)

def bar_chart_stores(pred_manager):
    st.title('Vendas totais por loja')

    df = pred_manager.get_table('tabela_lojas')
    df = df.set_index('store_id')

    st.bar_chart(df)

def bar_chart_categorys(pred_manager):
    st.title('Vendas totais por categoria')

    df = pred_manager.get_table('tabela_categorias')
    df = df.set_index('cat_id')

    st.bar_chart(df)

def bar_chart_foods(pred_manager):
    st.title('Top 10 itens alimentícios')

    df = pred_manager.get_table('tabela_comidas')
    df = df.set_index('id')

    st.bar_chart(df)

def bar_chart_hobbies(pred_manager):
    st.title('Top 10 Itens de Hobby')

    df = pred_manager.get_table('tabela_hobbies')
    df = df.set_index('id')

    st.bar_chart(df)

def bar_chart_household(pred_manager):
    st.title('Top 10 Itens de Casa')

    df = pred_manager.get_table('tabela_casa')
    df = df.set_index('id')
    
    st.bar_chart(df)

def main():
    st.title("Previsão de Vendas")
    st.sidebar.title("Menu")

    pred_manager = PredictionsManager('predictions.db')

    list_dfs = pred_manager.get_df_names()

    option = st.sidebar.selectbox("Selecione uma Base de Dados para previsão", list_dfs)

    plot_prediction(option, pred_manager)

    cat_plots_options = ['Vendas por Estado', 'Vendas por Loja', 'Vendas por Categoria']
    cat_option = st.sidebar.selectbox("Selecione uma opção para o total de vendas", cat_plots_options)

    if cat_option == 'Vendas por Estado':
        bar_chart_states(pred_manager)
    elif cat_option == 'Vendas por Loja':
        bar_chart_stores(pred_manager)
    elif cat_option == 'Vendas por Categoria':
        bar_chart_categorys(pred_manager)

    top_10_options = ['Itens Alimentícios', 'Itens de Hobby', 'Itens de Casa']
    top_10_option = st.sidebar.selectbox("Selecione uma opção para os 10 itens mais vendidos", top_10_options)

    if top_10_option == 'Itens Alimentícios':
        bar_chart_foods(pred_manager)
    elif top_10_option == 'Itens de Hobby':
        bar_chart_hobbies(pred_manager)
    elif top_10_option == 'Itens de Casa':
        bar_chart_household(pred_manager)


if __name__ == "__main__":
    main()
