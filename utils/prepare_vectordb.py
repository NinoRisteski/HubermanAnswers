
import os
import glob
from typing import List
from langchain.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


class PrepareVectorDB:
    def __init__(
            self,
            data_directory: str,
            persist_directory: str,
            embedding_model_engine: str,
            chunk_size: int,
            chunk_overlap: int,
            
    ) -> None:
        
        self.embedding_model_engine = embedding_model_engine
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " "]
        )

        self.data_directory = data_directory
        self.persist_directory = persist_directory
        self.embedding = OpenAIEmbeddings()

    def __load_all_documents(self) -> List:
        docs = [] 
        doc_counter = 0

        if isinstance(self.data_directory, str):
            print("Loading documents from directory:", self.data_directory)
            for file_path in glob.glob(os.path.join(self.data_directory, '*.txt')):
                doc = Document(file_path)
                docs.append(doc)
                doc_counter += 1
                print("Loaded document:", file_path)

            print(f"Loaded {doc_counter} documents")
            print(f"Total number of documents:", len(docs), "\n\n")
        else:
            print("Data directory should be a single string path.")

        return docs
    
    def __chunk_documents(self, docs: List) -> List:
        print("Chunking documents")
        chunked_documents = self.text_splitter.split_documents(docs)
        print(f"Total number of chunks: {len(chunked_documents)}")
        
        return chunked_documents
    
    def prepare_and_save_vectordb(self):
        docs = self.__load_all_documents()
        chunked_documents = self.__chunk_documents(docs)
        print("Preparing VectorDB...")
        vectordb = Chroma.from_documents(
            documents=chunked_documents,
            embedding=self.embedding,
            persist_directory=self.persist_directory
        )

        print("VectorDB prepared and saved successfully")
        print("Number of vectors in VectorDB:",
              vectordb._collection.count(), "\n\n")
        
        return vectordb