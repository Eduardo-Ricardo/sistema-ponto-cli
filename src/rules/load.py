"""Carga da hierarquia temporal para arquivo JSON."""

from __future__ import annotations

import json
from pathlib import Path


def export_to_json(
    hierarchy: dict[str, dict[str, dict[str, dict[str, list[str]]]]],
    output_path: str | Path = "data/processed/dados_ponto.json",
) -> Path:
    """Exporta hierarquia temporal para arquivo JSON com indentação legível."""
    output_path = Path(output_path)
    
    # Criar diretório de saída se não existir
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Serializar hierarquia para JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(hierarchy, f, indent=2, ensure_ascii=False)
    
    return output_path


def transform_level4(
    hierarchy: dict[str, dict[str, dict[str, dict[str, list[str]]]]],
    output_path: str | Path = "data/processed/dados_ponto.json",
) -> Path:
    """Executa a exportação para JSON (Fase 5)."""
    return export_to_json(hierarchy, output_path)
