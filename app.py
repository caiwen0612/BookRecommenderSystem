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

# st.set_page_config(initial_sidebar_state = "collapsed")

#Page STYLE
# st.markdown()

#Page Elements
# change = st.button("Change")
# if change: 
#     switch_page("Test")

my_path_books = os.path.join(os.getcwd(), "dataset", "books.csv")
data_books = pd.read_csv(my_path_books, low_memory=False)