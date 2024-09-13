import pandas as pd
import streamlit as st

# Title of the application
st.title('Game Correlation Finder')

# Load datasets
@st.cache  # Use caching to speed up loading after the first run
def load_data():
    path = 'NewDataSet.csv'
    df = pd.read_csv(path)
    path_user = 'User_Dataset.csv'
    userset = pd.read_csv(path_user)
    data = pd.merge(df, userset, on='Title').dropna()  # Merge and drop missing values
    return data

data = load_data()

# Create a pivot table for scores
score_matrix = data.pivot_table(index='user_id', columns='Title', values='user_score', fill_value=0)

# User input for the game title
game_title = st.text_input("Enter a game title", "")

# Display results only when a game title is entered
if game_title:
    if game_title in score_matrix.columns:
        game_user_score = score_matrix[game_title]
        similar_to_game = score_matrix.corrwith(game_user_score)
        corr_drive = pd.DataFrame(similar_to_game, columns=['Correlation']).dropna()

        # Display correlations
        st.subheader(f"Correlations for '{game_title}':")
        st.dataframe(corr_drive.sort_values('Correlation', ascending=False).head(10))

        # Join with user scores count
        user_scores_count = data.groupby('Title')['user_score'].count().rename('total num_of_user_score')
        merged_corr_drive = corr_drive.join(user_scores_count, how='left')

        # Filter and display high score correlations
        st.subheader("Detailed High Score Correlations:")
        high_score_corr = merged_corr_drive[merged_corr_drive['total num_of_user_score'] > 10].sort_values('Correlation', ascending=False).head()
        st.dataframe(high_score_corr)
    else:
        st.error(f"The game title '{game_title}' is not found in the dataset.")
else:
    st.info('Please enter a game title to see the correlations.')
