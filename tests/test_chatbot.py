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

    def test_clean_text(self):
        text = "&lt;p&gt;This is a &amp;lt;strong&amp;gt;test&amp;lt;/strong&amp;gt;.&lt;/p&gt;"

        cleaned_text = Chatbot.clean_text(text)

        assert cleaned_text, "<p>This is a &lt;strong&gt;test&lt;/strong&gt;.</p>"

    def test_format_metadata(self):
        metadata = {"author": "John", "date": "2022-01-01"}

        formatted_metadata = Chatbot.format_metadata(metadata)

        assert formatted_metadata, "### Metadata:\nauthor: John | date: 2022-01-01"

if __name__ == '__main__':
    pytest.main()