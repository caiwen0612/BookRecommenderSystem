import numpy as np
import pandas as pd
import os
import sage as sg

my_path_books = os.path.join(os.getcwd(), "dataset", "books.csv")
data_books = pd.read_csv(my_path_books)

#dropna()to remove null values from dataframe
data_books = data_books.dropna()

#drop data from two column, imageurl and smallimageurl 
data_books = data_books.drop(columns=['small_image_url'])
print(data_books.shape)

#drop_duplicates() used to remove duplicate rows from dataframe
ratings = os.path.join(os.getcwd(), "dataset", "ratings.csv")
ratings = pd.read_csv(ratings)
ratings = ratings.drop_duplicates()

tags = os.path.join(os.getcwd(),"dataset","tags.csv")
tags = pd.read_csv(tags)
booktags = os.path.join(os.getcwd(),"dataset","book_tags.csv")
booktags = pd.read_csv(booktags)
tags_join_DF = pd.merge(booktags, tags, left_on= 'tag_id', right_on= 'tag_id', how='inner')
toRead = os.path.join(os.getcwd(),"dataset","to_read.csv")
toRead = pd.read_csv(toRead)

#group rater that have less than 5 count into unwantedusers
unwantedusers = ratings.groupby('user_id')['user_id'].count()
unwantedusers = unwantedusers[unwantedusers < 5]


#drop ratings from unwantedusers out from the column
unwantedratings = ratings[ratings.user_id.isin(unwantedusers.index)]
newratings = ratings.drop(unwantedratings.index)


mergeBook = data_books.merge(newratings, on='book_id')

# sort ratings_count first then average_rating both in ascending order
data_books.sort_values(by = ['ratings_count','average_rating'],ascending=[False,False])

#display the table include title,id,rate count and average rating only
df_databooks = data_books[['original_title','book_id','ratings_count','average_rating']]

#formula to calculate the minimum number of rate count that eligible to be in chart
minNumRate = df_databooks['ratings_count'].quantile(0.80)

#formula to calculate the mean of average rating
meanRate = df_databooks['average_rating'].mean()

#Books that are eligible will be move to a new dataframe
eligibleBook = data_books.copy().loc[df_databooks['ratings_count']>= minNumRate]


#Calculate the average rating and the count rate accumulated = weighted rating
def weightedRating(x, m =minNumRate, C=meanRate):
    
    v = x['ratings_count']
    R = x['average_rating']
    
    return ( v/(v+m)*R)+(m/(m+v)*C)

eligibleBook['book_score']=eligibleBook.apply(weightedRating, axis=1)
#convert it to csv files
my_path_new = os.path.join(os.getcwd(), "dataset", "simpleData.csv")
eligibleBook.to_csv(my_path_new, index=False)


#Top 10 Book based on book score
#recommend the top 10 book that based on book score in ascending order
def recommend_book_review(input_book_recommend_count):
    tenBook= eligibleBook[["original_title",'book_id','original_publication_year','book_score','isbn','authors']]
    tenBook= tenBook.sort_values('book_score',ascending = False)

    # result = int(tenBook.head(input_book_recommend_count).index[0])
    # return result

#Top 10 Book based on author with good score
#required user to enter an author's name
def recommend_book_author(input_author_name,input_book_recommend_count):
    #recommend the top 10 book that based on the name of the author entered earlier along with good book score in ascending order
    input1 = [input_author_name]
    result1 = eligibleBook[eligibleBook['authors'].isin(input1)]
    authorBook = result1[['authors','original_title','book_id','original_publication_year','average_rating','isbn','book_score']]
    authorBook = authorBook.sort_values('book_score',ascending=False)
    return authorBook.head(input_book_recommend_count).id.get_loc()

#Top 10 Book based on publish year with good score
#required user to enter the year that the book is publish within the range
def recommend_book_year(publishYear,input_book_recommend_count):
    #recommend the top 10 book that is publish within the range of year entered by user along with good book score in ascending order
    input2 = [publishYear]
    result2 = eligibleBook[eligibleBook['original_publication_year'].isin(input2)]
    yearBook = result2[['original_publication_year','original_title','book_id','average_rating','authors','book_score']]
    yearBook = yearBook.sort_values('book_score',ascending= False)
    eligibleBook['book_id'] = eligibleBook['book_id'].astype('string').tolist()
    return yearBook.head(input_book_recommend_count)['book_id'].tolist()
    #return yearBook.head(input_book_recommend_count).index

#Top 10 most review book
#recommend the most reviwed book along with good book score in ascending order
def recommend_book_rating(input_book_recommend_count):
    ratingsCount= eligibleBook[['ratings_count','original_title','book_id','original_publication_year','average_rating','authors','book_score']]
    # ratingsCount= ratingsCount.sort_values('ratings_count',ascending= False)
    # return ratingsCount.head(input_book_recommend_count).index
    top_books = ratingsCount.head(input_book_recommend_count)
    return top_books



