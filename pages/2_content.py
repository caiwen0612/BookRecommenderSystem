import streamlit as st
import os
import pandas as pd
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

#Python Function
def recommend_book_TFIDF(input_book_name,input_book_recommend_count):
    #Read final csv files process
    my_path_finalBook = os.path.join(os.getcwd(), "dataset", "Final.csv")
    df_book = pd.read_csv(my_path_finalBook, low_memory=False)

    tfidf = TfidfVectorizer(analyzer = 'word', lowercase=True, ngram_range = (1,2), min_df = 0, stop_words = 'english')
    tfidf.fit(df_book['keywords'])

    matrix_tfidf = tfidf.fit_transform(df_book['keywords'])
    cosine_sim_tfidf = cosine_similarity(matrix_tfidf, matrix_tfidf)

    series_tfidf = pd.Series(df_book.index, index = df_book['title'])
    user_book_id_tfidf = series_tfidf[input_book_name]
    # #TODO :?
    # feature_array_tfidf = np.squeeze(matrix_tfidf[user_book_id_tfidf].toarray()) 
    # idx_tfidf = np.where(feature_array_tfidf > 0)

    n = int(input_book_recommend_count)
    top_idx_tfidf = np.flip(np.argsort(cosine_sim_tfidf[user_book_id_tfidf,]), axis = 0)[0:n]
    top_sim_values_tfidf = cosine_sim_tfidf[user_book_id_tfidf, top_idx_tfidf]
    ##Make sure the 1.0 result which is input did not put in
    top_idx_tfidf = top_idx_tfidf[top_sim_values_tfidf  > 0] 
    scores = top_sim_values_tfidf[top_sim_values_tfidf  > 0] 

    return top_idx_tfidf

def recommend_book_CV(input_book_name,input_book_recommend_count):
     #Read final csv files process
    my_path_finalBook = os.path.join(os.getcwd(), "dataset", "Final.csv")
    df_book = pd.read_csv(my_path_finalBook, low_memory=False)

    cv = CountVectorizer(analyzer='word', lowercase=True, stop_words = 'english',ngram_range = (1,2), min_df = 0.002)
    cv.fit(df_book['keywords'])

    matrix_cv = cv.fit_transform(df_book['keywords'])
    cosine_sim_cv = cosine_similarity(matrix_cv,matrix_cv)

    series_cv = pd.Series(df_book.index, index = df_book['title'])
    user_book_id_cv = series_cv[input_book_name]
    # #TODO :?
    # feature_array_cv = np.squeeze(matrix_cv[user_book_id_cv].toarray()) 
    # idx_cv = np.where(feature_array_cv > 0)

    n =  int(input_book_recommend_count) #how many books to be recommended
    #np.argsort = ascending order
    #flip = inverse the order so can get the descending order
    top_idx_cv = np.flip(np.argsort(cosine_sim_cv[user_book_id_cv,]), axis = 0)[0:n]
    top_sim_values_cv = cosine_sim_cv[user_book_id_cv, top_idx_cv]

    top_idx_cv = top_idx_cv[top_sim_values_cv  > 0] ## Index
    scores_cv = top_sim_values_cv[top_sim_values_cv  > 0] ## Score

    return top_idx_cv


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
        
        #Display output
        st.success('Here is the list of recommendations for CountVectorizer algorithm, The first row indicate the book that u have input')
        #Display Final Result
        my_path_finalBook = os.path.join(os.getcwd(), "dataset", "Final.csv")
        data_result = pd.read_csv(my_path_finalBook, low_memory=False)
        result_df = pd.DataFrame({
        "Image": data_result['image_url'].iloc[result_cv].values,
        "Title": data_result['title'].iloc[result_cv].values,
        "Author": data_result['authors'].iloc[result_cv].values
        }
        , columns = ["Image","Title","Author"])
        html_table = '<table><thead><tr><th>Book Image</th><th>Title</th><th>Author</th></tr></thead><tbody>'
        for i, row in result_df.iterrows():
            html_table += f'<tr><td><img src="{row["Image"]}"  /><td>{row["Title"]}</td></td><td>{row["Author"]}</td></tr>'
        html_table += '</tbody></table>'
        st.write(html_table, unsafe_allow_html=True)
