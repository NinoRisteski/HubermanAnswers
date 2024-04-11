import os
import yaml
import openai
import shutil
from dotenv import load_dotenv
from pyprojroot import here
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

def __init__(self) -> None:
    with open(here("configs/app_config.yml")) as cfg:
        app_config = yaml.load(cfg, Loader=yaml.FullLoader)

    # LLM Config
    self.llm_engine = app_config["llm_config"]["engine"]
    self.ll_system_role = app_config["llm_config"]["llm_system_role"]
    self.persist_directory = str(here(
        app_config["directories"]["persist_directory"]))
    self.custom_persist_directory = str(here(
        app_config["directories"]["custom_persist_directory"]))
    self.embedding_model = OpenAIEmbeddings()

