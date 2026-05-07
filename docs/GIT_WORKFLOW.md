# 🔀 Git Workflow

Padrão de branches, commits, PRs e merges.

## Git Flow

**Modelo**: Feature Branch + Testes + Merge para Main

```
main (produção)
 ↑
 ├── feature/fase-1-extracao (Fase 1)
 │   └── feature/fase-1-tests (Testes Fase 1)
 │
 ├── feature/fase-2-limpeza (Fase 2)
 │   └── feature/fase-2-tests (Testes Fase 2)
 │
 ├── feature/fase-3-anti-spam (Fase 3)
 │   └── feature/fase-3-tests (Testes Fase 3)
 │
 └── feature/fase-4-hierarquia (Fase 4)
     └── feature/fase-4-tests (Testes Fase 4)
```

---

## Branch Naming Convention

**Padrão**: `feature/fase-N-descricao`

| Branch | Propósito |
|--------|-----------|
| `main` | Código de produção, estável, apenas fast-forward merges |
| `feature/fase-N-descricao` | Feature branch da Fase N |
| `feature/fase-N-tests` | Testes da Fase N (opcional, usar se preciso isolação) |

**Exemplos**:
- ✅ `feature/fase-1-extracao`
- ✅ `feature/fase-2-limpeza`
- ✅ `feature/fase-3-anti-spam`
- ❌ `develop` (não usar Git Flow tradicional)
- ❌ `hotfix/*` (manter simples por enquanto)

---

## Commit Message Convention

**Padrão**: `[Tipo]: descrição breve (português)`

### Tipos

| Tipo | Uso |
|------|-----|
| `Fase N` | Implementação da Fase N (código principal) |
| `Testes` | Adicionar/atualizar testes |
| `Roadmap` | Atualizar README/progress |
| `Docs` | Adicionar/atualizar documentação |
| `Fix` | Corrigir bug |

### Exemplos

```
✅ Fase 1: extração — loader e docstrings
✅ Testes: adicionar pytest, fixtures e testes de extração
✅ Roadmap: marcar Fase 0 e Fase 1 como concluídas
✅ Docs: adicionar ARCHITECTURE.md e API.md
✅ Fix: corrigir encoding fallback em load_raw_log
```

**Estrutura completa** (quando aplicável):

```
Tipo: descrição breve

Descrição mais longa (opcional).
- Mudança 1
- Mudança 2

Co-authored-by: (se colaborativo)
```

---

## Workflow Passo-a-Passo

### 1. Criar Feature Branch

```bash
# Partir sempre de main
git checkout main
git pull origin main

# Criar nova branch
git checkout -b feature/fase-3-anti-spam
```

### 2. Implementar & Testar Localmente

```bash
# Editar código
# vim src/etl_pipeline.py

# Rodar testes
pytest -v

# Rodar code completo
python src/etl_pipeline.py
```

### 3. Commit Incremental

```bash
# Verificar mudanças
git status

# Stage seletivo (não git add .)
git add src/etl_pipeline.py
git commit -m "Fase 3: implementar identify_employee e apply_anti_spam_rule"

# Se testes em branch separada
git add tests/test_level2_anti_spam.py
git commit -m "Testes: adicionar testes anti-spam (5 casos)"
```

### 4. Push para Origin

```bash
# Primeira vez (cria remote branch)
git push -u origin feature/fase-3-anti-spam

# Próximas vezes
git push

# Verificar
git branch -a
# * feature/fase-3-anti-spam
#   origin/feature/fase-3-anti-spam
#   main
#   origin/main
```

### 5. Merge em Main (Local-First)

```bash
# Switch para main
git checkout main

# Verificar status
git status
# On branch main
# Your branch is up to date with 'origin/main'.

# Merge (sem criar commit)
git merge --ff-only feature/fase-3-anti-spam
# ou com squash (combinar commits)
git merge --squash feature/fase-3-anti-spam
git commit -m "Fase 3: anti-spam implementation"

# Push para origin
git push origin main

# Verificar
git log --oneline -n 5
```

### 6. PR (Opcional, para Review)

Se quiser PR antes de merge em main:

```bash
# Na branch feature
git push -u origin feature/fase-3-anti-spam

# Abrir PR via GitHub UI:
# https://github.com/Eduardo-Ricardo/sistema-ponto-cli/pull/new/feature/fase-3-anti-spam

# Template PR:
"""
## Fase 3: Anti-Spam

### O que muda?
- 3 novas funções: identify_employee, apply_anti_spam_rule, transform_level2
- 5 novos testes em test_level2_anti_spam.py
- main() atualizado para usar transform_level2()

### Validação
- ✅ 5/5 testes passando
- ✅ Pipeline L1 + L2 testado com fixture
- ✅ Sem erro de encoding

### Ready to merge
"""

# GitHub: Reviewer aprova → Merge (squash)
```

---

## Merging Strategy

### Fast-Forward Merge (Padrão)

```bash
git checkout main
git merge --ff-only feature/fase-3-anti-spam
```

**Quando usar**: Sem conflitos, história linear clara

**Resultado**: Um commit novo em main sem "merge commit"

### Squash Merge (Limpar Histórico)

```bash
git checkout main
git merge --squash feature/fase-3-anti-spam
git commit -m "Fase 3: anti-spam implementation"
```

**Quando usar**: Múltiplos commits pequenos na feature, quer história limpa

**Resultado**: Um único commit em main com todas as mudanças

### Rebase (Para SincronizaçãoAntes de Merge)

```bash
git checkout feature/fase-3-anti-spam
git rebase main

# Se houver conflitos
git rebase --continue
# ou
git rebase --abort

# Depois merge
git checkout main
git merge --ff-only feature/fase-3-anti-spam
```

**Quando usar**: Feature branch ficou desatualizada, quer avoid merge commits

---

## Resolving Conflicts

### Se houver conflito no merge

```bash
git merge feature/fase-3-anti-spam
# CONFLICT (content): Merge conflict in src/etl_pipeline.py

# Ver conflitos
git status
git diff

# Editar arquivo manualmente
# Buscar por <<<<<<< ======= >>>>>>>
# Decidir qual versão manter
```

**Arquivo conflitado exemplo**:

```python
<<<<<<< HEAD (main)
def transform_level2(df):
    return apply_anti_spam_rule(df)
=======
def transform_level2(df):
    result = apply_anti_spam_rule(df)
    return result
>>>>>>> feature/fase-3-anti-spam
```

**Resolver**:

```python
# Manter versão main (HEAD) ou feature, ou combinar
def transform_level2(df):
    result = apply_anti_spam_rule(df)
    return result  # ← combinado
```

**Após resolver**:

```bash
git add src/etl_pipeline.py
git commit -m "Merge branch feature/fase-3-anti-spam (resolve conflict)"
git push origin main
```

---

## Viewing History

### Ver commits

```bash
# Últimos 10 commits
git log --oneline -n 10

# Com branch info
git log --graph --oneline --all -n 15

# De uma branch específica
git log origin/feature/fase-3-anti-spam --oneline
```

### Ver diffs

```bash
# Entre branches
git diff main feature/fase-3-anti-spam

# Entre commits
git diff 79b1e14 ee0a652

# De um arquivo específico
git diff src/etl_pipeline.py
```

### Ver commits por author/date

```bash
# Commits de hoje
git log --since="today" --oneline

# Commits do último commit de merge
git log main..feature/fase-3-anti-spam
```

---

## Common Commands Reference

```bash
# ========== BASICS ==========
git status                          # Ver status
git branch -a                       # Listar todas as branches
git log --oneline -n 15            # Ver últimos 15 commits

# ========== CREATE & SWITCH ==========
git checkout -b feature/nova-fase   # Criar + switch
git checkout main                   # Switch para main
git switch -c feature/nova-fase    # (Git 2.23+) Criar + switch

# ========== STAGE & COMMIT ==========
git add arquivo.py                  # Stage arquivo
git add src/                        # Stage pasta
git add .                           # Stage tudo (evitar!)
git commit -m "Fase 3: descrição"   # Commit
git commit --amend                  # Corrigir último commit

# ========== PUSH & PULL ==========
git push -u origin feature/fase-3   # Push + set upstream
git push                            # Push subsequentes
git pull origin main                # Pull de main
git fetch                           # Baixar sem merge

# ========== MERGE & REBASE ==========
git merge --ff-only feature/fase-3  # FF merge
git merge --squash feature/fase-3   # Squash merge
git rebase main                     # Rebase na main
git merge --abort                   # Cancelar operação

# ========== UNDO ==========
git reset HEAD arquivo.py           # Unstage
git restore arquivo.py              # Descartar mudanças
git revert COMMIT_HASH              # Desfazer commit (novo commit)
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| "Permission denied (publickey)" | Adicionar SSH key ao GitHub |
| "Branch conflicts" | `git merge --abort`, `git rebase --abort`, resolver manual |
| "Esqueci de stagear" | `git commit --amend` depois `git push --force-with-lease` |
| "Errei o commit" | `git reset --soft HEAD~1`, editar, `git commit` |
| "Branch está desatualizada" | `git fetch`, `git rebase origin/main`, `git push --force-with-lease` |
| "Preciso copiar um commit" | `git cherry-pick COMMIT_HASH` |

---

## Best Practices

✅ **DO**:
- Commit frequente (incrementalmente)
- Push diariamente
- Use descrições claras em commits
- Sempre testar antes de merge
- Pull origin/main antes de começar nova feature
- Usar branches isoladas por feature

❌ **DON'T**:
- Giant commits (200+ linhas)
- Commit sem message ou message vaga ("fix", "update")
- Diretamente em main (sempre feature branch)
- Força push em main (`--force` proibido)
- Merge com conflitos não resolvidos
- Commits de debug (`print("TESTE")`)

---

**Última atualização**: 2 de maio de 2026
