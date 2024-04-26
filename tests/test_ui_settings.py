import pytest
import gradio as gr
from utils.ui_settings import UISettings  

def test_toggle_sidebar():
    # Test when the initial state is True
    initial_state_true = True
    expected_output_true = (gr.update(visible=False), False)
    assert UISettings.toggle_sidebar(initial_state_true) == expected_output_true, "Failed when initial state is True"

    # Test when the initial state is False
    initial_state_false = False
    expected_output_false = (gr.update(visible=True), True)
    assert UISettings.toggle_sidebar(initial_state_false) == expected_output_false, "Failed when initial state is False"
