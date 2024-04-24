import pytest
from utils.chatbot import Chatbot

class TestChatbot(pytest.TestCase):
    def test_respond_with_existing_VectorDB(self):
        """
        Test case to verify the behavior of the respond method when using an existing VectorDB.

        Steps:
        1. Create an empty chatbot list.
        2. Set the message to "Hello, how are you?".
        3. Set the temperature to 0.5.
        4. Call the Chatbot.respond method with the chatbot, message, and temperature.
        5. Verify that the response is an empty string.
        6. Verify that the updated_chatbot list has a length of 1.
        7. Verify that the first element of the updated_chatbot list is equal to the message.
        8. Verify that the retrieved_content is not None.
        """

        chatbot = []
        message = "Hello, how are you?"
        temperature = 0.5

        response, updated_chatbot, retrieved_content = Chatbot.respond(chatbot, message, temperature)

        self.assertEqual(response, "")
        self.assertEqual(len(updated_chatbot), 1)
        self.assertEqual(updated_chatbot[0][0], message)
        self.assertIsNotNone(retrieved_content)

if __name__ == '__main__':
    pytest.main()