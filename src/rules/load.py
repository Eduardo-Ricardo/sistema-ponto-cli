"""Carga do resultado final para arquivo CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

def prepare_csv_output(df: pd.DataFrame) -> pd.DataFrame:
    """Seleciona e renomeia as colunas finais do CSV."""
    result = df.copy()
    result["DATA"] = result["DateTime"].dt.strftime("%Y-%m-%d")
    result["HORA"] = result["DateTime"].dt.strftime("%H:%M:%S")
    result = result.rename(columns={"EnNo": "ID", "Name": "NOME"})
    return result[["ID", "NOME", "DATA", "HORA"]]


def export_to_csv(
    df: pd.DataFrame,
    output_path: str | Path = "data/processed/dados_ponto.csv",
) -> Path:
    """Exporta o resultado final para arquivo CSV."""
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    prepared = prepare_csv_output(df)
    prepared.to_csv(output_path, index=False, encoding="utf-8")

    return output_path


def transform_level4(
    df: pd.DataFrame,
    output_path: str | Path = "data/processed/dados_ponto.csv",
) -> Path:
    """Executa a exportação para CSV."""
    return export_to_csv(df, output_path)
