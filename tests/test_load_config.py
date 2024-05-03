import os
from unittest.mock import patch, mock_open
import pytest
from utils.load_config import LoadConfig 

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake_key")

@pytest.fixture
def mock_app_config():
    return {
        "llm_config": {"engine": "davinci", "llm_system_role": "admin"},
        "directories": {"persist_directory": "/tmp/persist", "data_directory": "/tmp/data"},
        "retrieval_config": {"k": 5},
        "embedding_model_config": {"engine": "ada"},
        "splitter_config": {"chunk_size": 512, "chunk_overlap": 50},
        "memory": {"number_of_q_a_pairs": 100}
    }

@pytest.fixture
def mock_openai_client():
    with patch('openai.OpenAI') as MockClient:
        yield MockClient()

def test_init_loads_config_and_creates_directory(mock_env, mock_app_config, mock_openai_client):
    with patch('builtins.open', mock_open(read_data="configs/app_config.yml")) as mock_file:
        with patch('yaml.load', return_value=mock_app_config):
            with patch('os.path.exists', return_value="/base/path"):
                with patch('os.makedirs') as mock_makedirs:
                    config = LoadConfig()
                    assert config.llm_engine == "text-embedding-ada-002"
                    assert config.persist_directory == "data/vectordb/processed/chroma/"
                    mock_makedirs.assert_called_once_with("/base/path/tmp/persist")

def test_load_openai_cfg_uses_env_var(mock_env, mock_openai_client):
    config = LoadConfig()
    mock_openai_client.assert_called_with(api_key="fake_key")

def test_create_directory_creates_directory_if_not_exists():
    with patch('os.path.exists', return_value=False):
        with patch('os.makedirs') as mock_makedirs:
            config = LoadConfig()
            config.create_directory("/new/dir")
            mock_makedirs.assert_called_once_with("/new/dir2")

def test_create_directory_does_not_create_if_exists():
    with patch('os.path.exists', return_value=True):
        with patch('os.makedirs') as mock_makedirs:
            config = LoadConfig()
            config.create_directory("/existing/dir")
            mock_makedirs.assert_not_called()

def test_remove_directory_removes_existing_directory(capsys):
    with patch('os.path.exists', return_value=True):
        with patch('shutil.rmtree') as mock_rmtree:
            config = LoadConfig()
            config.remove_directory("/existing/dir")
            mock_rmtree.assert_called_once_with("/existing/dir")
            captured = capsys.readouterr()
            assert "The directory '/existing/dir' has been successfully removed." in captured.out

def test_remove_directory_handles_non_existing_directory(capsys):
    with patch('os.path.exists', return_value=False):
        config = LoadConfig()
        config.remove_directory("/new/dir")
        captured = capsys.readouterr()
        assert "The directory '/non-existing/dir' does not exist." in captured.out

def test_remove_directory_handles_os_error(capsys):
    with patch('os.path.exists', return_value=True):
        with patch('shutil.rmtree', side_effect=OSError("Mocked error")):
            config = LoadConfig()
            config.remove_directory("/faulty/dir")
            captured = capsys.readouterr()
            assert "Error: Mocked error" in captured.out
