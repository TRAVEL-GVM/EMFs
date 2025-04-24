import streamlit as st
from get_emfs_data import *
from config import *

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

df = pd.read_csv('Data/emfs.csv')
st.dataframe(df)