import streamlit as st
import pandas as pd
from src import names, simulate, model, data_loader
import copa_realidade 

# Configuração da página
st.set_page_config(page_title="Simulador Copa 2026", layout="wide")

# 1. Carregar e preparar os dados com injeção da realidade
@st.cache_data
def carregar_dados():
    # Carrega histórico base
    df = data_loader.load_matches()
    
    # Injeção: Adiciona resultados da Copa 2026
    df_real = copa_realidade.obter_resultados_df()
    df = pd.concat([df, df_real], ignore_index=True)
    
    # Treina o modelo com a realidade incluída
    mm = model.MatchModel().fit(df)
    
    # Ajuste: Penaliza eliminados e bonifica vencedores nos ratings
    mm.ratings = copa_realidade.aplicar_ajustes(mm.ratings)
    
    # Simulação
    tables = mm.build_tables(names.TEAMS)
    res = simulate.simulate(tables)
    return simulate.to_dataframe(res)

try:
    df_resultados = carregar_dados()

    st.title("🏆 Simulador Copa do Mundo 2026")
    st.write("Resultados reais integrados ao modelo de Monte Carlo.")

    # 2. Abas para visualização
    tab1, tab2, tab3 = st.tabs(["📊 Top 10", "🇧🇷 Brasil", "⚽ Grupos"])

    with tab1:
        st.header("Top 10 Seleções por Probabilidade de Título")
        # Filtra apenas times com probabilidade relevante (removendo eliminados pelo rating)
        df_top = df_resultados.sort_values(by='P_campeao', ascending=False)
        st.table(df_top.head(10)[['selecao', 'P_campeao']])

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
    st.info("Verifique se o arquivo copa_realidade.py está na raiz.")
