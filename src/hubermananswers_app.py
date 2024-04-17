import gradio as gr
from utils.chatbot import Chatbot
from utils.ui_settings import UISettings

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("Huberman Answers"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                with gr.Column(visible=False) as reference_bar:
                    ref_output = gr.Markdown()
                    # ref_output = gr.Textbox(
                    #     lines=22,
                    #     max_lines=22,
                    #     interactive=False,
                    #     type="text",
                    #     label="References",
                    #     show_copy_button=True
                    # )

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        bubble_full_width=False,
                        height=500,
                        avatar_images=(
                            ("assets/ninor.png"), "assets/andrew.png"),
                    )
              
            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Ask a question...",
                    container=False,
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit text")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(
                    value="References")
                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [
                    reference_bar, sidebar_state])
                temperature_bar = gr.Slider(minimum=0, maximum=1, value=0, step=0.1,
                                            label="Temperature", info="Choose between 0 and 1")
            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.process_uploaded_files, inputs=[
                upload_btn, chatbot, rag_with_dropdown], outputs=[input_txt, chatbot], queue=False)

            txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown, temperature_bar],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=Chatbot.respond,
                                            inputs=[chatbot, input_txt,
                                                    rag_with_dropdown, temperature_bar],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":
    demo.launch()