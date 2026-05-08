"""Limpeza estrutural do arquivo de ponto."""

from __future__ import annotations

import pandas as pd


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove colunas inúteis."""
    cols_to_drop = ["No", "TMNo", "GMNo", "Mode"]
    return df.drop(columns=cols_to_drop, errors="ignore")


def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Converte DateTime para datetime64[ns]."""
    df = df.copy()
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%Y/%m/%d %H:%M:%S", errors="raise")
    return df


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza Name com strip() e Title Case."""
    df = df.copy()
    df["Name"] = df["Name"].str.strip().str.title()
    return df


def transform_level1(df: pd.DataFrame) -> pd.DataFrame:
    """Executa a limpeza estrutural da Fase 1."""
    df = clean_columns(df)
    df = parse_datetime(df)
    df = clean_names(df)
    return df