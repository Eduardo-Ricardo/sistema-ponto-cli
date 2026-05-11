# ⚡ Quick Start

Setup e primeiros testes em 2 minutos.

## 1. Setup Inicial

```bash
# Clonar repositório
git clone https://github.com/Eduardo-Ricardo/sistema-ponto-cli.git
cd sistema-ponto-cli

# Instalar dependências
python -m pip install -r requirements.txt

# Colocar arquivo de entrada
# Copiar AGL_001.TXT para data/raw/ ou na raiz do projeto
cp /caminho/para/AGL_001.TXT data/raw/  # ou ./
```

## 2. Rodar Testes

```bash
# Todos os testes
pytest -v

# Apenas Fase 1 (Extração)
pytest tests/test_extraction.py -v

# Apenas Fase 2 (Limpeza)
pytest tests/test_level1_cleaning.py -v

# Apenas Fase 3 (Anti-Spam)
pytest tests/test_level2_anti_spam.py -v

# Apenas Fase 4 (Hierarquia)
pytest tests/test_level3_hierarchy.py -v

# Com coverage
pytest --cov=src tests/
```

## 3. Rodar Pipeline

```bash
# Entrypoint: carrega raw → limpa L1 → aplica anti-spam → monta hierarquia
python src/main.py
```

Output esperado: impressão da hierarquia temporal após a Fase 4.

## 4. Estrutura de Pastas

```
sistemaponto-cli/
├── data/
│   ├── raw/              # Input: AGL_001.TXT bruto
│   └── processed/        # Output: dados_ponto.json (quando Fase 5 estiver pronta)
├── src/
│   ├── main.py           # Fachada do pipeline ETL
│   └── __init__.py       # Package marker
├── tests/
│   ├── test_extraction.py           # Testes Fase 1 (2 testes)
│   ├── test_level1_cleaning.py      # Testes Fase 2 (4 testes)
│   ├── test_level2_anti_spam.py     # Testes Fase 3 (5 testes)
│   └── fixtures/
│       └── sample_agl.txt           # Fixture tab-delimitado reutilizável
├── docs/                 # Esta documentação
├── .gitignore
├── requirements.txt
└── README.md             # Índice resumido
```

## 5. Primeiros Comandos

```bash
# Ver status do git
git status

# Ver branches
git branch -a

# Ver histórico das 5 últimas ações
git log --oneline -n 5

# Rodar teste único
pytest tests/test_extraction.py::test_load_raw_log_columns_and_datetime -v

# Ver os dados carregados
python -c "
from src.main import load_raw_log
df = load_raw_log()
print(df.head())
print(f'Shape: {df.shape}')
"
```

## 6. Próximos Passos

- **Para iniciar Fase 5**: Ver [PHASES.md](PHASES.md#fase-5-carga-load-)
- **Para entender arquitetura**: Ver [ARCHITECTURE.md](ARCHITECTURE.md)
- **Para ver referência de funções**: Ver [API.md](API.md)
- **Para contribuir**: Ver [GIT_WORKFLOW.md](GIT_WORKFLOW.md)

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `FileNotFoundError: Raw file not found` | Copiar `AGL_001.TXT` para `data/raw/` ou raiz do projeto |
| `ModuleNotFoundError: No module named 'pandas'` | Rodar `pip install -r requirements.txt` |
| `UnicodeDecodeError` | Verificar encoding do arquivo (padrão: utf-8-sig, cp1252, latin1) |
| Testes falhando | Rodar `pytest -v` para ver detalhes; ver [TESTING.md](TESTING.md) |

---

**Estado**: Pronto para usar! Fases 1-4 completas, Fase 5 em planejamento.
