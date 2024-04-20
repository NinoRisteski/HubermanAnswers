
import os
import yaml
from openai import OpenAI
import shutil
from dotenv import load_dotenv
from pyprojroot import here
from langchain_openai import OpenAIEmbeddings

load_dotenv()

class LoadConfig:

    def __init__(self) -> None:
        with open(here("configs/app_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # LLM Config
        self.llm_engine = app_config["llm_config"]["engine"]
        self.llm_system_role = app_config["llm_config"]["llm_system_role"]
        self.persist_directory = str(here(
            app_config["directories"]["persist_directory"]))
        self.embedding_model = OpenAIEmbeddings()

        # Retrieval Config
        self.data_directory = app_config["directories"]["data_directory"]
        self.k = app_config["retrieval_config"]["k"]
        self.embedding_model_engine = app_config["embedding_model_config"]["engine"]
        self.chunk_size = app_config["splitter_config"]["chunk_size"]
        self.chunk_overlap = app_config["splitter_config"]["chunk_overlap"]
        
        # Memory
        self.number_of_q_a_pairs = app_config["memory"]["number_of_q_a_pairs"]

        # Load OpenAI Credentials
        self.load_openai_cfg()

        # Clean up the upload doc vectordb if it exists
        self.create_directory(self.persist_directory)

    def load_openai_cfg(self):
        self.client = OpenAI(
            api_key = os.environ["OPENAI_API_KEY"],
        )
    def create_directory(self, directory_path: str):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def remove_directory(self, directory_path: str):
   
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(
                    f"The directory '{directory_path}' has been successfully removed.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"The directory '{directory_path}' does not exist.")