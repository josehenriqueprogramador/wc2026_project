import streamlit as st
import pandas as pd
from src import names, simulate, model, data_loader

# Configuração da página
st.set_page_config(page_title="Simulador Copa 2026", layout="wide")

# 1. Carregar e preparar os dados
@st.cache_data
def carregar_dados():
    df = data_loader.load_matches()
    mm = model.MatchModel().fit(df)
    tables = mm.build_tables(names.TEAMS)
    res = simulate.simulate(tables)
    return simulate.to_dataframe(res)

try:
    df_resultados = carregar_dados()

    st.title("🏆 Simulador Copa do Mundo 2026")
    st.write("Resultados baseados em simulações de Monte Carlo.")

    # 2. Abas para visualização
    tab1, tab2, tab3 = st.tabs(["📊 Top 10", "🇧🇷 Brasil", "⚽ Grupos"])

    with tab1:
        st.header("Top 10 Seleções por Probabilidade de Título")
        st.table(df_resultados.sort_values(by='P_campeao', ascending=False).head(10)[['selecao', 'P_campeao']])

    with tab2:
        st.header("Análise: Brasil")
        brasil = df_resultados[df_resultados['selecao'] == 'Brasil']
        st.dataframe(brasil, use_container_width=True)

    with tab3:
        st.header("Filtro por Grupo")
        grupo_selecionado = st.selectbox("Escolha o Grupo", sorted(df_resultados['grupo'].unique()))
        st.table(df_resultados[df_resultados['grupo'] == grupo_selecionado][['selecao', 'P_classifica', 'P_campeao']])

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.info("Certifique-se de que a estrutura src/ está correta e os dados carregáveis.")
