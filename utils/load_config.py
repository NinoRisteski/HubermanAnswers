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
        app_cofing = yaml.load(ccfg, Loader=yaml.FullLoader)

    