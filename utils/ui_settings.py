import gradio as gr

class UISettings:
    @staticmethod
    def toggle_sidebar(state):
        state = not state
        return gr.update(visible=state), state