import pytest
from utils.chatbot import Chatbot

class TestChatbot():
    def test_respond_with_existing_VectorDB(self):

        chatbot = []
        message = "Hello, how are you?"
        temperature = 0.5

        response, updated_chatbot, retrieved_content = Chatbot.respond(chatbot, message, temperature)

        assert(response == "")
        assert len(updated_chatbot), 1
        assert updated_chatbot[0][0], message 
        assert(retrieved_content)

    def test_clean_references(self):
        documents = [
            {"content": "Document 1", "metadata": {"author": "John"}},
            {"content": "Document 2", "metadata": {"author": "Jane"}}
        ]

        cleaned_documents = Chatbot.clean_references(documents)

        assert"Document 1", cleaned_documents
        assert"Document 2", cleaned_documents
        assert"author: John", cleaned_documents
        assert"author: Jane", cleaned_documents

if __name__ == '__main__':
    pytest.main()