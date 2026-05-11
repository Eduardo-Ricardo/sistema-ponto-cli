"""Fachada do pipeline ETL.

Este módulo preserva a API pública usada pelos testes e scripts, enquanto a
implementação real vive em módulos especializados.
"""

from __future__ import annotations

from cleaning import clean_columns, clean_names, parse_datetime, transform_level1
from extraction import load_raw_log, resolve_raw_file_path
from rules.anti_spam import apply_anti_spam_rule, identify_employee, transform_level2
from rules.hierarchy import build_hierarchy, extract_temporal_keys, transform_level3
from rules.load import export_to_json, transform_level4


def main() -> None:
    """Entrypoint do pipeline ETL completo: carrega, limpa, filtra, hierarquiza e exporta para JSON."""
    raw_log = load_raw_log()
    cleaned = transform_level1(raw_log)
    filtered = transform_level2(cleaned)
    hierarchy = transform_level3(filtered)
    output_file = transform_level4(hierarchy)
    print(f"✓ Pipeline concluído. JSON exportado: {output_file.resolve()}")


if __name__ == "__main__":
    main()