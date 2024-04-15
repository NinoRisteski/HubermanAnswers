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
        if data_type == "Preprocessed":
            if os.path.exists(APPCFG.persist_directory):
                vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                                  embedding_function=APPCFG.embedding_model)
            else:
                chatbot.append(
                    (message, f"VectorDB doesn't exist. Please upload a document and execute the 'upload_data_manually.py to create VectorDB."))
                return "", chatbot, None

        docs = vectordb.similarity_search(message, k=APPCFG.k)
        print(docs)
        question = "# User new question:\n" + message
        retrieved_content = Chatbot.clean_references(docs)
        response = openai.ChatCompletion.create(
            engine=APPCFG.llm_engine,
            message=[
                {"role": "system", "content": APPCFG.ll_system_role}
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        chatbot.append(
            (message, response["choices"][0]["message"]["content"]))
            time.sleep(1)
        
            return "", chatbot, retrieved_content

        @staticmethod
        def clean_references(documents: List) -> str:
            server_url = "http://localhost:8000"
            documents = [str(x)+"\n\n" for x in documents]
            markdown_documents = ""
            counter = 1
            