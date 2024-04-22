import os
import sys
from utils.prepare_vectordb import PrepareVectorDB
from utils.load_config import LoadConfig

sys.path.append('/Users/fliprise/HubermanAnswers')


CONFIG = LoadConfig() 

def upload_data_manually() -> None:
    prepare_vectordb_instance = PrepareVectorDB(
        data_directory=CONFIG.data_directory,  # Set the data directory
        persist_directory=CONFIG.persist_directory,  # Set the directory to persist the VectorDB
        embedding_model_engine=CONFIG.embedding_model_engine,  # Set the embedding model engine
        chunk_size=CONFIG.chunk_size,  # Set the chunk size for processing data
        chunk_overlap=CONFIG.chunk_overlap,  # Set the overlap between chunks
    )
    
    if not len(os.listdir(CONFIG.persist_directory)) != 0:  # Check if the persist directory is empty
        prepare_vectordb_instance.prepare_and_save_vectordb()  
    else:
        print(f"VectorDB already exists in {CONFIG.persist_directory}")
    
    return None


if __name__ == "__main__":
    upload_data_manually()  
