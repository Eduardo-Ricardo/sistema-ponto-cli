"""Transformação de hierarquia temporal do pipeline ETL."""

from __future__ import annotations

import pandas as pd


def extract_temporal_keys(df: pd.DataFrame) -> pd.DataFrame:
    """Extrai chaves temporais em formato textual com zero-padding."""
    result = df.copy()
    result["Year"] = result["DateTime"].dt.strftime("%Y")
    result["Month"] = result["DateTime"].dt.strftime("%m")
    result["Day"] = result["DateTime"].dt.strftime("%d")
    return result


def build_hierarchy(df: pd.DataFrame) -> dict[str, dict[str, dict[str, dict[str, list[str]]]]]:
    """Monta a hierarquia Ano -> Mês -> Funcionário -> Dia -> horários."""
    if df.empty:
        return {}

    hierarchy: dict[str, dict[str, dict[str, dict[str, list[str]]]]] = {}
    ordered = df.sort_values(
        ["Year", "Month", "EnNo", "Name", "Day", "DateTime"],
        kind="mergesort",
    )

    for (year, month, en_no, name, day), group in ordered.groupby(
        ["Year", "Month", "EnNo", "Name", "Day"], sort=True
    ):
        employee_key = f"{en_no}_{name}"
        emp_bucket = hierarchy.setdefault(year, {}).setdefault(month, {}).setdefault(employee_key, {})
        emp_bucket[day] = [timestamp.strftime("%H:%M:%S") for timestamp in group["DateTime"]]

    return hierarchy


def transform_level3(df: pd.DataFrame) -> dict[str, dict[str, dict[str, dict[str, list[str]]]]]:
    """Executa a transformação de hierarquia temporal."""
    if df.empty:
        return {}

    keyed = extract_temporal_keys(df)
    return build_hierarchy(keyed)