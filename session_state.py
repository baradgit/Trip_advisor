import streamlit as st

def initialize_session_state(key, value):
    """Initialize a session state variable with a default value if it is not already set."""
    if key not in st.session_state:
        st.session_state[key] = value
