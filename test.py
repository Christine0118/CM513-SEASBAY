import streamlit as st
import pandas as pd

# 創建一個包含課程評分信息的 Pandas DataFrame
df = pd.DataFrame(
    [
       {"course": "Chinese", "rating": 4, "Done_Today": True},
       {"course": "English", "rating": 5, "Done_Today": False},
       {"course": "Math", "rating": 3, "Done_Today": False},
   ]
)

key_name = 'my_df'
edited_df = st.data_editor(
    df,
    disabled=["course", "rating"],#選擇要固定的行
    num_rows="dynamic",#前面可以勾選刪除
    hide_index=True,#刪除索引項次
    args=[key_name],
    key=key_name
)


