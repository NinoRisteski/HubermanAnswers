import pytest
from unittest.mock import MagicMock, patch
from utils.chatbot import Chatbot, LoadConfig

@pytest.fixture
def setup_chatbot():
    LoadConfig.persist_directory = 'data/vectordb'
    LoadConfig.embedding_model = MagicMock()
    LoadConfig.k = 2
    LoadConfig.number_of_q_a_pairs = 2
    LoadConfig.llm_engine = 'text-davinci-003'
    LoadConfig.llm_system_role = "Initialize chat"
    return [], LoadConfig  # Return a clean chatbot list and a config

@pytest.mark.parametrize("exists", [True, False])
def test_respond(setup_chatbot, exists):
    chatbot, config = setup_chatbot
    message = "Hello, how are you?"

    with patch('os.path.exists', return_value=exists), \
         patch('langchain.vectorstores.chroma.Chroma') as mock_chroma, \
         patch('openai.OpenAI') as mock_openai:

        if exists:
            mock_vectordb = MagicMock()
            mock_chroma.return_value = mock_vectordb
            mock_vectordb.similarity_search.return_value = [{'content': 'sample content', 'metadata': {'author': 'Test'}}]
            mock_openai.return_value.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="I'm good, thanks!"))])

        output = Chatbot.respond(chatbot, message)
        assert output[1] == chatbot  # Ensure chatbot is returned correctly
        if exists:
            assert len(chatbot) == 1  # Confirm the message was appended
        else:
            assert chatbot[-1][1].startswith("VectorDB doesn't exist")  # Check error handling

def test_clean_references():
    documents = [{'content': 'Hello, world! &lt;test&gt;', 'metadata': {'author': 'Someone', 'date': '2022-01-01'}}]
    cleaned = Chatbot.clean_references(documents)
    assert 'Hello, world! <test>' in cleaned  # Check HTML entity decoding
    assert 'author: Someone' in cleaned  # Metadata formatting

def test_clean_text():
    raw_text = " Hello &lt;world&gt;    "
    clean_text = Chatbot.clean_text(raw_text)
    assert clean_text == "Hello <world>"

def test_format_metadata():
    metadata = {'author': 'John Doe', 'date': '2021-12-31'}
    formatted = Chatbot.format_metadata(metadata)
    assert "author: John Doe" in formatted
    assert "date: 2021-12-31" in formatted
