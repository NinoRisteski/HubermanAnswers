![Alt text](assets/ah-lab-main.jpg)
# Huberman Answers
If you’re looking for a quick answer into the topics discussed on the [HubermanLab Podcast](https://www.hubermanlab.com/) but don’t have time to listen to full episodes, you’ve come to the right place. This chatbot is a `RAG-GPT` system with `OpenAI's GPT`, `Langchain`, `ChromaDB`, and `Gradio`, delivers pinpoint answers to your questions. 

Submit your question and get insights on neuroscience, biology, and human performance directly from Dr. Andrew Huberman’s discussions.

This chatbot is perfect for the curious people who want to learn about human performance quickly and efficiently from the great Huberman. 
Plus, each answer comes with the name and number of the podcast episode if you want to watch it.

## Interface
![Alt text](assets/ah-example-chat.png)

## Data
This project utilizes transcripts from the Huberman Lab podcast, originally transcribed by Marko Simic. 
You can find his project [here](https://www.simicvm.com/hubcap/).

Transcripts are stored in the data directory `data/docs`: For files that should be processed in advance.
Vector database (VectorDB) is generated within the data folder for the project's functionality.

### Data Acquisition

* Episodes were downloaded using the [yt-dlp](https://github.com/yt-dlp/yt-dlp) tool.
* The obtained audio files were transcribed using OpenAI's [Whisper](https://github.com/openai/whisper) `medium.en model`.

## Schema

## Usage

1. Open app_config.py and fill in your GPT API credentials.
2. Activate Your Environment.
3. Ensure you are in the hubermananswers directory

4. Run the Application:

In Terminal 1:

python3 src\serve.py

In Terminal 2:

python3 src\hubermananswers_app.py


## Credits 
*to be written: Huberman data credits and visuals credits*


## Contact
If you liked this project, feel free to reach out on: 
* [X](https://twitter.com/ninoristeski)
* [LinkedIn](https://www.linkedin.com/in/nino-risteski/).