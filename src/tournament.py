"""Primitivas vetorizadas da simulação (compartilhadas por 2026 e backtest).

Cada partida é resolvida para TODAS as simulações de uma vez (arrays de tamanho
n_sims), amostrando placares a partir da CDF pré-computada em Tables.
"""
from __future__ import annotations

from typing import Optional, Tuple

import numpy as np

from .brackets.wc2026 import GROUP_FIXTURES


def play_matches(
    tables,
    t1: np.ndarray,
    t2: np.ndarray,
    u_score: np.ndarray,
    knockout: bool = False,
    u_draw: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """Amostra o placar de t1 vs t2 (arrays de índices de time).

    Retorna (gols_t1, gols_t2, vencedor). No mata-mata, empates nos 90' são
    resolvidos por prorrogação+pênaltis via tables.adv_if_draw.
    """
    cdfs = tables.cdf[t1, t2]                      # (S, ncell)
    cells = (u_score[:, None] > cdfs).sum(axis=1)  # 1º índice com cdf >= u
    cells = np.clip(cells, 0, cdfs.shape[1] - 1)
    g1 = (cells // tables.gdim).astype(np.int16)
    g2 = (cells % tables.gdim).astype(np.int16)
    if not knockout:
        return g1, g2, None
    winner = np.where(g1 > g2, t1, t2)
    draw = g1 == g2
    if draw.any():
        adv = tables.adv_if_draw[t1, t2]
        t1_adv = u_draw < adv
        winner = np.where(draw, np.where(t1_adv, t1, t2), winner)
    return g1, g2, winner.astype(t1.dtype)


def simulate_groups(tables, group_idx: np.ndarray, rng, n_sims: int):
    """Simula a fase de grupos (grupos de 4) para n_sims realizações.

    group_idx : (NG, 4) índices globais dos times de cada grupo.
    Retorna place_team, place_pts, place_gd, place_gf de shape (NG, 4, n_sims),
    ordenados por colocação (0 = 1º ... 3 = 4º), com desempate
    pontos > saldo > gols pró > aleatório residual.
    """
    NG = group_idx.shape[0]
    place_team = np.zeros((NG, 4, n_sims), dtype=np.int32)
    place_pts = np.zeros((NG, 4, n_sims))
    place_gd = np.zeros((NG, 4, n_sims))
    place_gf = np.zeros((NG, 4, n_sims))

    for g in range(NG):
        teams = group_idx[g]
        pts = np.zeros((4, n_sims))
        gf = np.zeros((4, n_sims))
        ga = np.zeros((4, n_sims))
        for hp, ap in GROUP_FIXTURES:
            t1 = np.full(n_sims, teams[hp], dtype=np.int32)
            t2 = np.full(n_sims, teams[ap], dtype=np.int32)
            g1, g2, _ = play_matches(tables, t1, t2, rng.random(n_sims))
            gf[hp] += g1; ga[hp] += g2
            gf[ap] += g2; ga[ap] += g1
            pts[hp] += np.where(g1 > g2, 3, np.where(g1 == g2, 1, 0))
            pts[ap] += np.where(g2 > g1, 3, np.where(g1 == g2, 1, 0))
        gd = gf - ga
        rnd = rng.random((4, n_sims)) * 0.01
        key = pts * 1e6 + (gd + 100.0) * 1e3 + gf + rnd
        order = np.argsort(-key, axis=0)               # (4, n_sims)
        for place in range(4):
            row = order[place]
            place_team[g, place] = teams[row]
            place_pts[g, place] = np.take_along_axis(pts, row[None, :], 0)[0]
            place_gd[g, place] = np.take_along_axis(gd, row[None, :], 0)[0]
            place_gf[g, place] = np.take_along_axis(gf, row[None, :], 0)[0]
    return place_team, place_pts, place_gd, place_gf


def rank_key(pts: np.ndarray, gd: np.ndarray, gf: np.ndarray, rng=None) -> np.ndarray:
    """Chave de ordenação (maior = melhor) para ranquear times/terceiros."""
    k = pts * 1e6 + (gd + 100.0) * 1e3 + gf
    if rng is not None:
        k = k + rng.random(pts.shape) * 0.01
    return k
