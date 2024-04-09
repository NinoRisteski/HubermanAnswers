import logging
from pathlib import Path

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Corrected list of files with commas added to separate items properly
list_of_files = [
    ".github/workflows/.gitkeep",
    "requirements.txt",
    "configs/app_config.yml",
    "data/docs/",
    "src/hubermananswers_app.py",
    "src/serve.py",
    "utils/chatbot.py",
    "utils/load_config.py",
    "utils/prepare_vectordb.py",
    "utils/summarizer.py",
    "utils/ui_settings.py",
    "utils/utilities.py",
]

for filepath_str in list_of_files:
    filepath = Path(filepath_str)  # Create a Path object for each filepath

    if filepath.suffix:  # This checks if the path ends with a file extension
        # Ensure the directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Ensuring directory exists: {filepath.parent} for the file: {filepath.name}")

        # Check if the file does not exist or is empty, then create or overwrite it
        if not filepath.exists() or filepath.stat().st_size == 0:
            filepath.touch()
            logging.info(f"Creating empty file: {filepath}")
        else:
            logging.info(f"File already exists and is not empty: {filepath.name}")
    else:
        # If the path doesn't end with a file extension, treat it as a directory
        filepath.mkdir(parents=True, exist_ok=True)
        logging.info(f"Creating directory: {filepath}")
