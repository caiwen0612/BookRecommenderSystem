import streamlit as st
import os
import pandas as pd
from model.content_model import recommend_book_CV,recommend_book_TFIDF
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
# st.set_page_config(
#     page_title = "Recommender System",
#     page_icon = "📚" ,
# )

st.title("Content based Recommender system")
st.write("""
Book Recommender System
""")

#Import dataset that had prepare by dataPreprocessing 
my_path_books = os.path.join(os.getcwd(), "dataset", "Final.csv")
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

if input_book_recommend_count:
    try:
        recommend_count = int(input_book_recommend_count)
    except ValueError:
        st.error('Please enter a valid integer value.')

#Provide a button let user click
button_recommend = st.button('Show Me What You Got!!')


#Validation for user input
isEmpty = False
if button_recommend:  
    if input_book_name.strip() == '':
        st.write("Please enter a book")
        isEmpty = True
    elif input_book_recommend_count.strip() == '':
        st.write("Please enter quantity")
        isEmpty = True

#Process input and generate result    
    if(isEmpty == False):
        with st.spinner('Loading... '):
            result_tfidf = recommend_book_TFIDF(input_book_name,input_book_recommend_count)
            
        
        #Display output
        st.success('Here is the list of recommendations for TFIDF algorithm, The first row indicate the book that u have input')

        #Display Final Result
        my_path_finalBook = os.path.join(os.getcwd(), "dataset", "Final.csv")
        data_result = pd.read_csv(my_path_finalBook, low_memory=False)
        result_df = pd.DataFrame({
        "Image": data_result['image_url'].iloc[result_tfidf].values,
        "Title": data_result['title'].iloc[result_tfidf].values,
        "Author": data_result['authors'].iloc[ result_tfidf].values
        }
        , columns = ["Image","Title","Author"])
        html_table = '<table><thead><tr><th>Book Image</th><th>Title</th><th>Author</th></tr></thead><tbody>'
        for i, row in result_df.iterrows():
            html_table += f'<tr><td><img src="{row["Image"]}"  /><td>{row["Title"]}</td></td><td>{row["Author"]}</td></tr>'
        html_table += '</tbody></table>'
        st.write(html_table, unsafe_allow_html=True)

        with st.spinner('Loading... for second recommendation '):
            result_cv = recommend_book_CV(input_book_name,input_book_recommend_count)
        
        st.write("")
        st.write("")
        #Display output
        st.success('Here is the list of recommendations for CountVectorizer algorithm, The first row indicate the book that u have input')
        #Display Final Result
        my_path_finalBook = os.path.join(os.getcwd(), "dataset", "Final.csv")
        data_result = pd.read_csv(my_path_finalBook, low_memory=False)
        result_df = pd.DataFrame({
        "Image": data_result['image_url'].iloc[result_cv].values,
        "Title": data_result['title'].iloc[result_cv].values,
        "Author": data_result['authors'].iloc[result_cv].values,
        }
        , columns = ["Image","Title","Author"])
        html_table = '<table><thead><tr><th>Book Image</th><th>Title</th><th>Author</th></tr></thead><tbody>'
        for i, row in result_df.iterrows():
            html_table += f'<tr><td><img src="{row["Image"]}"  /><td>{row["Title"]}</td></td><td>{row["Author"]}</td></tr>'
        html_table += '</tbody></table>'
        st.write(html_table, unsafe_allow_html=True)
