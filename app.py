from pathlib import Path
import pandas as pd
import streamlit as st
import os          

#Web pages configuration
st.set_page_config(
    page_title = "Recommender System",
    page_icon = "📚" ,
)

st.sidebar.success("Select type of recommender system")
st.title("Welcome to our book recommender system")
st.title("How to use our system?")
st.title("Click the icon > that located at top left to start your navigation")