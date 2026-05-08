"""Extração do arquivo bruto de ponto."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_RAW_FILE = ROOT_DIR / "data" / "raw" / "AGL_001.TXT"
FALLBACK_RAW_FILE = ROOT_DIR / "AGL_001.TXT"
RAW_ENCODINGS = ("utf-8-sig", "cp1252", "latin1")


def resolve_raw_file_path(raw_file: str | Path | None = None) -> Path:
    """Resolve o caminho do arquivo bruto."""
    candidate = Path(raw_file) if raw_file is not None else DEFAULT_RAW_FILE

    if candidate.exists():
        return candidate

    if raw_file is None and FALLBACK_RAW_FILE.exists():
        return FALLBACK_RAW_FILE

    raise FileNotFoundError(f"Raw file not found: {candidate}")


def load_raw_log(raw_file: str | Path | None = None) -> pd.DataFrame:
    """Carrega o log bruto em um DataFrame tabulado."""
    file_path = resolve_raw_file_path(raw_file)
    last_error: UnicodeDecodeError | None = None

    for encoding in RAW_ENCODINGS:
        try:
            return pd.read_csv(file_path, sep="\t", encoding=encoding)
        except UnicodeDecodeError as error:
            last_error = error

    raise UnicodeDecodeError(
        last_error.encoding if last_error else RAW_ENCODINGS[0],
        last_error.object if last_error else b"",
        last_error.start if last_error else 0,
        last_error.end if last_error else 0,
        "Unable to decode the raw log with the supported encodings.",
    ) from last_error