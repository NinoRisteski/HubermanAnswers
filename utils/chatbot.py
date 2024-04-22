import os
import re
import ast
import html
import time
import openai
from typing import List, Tuple
from utils.load_config import LoadConfig
from langchain.vectorstores.chroma import Chroma

# Load configuration
APPCFG = LoadConfig()

# Define Chatbot class
class Chatbot:
    @staticmethod
    def respond(chatbot: List, message: str, temperature: float = 0.0) -> Tuple:
        # Check if VectorDB exists
        if os.path.exists(APPCFG.persist_directory):
            vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                              embedding_function=APPCFG.embedding_model)
        else:
            # If VectorDB doesn't exist, return error message
            chatbot.append(
                (message, "VectorDB doesn't exist. Please upload a document and execute the 'upload_data_manually.py' to create VectorDB."))
            return "", chatbot, None

        # Perform similarity search
        docs = vectordb.similarity_search(message, k=APPCFG.k)
        print(docs)

        # Prepare prompt for language model
        question = "# User new question:\n" + message
        retrieved_content = Chatbot.clean_references(docs)
        chat_history = f"Chat history:\n {str(chatbot[-APPCFG.number_of_q_a_pairs:])}\n\n"
        prompt = f"{chat_history}{retrieved_content}{question}"
        print("========================")
        print(prompt)

        # Generate response using language model
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=APPCFG.llm_engine,
            messages=[
                {"role": "system", "content": APPCFG.llm_system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )

        # Append user message and response to chatbot history
        chatbot.append(
            (message, response.choices[0].message.content)
        )
        time.sleep(2)

        return "", chatbot, retrieved_content

    @staticmethod
    def clean_references(documents: List) -> str:
        # Clean and format the retrieved documents
        documents_cleaned = ""
        for doc in documents:
            content, metadata = Chatbot.extract_vtt_content_and_metadata(doc)
            cleaned_content = Chatbot.clean_text(content)
            metadata_formatted = Chatbot.format_metadata(metadata)
            documents_cleaned += f"## Content:\n{cleaned_content}\n\n{metadata_formatted}\n\n"
        return documents_cleaned

    @staticmethod
    def extract_vtt_content_and_metadata(doc):
        # Extract content and metadata from the document
        # Print all available attributes and methods of the Document object
        print(dir(doc))
        # Then, use the correct attribute or method based on the output
        content = doc.content if hasattr(doc, 'content') else ""
        metadata = doc.metadata if hasattr(doc, 'metadata') else {}
        return content, metadata

    @staticmethod
    def clean_text(text: str) -> str:
        # Perform cleaning operations on the text
        text = html.unescape(text)  # Decode HTML entities
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
        text = text.encode('latin1').decode('utf-8', 'ignore')  # Fix encoding issues
        return text

    @staticmethod
    def format_metadata(metadata: dict) -> str:
        # Format metadata for display
        metadata_formatted = " | ".join(f"{key}: {value}" for key, value in metadata.items())
        return f"### Metadata:\n{metadata_formatted}"
