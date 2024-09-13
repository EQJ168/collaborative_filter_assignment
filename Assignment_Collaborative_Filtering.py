import pandas as pd
import streamlit as st

# Load the dataset using the correct file path
path = 'NewDataSet.csv'
df = pd.read_csv(path)

# Load another dataset
path_user = 'User_Dataset.csv'
userset = pd.read_csv(path_user)

# Merge datasets
data = pd.merge(df, userset, on='Title')

# Handle missing values
data = data.dropna()

# Pivot table for scores
score_matrix = data.pivot_table(index='user_id', columns='Title', values='user_score', fill_value=0)

# Get user input for the game title
game_title = st.text_input("Enter a game title:", "Pro Evolution Soccer 2018")

if game_title in score_matrix.columns:
    # Display similar game correlations
    game_user_score = score_matrix[game_title]
    similar_to_game = score_matrix.corrwith(game_user_score)
    corr_drive = pd.DataFrame(similar_to_game, columns=['Correlation']).dropna()

    # Display correlations
    st.write(f"Correlations with '{game_title}':")
    st.dataframe(corr_drive.head())

    # Drop unnecessary column and sort correlations
    corr_drive_sorted = corr_drive.sort_values('Correlation', ascending=False).head(10)
    
    # Create DataFrame for user scores count
    user_scores_count = data.groupby('Title')['user_score'].count().reset_index()
    user_scores_count.columns = ['Title', 'total num_of_user_score']

    # Join with correlation DataFrame
    merged_corr_drive = corr_drive_sorted.join(user_scores_count.set_index('Title'), on='Title')

    # Display top 10 correlations
    st.write("Top 10 Correlations:")
    st.dataframe(merged_corr_drive)

    # Check for missing scores
    if 'total num_of_user_score' in merged_corr_drive.columns:
        missing_scores = merged_corr_drive['total num_of_user_score'].isnull().sum()
        st.write(f"Number of missing 'total num_of_user_score': {missing_scores}")

        # Filter and display high score correlations
        high_score_corr = merged_corr_drive[merged_corr_drive['total num_of_user_score'] > 10].sort_values('Correlation', ascending=False).head()
        st.write("Correlations with 'total num_of_user_score' > 10:")
        st.dataframe(high_score_corr)
    else:
        st.write("Column 'total num_of_user_score' is missing in the merged DataFrame.")
else:
    st.write(f"The game title '{game_title}' is not in the dataset.")
