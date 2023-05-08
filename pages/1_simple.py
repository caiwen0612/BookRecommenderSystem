import streamlit as st
import os
import pandas as pd
from model.simple_model import recommend_book_review,recommend_book_author,recommend_book_year,recommend_book_rating

st.title("Simple Recommender System")
st.write("""
Book Recommender System
""")

#Choose the type of recommender System
result_type = st.selectbox(
    'Select the result type', 
    ["Author", "Year", "Best Overall", "Most Reviewed"]
)
#Year and Author need input
#Rating, review no need input


#Import dataset that had prepare by dataPreprocessing 
my_path_books = os.path.join(os.getcwd(), "dataset", "Final.csv")
data_books = pd.read_csv(my_path_books, low_memory=False)

#COPY DATASET TO MODIFY dataset to make input more reasonable
data_books2 = data_books.copy()
data_books2 = data_books['original_publication_year'].astype('Int64').tolist()
inputValue2 = data_books2.insert(0, '')

data_books3 = data_books.copy()
data_books3 = data_books['authors'].tolist()
inputValue3 = data_books3.insert(0, '')

# Request user input
if(result_type == "Year" ):
    input_book_year = st.selectbox('Enter a year',data_books2)
if(result_type == "Author"):
    input_book_author = st.selectbox('Enter the name of the author: ',data_books3)

input_book_recommend_count = st.text_input('Enter how much you want the system to recommend: ')
button_recommend = st.button('Show Me What You Got!!')

resultDone = False
result_simple = []
if button_recommend and result_type == "Best Overall":
    with st.spinner('Loading...Best Overall'):
        result_simple = recommend_book_review(input_book_recommend_count)
        resultDone = True
elif button_recommend and result_type == "Author":
    with st.spinner('Loading... Author'):
        result_simple = recommend_book_author(input_book_author,input_book_recommend_count)
        resultDone = True
elif button_recommend and result_type == "Year":
    with st.spinner('Loading... Year'):
        result_simple = recommend_book_year(input_book_year,input_book_recommend_count)
        resultDone = True
elif button_recommend and result_type == "Most Reviewed":
    with st.spinner('Loading... Most Reviewed'):
        result_simple = recommend_book_rating(input_book_recommend_count)
        resultDone = True

st.dataframe(result_simple)

# if resultDone == True:
#     #Display result
#     my_path_finalBook = os.path.join(os.getcwd(), "dataset", "simpleData.csv")
#     data_result = pd.read_csv(my_path_finalBook, low_memory=False)
#     result_df = pd.DataFrame({
#             "Image": data_result['image_url'].iloc[result_simple].values,
#             "Title": data_result['title'].iloc[result_simple].values,
#             "Author": data_result['authors'].iloc[result_simple].values,
#             # "Scores": data_result['book_score'].iloc[result_simple].values
#             }, columns = ["Image","Title","Author"])
#     html_table = '<table><thead><tr><th>Book Image</th><th>Title</th><th>Author</th><th>Score</th></tr></thead><tbody>'
#     for i, row in result_df.iterrows():
#         html_table += f'<tr><td><img src="{row["Image"]}"  /><td>{row["Title"]}</td></td><td>{row["Author"]}</td></tr>'
#     html_table += '</tbody></table>'
#     st.write(html_table, unsafe_allow_html=True)
