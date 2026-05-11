# 📋 Fases do ETL

Detalhamento de cada uma das 5 fases, objetivo, implementação e status.

## Fase 0: Setup Inicial ✅

**Objetivo**: Infraestrutura, decisões arquiteturais, repo limpo.

**Tarefas**:
- [x] Definir arquitetura do pipeline
- [x] Estruturar pastas (data/, src/, tests/, docs/)
- [x] Inicializar Git com README e .gitignore
- [x] Configurar requirements.txt

**Resultado**: Repositório pronto, documentação base.

**Status**: ✅ **COMPLETO**

---

## Fase 1: Extração (Extract) ✅

**Objetivo**: Ler arquivo TXT bruto com tratamento robusto de encoding.

**Input**: `data/raw/AGL_001.TXT` ou `./AGL_001.TXT`

**Output**: DataFrame pandas com 7 colunas (No, TMNo, EnNo, Name, GMNo, Mode, DateTime)

### Funções Implementadas

```python
def resolve_raw_file_path(raw_file: str | Path | None = None) -> Path:
    """Localiza arquivo bruto com fallback automático."""
    # Tenta data/raw/AGL_001.TXT → fallback ./AGL_001.TXT
    # Lança FileNotFoundError se não encontrar

def load_raw_log(raw_file: str | Path | None = None) -> pd.DataFrame:
    """Carrega TXT com fallback de encoding."""
    # Tenta: utf-8-sig → cp1252 → latin1
    # Usa separador \t
    # Lança UnicodeDecodeError se nenhum encoding funciona
```

### Testes (2 testes ✅)

- `test_resolve_raw_file_path_fixture()` — Arquivo encontrado, path retornado
- `test_load_raw_log_columns_and_datetime()` — 7 colunas, ~7744 linhas, 1º datetime válido

**Resultado**: 2/2 testes passando em 0.36s

**Status**: ✅ **COMPLETO**

**Commit**: `Fase 1: extração — loader e docstrings`

---

## Fase 2: Transformação Nível 1 (Limpeza) ✅

**Objetivo**: Padronizar tipos e remover colunas inúteis.

**Input**: DataFrame bruto (7 colunas)

**Output**: DataFrame limpo (4 colunas: EnNo, Name, DateTime, ...)

### Funções Implementadas

```python
def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove colunas inúteis: No, TMNo, GMNo, Mode."""
    return df.drop(columns=["No", "TMNo", "GMNo", "Mode"], errors="ignore")

def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Converte DateTime para datetime64[ns]."""
    df["DateTime"] = pd.to_datetime(
        df["DateTime"], 
        format="%Y/%m/%d %H:%M:%S"
    )
    return df

def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza Name: strip + Title Case."""
    df["Name"] = df["Name"].str.strip().str.title()
    return df

def transform_level1(df: pd.DataFrame) -> pd.DataFrame:
    """Orquestrador: limpa colunas → parse datetime → padroniza names."""
    df = clean_columns(df)
    df = parse_datetime(df)
    df = clean_names(df)
    return df
```

### Testes (4 testes ✅)

- `test_clean_columns()` — No, TMNo, GMNo, Mode removidas
- `test_parse_datetime()` — DateTime é datetime64[ns]
- `test_clean_names()` — Names sem espaços, Title Case
- `test_transform_level1_pipeline()` — Pipeline completo

**Resultado**: 4/4 testes passando em 0.45s

**Status**: ✅ **COMPLETO**

**Commit**: `Fase 2: limpeza estrutural — aplicar transformações nível 1`

---

## Fase 3: Transformação Nível 2 (Anti-Spam) ✅

**Objetivo**: Remover duplicatas ("duplos cliques" < 5 min apart).

**Input**: DataFrame limpo (do `transform_level1()`)

**Output**: DataFrame filtrado (sem duplicatas)

### Funções Implementadas

```python
def identify_employee(df: pd.DataFrame) -> pd.DataFrame:
    """Cria coluna Employee = 'EnNo_Name' para agrupamento."""
    df["Employee"] = df["EnNo"].astype(str) + "_" + df["Name"]
    return df

def apply_anti_spam_rule(
    df: pd.DataFrame, 
    min_gap_minutes: int = 5
) -> pd.DataFrame:
    """Remove batidas consecutivas com gap < min_gap_minutes."""
    # 1. Identifica todo employee
    # 2. Agrupa por Employee, ordena por DateTime
    # 3. Para cada grupo, mantém apenas batidas com gap >= 5 min
    # 4. Remove coluna Employee antes de retornar
    
def transform_level2(df: pd.DataFrame) -> pd.DataFrame:
    """Orquestrador: aplica regra anti-spam."""
    return apply_anti_spam_rule(df, min_gap_minutes=5)
```

### Exemplo

**Input**:
```
EnNo | Name      | DateTime
1    | Usuario 1 | 10:00:00
1    | Usuario 1 | 10:03:00 ← gap 3 min < 5 min (SPAM)
1    | Usuario 1 | 10:10:00
2    | Usuario 2 | 08:05:00
2    | Usuario 2 | 08:06:00 ← gap 1 min < 5 min (SPAM)
```

**Output**:
```
EnNo | Name      | DateTime
1    | Usuario 1 | 10:00:00
1    | Usuario 1 | 10:10:00 ← 10:03:00 removida
2    | Usuario 2 | 08:05:00 ← 08:06:00 removida
```

### Testes Planejados (5 testes)

- `test_identify_employee()` — Coluna Employee criada corretamente
- `test_apply_anti_spam_rule_consecutive_duplicates()` — Remove spam (gap < 5 min)
- `test_apply_anti_spam_rule_preserves_valid_batidas()` — Preserva batidas válidas (gap >= 5)
- `test_apply_anti_spam_rule_multiple_employees()` — Múltiplos employees não interferem
- `test_transform_level2_full_pipeline()` — Pipeline L1 + L2 completo

**Resultado**: 5/5 testes passando em 0.42s

**Status**: ✅ **COMPLETO** — Código em [src/rules/anti_spam.py](../../src/rules/anti_spam.py), testes em [tests/test_level2_anti_spam.py](../../tests/test_level2_anti_spam.py)

**Commit**: Incluído em `refactor/modularize` (modularizar + renomear + limpar)

---

## Fase 4: Transformação Nível 3 (Hierarquia) [ ]

**Objetivo**: Estruturar dados em hierarquia temporal: Ano → Mês → Dia → Funcionário → [Horários]

**Input**: DataFrame anti-spam (do `transform_level2()`)

**Output**: Dicionário aninhado com estrutura hierárquica

### Funções Implementadas

- `extract_temporal_keys(df)` — extrai Year, Month, Day
- `build_hierarchy(df)` — constrói estrutura aninhada
- `transform_level3(df)` — orquestrador

### Testes

- `test_extract_temporal_keys()` — extração de chaves temporais
- `test_build_hierarchy()` — estrutura aninhada correta
- `test_hierarchy_sorted()` — horários ordenados cronologicamente
- `test_transform_level3_full_pipeline()` — pipeline completo L1+L2+L3

**Status**: ✅ **COMPLETO** — Implementado em [src/rules/hierarchy.py](../../src/rules/hierarchy.py)

---

## Fase 5: Carga (Load) [ ]

**Objetivo**: Exportar hierarquia estruturada para arquivo JSON.

**Input**: Dicionário hierárquico (do `transform_level3()`)

**Output**: `data/processed/dados_ponto.json`

### Funções Planejadas

- `export_to_json(hierarchy, output_path)` — serializa hierarquia para JSON

### Testes Planejados

- `test_export_to_json()` — arquivo criado, JSON válido
- `test_export_path_creation()` — diretórios criados automaticamente
- `test_json_content_matches_hierarchy()` — conteúdo bate com input

**Status**: [ ] **NÃO INICIADO** — Planejado após Fase 4

---

## Roadmap Visual

```
Fase 0 (Setup)
    ↓ [✅ COMPLETO]
Fase 1 (Extração)
    ↓ [✅ COMPLETO]
Fase 2 (Limpeza)
    ↓ [✅ COMPLETO]
Fase 3 (Anti-Spam)
    ↓ [✅ COMPLETO]
Fase 4 (Hierarquia)
    ↓ [✅ COMPLETO]
Fase 5 (Carga JSON)
    ↓ [ ] NÃO INICIADO
FINAL: dados_ponto.json
```

---

## Métricas

| Fase | Funções | Testes | Status | Commits |
|------|---------|--------|--------|---------|
| 0 | 0 | 0 | ✅ | 1 |
| 1 | 2 | 2 | ✅ | 2 |
| 2 | 4 | 4 | ✅ | 2 |
| 3 | 3 | 5 | ✅ | 4 (refactor/modularize) |
| 4 | 3 | 4 | ✅ | 1 |
| 5 | 1 | 3 | [ ] | 0 |
| **TOTAL** | **13** | **18** | — | **10** |

---

**Última atualização**: 11 de maio de 2026
