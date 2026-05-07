import sys
from pathlib import Path
import pandas as pd
import shutil
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from etl_pipeline import load_raw_log, transform_level1, identify_employee, apply_anti_spam_rule, transform_level2


def test_identify_employee(tmp_path):
    """Valida que coluna Employee é criada corretamente (EnNo_Name)."""
    src = Path("tests/fixtures/sample_agl.txt")
    dest = tmp_path / "sample_agl.txt"
    shutil.copy(src, dest)
    
    df = load_raw_log(dest)
    identified = identify_employee(df)
    
    assert "Employee" in identified.columns
    # Verifica formato "EnNo_Name"
    for emp in identified["Employee"]:
        assert "_" in emp
        parts = emp.split("_")
        assert len(parts) == 2


def test_apply_anti_spam_rule_consecutive_duplicates(tmp_path):
    """Valida remoção de duplicatas (gap < 5 min)."""
    # Criar fixture com 2 batidas do mesmo employee, gap = 3 min
    fixture_content = """EnNo	Name	DateTime
1	Usuario 1	2000/05/28 10:00:00
1	Usuario 1	2000/05/28 10:03:00
"""
    
    dest = tmp_path / "fixture_duplicates.txt"
    dest.write_text(fixture_content)
    
    df = load_raw_log(dest)
    df = transform_level1(df)
    filtered = apply_anti_spam_rule(df, min_gap_minutes=5)
    
    # Esperado: apenas 1 linha (segunda removida)
    assert len(filtered) == 1
    assert filtered.iloc[0]["DateTime"].hour == 10
    assert filtered.iloc[0]["DateTime"].minute == 0


def test_apply_anti_spam_rule_preserves_valid_batidas(tmp_path):
    """Valida preservação de batidas com gap >= 5 min."""
    # Criar fixture com 2 batidas do mesmo employee, gap = 10 min
    fixture_content = """EnNo	Name	DateTime
1	Usuario 1	2000/05/28 10:00:00
1	Usuario 1	2000/05/28 10:10:00
"""
    
    dest = tmp_path / "fixture_valid.txt"
    dest.write_text(fixture_content)
    
    df = load_raw_log(dest)
    df = transform_level1(df)
    filtered = apply_anti_spam_rule(df, min_gap_minutes=5)
    
    # Esperado: 2 linhas (ambas preservadas)
    assert len(filtered) == 2
    assert filtered.iloc[0]["DateTime"].minute == 0
    assert filtered.iloc[1]["DateTime"].minute == 10


def test_apply_anti_spam_rule_multiple_employees(tmp_path):
    """Valida comportamento correto com múltiplos funcionários."""
    # Fixture com múltiplos employees e mix de gaps
    fixture_content = """EnNo	Name	DateTime
1	Usuario 1	2000/05/28 08:00:00
1	Usuario 1	2000/05/28 08:02:00
1	Usuario 1	2000/05/28 08:10:00
2	Usuario 2	2000/05/28 08:05:00
2	Usuario 2	2000/05/28 08:06:00
"""
    
    dest = tmp_path / "fixture_mixed.txt"
    dest.write_text(fixture_content)
    
    df = load_raw_log(dest)
    df = transform_level1(df)
    filtered = apply_anti_spam_rule(df, min_gap_minutes=5)
    
    # Esperado: 4 linhas (Usuario 1: 08:00 + 08:10; Usuario 2: 08:05)
    # Usuario 1 08:02 removida (gap 2 min < 5)
    # Usuario 2 08:06 removida (gap 1 min < 5)
    assert len(filtered) == 3


def test_transform_level2_full_pipeline(tmp_path):
    """Valida pipeline completo L1 + L2."""
    src = Path("tests/fixtures/sample_agl.txt")
    dest = tmp_path / "sample_agl.txt"
    shutil.copy(src, dest)
    
    df = load_raw_log(dest)
    cleaned = transform_level1(df)
    filtered = transform_level2(cleaned)
    
    # Validações:
    # 1. Colunas removidas em L1
    assert "No" not in filtered.columns
    assert "Mode" not in filtered.columns
    # 2. DateTime convertido
    assert pd.api.types.is_datetime64_any_dtype(filtered["DateTime"])
    # 3. Names padronizados
    for name in filtered["Name"]:
        assert name == name.strip().title()
    # 4. Sem coluna Employee (deve ser removida em apply_anti_spam_rule)
    assert "Employee" not in filtered.columns
    # 5. Linhas preservadas ou reduzidas (não aumentadas)
    assert len(filtered) <= len(df)
