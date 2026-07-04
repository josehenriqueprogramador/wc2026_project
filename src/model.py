from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


@dataclass
class EloConfig:
    base_rating: float = 1500.0
    k_factor: float = 20.0
    home_advantage: float = 60.0
    draw_margin: float = 0.0
    min_expected: float = 0.01
    max_expected: float = 0.99


class MatchModel:
    def __init__(self, config: Optional[EloConfig] = None):
        self.config = config or EloConfig()
        self.ratings: Dict[str, float] = {}
        self.names: List[str] = []
        self.w = 0.0

    def _expected_home(self, home_rating: float, away_rating: float) -> float:
        diff = (home_rating + self.config.home_advantage) - away_rating
        exp = 1.0 / (1.0 + 10.0 ** (-diff / 400.0))
        return float(np.clip(exp, self.config.min_expected, self.config.max_expected))

    def _result_score(self, home_score: int, away_score: int) -> float:
        if home_score > away_score:
            return 1.0
        if home_score < away_score:
            return 0.0
        return 0.5

    def fit(self, df: pd.DataFrame):
        if df.empty:
            self.ratings = {}
            self.names = []
            return self

        teams = pd.unique(df[["home_team", "away_team"]].values.ravel())
        self.names = list(teams)
        self.ratings = {team: self.config.base_rating for team in teams}

        if "date" in df.columns:
            df = df.sort_values("date").reset_index(drop=True)

        for row in df.itertuples(index=False):
            home = getattr(row, "home_team")
            away = getattr(row, "away_team")
            hs = int(getattr(row, "home_score"))
            a_s = int(getattr(row, "away_score"))

            rh = self.ratings.get(home, self.config.base_rating)
            ra = self.ratings.get(away, self.config.base_rating)
            eh = self._expected_home(rh, ra)
            sh = self._result_score(hs, a_s)
            delta = self.config.k_factor * (sh - eh)

            self.ratings[home] = rh + delta
            self.ratings[away] = ra - delta

        return self

    def _rating_for(self, team: str) -> float:
        return float(self.ratings.get(team, self.config.base_rating))

    def build_tables(self, teams):
        ds = [getattr(t, "ds", getattr(t, "pt", None)) for t in teams]
        idxs = [getattr(t, "idx") for t in teams]
        ratings = np.array([self._rating_for(name) for name in ds], dtype=float)
        n = len(teams)

        p_home = np.zeros((n, n), dtype=float)
        p_draw = np.zeros((n, n), dtype=float)
        p_away = np.zeros((n, n), dtype=float)

        for i in range(n):
            for j in range(n):
                if i == j:
                    p_home[i, j] = 0.0
                    p_draw[i, j] = 1.0
                    p_away[i, j] = 0.0
                    continue

                exp_home = self._expected_home(ratings[i], ratings[j])
                draw = max(0.0, 1.0 - abs(exp_home - 0.5) * 2.0 - abs(self.config.draw_margin))
                home = max(0.0, exp_home - draw / 2.0)
                away = max(0.0, 1.0 - exp_home - draw / 2.0)
                s = home + draw + away

                p_home[i, j] = home / s
                p_draw[i, j] = draw / s
                p_away[i, j] = away / s

        class Table:
            pass

        tab = Table()
        tab.p_home = p_home
        tab.p_draw = p_draw
        tab.p_away = p_away
        tab.ratings = {name: float(r) for name, r in zip(ds, ratings)}
        tab.team_index = {name: idx for name, idx in zip(ds, idxs)}
        return tab
