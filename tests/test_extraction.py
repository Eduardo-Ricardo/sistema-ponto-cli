import shutil
from pathlib import Path
import sys
import pandas as pd

# Ensure 'src' package is importable when pytest runs from project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import resolve_raw_file_path, load_raw_log


def test_resolve_raw_file_path_fixture(tmp_path):
	# copy fixture to temp and resolve
	src = Path("tests/fixtures/sample_agl.txt")
	dest = tmp_path / "sample_agl.txt"
	shutil.copy(src, dest)
	p = resolve_raw_file_path(dest)
	assert p.exists()


def test_load_raw_log_columns_and_datetime(tmp_path):
	src = Path("tests/fixtures/sample_agl.txt")
	dest = tmp_path / "sample_agl.txt"
	shutil.copy(src, dest)
	df = load_raw_log(dest)
	expected = ["No", "TMNo", "EnNo", "Name", "GMNo", "Mode", "DateTime"]
	for col in expected:
		assert col in df.columns
	# verify DateTime parses to datetime dtype
	df["DateTime"] = pd.to_datetime(df["DateTime"], errors="raise")
	assert pd.api.types.is_datetime64_any_dtype(df["DateTime"])
	assert len(df) == 3
