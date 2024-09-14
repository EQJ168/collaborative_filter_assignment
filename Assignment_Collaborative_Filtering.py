import pandas as pd
import streamlit as st

st.title('Game Correlation Finder')

@st.cache  
def load_data():
    path = 'NewDataSet.csv'
    df = pd.read_csv(path)
    path_user = 'User_Dataset.csv'
    userset = pd.read_csv(path_user)
    data = pd.merge(df, userset, on='Title').dropna()  
    return data

data = load_data()

score_matrix = data.pivot_table(index='user_id', columns='Title', values='user_score', fill_value=0)

game_titles = score_matrix.columns.sort_values().tolist()  
game_title = st.selectbox("Select a game title", game_titles)

if game_title:
    game_user_score = score_matrix[game_title]
    similar_to_game = score_matrix.corrwith(game_user_score)
    corr_drive = pd.DataFrame(similar_to_game, columns=['Correlation']).dropna()

    st.subheader(f"Correlations for '{game_title}':")
    st.dataframe(corr_drive.sort_values('Correlation', ascending=False).head(10))

    user_scores_count = data.groupby('Title')['user_score'].count().rename('total num_of_user_score')
    merged_corr_drive = corr_drive.join(user_scores_count, how='left')

    st.subheader("Detailed High Score Correlations:")
    high_score_corr = merged_corr_drive[merged_corr_drive['total num_of_user_score'] > 10].sort_values('Correlation', ascending=False).head()
    st.dataframe(high_score_corr)

else:
    st.info('Please select a game title from the dropdown to see the correlations.')
