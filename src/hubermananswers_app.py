import sys
sys.path.append('/Users/fliprise/HubermanAnswers')

import gradio as gr
from utils.chatbot import Chatbot
from utils.ui_settings import UISettings
import logging
# Set up logging configuration
logging.basicConfig(filename='app.log', level=logging.INFO)

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("HubermanLab Answers"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                with gr.Column(visible=False) as reference_bar:
                    ref_output = gr.Textbox(
                         lines=22,
                         max_lines=22,
                         interactive=False,
                         type="text",
                         label="Source",
                         show_copy_button=True
                     )

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        bubble_full_width=False,
                        height=500,
                        avatar_images=(
                            ("/Users/fliprise/HubermanAnswers/assets/ninor.png"), "/Users/fliprise/HubermanAnswers/assets/andrew.png"),
                        )
              
            ##############
            # SECOND ROW:
            ##############
            with gr.Row()as row_two:
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="How does body temperature affect high-performance and what cooling methods do you suggest?",
                    container=False,
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_three:
                text_submit_btn = gr.Button(value="Submit")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(
                    value="Source")
                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [
                    reference_bar, sidebar_state])
                temperature_bar = gr.Slider(minimum=0, maximum=1, value=0, step=0.1,
                                            label="Temperature", info="Choose between 0 and 1")
            ##############
            # Process:
            ##############
            txt_msg = input_txt.submit(fn=Chatbot.respond,
                                       inputs=[chatbot, input_txt,
                                                temperature_bar],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=Chatbot.respond,
                                            inputs=[chatbot, input_txt,
                                                    temperature_bar],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":
    logging.info("Starting the application")
    demo.launch()