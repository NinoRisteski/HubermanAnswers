import os
import glob
from typing import List, Tuple
from langchain.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import concurrent.futures
import logging

class PrepareVectorDB:
    def __init__(
            self,
            data_directory: str,
            persist_directory: str,
            embedding_model_engine: str,
            chunk_size: int,
            chunk_overlap: int,
    ) -> None:
        # Initialize the PrepareVectorDB class with the given parameters
        self.embedding_model_engine = embedding_model_engine
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " "]
        )

        self.data_directory = data_directory
        self.persist_directory = persist_directory
        self.embedding = OpenAIEmbeddings()

        # Set up logging configuration
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def __load_all_documents(self) -> List:
        # Load all documents from the specified directory
        logging.info("Loading documents from directory: %s", self.data_directory)
        doc_files = glob.glob(os.path.join(self.data_directory, '*.vtt'))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            docs = list(executor.map(self.__load_document, doc_files))

        logging.info("Loaded %d documents", len(docs))
        return docs

    def __load_document(self, file_path: str) -> Document:
        # Load a single document from the given file path
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            text = self.__extract_text_from_vtt(content)
            return Document(text, metadata={'path': file_path})
        except Exception as e:
            logging.error("Failed to load document %s: %s", file_path, str(e))
            return None

    def __extract_text_from_vtt(self, content: str) -> str:
        # Extract the text from a VTT file content
        lines = content.split('\n')
        text = [line.strip() for line in lines if not line.startswith(('NOTE', 'WEBVTT', 'STYLE')) and '-->' not in line]
        return ' '.join(text).replace('  ', ' ')

    def __chunk_documents(self, docs: List) -> List:
        # Chunk the documents into smaller parts
        logging.info("Chunking documents")
        chunked_documents = self.text_splitter.split_documents(docs)
        logging.info("Total number of chunks: %d", len(chunked_documents))
        return chunked_documents
    
    def prepare_and_save_vectordb(self):
        # Prepare and save the VectorDB
        docs = self.__load_all_documents()
        chunked_documents = self.__chunk_documents(docs)
        logging.info("Preparing VectorDB...")
        vectordb = Chroma.from_documents(
            documents=chunked_documents,
            embedding=self.embedding,
            persist_directory=self.persist_directory
        )

        logging.info("VectorDB prepared and saved successfully")
        logging.info("Number of vectors in VectorDB: %d", vectordb._collection.count())
        return vectordb
