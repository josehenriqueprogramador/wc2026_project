import pandas as pd

# Resultados oficiais até 03/07/2026
JOGOS_REALIZADOS = [
    {'date': '2026-07-01', 'home': 'Australia', 'away': 'Egypt', 'winner': 'Egypt', 'score_h': 1, 'score_a': 1, 'p_winner': 'Egypt'},
    {'date': '2026-07-01', 'home': 'Switzerland', 'away': 'Algeria', 'winner': 'Switzerland', 'score_h': 2, 'score_a': 0},
    {'date': '2026-07-01', 'home': 'Portugal', 'away': 'Croatia', 'winner': 'Portugal', 'score_h': 2, 'score_a': 1},
    {'date': '2026-07-02', 'home': 'Spain', 'away': 'Austria', 'winner': 'Spain', 'score_h': 3, 'score_a': 0},
    {'date': '2026-07-02', 'home': 'United States', 'away': 'Bosnia and Herzegovina', 'winner': 'United States', 'score_h': 2, 'score_a': 0},
    {'date': '2026-07-02', 'home': 'Belgium', 'away': 'Senegal', 'winner': 'Belgium', 'score_h': 3, 'score_a': 2},
    {'date': '2026-07-03', 'home': 'England', 'away': 'DR Congo', 'winner': 'England', 'score_h': 2, 'score_a': 1},
    {'date': '2026-07-03', 'home': 'Mexico', 'away': 'Ecuador', 'winner': 'Mexico', 'score_h': 2, 'score_a': 0},
    {'date': '2026-07-03', 'home': 'France', 'away': 'Sweden', 'winner': 'France', 'score_h': 3, 'score_a': 0},
    {'date': '2026-07-03', 'home': 'Norway', 'away': 'Ivory Coast', 'winner': 'Norway', 'score_h': 2, 'score_a': 1},
    {'date': '2026-07-03', 'home': 'Morocco', 'away': 'Netherlands', 'winner': 'Morocco', 'score_h': 1, 'score_a': 1, 'p_winner': 'Morocco'},
    {'date': '2026-07-03', 'home': 'Paraguay', 'away': 'Germany', 'winner': 'Paraguay', 'score_h': 1, 'score_a': 1, 'p_winner': 'Paraguay'},
    {'date': '2026-07-03', 'home': 'Brazil', 'away': 'Japan', 'winner': 'Brazil', 'score_h': 2, 'score_a': 1}
]

ELIMINADOS = [
    'Australia', 'Algeria', 'Croatia', 'Austria', 'Bosnia and Herzegovina', 
    'Senegal', 'DR Congo', 'Ecuador', 'Sweden', 'Ivory Coast', 'Netherlands', 'Germany', 'Japan'
]

def aplicar_ajustes(ratings):
    """
    Ajusta os ratings calculados pelo modelo com base na realidade da Copa.
    """
    # 1. Penaliza severamente quem foi eliminado
    for time in ELIMINADOS:
        if time in ratings:
            ratings[time] *= 0.01  # Força cai drasticamente
            
    # 2. Bônus para quem permanece vivo e venceu
    for jogo in JOGOS_REALIZADOS:
        vencedor = jogo['p_winner'] if 'p_winner' in jogo else jogo['winner']
        if vencedor in ratings:
            ratings[vencedor] *= 1.15
            
    return ratings

def obter_resultados_df():
    # Converte para formato compatível com o seu data_loader
    data = []
    for j in JOGOS_REALIZADOS:
        data.append({'date': j['date'], 'home_team': j['home'], 'away_team': j['away'], 
                     'home_score': j['score_h'], 'away_score': j['score_a'], 'tournament': 'World Cup'})
    return pd.DataFrame(data)
