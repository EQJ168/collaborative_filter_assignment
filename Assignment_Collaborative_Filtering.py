import pandas as pd
import streamlit as st

st.title('Game Recommender System (Item-Based Collaborative Filtering)')

@st.cache  
def load_data():
    path = 'NewDataSet.csv'  # Game dataset
    df = pd.read_csv(path)
    path_user = 'User_Dataset.csv'  # User ratings dataset
    userset = pd.read_csv(path_user)
    
    # Merging the two datasets on the 'Title' column and removing missing values
    data = pd.merge(df, userset, on='Title').dropna()
    return data

data = load_data()

# Creating the user-score matrix for collaborative filtering
score_matrix = data.pivot_table(index='user_id', columns='Title', values='user_score', fill_value=0)

# List of game titles available
game_titles = score_matrix.columns.sort_values().tolist()

# User selects a game title for recommendation
game_title = st.selectbox("Select a game title to get recommendations", game_titles)

if game_title:
    # Retrieving the user scores for the selected game
    game_user_score = score_matrix[game_title]

    # Calculating the correlation of the selected game with other games
    similar_to_game = score_matrix.corrwith(game_user_score)
    
    # Creating a DataFrame to store the correlations
    corr_drive = pd.DataFrame(similar_to_game, columns=['Correlation']).dropna()

    # Displaying top similar games based on correlation
    st.subheader(f"Games similar to '{game_title}':")
    st.dataframe(corr_drive.sort_values('Correlation', ascending=False).head(10))

    # Filtering games that have more than 10 user ratings
    user_scores_count = data.groupby('Title')['user_score'].count().rename('total num_of_user_score')
    merged_corr_drive = corr_drive.join(user_scores_count, how='left')

    # Displaying games with high score correlations and more than 10 ratings
    st.subheader("Top Recommended Games with Sufficient Ratings:")
    high_score_corr = merged_corr_drive[merged_corr_drive['total num_of_user_score'] > 10].sort_values('Correlation', ascending=False).head()
    st.dataframe(high_score_corr)

else:
    st.info('Please select a game title from the dropdown to get recommendations.')
