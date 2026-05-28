import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import export_to_csv, prepare_csv_output, transform_level4


def test_prepare_csv_output_creates_expected_columns():
    """Valida que o DataFrame final tem as colunas do CSV."""
    df = pd.DataFrame(
        [
            {"EnNo": 1, "Name": "usuario 1", "DateTime": pd.Timestamp("2000-05-28 10:51:39")},
            {"EnNo": 2, "Name": "usuario 2", "DateTime": pd.Timestamp("2000-05-28 11:00:00")},
        ]
    )

    prepared = prepare_csv_output(df)

    assert list(prepared.columns) == ["ID", "NOME", "DATA", "HORA"]
    assert prepared.loc[0, "ID"] == 1
    assert prepared.loc[0, "NOME"] == "usuario 1"
    assert prepared.loc[0, "DATA"] == "2000-05-28"
    assert prepared.loc[0, "HORA"] == "10:51:39"


def test_export_to_csv_creates_file(tmp_path):
    """Valida que o arquivo CSV é criado no caminho especificado."""
    df = pd.DataFrame(
        [
            {"EnNo": 1, "Name": "usuario 1", "DateTime": pd.Timestamp("2000-05-28 10:51:39")},
            {"EnNo": 2, "Name": "usuario 2", "DateTime": pd.Timestamp("2000-05-28 11:00:00")},
        ]
    )

    output_file = tmp_path / "test_output.csv"
    result = export_to_csv(df, output_file)

    assert result == output_file
    assert output_file.exists()
    assert output_file.is_file()


def test_export_to_csv_creates_parent_directory(tmp_path):
    """Valida que diretório pai é criado automaticamente se não existir."""
    df = pd.DataFrame(
        [{"EnNo": 1, "Name": "usuario 1", "DateTime": pd.Timestamp("2000-05-28 10:51:39")}]
    )

    nested_output = tmp_path / "deep" / "nested" / "path" / "output.csv"
    result = export_to_csv(df, nested_output)

    assert result.exists()
    assert nested_output.parent.exists()


def test_transform_level4_full_pipeline(tmp_path):
    """Valida que transform_level4 encadeia export_to_csv corretamente."""
    df = pd.DataFrame(
        [
            {"EnNo": 1, "Name": "usuario 1", "DateTime": pd.Timestamp("2000-05-28 10:51:39")},
            {"EnNo": 2, "Name": "usuario 2", "DateTime": pd.Timestamp("2000-05-28 11:00:00")},
        ]
    )

    output_file = tmp_path / "final_output.csv"
    result = transform_level4(df, output_file)

    assert result == output_file
    assert output_file.exists()

    loaded = pd.read_csv(output_file)
    assert list(loaded.columns) == ["ID", "NOME", "DATA", "HORA"]
    assert loaded.loc[0, "DATA"] == "2000-05-28"
    assert loaded.loc[0, "HORA"] == "10:51:39"
