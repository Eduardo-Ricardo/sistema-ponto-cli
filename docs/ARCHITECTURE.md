# Arquitetura

Padrão do projeto: ETL simples para CSV.

## Fluxo

```text
TXT bruto
  -> load_raw_log()
  -> transform_level1()
  -> transform_level2()
  -> transform_level4()
  -> CSV final
```

## Decisoes

- A extração continua lendo o TXT tabulado com fallback de encoding.
- A limpeza continua removendo colunas inutiles e convertendo `DateTime`.
- A regra anti-spam continua ativa.
- A saida final deixa de ser JSON e passa a ser CSV.

## Componentes

- [src/extraction.py](../src/extraction.py): leitura do arquivo bruto.
- [src/cleaning.py](../src/cleaning.py): limpeza estrutural e parsing de data.
- [src/rules/anti_spam.py](../src/rules/anti_spam.py): filtro de batidas repetidas.
- [src/rules/load.py](../src/rules/load.py): preparacao e exportacao do CSV.
- [src/main.py](../src/main.py): fachada do pipeline.

## Saida

O arquivo gerado fica em `data/processed/dados_ponto.csv`.
