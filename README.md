![Alt text](assets/ah-lab-main.jpg)
# Huberman Answers
If you’re looking for a quick answer to the topics discussed on the [HubermanLab Podcast](https://www.hubermanlab.com/) but don’t have time to listen to full episodes, you’ve come to the right place. This chatbot is a `RAG-GPT` system with `OpenAI's GPT 3.5 Turbo`, `Langchain`, `ChromaDB`, and `Gradio`, delivers pinpoint answers to your questions. 

Submit your question and get insights on neuroscience, biology, and human performance directly from Dr. Andrew Huberman’s discussions.
Each answer comes with the name and number of the podcast episode if you want to watch it.

## Interface
![Alt text](assets/ah-example-chat.png)

## Data
This project utilizes `.vtt` transcripts from the Huberman Lab podcast, originally transcribed by Marko Simic. (Find his project [here](https://www.simicm.com/hubcap/).)

Transcripts are stored in the data directory `data/docs`: For files that should be processed in advance.
Vector database `vectordb` is generated within the `data` folder for the project's functionality.

### Data Acquisition
* Episodes were downloaded using the [yt-dlp](https://github.com/yt-dlp/yt-dlp) tool.
* The obtained audio files were transcribed using OpenAI's [Whisper](https://github.com/openai/whisper) `medium.en model`.

## Usage
`Huberman Answers` is a project designed to run locally. 

To run it, go through the following steps:

1. Clone the repository and navigate to the project directory:
```python 
git clone https://github.com/NinoRisteski/HubermanAnswers.git
cd hubermananswers
```
2. Create and activate a new virtual environment:
```python
conda create --name hubermananswers python=3.9.6
conda activate hubermananswers
source venv/bin/activate
```
3. Install the requirements:
```python
pip install -r requirements.txt
```
4. Open `app_config.py` and fill in your OpenAI API key.
5. Run `upload_data_manually.py` to process data and create `vectordb`:
```python
python3 src/upload_data_manually.py
```
*Only initially to process the transcripts. Don't run it every time you run the app.*

6. Run the application:

* In Terminal 1:

```python
python3 src\serve.py
```
The `serve.py` module hosts the .vtt files in a server, making them accessible for user viewing. 

* In Terminal 2:

```python
python3 src\hubermananswers_app.py
```
*Don't forget to activate the environments in each terminal*

7. Finally, ask Huberman simple to complex questions and receive thoughtful answers along with the episode titles.

## Credits 
[Marko Simic](https://www.simicvm.com/)
* For creating the Huberman Lab transcripts dataset.
        
[Emanuel Risteski](https://www.linkedin.com/in/emanuelristeski/)
* For creating the visuals for the project.

Photo Credits: 
* I don't own the rights to the main black and white photo of Andrew Huberman. Photo credits go to [Huberman Lab.](https://www.hubermanlab.com/)

*This project is created for experimental purposes only and is not affiliated with Dr. Andrew Huberman. It is not intended for commercial use.*

## Contact
Reach out on [X](https://x.com/ninoristeski) or [LinkedIn](https://www.linkedin.com/in/nino-risteski/).
