import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt

import numpy as np
import plotly_express as px

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2024))))

# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team selection
team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team',team,team)


# Sidebar - Position selection
posistion = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', posistion, posistion)


# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Histogram'):
    st.header('Top Players')
    fig = px.histogram(df_selected_team, x='Player',y='PTS',color='Tm',text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig, theme="streamlit",yaxis_title="Moyenne",use_container_width=True)

    st.header('Top Players(3P)')
    fig = px.histogram(df_selected_team, x='Player',y='3P',color='Tm',text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig, theme="streamlit",yaxis_title="Moyenne",use_container_width=True)

    st.header('Top Players(AST)')
    fig = px.histogram(df_selected_team, x='Player',y='AST',color='Tm',text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig, theme="streamlit",yaxis_title="Moyenne",use_container_width=True)


    st.header('Average Age Per Team')
    fig = px.histogram(df_selected_team, x='Tm',y='Age',color='Tm',histfunc="avg",text_auto=True).update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig, theme="streamlit",yaxis_title="Moyenne",use_container_width=True)

