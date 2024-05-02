import os
from unittest.mock import MagicMock, patch
import pytest
from utils.prepare_vectordb import PrepareVectorDB, Document  

@pytest.fixture
def vectordb_setup():
    # Setup for testing
    return PrepareVectorDB(
        data_directory='data/docs',
        persist_directory='data/vectordb/processed/chroma/',
        embedding_model_engine='text-embedding-ada-002',
        chunk_size=500,
        chunk_overlap=50
    )

def test_constructor(vectordb_setup):
    # Test that the constructor correctly initializes the instance
    assert vectordb_setup.data_directory == 'data/docs'
    assert vectordb_setup.persist_directory == 'data/vectordb/processed/chroma/'
    assert vectordb_setup.embedding_model_engine == 'text-embedding-ada-002'
    assert isinstance(vectordb_setup.text_splitter, RecursiveCharacterTextSplitter)

@patch('os.path.join')
@patch('glob.glob')
def test_load_all_documents(mock_glob, mock_join, vectordb_setup):
    # Mock dependencies
    mock_glob.return_value = ['data/docs/ADHD & How Anyone Can Improve Their Focus ｜ Huberman Lab Podcast #37.mp3.vtt', 'data/docs/Biological Influences On Sex, Sex Differences & Preferences ｜ Huberman Lab Podcast #14.mp3.vtt']
    mock_join.return_value = 'data/docs/Control Pain & Heal Faster with Your Brain ｜ Huberman Lab Podcast #9.mp3.vtt'

    with patch('concurrent.futures.ThreadPoolExecutor') as mock_executor:
        mock_executor.return_value.__enter__.return_value.map.return_value = [Document("text", {}), Document("more text", {})]
        docs = vectordb_setup._PrepareVectorDB__load_all_documents()
        assert len(docs) == 2  # Assumes 2 documents were mocked to be loaded

from unittest.mock import patch, mock_open

@patch('builtins.open', new_callable=mock_open, read_data="WEBVTT\nNOTE Some note\n1\n00:00:01.000 --> 00:00:04.000\nHello world!")
def test_load_document(mocked_open, vectordb_setup):
    doc = vectordb_setup._PrepareVectorDB__load_document('/path/to/data/doc1.vtt')
    assert doc.text == "Hello world!"


def test_extract_text_from_vtt(vectordb_setup):
    vtt_content = "WEBVTT\n\nNOTE duration:positive\n1\n00:00:00.000 --> 00:00:01.000\nThis is a test."
    text = vectordb_setup._PrepareVectorDB__extract_text_from_vtt(vtt_content)
    assert text == "This is a test."

def test_chunk_documents(vectordb_setup):
    docs = [Document("Test document content", {})]
    with patch.object(vectordb_setup.text_splitter, 'split_documents', return_value=[Document("Test document content", {})]) as mock_split:
        chunked_docs = vectordb_setup._PrepareVectorDB__chunk_documents(docs)
        assert len(chunked_docs) == 1

@patch('langchain.vectorstores.Chroma.from_documents')
def test_prepare_and_save_vectordb(mock_from_docs, vectordb_setup):
    # Mock the methods that load and chunk documents
    vectordb_setup._PrepareVectorDB__load_all_documents = MagicMock(return_value=[Document("Test", {})])
    vectordb_setup._PrepareVectorDB__chunk_documents = MagicMock(return_value=[Document("Test", {})])
    vectordb = vectordb_setup.prepare_and_save_vectordb()
    mock_from_docs.assert_called_once()  # Check if Chroma.from_documents was called
