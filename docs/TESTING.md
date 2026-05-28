# Testing Guide

## Estrategia

- Testes unitarios para extração, limpeza, anti-spam e exportacao CSV.
- Teste de pipeline para a saida final.
- Fixtures pequenas em `tests/fixtures/`.

## Como rodar

```bash
pytest -q
pytest tests/test_extraction.py -v
pytest tests/test_level1_cleaning.py -v
pytest tests/test_level2_anti_spam.py -v
pytest tests/test_level4_load.py -v
```

## Cobertura atual

- Fase 1: extração
- Fase 2: limpeza
- Fase 3: anti-spam
- Fase 4: exportacao CSV

## Status esperado

- `tests/test_extraction.py`
- `tests/test_level1_cleaning.py`
- `tests/test_level2_anti_spam.py`
- `tests/test_level4_load.py`

## Fixture principal

`tests/fixtures/sample_agl.txt` imita o arquivo bruto real e é usada nos testes de leitura e limpeza.
