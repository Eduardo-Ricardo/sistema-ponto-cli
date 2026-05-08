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

Cada transformação é uma função isolada em seu módulo:
- [src/extraction.py](../../src/extraction.py): `resolve_raw_file_path()`, `load_raw_log()`
- [src/cleaning.py](../../src/cleaning.py): `clean_columns()`, `parse_datetime()`, `clean_names()`
- [src/rules/anti_spam.py](../../src/rules/anti_spam.py): `identify_employee()`, `apply_anti_spam_rule()`

**Vantagem**: Testável isoladamente, reutilizável, fácil de debugar.

### 2. Orquestração Clara

**Cada "nível" de transformação tem um orquestrador**:
- `transform_level1(df)` — Encadeia as 3 funções de limpeza
- `transform_level2(df)` — Encadeia funções de anti-spam
- `transform_level3(df)` — (Futuro) Encadeia hierarquia

**Vantagem**: Fácil ver o fluxo completo, mudar ordem de operações, adicionar novos passos.

### 3. Imutabilidade Local

Cada função retorna um novo `DataFrame`, não modifica in-place. Ver implementações em [src/cleaning.py](../../src/cleaning.py) e [src/rules/anti_spam.py](../../src/rules/anti_spam.py).

**Vantagem**: Sem efeitos colaterais, fácil debugar, seguro para testes paralelos.

### 4. Composição Over Herança

Funções se combinam naturalmente: ver [src/main.py](../../src/main.py) (`main()`) e orquestradores em [src/main.py](../../src/main.py).

**Vantagem**: Zero overhead, código explícito e linear.

## Decisões de Design

### Encoding: Fallback Triplo

Tenta encodings em sequência: utf-8-sig → cp1252 → latin1. Ver [src/extraction.py](../../src/extraction.py).

**Por quê**: Relógios de ponto físicos salvam em múltiplos encodings. Fallback garante robustez.

### Identificação de Funcionário: String Composta

Combina `EnNo` + `Name` em formato chave única. Ver [src/rules/anti_spam.py](../../src/rules/anti_spam.py) (`identify_employee()`).

**Por quê**: Duas chaves naturais: EnNo (ID do equipamento) + Name (nome). String é simples para groupby/join.

### Anti-Spam: Gap Mínimo de 5 Minutos

Remove batidas consecutivas com intervalo < 5 minutos. Ver [src/rules/anti_spam.py](../../src/rules/anti_spam.py) (`apply_anti_spam_rule()`).

**Por quê**: Regra de negócio. Ninguém pode legitimamente bater duas vezes em menos de 5 minutos.

### Separador: Tabulação (\t)

Arquivo bruto usa tab como separador. Ver [src/extraction.py](../../src/extraction.py) (`load_raw_log()`).

**Por quê**: Formato padrão de relógio de ponto AGLogic. Garante que nomes com espaços não quebrem.

**Para ver o fluxo de transformação detalhado em cada fase** (input, transformações, output), consulte [PHASES.md](PHASES.md).

## Extensibilidade

Para adicionar nova transformação:

1. Criar função isolada no módulo apropriado
2. Adicionar testes em `tests/test_level_X.py`
3. Integrar no orquestrador correspondente (`transform_levelX`)
4. Atualizar `main()` e docstring

Ver padrão em [src/cleaning.py](../../src/cleaning.py) e [src/rules/anti_spam.py](../../src/rules/anti_spam.py).

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
