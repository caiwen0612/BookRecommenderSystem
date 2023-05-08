import numpy as np
import os
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

#Get books
my_path_books = os.path.join(os.getcwd(), "dataset", "books.csv")
data_books = pd.read_csv(my_path_books, low_memory=False)

#Get ratings
my_path_ratings = os.path.join(os.getcwd(), "dataset", "ratings.csv")
data_ratings = pd.read_csv(my_path_ratings, low_memory=False)

bookID_merged = pd.merge(data_ratings, data_books, on="book_id")

combine_book_rating = bookID_merged.dropna(axis=0, subset=['title'])
combine_book_rating = combine_book_rating.drop_duplicates(subset=['title', 'user_id'])

book_ratingCount = (combine_book_rating.
     groupby(by=['title'])['rating'].
     count().
     reset_index().
     rename(columns={'rating': 'totalRatingCount'})
     [['title', 'totalRatingCount']]
)

book_ratingCount = pd.merge(book_ratingCount, bookID_merged[["title", "authors", "image_url", "small_image_url"]], on='title', how='left')
book_ratingCount = book_ratingCount.drop_duplicates(subset=['title']).reset_index(drop=True)


my_path_new = os.path.join(os.getcwd(), "dataset", "collab.csv")
book_ratingCount.to_csv(my_path_new, index=False)

rating_with_totalRatingCount = combine_book_rating.merge(book_ratingCount, left_on = 'title', right_on = 'title', how = 'left')

# pd.set_option('display.float_format', lambda x: '%.3f' % x)
# print(book_ratingCount['totalRatingCount'].describe())

#only considering books with >= 50 ratings
popularity_threshold = 50

rating_popular_books= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')

## Create user-item matrix
books_features_df = rating_popular_books.pivot_table(index='title',columns='user_id',values='rating').fillna(0)
## Data normalization 
books_features_norm_df = books_features_df.subtract(books_features_df.mean(axis = 1), axis = 'rows')




books_features_df_matrix = csr_matrix(books_features_norm_df.values)

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(books_features_df_matrix)

def recommend_book_cf(input_recommendation_book,input_recommendation_amount):
    n = int(input_recommendation_amount)
    n_neighbors = n + 1
    # fetch index
    query_index = np.where(books_features_norm_df.index == input_recommendation_book)[0][0]
    # check index and name
    #print(query_index, book_name)
    distances, indices = model_knn.kneighbors(books_features_norm_df.
                                              iloc[query_index,:].
                                              values.reshape(1, -1), 
                                              n_neighbors)
    
    # get recommendation    
    recommendations = []
    resultIndex = []
    for i in range(1, len(distances.flatten())):
        book_index = indices.flatten()[i]
        book_title = books_features_norm_df.index[book_index]
        recommendations.append((i, book_index, book_title))
        resultIndex.append(book_index)

    
    recommendations_df = pd.DataFrame(recommendations, columns=["#", "Index", "Book Title"])
    recommendations_df.set_index("#", inplace=True)
    print("Recommendations for {}:\n".format(books_features_norm_df.index[query_index]))
    print(recommendations_df)

    return resultIndex