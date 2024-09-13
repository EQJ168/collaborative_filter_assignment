import pandas as pd
import streamlit as st

# Load the dataset using the correct file path
path = 'NewDataSet.csv'
df = pd.read_csv(path)

# Display the first few rows of the dataset
st.write("First few rows of the dataset:")
st.dataframe(df.head())

# Load another dataset
path_user = 'User_Dataset.csv'
userset = pd.read_csv(path_user)

# Display the first few rows of the second dataframe
st.write("First few rows of the user dataset:")
st.dataframe(userset.head())

# Merge datasets
data = pd.merge(df, userset, on='Title')

# Display the merged data
st.write("Merged dataset:")
st.dataframe(data.head())

# Handle missing values
data = data.dropna()

# Display the number of missing values
st.write("Missing values after dropping NA:")
st.write(data.isna().sum())

# Groupby and calculate the mean user_score
grouped_data = data.groupby('Title')['user_score'].mean().sort_values(ascending=False).head()

# Display the groupby results
st.write("Top Titles by average user_score:")
st.dataframe(grouped_data)

# Group by and count user scores
score_counts = data.groupby('Title')['user_score'].count().sort_values(ascending=False).head()

# Display the count of user scores
st.write("Top Titles by number of user scores:")
st.dataframe(score_counts)

# Pivot table for scores
score_matrix = data.pivot_table(index='user_id', columns='Title', values='user_score', fill_value=0)

# Display the score matrix
st.write("Score matrix:")
st.dataframe(score_matrix.head())

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
    st.write("Columns in corr_drive_sorted:")
    st.write(corr_drive_sorted.columns.tolist())

    # Join with user score count
    user_scores_count = pd.DataFrame(data.groupby('Title')['user_score'].count(), columns=['total num of user_score'])
    st.write("Columns in user_scores_count:")
    st.write(user_scores_count.columns.tolist())

    merged_corr_drive = corr_drive_sorted.join(user_scores_count, how='left')
    st.write("Columns in merged_corr_drive after join:")
    st.write(merged_corr_drive.columns.tolist())

    # Display top 10 correlations
    st.write("Top 10 Correlations:")
    st.dataframe(merged_corr_drive)

    # Check for missing scores
    missing_scores = merged_corr_drive['total num of user_score'].isnull().sum()
    st.write(f"Number of missing 'total num of user_score': {missing_scores}")

    # Filter and display high score correlations
    high_score_corr = merged_corr_drive[merged_corr_drive['total num_of_user_score'] > 10].sort_values('Correlation', ascending=False).head()
    st.write("Correlations with 'total num of user_score' > 10:")
    st.dataframe(high_score_corr)
else:
    st.write(f"The game title '{game_title}' is not in the dataset.")
