"""Regra anti-spam para batidas consecutivas."""

from __future__ import annotations

import pandas as pd


def identify_employee(df: pd.DataFrame) -> pd.DataFrame:
    """Cria a coluna Employee a partir de EnNo e Name."""
    df = df.copy()
    df["Employee"] = df["EnNo"].astype(str) + "_" + df["Name"]
    return df


def apply_anti_spam_rule(df: pd.DataFrame, min_gap_minutes: int = 5) -> pd.DataFrame:
    """Remove batidas consecutivas com intervalo menor que o mínimo."""
    df = identify_employee(df)
    rows_to_keep: list[int] = []

    for _, group in df.groupby("Employee"):
        group_sorted = group.sort_values("DateTime")
        previous_index = None

        for current_index, current_row in group_sorted.iterrows():
            if previous_index is None:
                rows_to_keep.append(current_index)
                previous_index = current_index
                continue

            previous_row = group_sorted.loc[previous_index]
            gap_minutes = (current_row["DateTime"] - previous_row["DateTime"]).total_seconds() / 60

            if gap_minutes >= min_gap_minutes:
                rows_to_keep.append(current_index)
                previous_index = current_index

    result = df.loc[rows_to_keep].drop(columns=["Employee"])
    return result.reset_index(drop=True)


def transform_level2(df: pd.DataFrame) -> pd.DataFrame:
    """Executa a regra anti-spam da Fase 2."""
    return apply_anti_spam_rule(df)