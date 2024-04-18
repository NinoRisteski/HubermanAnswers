import sys
sys.path.append('/Users/fliprise/HubermanAnswers')

import os
import re
import ast 
import html
import time
import openai
import gradio as gr
from typing import List, Tuple
from utils.load_config import LoadConfig
from langchain.vectorstores.chroma import Chroma

APPCFG = LoadConfig()

class Chatbot:
    @staticmethod
    def respond(chatbot: List, message: str, data_type: str = "Preprocessed", temperature: float = 0) -> Tuple:
        vectordb = None

        if data_type == "Preprocessed":
            if os.path.exists(APPCFG.persist_directory):
                vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                                  embedding_function=APPCFG.embedding_model)
            else:
                chatbot.append(
                    (message, f"VectorDB doesn't exist. Please upload a document and execute the 'upload_data_manually.py' to create VectorDB."))
                return "", chatbot, None

        if vectordb is not None:
            docs = vectordb.similarity_search(message, k=APPCFG.k)
            print(docs)
            question = "# User new question:\n" + message
            retrieved_content = Chatbot.clean_references(docs)
            response = openai.ChatCompletion.create(
            engine=APPCFG.llm_engine,
            messages=[
                {"role": "system", "content": APPCFG.ll_system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            )
            chatbot.append(
            (message, response["choices"][0]["message"]["content"]))
            time.sleep(2)
        else:
            chatbot.append(
            (message, "Error: VectorDB is not available. Cannot process the message."))
            retrieved_content = None
        
        return "", chatbot, retrieved_content

    @staticmethod
    def clean_references(documents: List) -> str:
        server_url = "http://localhost:8000"
        documents = [str(x)+"\n\n" for x in documents]
        markdown_documents = ""
        counter = 1
        for doc in documents:
            content, metadata = re.match(
                r"page_content=(.*?)( metadata=\{.*\})", doc).groups()
            metadata = metadata.split('=', 1)[1]
            metadata_dict = ast.literal_eval(metadata)

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

            txt_url = f"{server_url}/{os.path.basename(metadata_dict['source'])}"

            # Append cleaned content to the markdown string with two newlines between documents
            markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n" + \
                f"Source: {os.path.basename(metadata_dict['source'])}" + " | " +\
                f"Page number: {str(metadata_dict['page'])}" + " | " +\
                f"[View Episode txt]({txt_url})" "\n\n"
            counter += 1

        return markdown_documents
