# 📊 Sistema Ponto CLI — ETL de Relógio Eletrônico

Pipeline ETL que transforma logs brutos de relógio de ponto em dados estruturados e limpos.

## ⚡ Quick Links

- 🚀 **[Quick Start](docs/QUICK_START.md)** — Setup e primeiro teste em 2 minutos
- 📚 **[Documentação Completa](docs/README.md)** — Índice de todos os guias
- 🏗️ **[Arquitetura](docs/ARCHITECTURE.md)** — Padrão de design e princípios
- 📋 **[Fases (1-5)](docs/PHASES.md)** — Detalhamento de cada etapa do ETL
- 🔧 **[API Reference](docs/API.md)** — Todas as funções públicas
- 🧪 **[Testing Guide](docs/TESTING.md)** — Estratégia de testes
- 🔀 **[Git Workflow](docs/GIT_WORKFLOW.md)** — Branches, commits, merges

## O que faz?

**Input**: `data/raw/AGL_001.TXT` (tab-delimitado, ~7744 linhas)
```
No | TMNo | EnNo | Name       | GMNo | Mode | DateTime
1  | 1    | 1    | usuario 1  | 0    | 1    | 2000/05/28 10:51:39
2  | 1    | 1    | usuario 1  | 0    | 1    | 2000/05/28 10:51:46  ← duplicata
```

**Output**: `data/processed/dados_ponto.json` (hierarquia limpa)
```json
{
  "2000": {
    "05": {
      "28": {
        "1_Usuario 1": ["10:51:39"],
        "2_Usuario 2": ["11:00:00"]
      }
    }
  }
}
```

## Status

- ✅ **Fase 1** (Extração) — Completo
- ✅ **Fase 2** (Limpeza L1) — Completo
- ✅ **Fase 3** (Anti-Spam) — Completo (11 testes passando)
- [ ] **Fase 4** (Hierarquia) — Planejado
- [ ] **Fase 5** (Carga JSON) — Planejado

## Setup Rápido

```bash
git clone https://github.com/Eduardo-Ricardo/sistema-ponto-cli.git
cd sistema-ponto-cli
pip install -r requirements.txt
pytest -v
python src/main.py
```

---

## Estrutura

## Estrutura

```
sistema-ponto-cli/
├── data/
│   ├── raw/                  # Input: AGL_001.TXT bruto
│   └── processed/            # Output: dados_ponto.json (Fase 5)
├── src/
│   ├── main.py               # Fachada do pipeline ETL
│   ├── extraction.py         # Módulo de leitura (Fase 1)
│   ├── cleaning.py           # Módulo de limpeza (Fase 2)
│   ├── rules/
│   │   ├── __init__.py
│   │   └── anti_spam.py      # Módulo anti-spam (Fase 3)
│   ├── utils.py              # Utilitários
│   └── __init__.py
├── tests/
│   ├── test_extraction.py           # Testes Fase 1 (2 testes ✅)
│   ├── test_level1_cleaning.py      # Testes Fase 2 (4 testes ✅)
│   ├── test_level2_anti_spam.py     # Testes Fase 3 (5 testes 🚧)
│   └── fixtures/sample_agl.txt      # Fixture reutilizável
├── docs/
│   ├── README.md             # Índice da documentação
│   ├── QUICK_START.md        # Setup em 2 minutos
│   ├── ARCHITECTURE.md       # Padrão arquitetural
│   ├── PHASES.md             # Detalhamento das 5 fases
│   ├── API.md                # Referência de funções
│   ├── TESTING.md            # Estratégia de testes
│   └── GIT_WORKFLOW.md       # Branches, commits, merges
├── .gitignore
├── requirements.txt          # pandas, pytest
└── README.md                 # Este arquivo
```

## Tech Stack

- **Python 3.12.1**
- **pandas 3.0.2** — Manipulação de dados tabular
- **pytest 9.0.3** — Testes unitários
- **Git Flow** — Versionamento com feature branches

## Roadmap (Checklist)

### ✅ Completo

- [x] **Fase 0**: Setup, estrutura de pastas, git
- [x] **Fase 1**: Extração com encoding fallback
- [x] **Fase 2**: Limpeza estrutural (drop coluna, type cast, strings)

### 🚧 Em Desenvolvimento

- [ ] **Fase 4**: Hierarquia (estruturar em árvore temporal)
- [ ] **Fase 5**: Carga (exportar JSON final)

**Detalhamento completo**: Ver [docs/PHASES.md](docs/PHASES.md)

## Como Começar

### 1️⃣ Instalar

```bash
pip install -r requirements.txt
```

### 2️⃣ Rodar Testes

```bash
# Testes Fases 1+2 (✅ devem passar)
pytest -v

# Apenas Fase 1
pytest tests/test_extraction.py -v

# Apenas Fase 2
pytest tests/test_level1_cleaning.py -v

# Com coverage
pytest --cov=src tests/
```

### 3️⃣ Rodar Pipeline

```bash
python src/main.py
```

Esperado: `head()` dos dados após Fase 3 (anti-spam aplicado).

### 4️⃣ Ver Documentação

Completa em [docs/README.md](docs/README.md)

## Exemplos Rápidos

### Carregar e Limpar

```python
from src.etl_pipeline import load_raw_log, transform_level1, transform_level2

# Fase 1: Carregar
raw = load_raw_log()  # (7744, 7)

# Fase 2: Limpar
clean = transform_level1(raw)  # (7744, 3)

# Fase 3: Anti-spam
filtered = transform_level2(clean)  # (7200, 3)
```

### Inspecionar Dados

```python
from src.etl_pipeline import load_raw_log

df = load_raw_log()
print(df.info())
print(df.describe())
print(df.head(10))
```

---

## Contribuindo

Siga [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) para branches e commits.

**Checklist rápido**:
- [ ] Feature branch `feature/fase-X-descricao`
- [ ] Testes passando localmente
- [ ] Commits com mensagens claras
- [ ] Push e merge em `main`
- [ ] Atualizar documentação

---

## Troubleshooting

| Erro | Solução |
|------|---------|
| `FileNotFoundError: Raw file not found` | Copiar `AGL_001.TXT` para `data/raw/` ou raiz do projeto |
| `ModuleNotFoundError: No module named 'pandas'` | `pip install -r requirements.txt` |
| Testes falhando | Ver [docs/TESTING.md](docs/TESTING.md#debugging-testes-falhando) |

---

## Status & Métricas

| Métrica | Valor |
|---------|-------|
| Funções públicas | 9 |
| Testes | 11/18 passando (Fases 1-2) |
| Cobertura | ~96% (Fases 1-2) |
| Linhas de código | ~400 |
| Fases completas | 2/5 |

---

**Última atualização**: 2 de maio de 2026

Para mais informações, visite [docs/README.md](docs/README.md)