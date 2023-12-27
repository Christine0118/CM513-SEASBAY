import streamlit as st
from PIL import Image

# 讀取設定檔
with open('./config.yaml', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
pic = Image.open('sunrise.jpg')
st.image(pic, caption='**Sunrise**')