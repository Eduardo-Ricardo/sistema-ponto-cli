# 🏗️ Arquitetura

Padrão arquitetural, princípios de design e decisões técnicas.

## Padrão: Modular ETL Pipeline

**Escolha**: Rejeitar MVC/padrões convencionais em favor de um pipeline funcional estrito.

**Razão**: Pipelines de dados fazem transformações sequenciais e isoladas. Fácil de testar, debugar e estender.

**Estrutura**:

```
entrada (raw TXT)
    ↓
    resolver_caminho()
    ↓
    carregar_bruto()
    ↓
    [FASE 1: limpar_colunas → parse_datetime → limpar_nomes]
    ↓
    [FASE 2: identificar_employee → aplicar_anti_spam]
    ↓
    [FASE 3: extrair_hierarquia]
    ↓
    [FASE 4: exportar_json]
    ↓
    saída (JSON estruturado)
```

## Princípios

### 1. Modularidade Estrita

**Cada transformação é uma função isolada**:
- `clean_columns(df)` — Remove colunas inúteis
- `parse_datetime(df)` — Converte tipos
- `clean_names(df)` — Padroniza strings
- `apply_anti_spam_rule(df)` — Remove duplicatas

**Vantagem**: Testável isoladamente, reutilizável, fácil de debugar.

### 2. Orquestração Clara

**Cada "nível" de transformação tem um orquestrador**:
- `transform_level1(df)` — Encadeia as 3 funções de limpeza
- `transform_level2(df)` — Encadeia funções de anti-spam
- `transform_level3(df)` — (Futuro) Encadeia hierarquia

**Vantagem**: Fácil ver o fluxo completo, mudar ordem de operações, adicionar novos passos.

### 3. Imutabilidade Local

**Cada função retorna um novo DataFrame, não modifica in-place**:

```python
def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_drop = ["No", "TMNo", "GMNo", "Mode"]
    return df.drop(columns=cols_to_drop, errors="ignore")
    # ↑ Retorna novo DataFrame, original intacto
```

**Vantagem**: Sem efeitos colaterais, fácil debugar, seguro para testes paralelos.

### 4. Composição Over Herança

**Funções se combinam naturalmente, sem precisar de base classes**:

```python
# Fase 2: combinar extração de employee + anti-spam
df = identify_employee(df)  # Adiciona coluna "Employee"
df = apply_anti_spam_rule(df)  # Filtra e remove coluna "Employee"
```

**Vantagem**: Zero overhead, código explícito e linear.

## Decisões de Design

### Encoding: Fallback Triplo

```python
RAW_ENCODINGS = ("utf-8-sig", "cp1252", "latin1")

for encoding in RAW_ENCODINGS:
    try:
        return pd.read_csv(file_path, sep="\t", encoding=encoding)
    except UnicodeDecodeError:
        continue
```

**Por quê**: Relógios de ponto físicos salvam em múltiplos encodings dependendo da origem. Fallback silencioso garante robustez.

### Identificação de Funcionário: String Composta

```python
df["Employee"] = df["EnNo"].astype(str) + "_" + df["Name"]
# Exemplo: "1_usuario 1", "2_usuario 2"
```

**Por quê**: Duas chaves naturais: EnNo (ID do equipamento) + Name (nome). String é simples para groupby/join, mais fácil que tupla.

### Anti-Spam: Gap Mínimo de 5 Minutos

```python
def apply_anti_spam_rule(df, min_gap_minutes: int = 5):
    # Se duas batidas do mesmo employee ocorrem < 5 min apart,
    # a segunda é descartada (presumidamente acidental)
```

**Por quê**: Regra de negócio. Mesmo que rápido, alguém não pode "bater" duas vezes em < 5 min de forma legítima.

### Separador: Tabulação (\t)

```python
pd.read_csv(file_path, sep="\t", encoding=encoding)
```

**Por quê**: Formato padrão de relógio de ponto (equipamento AGLogic). Tabulação garante que nomes com espaços não quebrem.

**Para ver o fluxo de transformação detalhado em cada fase** (input, transformações, output), consulte [PHASES.md](PHASES.md).

## Extensibilidade

**Para adicionar nova transformação**:

1. Criar função isolada:
```python
def nova_transformacao(df: pd.DataFrame) -> pd.DataFrame:
    """Descrição breve."""
    df = df.copy()
    # lógica
    return df
```

2. Adicionar testes em `tests/test_level_X.py`

3. Integrar no orquestrador:
```python
def transform_levelX(df: pd.DataFrame) -> pd.DataFrame:
    df = outra_transformacao(df)
    df = nova_transformacao(df)  # ← no lugar certo
    return df
```

4. Atualizar `main()` e docstring do módulo

**Zero refatoração necessária**.

## Performance

- **Extração**: ~1s para 7744+ linhas (AGL_001.TXT real)
- **Limpeza L1**: <100ms (drop colunas + type casting)
- **Anti-Spam**: ~500ms (groupby + iteração)
- **Total**: ~2s para processamento completo

Gargalo atual: iteração no `apply_anti_spam_rule` (groupby com loop). Possível otimizar com vectorização se necessário em Fase 4+.

## Testes

**Estratégia**: Cada função tem teste isolado + teste de pipeline completo.

Ver [TESTING.md](TESTING.md) para cobertura e casos de teste.

---

**Resumo**: Pipeline modular, isolado, testável. Fácil de estender. Sem frameworks desnecessários.
