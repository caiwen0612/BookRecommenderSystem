import streamlit as st
import os
import pandas as pd
from model.collaborative_model import recommend_book_cf

st.title("Collaborative Recommender System")
st.write("""
Book Recommender System
""")

#Import dataset that had prepare by dataPreprocessing 
my_path_books = os.path.join(os.getcwd(), "dataset", "collab.csv")
data_books = pd.read_csv(my_path_books, low_memory=False)

#COPY DATASET TO MODIFY dataset to make input more reasonable
data_books2 = data_books.copy()
data_books2 = data_books['title'].tolist()
inputValue = data_books2.insert(0, '')

 #Request input from user
input_book_name = st.selectbox(
    'Enter a book',
    data_books2
)
input_book_recommend_count = st.text_input('Enter how much you want the system to recommend: ')
button_recommend = st.button('Show Me What You Got!!')
if button_recommend:
    with st.spinner('Loading... '):
        result_cf = recommend_book_cf(input_book_name,input_book_recommend_count)

        my_path_finalBook = os.path.join(os.getcwd(), "dataset", "Final.csv")
        data_result = pd.read_csv(my_path_finalBook, low_memory=False)
        result_df = pd.DataFrame({
        "Image": data_result['image_url'].iloc[result_cf].values,
        "Title": data_result['title'].iloc[result_cf].values,
        "Author": data_result['authors'].iloc[ result_cf].values
        }, columns = ["Image","Title","Author"])
        html_table = '<table><thead><tr><th>Book Image</th><th>Title</th><th>Author</th></tr></thead><tbody>'
        for i, row in result_df.iterrows():
            html_table += f'<tr><td><img src="{row["Image"]}"  /><td>{row["Title"]}</td></td><td>{row["Author"]}</td></tr>'
        html_table += '</tbody></table>'
        st.write(html_table, unsafe_allow_html=True)
