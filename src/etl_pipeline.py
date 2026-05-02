"""ETL — extração inicial do arquivo de ponto.

Módulo responsável pela leitura do arquivo bruto AGL_001.TXT e transformações
iniciais (Fase 1: Extração, Fase 2: Limpeza Estrutural).

Funções públicas:
- `resolve_raw_file_path(raw_file)`: localiza o arquivo bruto.
- `load_raw_log(raw_file)`: carrega o TXT tab-delimitado.
- `clean_columns(df)`: remove colunas inúteis.
- `parse_datetime(df)`: converte DateTime para datetime64[ns].
- `clean_names(df)`: padroniza Name (strip + Title Case).
- `transform_level1(df)`: orquestrador da limpeza estrutural.

As docstrings são concisas para não poluir o corpo das funções.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_RAW_FILE = ROOT_DIR / "data" / "raw" / "AGL_001.TXT"
FALLBACK_RAW_FILE = ROOT_DIR / "AGL_001.TXT"
RAW_ENCODINGS = ("utf-8-sig", "cp1252", "latin1")


def resolve_raw_file_path(raw_file: str | Path | None = None) -> Path:
    """Resolve o caminho do arquivo bruto.

    Se `raw_file` for fornecido, converte para `Path` e retorna se existir.
    Caso contrário, tenta `data/raw/AGL_001.TXT` e faz fallback para
    `AGL_001.TXT` na raiz quando presente.

    Lança `FileNotFoundError` se nenhum dos candidatos existir.
    """
    candidate = Path(raw_file) if raw_file is not None else DEFAULT_RAW_FILE

    if candidate.exists():
        return candidate

    if raw_file is None and FALLBACK_RAW_FILE.exists():
        return FALLBACK_RAW_FILE

    raise FileNotFoundError(f"Raw file not found: {candidate}")


def load_raw_log(raw_file: str | Path | None = None) -> pd.DataFrame:
    """Carrega o log bruto em um DataFrame.

    Tenta os encodings definidos em `RAW_ENCODINGS` até encontrar um que
    funcione. Usa separador de tabulação. Retorna o DataFrame lido.
    """
    file_path = resolve_raw_file_path(raw_file)
    last_error: UnicodeDecodeError | None = None

    for encoding in RAW_ENCODINGS:
        try:
            return pd.read_csv(file_path, sep="\t", encoding=encoding)
        except UnicodeDecodeError as error:
            last_error = error

    # Propaga um UnicodeDecodeError com contexto se nenhum encoding funcionou.
    raise UnicodeDecodeError(
        last_error.encoding if last_error else RAW_ENCODINGS[0],
        last_error.object if last_error else b"",
        last_error.start if last_error else 0,
        last_error.end if last_error else 0,
        "Unable to decode the raw log with the supported encodings.",
    ) from last_error


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove colunas inúteis (No, TMNo, GMNo, Mode)."""
    cols_to_drop = ["No", "TMNo", "GMNo", "Mode"]
    return df.drop(columns=cols_to_drop, errors="ignore")


def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Converter coluna DateTime para datetime64[ns]."""
    df = df.copy()
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%Y/%m/%d %H:%M:%S", errors="raise")
    return df


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    """Padronizar coluna Name: strip() + Title Case."""
    df = df.copy()
    df["Name"] = df["Name"].str.strip().str.title()
    return df


def transform_level1(df: pd.DataFrame) -> pd.DataFrame:
    """Orquestrador da Transformação Nível 1 (Limpeza Estrutural).

    Aplica: remoção de colunas, parsing de DateTime, padronização de Names.
    Retorna DataFrame limpo pronto para Nível 2.
    """
    df = clean_columns(df)
    df = parse_datetime(df)
    df = clean_names(df)
    return df


def main() -> None:
    """Entrypoint mínimo para inspeção: imprime `head()` do DataFrame limpo."""
    raw_log = load_raw_log()
    cleaned = transform_level1(raw_log)
    print(cleaned.head())


if __name__ == "__main__":
    main()
