import sys
from pathlib import Path
import pandas as pd
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from main import load_raw_log, clean_columns, parse_datetime, clean_names, transform_level1


def test_clean_columns(tmp_path):
    src = Path("tests/fixtures/sample_agl.txt")
    dest = tmp_path / "sample_agl.txt"
    shutil.copy(src, dest)
    df = load_raw_log(dest)
    cleaned = clean_columns(df)
    assert "No" not in cleaned.columns
    assert "TMNo" not in cleaned.columns
    assert "GMNo" not in cleaned.columns
    assert "Mode" not in cleaned.columns
    assert "Name" in cleaned.columns


def test_parse_datetime(tmp_path):
    src = Path("tests/fixtures/sample_agl.txt")
    dest = tmp_path / "sample_agl.txt"
    shutil.copy(src, dest)
    df = load_raw_log(dest)
    parsed = parse_datetime(df)
    assert pd.api.types.is_datetime64_any_dtype(parsed["DateTime"])


def test_clean_names(tmp_path):
    src = Path("tests/fixtures/sample_agl.txt")
    dest = tmp_path / "sample_agl.txt"
    shutil.copy(src, dest)
    df = load_raw_log(dest)
    cleaned = clean_names(df)
    # Verify no leading/trailing spaces and title case
    for name in cleaned["Name"]:
        assert name == name.strip()
        assert name == name.title()


def test_transform_level1_pipeline(tmp_path):
    src = Path("tests/fixtures/sample_agl.txt")
    dest = tmp_path / "sample_agl.txt"
    shutil.copy(src, dest)
    df = load_raw_log(dest)
    cleaned = transform_level1(df)
    # Colunas removidas
    assert "No" not in cleaned.columns
    # DateTime convertido
    assert pd.api.types.is_datetime64_any_dtype(cleaned["DateTime"])
    # Names padronizados
    for name in cleaned["Name"]:
        assert name == name.strip().title()
    # Linhas preservadas
    assert len(cleaned) == len(df)
