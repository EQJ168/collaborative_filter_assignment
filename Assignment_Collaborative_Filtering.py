import pandas as pd
import streamlit as st

st.title('Games You May Like (Personalized Recommendations)')

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

# List of users available
user_ids = score_matrix.index.sort_values().tolist()

# Select a user to provide recommendations
user_id = st.selectbox("Select your user ID to get personalized game recommendations", user_ids)

if user_id:
    # Retrieve the user's ratings
    user_ratings = score_matrix.loc[user_id]
    
    # Filtering out games the user has not rated (where score is 0)
    user_ratings = user_ratings[user_ratings > 0]

    st.subheader(f"Games you've rated:")
    st.write(user_ratings.sort_values(ascending=False))

    # Find games that are similar to the ones the user has rated
    similar_games = pd.Series(dtype=float)  # Initialize as empty series
    
    for game in user_ratings.index:
        # Get correlation for each rated game
        similar_to_game = score_matrix.corrwith(score_matrix[game])
        
        # Concatenate the Series for each game to the list of similar games
        similar_games = pd.concat([similar_games, similar_to_game])

    # Group by game title and sum up the correlations
    similar_games = similar_games.groupby(similar_games.index).mean()
    
    # Remove games the user has already rated
    similar_games = similar_games.drop(user_ratings.index, errors='ignore')

    # Convert the Series to DataFrame and sort by correlation
    recommended_games = pd.DataFrame(similar_games, columns=['Correlation']).dropna().sort_values('Correlation', ascending=False)
    
    st.subheader("Games You May Like (Recommended):")
    st.dataframe(recommended_games.head(10))

    # Filtering games that have more than 10 user ratings for better recommendations
    user_scores_count = data.groupby('Title')['user_score'].count().rename('total num_of_user_score')
    merged_corr_drive = recommended_games.join(user_scores_count, how='left')

    st.subheader("Top Recommended Games with Sufficient Ratings:")
    high_score_corr = merged_corr_drive[merged_corr_drive['total num_of_user_score'] > 10].sort_values('Correlation', ascending=False).head()
    st.dataframe(high_score_corr)

else:
    st.info('Please select your user ID to get recommendations.')
