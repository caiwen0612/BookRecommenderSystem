import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#TODO GENERAL FOR TFIDF AND CV
my_path_finalBook = os.path.join(os.getcwd(), "dataset", "Final.csv")
df_book = pd.read_csv(my_path_finalBook, low_memory=False)
series = pd.Series(df_book.index, index = df_book['title'])

#TODO:TFIDF
tfidf = TfidfVectorizer(analyzer = 'word', lowercase=True, ngram_range = (1,2), min_df = 0, stop_words = 'english')
tfidf.fit(df_book['keywords'])
matrix_tfidf = tfidf.fit_transform(df_book['keywords'])
cosine_sim_tfidf = cosine_similarity(matrix_tfidf, matrix_tfidf)

#TODO: CV
# #Read final csv files process
cv = CountVectorizer(analyzer='word', lowercase=True, stop_words = 'english',ngram_range = (1,2), min_df = 0.002)
cv.fit(df_book['keywords'])
matrix_cv = cv.fit_transform(df_book['keywords'])
cosine_sim_cv = cosine_similarity(matrix_cv,matrix_cv)

# Python Function
def recommend_book_TFIDF(input_book_name,input_book_recommend_count):
    user_book_id_tfidf = series[input_book_name]
    n = int(input_book_recommend_count)
    top_idx_tfidf = np.flip(np.argsort(cosine_sim_tfidf[user_book_id_tfidf,]), axis = 0)[0:n]
    top_sim_values_tfidf = cosine_sim_tfidf[user_book_id_tfidf, top_idx_tfidf]
    top_idx_tfidf = top_idx_tfidf[top_sim_values_tfidf  > 0] 
    scores = top_sim_values_tfidf[top_sim_values_tfidf  > 0] 

    return top_idx_tfidf

def recommend_book_CV(input_book_name,input_book_recommend_count):
    user_book_id_cv = series[input_book_name]
    n =  int(input_book_recommend_count) #how many books to be recommended
    top_idx_cv = np.flip(np.argsort(cosine_sim_cv[user_book_id_cv,]), axis = 0)[0:n]
    top_sim_values_cv = cosine_sim_cv[user_book_id_cv, top_idx_cv]
    top_idx_cv = top_idx_cv[top_sim_values_cv  > 0] ## Index
    scores_cv = top_sim_values_cv[top_sim_values_cv  > 0] ## Score

    return top_idx_cv


