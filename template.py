import os
from pathlib import Path
import logging

#Logging string
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
    ".github/workflows/.gitkeep",
    "requirements.txt",
    f"configs/app_config.yml",
    f"data/docs/",
    f"src/hubermananswers_app.py",
    f"src/serve.py",
    f"utils/chatbot.py"
    f"utils/load_config.py",
    f"utils/prepare_vectordb.py",
    f"utils/summarizer.py"
    f"utils/ui_settings.py",
    f"utils/utilities.py",


]

for filepath in list_of_files:
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