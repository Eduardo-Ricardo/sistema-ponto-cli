import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import export_to_json, transform_level4


def test_export_to_json_creates_file(tmp_path):
	"""Valida que o arquivo JSON é criado no caminho especificado."""
	test_hierarchy = {
		"2000": {
			"05": {
				"28": {
					"1_Usuario 1": ["10:51:39"],
					"2_Usuario 2": ["11:00:00"],
				}
			}
		}
	}
	
	output_file = tmp_path / "test_output.json"
	result = export_to_json(test_hierarchy, output_file)
	
	assert result == output_file
	assert output_file.exists()
	assert output_file.is_file()


def test_export_to_json_valid_json(tmp_path):
	"""Valida que o arquivo JSON é válido e relável."""
	test_hierarchy = {
		"2000": {
			"05": {
				"28": {
					"1_Usuario 1": ["10:51:39"],
					"2_Usuario 2": ["11:00:00"],
				}
			}
		}
	}
	
	output_file = tmp_path / "test_output.json"
	export_to_json(test_hierarchy, output_file)
	
	# Tentar recarregar o arquivo
	with open(output_file, "r", encoding="utf-8") as f:
		loaded = json.load(f)
	
	assert loaded == test_hierarchy


def test_export_to_json_creates_parent_directory(tmp_path):
	"""Valida que diretório pai é criado automaticamente se não existir."""
	test_hierarchy = {"2000": {"05": {"28": {"1_Usuario 1": ["10:51:39"]}}}}
	
	nested_output = tmp_path / "deep" / "nested" / "path" / "output.json"
	result = export_to_json(test_hierarchy, nested_output)
	
	assert result.exists()
	assert nested_output.parent.exists()


def test_transform_level4_full_pipeline(tmp_path):
	"""Valida que transform_level4 encadeia export_to_json corretamente."""
	test_hierarchy = {
		"2000": {
			"05": {
				"28": {
					"1_Usuario 1": ["10:51:39"],
					"2_Usuario 2": ["11:00:00"],
				}
			}
		}
	}
	
	output_file = tmp_path / "final_output.json"
	result = transform_level4(test_hierarchy, output_file)
	
	assert result == output_file
	assert output_file.exists()
	
	# Validar conteúdo
	with open(output_file, "r", encoding="utf-8") as f:
		loaded = json.load(f)
	
	assert loaded == test_hierarchy
