"""Fachada do pipeline ETL.

Este módulo preserva a API pública usada pelos testes e scripts, enquanto a
implementação real vive em módulos especializados.
"""

from __future__ import annotations

from cleaning import clean_columns, clean_names, parse_datetime, transform_level1
from extraction import load_raw_log, resolve_raw_file_path
from rules.anti_spam import apply_anti_spam_rule, identify_employee, transform_level2


def main() -> None:
    """Entrypoint mínimo para inspeção: imprime o `head()` após L2."""
    raw_log = load_raw_log()
    cleaned = transform_level1(raw_log)
    filtered = transform_level2(cleaned)
    print(filtered.head())


if __name__ == "__main__":
    main()
