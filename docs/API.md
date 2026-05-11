# 🔧 API Reference

Referência completa de funções públicas em `src/main.py`.

## Visão Geral

| Função | Fase | Input | Output | Objetivo |
|--------|------|-------|--------|----------|
| `resolve_raw_file_path` | 1 | str/Path/None | Path | Localizar arquivo bruto |
| `load_raw_log` | 1 | str/Path/None | DataFrame | Carregar TXT bruto |
| `clean_columns` | 2 | DataFrame | DataFrame | Drop colunas inúteis |
| `parse_datetime` | 2 | DataFrame | DataFrame | Converter DateTime para datetime64 |
| `clean_names` | 2 | DataFrame | DataFrame | Padronizar nomes |
| `transform_level1` | 2 | DataFrame | DataFrame | Orquestrador Fase 2 |
| `identify_employee` | 3 | DataFrame | DataFrame | Criar coluna Employee |
| `apply_anti_spam_rule` | 3 | DataFrame | DataFrame | Remover duplicatas |
| `transform_level2` | 3 | DataFrame | DataFrame | Orquestrador Fase 3 |
| `extract_temporal_keys` | 4 | DataFrame | DataFrame | Extrair Year/Month/Day |
| `build_hierarchy` | 4 | DataFrame | dict | Montar hierarquia temporal |
| `transform_level3` | 4 | DataFrame | dict | Orquestrador Fase 4 |

---

## Fase 1: Extração

### `resolve_raw_file_path(raw_file: str | Path | None = None) -> Path`

**Localiza o arquivo bruto com fallback automático.**

**Parâmetros**:
- `raw_file` (str | Path | None) — Caminho explícito ou None para usar padrões

**Retorno**: `Path` — Caminho absoluto do arquivo

**Erros**: `FileNotFoundError` se arquivo não existir

**Lógica**:
1. Se `raw_file` informado e existe → retorna como Path
2. Se None, tenta `data/raw/AGL_001.TXT`
3. Se não existir, tenta fallback `./AGL_001.TXT` na raiz
4. Se nenhum existir → lança FileNotFoundError

**Exemplo**:
```python
>>> from src.main import resolve_raw_file_path
>>> resolve_raw_file_path()
PosixPath('/workspaces/sistema-ponto-cli/data/raw/AGL_001.TXT')

>>> resolve_raw_file_path("./arquivo_customizado.txt")
PosixPath('/workspaces/sistema-ponto-cli/arquivo_customizado.txt')
```

---

### `load_raw_log(raw_file: str | Path | None = None) -> pd.DataFrame`

**Carrega arquivo TXT bruto com fallback de encoding.**

**Parâmetros**:
- `raw_file` (str | Path | None) — Caminho do arquivo (opcional)

**Retorno**: `pd.DataFrame` com 7 colunas: No, TMNo, EnNo, Name, GMNo, Mode, DateTime

**Erros**:
- `FileNotFoundError` — Se arquivo não encontrado (delegado a `resolve_raw_file_path()`)
- `UnicodeDecodeError` — Se nenhum encoding funciona

**Codificações tentadas** (em ordem):
1. `utf-8-sig` (padrão UTF-8 com BOM)
2. `cp1252` (Windows Latin)
3. `latin1` (ISO-8859-1)

**Separador**: `\t` (tabulação)

**Exemplo**:
```python
>>> from src.main import load_raw_log
>>> df = load_raw_log()
>>> df.shape
(7744, 7)

>>> df.head()
   No  TMNo  EnNo         Name  GMNo  Mode            DateTime
0   1     1     1    usuario 1     0     1  2000/05/28 10:51:39
1   2     1     1    usuario 1     0     1  2000/05/28 10:51:46
```

---

## Fase 2: Limpeza

### `clean_columns(df: pd.DataFrame) -> pd.DataFrame`

**Remove colunas inúteis.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame com colunas a remover

**Retorno**: `pd.DataFrame` — Cópia sem colunas: No, TMNo, GMNo, Mode

**Colunas removidas**: No, TMNo, GMNo, Mode

**Colunas mantidas**: EnNo, Name, DateTime (+ qualquer outra coluna adicional)

**Nota**: Usa `errors="ignore"` para não falhar se coluna de remoção não existir

**Exemplo**:
```python
>>> df_original.columns
Index(['No', 'TMNo', 'EnNo', 'Name', 'GMNo', 'Mode', 'DateTime'], dtype='object')

>>> df_cleaned = clean_columns(df_original)
>>> df_cleaned.columns
Index(['EnNo', 'Name', 'DateTime'], dtype='object')
```

---

### `parse_datetime(df: pd.DataFrame) -> pd.DataFrame`

**Converte coluna DateTime para tipo datetime64[ns].**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame com coluna "DateTime" em formato string

**Retorno**: `pd.DataFrame` — Cópia com DateTime como datetime64[ns]

**Formato esperado**: `"%Y/%m/%d %H:%M:%S"` (ex: `2000/05/28 10:51:39`)

**Erros**: `ValueError` se alguma linha não conseguir parsear

**Exemplo**:
```python
>>> df["DateTime"].dtype
object

>>> df_parsed = parse_datetime(df)
>>> df_parsed["DateTime"].dtype
datetime64[ns]

>>> df_parsed["DateTime"][0]
Timestamp('2000-05-28 10:51:39')
```

---

### `clean_names(df: pd.DataFrame) -> pd.DataFrame`

**Padroniza coluna Name: remove espaços + Title Case.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame com coluna "Name"

**Retorno**: `pd.DataFrame` — Cópia com Name padronizado

**Transformações**:
1. `.str.strip()` — Remove espaços início/fim
2. `.str.title()` — Converte para Title Case

**Exemplo**:
```python
>>> df["Name"].unique()
array(['usuario 1 ', '  user 2', 'USER 3'], dtype=object)

>>> df_cleaned = clean_names(df)
>>> df_cleaned["Name"].unique()
array(['Usuario 1', 'User 2', 'User 3'], dtype=object)
   # ↑ Sem espaços, Title Case
```

---

### `transform_level1(df: pd.DataFrame) -> pd.DataFrame`

**Orquestrador da Fase 2: aplica as 3 transformações de limpeza.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame bruto

**Retorno**: `pd.DataFrame` — Limpo e padronizado

**Fluxo interno**:
1. `clean_columns()` — Remove No, TMNo, GMNo, Mode
2. `parse_datetime()` — Converte DateTime para datetime64[ns]
3. `clean_names()` — Strip + Title Case em Name

**Exemplo**:
```python
>>> df_raw = load_raw_log()
>>> df_clean = transform_level1(df_raw)

>>> df_raw.columns
Index(['No', 'TMNo', 'EnNo', 'Name', 'GMNo', 'Mode', 'DateTime'], dtype='object')

>>> df_clean.columns
Index(['EnNo', 'Name', 'DateTime'], dtype='object')

>>> df_raw["DateTime"].dtype
object

>>> df_clean["DateTime"].dtype
datetime64[ns]
```

---

## Fase 3: Anti-Spam

### `identify_employee(df: pd.DataFrame) -> pd.DataFrame`

**Cria coluna "Employee" combinando EnNo + Name para agrupamento único.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame com colunas "EnNo" e "Name"

**Retorno**: `pd.DataFrame` — Cópia com coluna "Employee" adicionada

**Formato de Employee**: `"{EnNo}_{Name}"` (ex: `"1_Usuario 1"`, `"2_Usuario 2"`)

**Nota**: Coluna "Employee" é intermediária, normalmente removida após groupby

**Exemplo**:
```python
>>> df[["EnNo", "Name"]].head()
   EnNo         Name
0     1   Usuario 1
1     1   Usuario 1
2     2   Usuario 2

>>> df_identified = identify_employee(df)
>>> df_identified["Employee"].head()
0    1_Usuario 1
1    1_Usuario 1
2    2_Usuario 2
Name: Employee, dtype: object
```

---

### `apply_anti_spam_rule(df: pd.DataFrame, min_gap_minutes: int = 5) -> pd.DataFrame`

**Remove batidas duplicadas (gap < min_gap_minutes do mesmo funcionário).**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame com colunas "EnNo", "Name", "DateTime"
- `min_gap_minutes` (int, padrão=5) — Gap mínimo em minutos entre batidas legítimas

**Retorno**: `pd.DataFrame` — Filtrado (sem duplicatas), coluna "Employee" removida

**Lógica**:
1. Cria coluna "Employee" (EnNo_Name)
2. Agrupa por Employee
3. Para cada grupo, ordena por DateTime
4. Itera e mantém apenas batidas com gap >= min_gap_minutes da anterior
5. Remove coluna "Employee" e retorna resultado

**Exemplo**:
```python
# Input: 3 batidas do employee "1_Usuario 1"
>>> df
   EnNo         Name            DateTime
0     1   Usuario 1  2000-05-28 10:00:00
1     1   Usuario 1  2000-05-28 10:03:00  ← gap 3 min (SPAM)
2     1   Usuario 1  2000-05-28 10:10:00

>>> df_filtered = apply_anti_spam_rule(df, min_gap_minutes=5)
>>> df_filtered
   EnNo         Name            DateTime
0     1   Usuario 1  2000-05-28 10:00:00
1     1   Usuario 1  2000-05-28 10:10:00
   # ↑ 10:03:00 removida (gap < 5 min)

>>> len(df_filtered)
2  # de 3 → 2 linhas
```

---

### `transform_level2(df: pd.DataFrame) -> pd.DataFrame`

**Orquestrador da Fase 3: aplica regra anti-spam.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame limpo (do `transform_level1()`)

**Retorno**: `pd.DataFrame` — Filtrado (sem duplicatas)

**Fluxo interno**:
- Chama `apply_anti_spam_rule(df, min_gap_minutes=5)`

**Exemplo**:
```python
>>> df_raw = load_raw_log()
>>> df_clean = transform_level1(df_raw)
>>> df_filtered = transform_level2(df_clean)

>>> print(f"Antes: {len(df_clean)} linhas")
Antes: 7744 linhas

>>> print(f"Depois: {len(df_filtered)} linhas")
Depois: 7200 linhas
   # ~544 linhas removidas como spam
```

---

## Fase 4: Hierarquia Temporal

### `extract_temporal_keys(df: pd.DataFrame) -> pd.DataFrame`

**Extrai Year, Month e Day a partir de DateTime com zero-padding.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame com coluna `DateTime` em datetime64[ns]

**Retorno**: `pd.DataFrame` — Cópia com colunas `Year`, `Month` e `Day`

**Formato das chaves**:
- `Year` como `"2000"`
- `Month` como `"05"`
- `Day` como `"28"`

---

### `build_hierarchy(df: pd.DataFrame) -> dict`

**Monta a estrutura Ano -> Mês -> Dia -> Funcionário -> horários.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame com colunas `EnNo`, `Name`, `DateTime`, `Year`, `Month`, `Day`

**Retorno**: `dict` — Hierarquia aninhada

**Regras**:
- Datas e funcionários são ordenados explicitamente
- Horários são formatados como `HH:MM:SS`
- Se o DataFrame estiver vazio, retorna `{}`

---

### `transform_level3(df: pd.DataFrame) -> dict`

**Orquestrador da Fase 4: extrai chaves temporais e monta a hierarquia.**

**Parâmetros**:
- `df` (pd.DataFrame) — DataFrame pós anti-spam

**Retorno**: `dict` — Hierarquia pronta para exibição ou persistência

**Exemplo**:
```python
>>> hierarchy = transform_level3(filtered)
>>> hierarchy["2000"]["05"]["28"]
{"1_Usuario 1": ["10:51:39"], "2_Usuario 2": ["11:00:00"]}
```

---

## Uso Prático

### Pipeline Completo (Fase 1-3)

```python
from src.main import load_raw_log, transform_level1, transform_level2

# Extração
raw = load_raw_log()
print(f"Raw: {raw.shape}")  # (7744, 7)

# Limpeza
cleaned = transform_level1(raw)
print(f"Cleaned: {cleaned.shape}")  # (7744, 3)
print(cleaned.columns)  # Index(['EnNo', 'Name', 'DateTime'])

# Anti-spam
filtered = transform_level2(cleaned)
print(f"Filtered: {filtered.shape}")  # (7200, 3)

print(f"Spam removido: {len(cleaned) - len(filtered)} linhas")  # 544
```

### Uso Interativo

```python
import pandas as pd
from src.main import load_raw_log, parse_datetime

df = load_raw_log()

# Inspecionar tipos
print(df.dtypes)
print(df.head())

# Único funcionário
unique_names = df["Name"].unique()
print(f"Funcionários: {len(unique_names)}")

# Período de dados
df_parsed = parse_datetime(df)
print(f"Período: {df_parsed['DateTime'].min()} até {df_parsed['DateTime'].max()}")
```

---

## Performance & Limites

| Operação | Dados | Tempo |
|----------|-------|-------|
| `load_raw_log()` | 7744 linhas | ~1s |
| `clean_columns()` | 7744 linhas | <1ms |
| `parse_datetime()` | 7744 linhas | ~50ms |
| `clean_names()` | 7744 linhas | ~30ms |
| `apply_anti_spam_rule()` | 7744 linhas | ~500ms |
| **Pipeline completo** | 7744 linhas | ~2s |

---

**Última atualização**: 2 de maio de 2026
