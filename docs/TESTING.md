# 🧪 Testes & Testing Strategy

Estratégia de testes, cobertura e como rodar.

## Estratégia

### Princípios

1. **Testes Isolados** — Cada função tem teste unitário independente
2. **Testes de Pipeline** — Cada "nível" temteste de integração (L1, L2, L3)
3. **Fixtures Reutilizáveis** — Dados de teste em `tests/fixtures/` 
4. **Fixtures Temp** — Testes usam `tmp_path` para não poluir filesystem
5. **Sem Dados Sensíveis** — Fixtures são mínimas, sintéticas

### Cobertura Esperada

| Fase | Funções | Unitários | Integração | Total |
|------|---------|-----------|------------|-------|
|   1  |    2    |     2     |      0     |   2   |
|   2  |    4    |     3     |      1     |   4   |
|   3  |    3    |     3     |      2     |   5   |
|   4  |    2    |     2     |      2     |   4   |
|   5  |    1    |     1     |      2     |   3   |
| **TOTAL** | **12** | **11** | **7** | **18** |

---

## Running Tests

### Todos os Testes

```bash
# Verbose mode (recomendado para debug)
pytest -v

# Com coverage
pytest --cov=src tests/

# Modo quiet (apenas summary)
pytest -q
```

### Testes por Fase

```bash
# Fase 1 (Extração)
pytest tests/test_extraction.py -v

# Fase 2 (Limpeza)
pytest tests/test_level1_cleaning.py -v

# Fase 3 (Anti-Spam)
pytest tests/test_level2_anti_spam.py -v
```

### Teste Específico

```bash
# Teste único
pytest tests/test_extraction.py::test_load_raw_log_columns_and_datetime -v

# Padrão (wildcard)
pytest -k "parse_datetime" -v
```

### Com Coverage Report

```bash
pytest --cov=src --cov-report=html tests/
# Abre coverage/index.html no navegador
```

---

## Fixtures

### Arquivo: `tests/fixtures/sample_agl.txt`

**Propósito**: Fixture tab-delimitado reutilizável, mimicando estrutura real de AGL_001.TXT

**Conteúdo**:
```
No	TMNo	EnNo	Name	GMNo	Mode	DateTime
1	1	1	usuario 1	0	1	2000/05/28 10:51:39
2	1	1	usuario 1	0	1	2000/05/28 10:51:46
3	1	2	usuario 2	0	1	2000/05/28 11:00:00
```

**3 linhas**:
1. Batida válida (usuario 1, primeira)
2. Batida duplicada (usuario 1, gap 7 seg < 5 min spam)
3. Batida válida de outro usuario

**Reutilização**:
```python
# Todos os testes fazem:
src = Path("tests/fixtures/sample_agl.txt")
dest = tmp_path / "sample_agl.txt"
shutil.copy(src, dest)
df = load_raw_log(dest)
```

---

## Status de Testes por Fase

**Para detalhes completos sobre testes de cada fase** (objetivo, dados, casos testados, arquivos), consulte [PHASES.md](PHASES.md).

**Resumo rápido**:
- **Fase 1 (Extração)**: 2/2 testes passando ✅
- **Fase 2 (Limpeza)**: 4/4 testes passando ✅
- **Fase 3 (Anti-Spam)**: 5/5 testes prontos 🚧
- **Fases 4-5**: Planejadas [ ]

---

## Como Escrever Novo Teste

### Template

```python
import sys
from pathlib import Path
import pandas as pd
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from main import load_raw_log, transform_levelX  # ← import necessário

def test_nova_funcao(tmp_path):
    """Breve descrição do que o teste valida."""
    # 1. Setup: copiar fixture ou criar dados
    src = Path("tests/fixtures/sample_agl.txt")
    dest = tmp_path / "sample_agl.txt"
    shutil.copy(src, dest)
    
    # 2. Executar
    df = load_raw_log(dest)
    resultado = transform_levelX(df)
    
    # 3. Validar
    assert resultado.shape[0] > 0  # tem linhas
    assert "coluna_esperada" in resultado.columns
    assert resultado["coluna_esperada"].dtype == "algum_tipo"
```

### Checklist para Novo Teste

- [ ] Arquivo criado em `tests/test_level*.py`
- [ ] Import correto de `sys, Path, pandas, shutil`
- [ ] `sys.path` manipulado para permitir import de `src/`
- [ ] Função começa com `test_` 
- [ ] Recebe `tmp_path` como argumento (pytest fixture)
- [ ] Usa `tmp_path` para criar dados temporários
- [ ] Ao menos 3 `assert` statements
- [ ] Docstring descrevendo o que testa

---

## Debugging Testes Falhando

### Erro: `ModuleNotFoundError: No module named 'main'`

**Causa**: sys.path não foi adicionado corretamente

**Solução**:
```python
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
```

No topo do arquivo `test_*.py`, ANTES de `from main import ...`

### Erro: `FileNotFoundError: Raw file not found`

**Causa**: Arquivo fixture não está em `tests/fixtures/sample_agl.txt`

**Solução**:
```bash
ls -la tests/fixtures/
# Verificar que sample_agl.txt existe
```

Se não existir:
```bash
cat > tests/fixtures/sample_agl.txt << 'EOF'
No	TMNo	EnNo	Name	GMNo	Mode	DateTime
1	1	1	usuario 1	0	1	2000/05/28 10:51:39
2	1	1	usuario 1	0	1	2000/05/28 10:51:46
3	1	2	usuario 2	0	1	2000/05/28 11:00:00
EOF
```

### Erro: `UnicodeDecodeError`

**Causa**: Encoding do arquivo fixture é inválido

**Solução**: Verificar que `sample_agl.txt` está em UTF-8
```bash
file tests/fixtures/sample_agl.txt
# Deve mostrar "UTF-8 Unicode text"
```

Se necessário, reconverter:
```bash
iconv -f cp1252 -t utf-8 sample_agl.txt -o sample_agl_utf8.txt
mv sample_agl_utf8.txt sample_agl.txt
```

### Erro: `AssertionError` em teste

**Debug**:
```python
# Adicione prints para ver valores reais
print(f"Coluna esperada não encontrada. Colunas: {resultado.columns.tolist()}")
print(f"Shape: {resultado.shape}")
print(f"Dtypes:\n{resultado.dtypes}")
print(f"First row:\n{resultado.head(1)}")
```

Reexecute com `-v -s` para ver output:
```bash
pytest tests/test_FILE.py::test_FUNCTION -v -s
```

---

## Coverage Report

### Gerar HTML Report

```bash
pytest --cov=src --cov-report=html tests/
```

Abre em: `htmlcov/index.html`

### Verificar Coverage %

```bash
pytest --cov=src tests/ --cov-report=term-missing
```

Mostra qual linhas não foram testadas.

### Targets

- **Target**: 90%+ cobertura de `src/main.py`
- **Status Fase 1**: ✅ ~95%
- **Status Fase 2**: ✅ ~98%
- **Status Fase 3**: 🚧 Em progresso

---

## CI/CD (Futuro)

**Quando GitHub Actions for configurado**:

```yaml
# .github/workflows/tests.yml (exemplo)
name: pytest
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest --cov=src tests/
```

---

## Test Data Strategy

### Dado Sintético vs Real

| Tipo | Uso | Vantagem |
|------|-----|----------|
| **Sintético** (fixtures) | Unitários + integração | Rápido, controlado, sem sensibilidade |
| **Real** (AGL_001.TXT) | Manual, exploratório | Reveala edge cases, real-world behavior |

### Cenários Testados

| Cenário | Fixture | Objetivo |
|---------|---------|----------|
| Normal | sample_agl.txt 3 linhas | Fluxo básico, múltiplos employees |
| Duplicatas | 2 linhas same employee, gap 3 min | Anti-spam remove-as |
| Válidas | 2 linhas same employee, gap 10 min | Anti-spam preserva-as |
| Múltiplos | 5 linhas, 2 employees, gaps variados | Sem interferência entre employees |
| Pipeline! | sample_agl.txt completo | L1 → L2 → L3 (quando pronto) |

---

**Última atualização**: 2 de maio de 2026

**Status de Testes**: 10/18 PASSED (Fases 1+2), 5/18 Prontos (Fase 3)
