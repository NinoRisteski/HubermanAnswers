import os
import sys
from utils.prepare_vectordb import PrepareVectorDB
from utils.load_config import LoadConfig

sys.path.append('/Users/.../HubermanAnswers')


CONFIG = LoadConfig()

def upload_data_manually() -> None:
    # Create an instance of PrepareVectorDB with the specified configuration
    prepare_vectordb_instance = PrepareVectorDB(
        data_directory=CONFIG.data_directory,
        persist_directory=CONFIG.persist_directory,
        embedding_model_engine=CONFIG.embedding_model_engine,
        chunk_size=CONFIG.chunk_size,
        chunk_overlap=CONFIG.chunk_overlap,
    )

    # Check if the persist directory is empty
    if not len(os.listdir(CONFIG.persist_directory)) != 0:
        # If the directory is empty, prepare and save the VectorDB
        prepare_vectordb_instance.prepare_and_save_vectordb()
    else:
        # If the directory is not empty, print a message indicating that VectorDB already exists
        print(f"VectorDB already exists in {CONFIG.persist_directory}")

    return None


if __name__ == "__main__":
    # Call the upload_data_manually function when the script is run directly
    upload_data_manually()