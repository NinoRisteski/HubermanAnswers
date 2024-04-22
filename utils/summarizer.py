from langchain_core.documents import Document
from utilities import count_num_tokens
import openai


class Summarizer:

    @staticmethod
    def summarize_the_podcast_episode(
        file_dir: str,
        max_final_token: int,
        token_threshold: int,
        gpt_model: str,
        temperature: float,
        summarizer_llm_system_role: str,
        final_summarizer_llm_system_role: str,
        character_overlap: int
    ):
        docs = []
        docs.extend(Document(file_dir).load())
        print(f"Podcast episode length: {len(docs)}")
        max_summarizer_output_token = int(
            max_final_token/len(docs)) - token_threshold
        full_summary = ""
        counter = 1
        print("Generating the summary...")
        
        full_summary = docs[0].page_content

        print(f"Podcast episode was summarized. ", end="")
        counter += 1
        print("\nFull summary token length:", count_num_tokens(
            full_summary, model=gpt_model))
        final_summary = Summarizer.get_llm_response(
            gpt_model,
            temperature,
            final_summarizer_llm_system_role,
            prompt=full_summary
        )
        return final_summary

    @staticmethod
    def get_llm_response(gpt_model: str, temperature: float, llm_system_role: str, prompt: str):

        response = openai.ChatCompletion.create(
            engine=gpt_model,
            messages=[
                {"role": "system", "content": llm_system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content