
import os
import pandas as pd

def dataPreparation():
    #TODO: Import dataset
    my_path_books = os.path.join(os.getcwd(), "dataset", "books.csv")
    data_books = pd.read_csv(my_path_books, low_memory=False)

    my_path_book_tags = os.path.join(os.getcwd(), "dataset", "book_tags.csv")
    data_book_tags = pd.read_csv(my_path_book_tags, low_memory=False)

    my_path_tags = os.path.join(os.getcwd(), "dataset", "tags.csv")
    data_tags = pd.read_csv(my_path_tags, low_memory=False)

    #TODO : Data Preprocessing
    #Cleaning duplicate data
    data_book_tags = data_book_tags.drop_duplicates(keep=False)
    
    #Converting data type
    #book
    data_books['isbn'] = data_books['isbn'].astype('string')
    data_books['authors'] = data_books['authors'].astype('string')
    data_books['original_title'] = data_books['original_title'].astype('string')
    data_books['title'] = data_books['title'].astype('string')
    data_books['language_code'] = data_books['language_code'].astype('string')
    data_books['image_url'] = data_books['image_url'].astype('string')
    data_books['small_image_url'] = data_books['small_image_url'].astype('string')
    #tag
    data_tags['tag_name'] = data_tags['tag_name'].astype('string')

    #Clean null data
    data_books.fillna('', inplace=True)

    #Drop useless column
    #TODO : Turn on this again
    data_books = data_books.drop(columns = ['work_id', 'books_count', 'isbn',
       'isbn13', 'average_rating', 'ratings_count',
       'work_ratings_count', 'work_text_reviews_count', 'ratings_1',
       'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5', 
       'small_image_url'])
    
    #TODO: Merge Dataset
    #Merge book_tag and data_tag
    data_merge = pd.merge(data_book_tags, data_tags, on='tag_id', how = 'inner')

    #Group all separate tag into one column
    data_merge = data_merge.groupby('goodreads_book_id')['tag_name'].apply(' '.join).reset_index()

    #Merge book with tag
    df_book = pd.merge(data_books,data_merge,left_on='book_id', right_on='goodreads_book_id' ,how = 'inner')

    #Merge title and tag form keyword column
    df_book['keywords'] = df_book['title'] + ' ' + df_book['tag_name']

    #TODO: SAVE FILE INTO FINAL
    my_path_new = os.path.join(os.getcwd(), "dataset", "Final.csv")
    df_book.to_csv(my_path_new, index=False)

dataPreparation()