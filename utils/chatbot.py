import os
import re
import ast 
import html
import time
import openai
import gradio as gr
from openai import OpenAI
from typing import List, Tuple
from utils.load_config import LoadConfig
from langchain.vectorstores.chroma import Chroma

APPCFG = LoadConfig()

class Chatbot:
    @staticmethod
    def respond(chatbot: List, message: str, temperature: float = 0.0) -> Tuple:
        if  os.path.exists(APPCFG.persist_directory):
            vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                              embedding_function=APPCFG.embedding_model)
        else:
            chatbot.append(
                (message, f"VectorDB doesn't exist. Please upload a document and execute the 'upload_data_manually.py' to create VectorDB."))
                
            return "", chatbot, None

        docs = vectordb.similarity_search(message, k=APPCFG.k)
        print(docs)

        question = "# User new question:\n" + message
        retrieved_content = Chatbot.clean_references(docs)
        # Memory: previous two Q&A pairs
        chat_history = f"Chat history:\n {str(chatbot[-APPCFG.number_of_q_a_pairs:])}\n\n"
        prompt = f"{chat_history}{retrieved_content}{question}"
        print("========================")
        print(prompt)
        client = OpenAI()
        response = client.chat.completions.create(
            model=APPCFG.llm_engine,
            messages=[
                {"role": "system", "content": APPCFG.llm_system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        chatbot.append(
            (message, response.choices[0].message.content)
        )
        time.sleep(2)

        return "", chatbot, retrieved_content

    @staticmethod
    def clean_references(documents: List) -> str:
        server_url = "http://localhost:8000"
        documents = [str(x)+"\n\n" for x in documents]
        markdown_documents = ""
        counter = 1

        for doc in documents:
            match = re.match(r"page_content=(.*?)( metadata=\{.*\})", doc)
            if match:
                content, metadata = match.groups()
                metadata = metadata.split('=', 1)[1]
                metadata_dict = ast.literal_eval(metadata)

            else:
                content = ""
                metadata = ""
                metadata_dict = {}

            # Decode newlines and escape sequences
            content = bytes(content, 'utf-8').decode('unicode_escape')

            # Replace escaped newlines with actual newlines
            content = re.sub(r"\\n", '\n', content)

            # Replace special tokens
            content = re.sub(r'\\n', '\n', content)

            # Remove any remaining multiple spaces
            content = re.sub(r'\s+', ' ', content).strip()

            # Decode html entities
            content = html.unescape(content)

            # Replace incorrect unicode characters with correct ones
            content = content.encode('latin1').decode('utf-8', 'ignore')

            # Remove or replace special characters and mathematical symbols
            content = re.sub(r'â', '-', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Ã', '×', content)
            content = re.sub(r'ï¬', 'fi', content)
            content = re.sub(r'â', '+', content)
            content = re.sub(r'Â·', '·', content)
            content = re.sub(r'â©', '∩', content)
            content = re.sub(r'â', '$', content)


            txt_url = f"{server_url}/{os.path.basename(metadata_dict['description'])}"

            # Append cleaned content to the markdown string with two newlines between documents
            markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n" + \
                f"description: {os.path.basename(metadata_dict['description'])}" + " | " +\
                f"Page number: {str(metadata_dict['page'])}" + " | " +\
                f"[View Episode txt]({txt_url})" "\n\n"
            counter += 1

        return markdown_documents