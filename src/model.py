import pandas as pd
import numpy as np

class MatchModel:
    def __init__(self):
        self.ratings = {}

    def fit(self, df):
        """
        Calcula a força de cada seleção baseada na média de gols marcados e sofridos.
        Este método substitui o modelo complexo anterior por um cálculo estatístico robusto.
        """
        # Identifica todos os times únicos no DataFrame
        teams = pd.unique(df[['home_team', 'away_team']].values.ravel())
        
        # Calcula a média geral de gols do torneio
        global_avg = df[['home_score', 'away_score']].values.mean()
        
        for team in teams:
            # Gols marcados por esse time
            scored = df[df['home_team'] == team]['home_score'].sum() +                      df[df['away_team'] == team]['away_score'].sum()
            # Gols sofridos por esse time
            conceded = df[df['home_team'] == team]['away_score'].sum() +                        df[df['away_team'] == team]['home_score'].sum()
            
            # Número de jogos
            games = df[(df['home_team'] == team) | (df['away_team'] == team)].shape[0]
            
            if games > 0:
                # Rating = (Média de gols feitos + Média de gols sofridos inversos)
                # Isso cria um índice de performance simples e eficaz
                attack_strength = (scored / games) / global_avg
                defense_strength = (conceded / games) / global_avg
                self.ratings[team] = attack_strength - (defense_strength - 1)
            else:
                self.ratings[team] = 1.0 # Rating neutro para times sem dados
        
        return self

    def build_tables(self, teams):
        # Retorna o dicionário de ratings que o seu simulador espera
        return self.ratings
