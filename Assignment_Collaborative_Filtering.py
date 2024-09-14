import pandas as pd
import streamlit as st

# Title of the application
st.title('Game Recommendation System (Collaborative Filtering)')

# Load datasets
@st.cache_data  # Use caching to speed up loading after the first run
def load_data():
    path = 'NewDataSet.csv'
    df = pd.read_csv(path)
    path_user = 'User_Dataset.csv'
    userset = pd.read_csv(path_user)
    data = pd.merge(df, userset, on='Title').dropna()  # Merge and drop missing values
    return data

data = load_data()

# Create a pivot table for user scores
score_matrix = data.pivot_table(index='user_id', columns='Title', values='user_score', fill_value=0)

# Dropdown menu for selecting a game title
game_titles = score_matrix.columns.sort_values().tolist()  # Sorting the game titles for better searchability
game_title = st.selectbox("Select a game title", game_titles)

# Collaborative Filtering (Item-based)
if game_title:
    # Get user scores for the selected game
    game_user_score = score_matrix[game_title]

    # Compute similarity with other games (Item-based collaborative filtering)
    similar_to_game = score_matrix.corrwith(game_user_score)
    
    # Convert correlation results into a DataFrame
    corr_drive = pd.DataFrame(similar_to_game, columns=['Correlation']).dropna()

    # Display correlations for the selected game
    st.subheader(f"Games similar to '{game_title}':")
    st.dataframe(corr_drive.sort_values('Correlation', ascending=False).head(10))

    # Join with the user score count to filter out games with too few ratings
    user_scores_count = data.groupby('Title')['user_score'].count().rename('total num_of_user_score')
    merged_corr_drive = corr_drive.join(user_scores_count, how='left')

    # Filter games that have more than a threshold number of ratings (to improve reliability)
    st.subheader("Filtered High Score Correlations:")
    high_score_corr = merged_corr_drive[merged_corr_drive['total num_of_user_score'] > 10].sort_values('Correlation', ascending=False).head()
    st.dataframe(high_score_corr)

else:
    st.info('Please select a game title from the dropdown to see similar games.')
