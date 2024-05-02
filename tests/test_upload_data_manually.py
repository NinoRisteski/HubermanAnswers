import os
from unittest.mock import patch, MagicMock
import pytest
from src.upload_data_manually import upload_data_manually, CONFIG


# Ensure the CONFIG object is properly loaded and has the expected attributes
def test_config_loaded():
    assert hasattr(CONFIG, "data_directory")
    assert hasattr(CONFIG, "persist_directory")
    assert hasattr(CONFIG, "embedding_model_engine")
    assert hasattr(CONFIG, "chunk_size")
    assert hasattr(CONFIG, "chunk_overlap")

# Test the scenario where the persist directory is empty and data needs to be uploaded
@patch('os.listdir')
@patch('src.upload_data_manually.PrepareVectorDB')
def test_upload_data_manually_empty_directory(mock_preparevectordb, mock_listdir):
    mock_listdir.return_value = []  # Simulate empty directory
    mock_instance = mock_preparevectordb.return_value

    upload_data_manually()

    mock_preparevectordb.assert_called_once_with(
        data_directory=CONFIG.data_directory,  
        persist_directory=CONFIG.persist_directory,  
        embedding_model_engine=CONFIG.embedding_model_engine, 
        chunk_size=CONFIG.chunk_size,  
        chunk_overlap=CONFIG.chunk_overlap
    )
    mock_instance.prepare_and_save_vectordb.assert_called_once()

# Test the scenario where the persist directory is not empty and upload should be skipped
@patch('os.listdir')
@patch('src.upload_data_manually.PrepareVectorDB')
def test_upload_data_manually_non_empty_directory(mock_preparevectordb, mock_listdir):
    mock_listdir.return_value = ['file1', 'file2']  # Simulate non-empty directory
    mock_instance = mock_preparevectordb.return_value

    with patch('builtins.print') as mock_print:
        upload_data_manually()

        mock_print.assert_called_once_with(f"VectorDB already exists in {CONFIG.persist_directory}")

    mock_preparevectordb.assert_not_called()
    mock_instance.prepare_and_save_vectordb.assert_not_called()

