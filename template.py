import os
from pathlib import Path
import logging

#Logging string
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

project_name= 'HubermanAnswers'

list_of_folders = [
    ".github/workflows/.gitkeep",
    "requirements.txt",
    f"configs/{project_name}/app_config.yml",
    f"data/{project_name}/docs/",
    f"src/{project_name}/hubermananswers_app.py",
    f"src/{project_name}/serve.py",
    f"utils/{project_name}/chatbot.py"
    f"utils/{project_name}/load_config.py",
    f"utils/{project_name}/prepare_vectordb.py",
    f"utils/{project_name}/summarizer.py"
    f"utils/{project_name}/ui_settings.py",
    f"utils/{project_name}/utilities.py",


]

for filepath in list_of_folders:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
            

    else:
        logging.info(f"File already exists: {filename}")