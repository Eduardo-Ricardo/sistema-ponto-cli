# Quick Start

## Setup

```bash
git clone https://github.com/Eduardo-Ricardo/sistema-ponto-cli.git
cd sistema-ponto-cli
python -m pip install -r requirements.txt
```

## Rodar testes

```bash
pytest -q
pytest tests/test_level4_load.py -v
```

## Rodar o pipeline

```bash
python src/main.py
```

Saida esperada: CSV em `data/processed/dados_ponto.csv`.

## Estrutura

- `src/main.py` orquestra o fluxo.
- `src/rules/load.py` escreve o CSV final.
- `tests/test_level4_load.py` valida a exportacao.

## Proximo passo

Use o arquivo bruto em `data/raw/AGL_001.TXT` ou na raiz do projeto para testar com seus dados.
