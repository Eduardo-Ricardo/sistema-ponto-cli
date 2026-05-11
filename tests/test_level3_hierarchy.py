import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import build_hierarchy, extract_temporal_keys, load_raw_log, transform_level1, transform_level2, transform_level3


def test_extract_temporal_keys(tmp_path):
	src = Path("tests/fixtures/sample_agl.txt")
	dest = tmp_path / "sample_agl.txt"
	shutil.copy(src, dest)

	df = load_raw_log(dest)
	cleaned = transform_level1(df)
	keyed = extract_temporal_keys(cleaned)

	assert keyed.loc[0, "Year"] == "2000"
	assert keyed.loc[0, "Month"] == "05"
	assert keyed.loc[0, "Day"] == "28"


def test_build_hierarchy_orders_employees_and_times():
	df = pd.DataFrame(
		[
			{"EnNo": 2, "Name": "Usuario 2", "DateTime": pd.Timestamp("2000-05-28 08:06:00"), "Year": "2000", "Month": "05", "Day": "28"},
			{"EnNo": 1, "Name": "Usuario 1", "DateTime": pd.Timestamp("2000-05-28 10:10:00"), "Year": "2000", "Month": "05", "Day": "28"},
			{"EnNo": 1, "Name": "Usuario 1", "DateTime": pd.Timestamp("2000-05-28 10:00:00"), "Year": "2000", "Month": "05", "Day": "28"},
		]
	)

	hierarchy = build_hierarchy(df)
	day_bucket = hierarchy["2000"]["05"]["28"]

	assert list(day_bucket.keys()) == ["1_Usuario 1", "2_Usuario 2"]
	assert day_bucket["1_Usuario 1"] == ["10:00:00", "10:10:00"]
	assert day_bucket["2_Usuario 2"] == ["08:06:00"]


def test_transform_level3_returns_empty_dict_for_empty_dataframe():
	assert transform_level3(pd.DataFrame()) == {}


def test_transform_level3_full_pipeline(tmp_path):
	src = Path("tests/fixtures/sample_agl.txt")
	dest = tmp_path / "sample_agl.txt"
	shutil.copy(src, dest)

	df = load_raw_log(dest)
	cleaned = transform_level1(df)
	filtered = transform_level2(cleaned)
	hierarchy = transform_level3(filtered)

	assert hierarchy == {
		"2000": {
			"05": {
				"28": {
					"1_Usuario 1": ["10:51:39"],
					"2_Usuario 2": ["11:00:00"],
				}
			}
		}
	}