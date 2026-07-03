import pandas as pd
import numpy as np

class MatchModel:
    def __init__(self):
        self.ratings = {}
        self.n = 1000
        self.names = []

    def fit(self, df):
        teams = pd.unique(df[['home_team', 'away_team']].values.ravel())
        self.names = list(teams)
        # Calcula média global para normalizar os ratings
        global_avg = df[['home_score', 'away_score']].values.mean()
        
        for team in teams:
            scored = df[df['home_team'] == team]['home_score'].sum() +                      df[df['away_team'] == team]['away_score'].sum()
            games = df[(df['home_team'] == team) | (df['away_team'] == team)].shape[0]
            # Rating normalizado pela média global
            self.ratings[team] = (scored / games) / global_avg if games > 0 else 1.0
        return self

    def build_tables(self, teams):
        return self.ratings
