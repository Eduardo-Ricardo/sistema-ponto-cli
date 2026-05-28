# API Reference

Referência do fluxo atual: TXT bruto -> limpeza -> anti-spam -> CSV.

## Funcoes publicas

| Funcao | Entrada | Saida | Objetivo |
|---|---|---|---|
| `resolve_raw_file_path` | `str | Path | None` | `Path` | Localizar o arquivo bruto |
| `load_raw_log` | `str | Path | None` | `DataFrame` | Carregar o TXT tabulado |
| `clean_columns` | `DataFrame` | `DataFrame` | Remover colunas inutiles |
| `parse_datetime` | `DataFrame` | `DataFrame` | Converter `DateTime` |
| `clean_names` | `DataFrame` | `DataFrame` | Padronizar `Name` |
| `transform_level1` | `DataFrame` | `DataFrame` | Orquestrar limpeza |
| `identify_employee` | `DataFrame` | `DataFrame` | Criar chave de agrupamento |
| `apply_anti_spam_rule` | `DataFrame` | `DataFrame` | Remover batidas com gap < 5 min |
| `transform_level2` | `DataFrame` | `DataFrame` | Orquestrar anti-spam |
| `prepare_csv_output` | `DataFrame` | `DataFrame` | Gerar `ID`, `NOME`, `DATA`, `HORA` |
| `export_to_csv` | `DataFrame` | `Path` | Salvar CSV em disco |
| `transform_level4` | `DataFrame` | `Path` | Orquestrar exportacao final |

## CSV final

Colunas geradas:
- `ID` <- `EnNo`
- `NOME` <- `Name`
- `DATA` <- parte de data de `DateTime`
- `HORA` <- parte de hora de `DateTime`

Exemplo de saida:

```csv
ID,NOME,DATA,HORA
1,Usuario 1,2000-05-28,10:51:39
2,Usuario 2,2000-05-28,11:00:00
```
