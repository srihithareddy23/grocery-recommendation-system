#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/Lawrence-Krukrubo/Building-a-Content-Based-Movie-Recommender-System/blob/master/building_a_content_based_recommendation_system.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# <h1 align="center"><font size="5">CONTENT-BASED FILTERING</font></h1>

# Recommendation systems are a collection of algorithms used to recommend items to users based on information taken from the user. These systems have become ubiquitous, and can be commonly seen in online stores, movies databases and job finders. In this notebook, we will explore Content-based recommendation systems and implement a simple version of one using Python and the Pandas library.

# In[1]:


# For creating and manipulating structured tabular data
import pandas as pd
pd.options.mode.chained_assignment = None  
import joblib
def fun(num):


    # Let's set maximum rows to be displayed at any time to not more than 20

    # In[2]:


    pd.set_option('max_rows', 20)


    # ### Saving the raw files from github
    # 
    # Both files have been saved in raw .csv format in  the code cell below, but if you want to download directly from the website, click this [link](https://grouplens.org/datasets/movielens/) and <br>
    # Select the file name 'ml-latest-small.zip (size: 1 MB)'

    # In[3]:


    grocery_data = 'C:/Users/snigdha\Documents/miniproject-master/models_and_data/grocery.csv'
    history_data='C:/Users/snigdha\Documents/miniproject-master/models_and_data/history.csv'


    # ### Defining additional NaN values

    # In[4]:


    missing_values = ['na','--','?','-','None','none','non']


    # ### Reading the data to the data frame

    # In[5]:


    grocery_df = pd.read_csv(grocery_data, na_values=missing_values)
    history_df = pd.read_csv(history_data, na_values=missing_values)


    # In[6]:


    print('grocery_df Shape:',grocery_df.shape)
    grocery_df


    # In[ ]:





    # ### Let's first explore and prepare the movies_df

    # Let's remove the year from the title column and place it in its own column, using the handy [extract](http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.extract.html) function of pandas, alongside python regex.

    # In[ ]:





    # In[ ]:





    # In[ ]:





    # In[7]:


    grocery_df['Category'] = grocery_df.Category.str.split('/')
    grocery_df.head()


    # With that, let's also split the values in the Genres column into a list of Genres to simplify future use. This can be achieved by applying Python's split string function on the correct column.

    # In[ ]:





    # Let's view summary of the data, the memory consumption and if the titles are arranged logically

    # In[8]:


    grocery_df.info()


    # In[9]:


    grocery_df_original_mem = grocery_df.memory_usage()
    grocery_df_original_mem


    # In[ ]:





    # Let's check for missing values

    # In[10]:


    grocery_df.isna().sum()


    # let's fill movies_df missing year  values with 0 to indicate the year is not readily available. we have only 13 rows 

    # In[ ]:





    # In[ ]:





    # In[ ]:





    # Let's see a summary of the data types again

    # In[ ]:





    # In[ ]:





    # Now, let's  One-Hot-Encode the list of genres. This encoding is needed for feeding categorical data. In this case, we store every different genre in columns that contain either 1 or 0. 1 shows that a movie has that genre and 0 shows that it doesn't. Let's also store this dataframe in another variable, just incase we need the one without genres at some point.
    # 

    # In[11]:


    # First let's make a copy of the movies_df
    grocery_with_Category = grocery_df.copy(deep=True)
    x = []
    for index, row in grocery_df.iterrows():
        x.append(index)
        for Category in row['Category']:
            grocery_with_Category.at[index, Category] = 1

    # Confirm that every row has been iterated and acted upon
    print(len(x) == len(grocery_df))

    grocery_with_Category.head(3)


    # In[12]:


    #Filling in the NaN values with 0 to show that a movie doesn't have that column's genre
    grocery_with_Category = grocery_with_Category.fillna(0)
    grocery_with_Category.head(3)


    # Let's look at the ratings data set now

    # In[13]:


    # print out the shape and first five rows of ratings data.
    print('grocery_df shape:',grocery_df.shape)          
    grocery_df.head()


    # In[ ]:





    # In[14]:


    # Let's confirm the right data types exist per column in ratings data_set

    grocery_df.dtypes


    # In[15]:


    # Let's check for missing values

    grocery_df.isna().sum()


    # ## Content Based recommender System

    # Now, let's implement a Content-Based or Item-Item recommendation systems. This technique attempts to figure out what a user's favourite aspects of an item is, and then recommends items that present those aspects. 
    # 
    # Let's begin by creating an input user to recommend movies to. The user's name will be Lawrence and we would assume Lawrence has rated the following movies with the following ratings:-
    # 
    # Notice: To add more movies, simply increase the amount of elements in the userInput. Feel free to add more in! Just be sure to write it in with capital letters and if a movie starts with a "The", like "The Matrix" then write it in like this: 'Matrix, The' .

    # Step 1: Creating Lawrence's Profile

    # In[16]:
    


    Lawrence_history_data = [
                {'CustomerID':num}
            ] 
    Lawrence_history_data = pd.DataFrame(Lawrence_history_data) 
    Lawrence_history_data



    # Add movieId to input user
    # With the input complete, let's extract the input movie's ID's from the movies dataframe and add them into it.
    # 
    # We can achieve this by first filtering out the rows that contain the input movie's title and then merging this subset with the input dataframe. We also drop unnecessary columns for the input to save memory space.

    # In[17]:



    # Extracting movie Ids from movies_df and updating lawrence_movie_ratings with movie Ids.

    Lawrence_movie_Id = history_df[history_df['CustomerID'].isin(Lawrence_history_data['CustomerID'])]



    # Merging Lawrence movie Id and ratings into the lawrence_movie_ratings data frame. 
    # This action implicitly merges both data frames by the title column.

    Lawrence_history_data = pd.merge(Lawrence_movie_Id, Lawrence_history_data)

    # Display the merged and updated data frame.

    Lawrence_history_data




    # Lets drop some columns that we do not need such as genres and year

    # In[ ]:





    # Step 2: Learning Lawrence's Profile

    # We're going to start by learning the input's preferences, so let's get the subset of movies that the input has watched from the Dataframe containing genres defined with binary values.

    # In[18]:


    # filter the selection by outputing movies that exist in both lawrence_movie_ratings and movies_with_genres
    Lawrence_genres_df = grocery_with_Category[grocery_with_Category.Title.isin(Lawrence_history_data.Title)]
    Lawrence_genres_df


    # We'll only need the actual genre table, so let's clean this up a bit by resetting the index and dropping the movieId, title, genres and year columns.

    # In[19]:


    # First, let's reset index to default and drop the existing index.
    Lawrence_genres_df.reset_index(drop=True, inplace=True)

    # Next, let's drop redundant columns
    Lawrence_genres_df.drop(['ItemID','Title','Category'], axis=1, inplace=True)

    # Let's view chamges

    Lawrence_genres_df


    # Step 3: Building Lawrence's Profile<br>
    # To do this, we're going to turn each genre into weights, by multiplying Lawrence's movie ratings by lawrence_genres_df table. And then summing up the resulting table by column. This operation is actually a dot product between a matrix and a vector.
    # First let's confirm the shapes of the data frames we have recently defined

    # In[ ]:





    # In[20]:


    # Let's find the dot product of transpose of Lawrence_genres_df by lawrence rating column
    Lawrence_profile = Lawrence_genres_df.sum()

    # Let's see the result
    Lawrence_profile


    # Just by Eye-balling his profile, it is clear that Lawrence loves 'Thriller', 'Action' and 'Horror' movies the most… apt as can be.<br>
    # Now, we have the weights for all his preferences. This is known as the User Profile. We can now recommend movies that satisfy Lawrence.<br>
    # Let's start by editing the original movies_with_genres data frame that contains all movies and their genres columns.

    # Step 4: Deploying The Content-Based Recommender System.

    # In[21]:


    # let's set the index to the movieId
    grocery_with_Category = grocery_with_Category.set_index(grocery_with_Category.ItemID)

    # let's view the head
    grocery_with_Category.head()


    # Let's delete irrelevant columns from the movies_with_genres data frame that contains all 9742 movies and distinctive columns of genres.

    # In[22]:


    # Deleting four unnecessary columns.
    grocery_with_Category.drop(['ItemID','Title','Category'], axis=1, inplace=True)

    # Viewing changes.
    grocery_with_Category.head()


    # With Lawrence's profile and the complete list of movies and their genres in hand, we're going to take the weighted average of every movie based on his profile and recommend the top twenty movies that match his preference.

    # In[23]:


    # Multiply the genres by the weights and then take the weighted average.

    recommendation_table_df = (grocery_with_Category.dot(Lawrence_profile)) / Lawrence_profile.sum()

    # Let's view the recommendation table
    recommendation_table_df.head(20)


    # Let's sort the recommendation table in descending order

    # In[24]:


    # Let's sort values from great to small
    recommendation_table_df.sort_values(ascending=False, inplace=True)

    #Just a peek at the values
    recommendation_table_df.head(30)


    # Now here's the recommendation table! Complete with movie details and genres for the top 20 movies that match Lawrence's profile.

    # In[89]:


    # first we make a copy of the original movies_df
    copy = grocery_df.copy(deep=True)

    # Then we set its index to movieId
    copy = copy.set_index('ItemID', drop=True)

    # Next we enlist the top 20 recommended movieIds we defined above
    top_20_index = recommendation_table_df.index[:30].tolist()

    # finally we slice these indices from the copied movies df and save in a variable
    recommended_movies = copy.loc[top_20_index, :]
    filename='finalized_model.sav'
    joblib.dump(recommended_movies,filename)

# Now we can display the top 20 movies in descending order of preference

    return recommended_movies





# In[ ]:





# In[ ]:





# Run this cell below to kill the note book and free up space in colab

# In[ ]:


#import os, signal
#os.kill(os.getpid(), signal.SIGKILL)

