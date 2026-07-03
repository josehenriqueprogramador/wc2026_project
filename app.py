import streamlit as st
import pandas as pd
import numpy as np
from src.model import MatchModel
from copa_realidade import obter_resultados_df

st.title("Simulador de Jogos WC2026")

df = obter_resultados_df()
model = MatchModel()
model.fit(df)
ratings = model.build_tables([])

# Interface para escolher os times
times = list(ratings.keys())
time_a = st.selectbox("Escolha o primeiro time:", times)
time_b = st.selectbox("Escolha o segundo time:", times)

if st.button("Simular Partida"):
    # Lógica de Poisson simples para gols
    # Força do time / média de gols esperada
    gols_a = np.random.poisson(ratings.get(time_a, 1.0))
    gols_b = np.random.poisson(ratings.get(time_b, 1.0))
    
    st.subheader("Resultado da Simulação:")
    st.write(f"**{time_a}** {gols_a} x {gols_b} **{time_b}**")
    
    if gols_a > gols_b:
        st.success(f"Vitória de {time_a}!")
    elif gols_b > gols_a:
        st.success(f"Vitória de {time_b}!")
    else:
        st.info("Empate!")
