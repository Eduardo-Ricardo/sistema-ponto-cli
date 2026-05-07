# 📚 Documentação — Sistema Ponto CLI

Documentação técnica do pipeline ETL de processamento de logs de relógio de ponto eletrônico.

## Índice Rápido

| Documento | Conteúdo |
|-----------|----------|
| [QUICK_START.md](QUICK_START.md) | Setup, primeiro teste, comandos básicos |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Padrão arquitetural, decisões de design |
| [PHASES.md](PHASES.md) | Detalhamento de cada fase do ETL (1-5) |
| [API.md](API.md) | Referência completa de funções públicas |
| [TESTING.md](TESTING.md) | Estratégia de testes, como rodar, cobertura |
| [GIT_WORKFLOW.md](GIT_WORKFLOW.md) | Git Flow, branches, commits, merges |

## Overview

**O que é**: Pipeline ETL que transforma logs brutos de relógio de ponto (TXT) em dados estruturados e limpos.

**Por que**: Remover duplicatas de leitura ("duplos cliques"), padronizar dados e organizar em hierarquia temporal para cálculos de folha.

**Input**: `data/raw/AGL_001.TXT` (tab-delimitado, múltiplos encodings)

**Output**: `data/processed/dados_ponto.json` (hierarquia ano/mês/funcionário/data)

## Fases (1-5)

1. **Extração** — Ler TXT bruto com tratamento de encoding ✅
2. **Limpeza L1** — Drop colunas, type casting, padronização de strings ✅
3. **Anti-Spam** — Remover duplicatas (gap < 5 min) 🚧
4. **Hierarquia** — Estruturar em árvore temporal [ ]
5. **Carga** — Exportar JSON final [ ]

## Stack

- **Python 3.12.1**
- **pandas 3.0.2** — Manipulação de dados
- **pytest 9.0.3** — Testes
- **Git Flow** — Versionamento (branches isoladas por fase)

## Status Atual

- ✅ **Fase 0+1+2**: Completa com testes passando
- 🚧 **Fase 3**: Código pronto, documentação em progresso
- [ ] **Fase 4+5**: Planejadas

Veja [PHASES.md](PHASES.md) para status detalhado de cada etapa.
