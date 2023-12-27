import streamlit as st
import pandas as pd

csv_file_path = 'book.csv'

# 讀取CSV檔案，將資料存入DataFrame
data = pd.read_csv(csv_file_path)

# 選擇地區
selected_region = st.selectbox("景點地區", ["所有地區", "旗津海港", "駁二時尚", "鹽埕風格", "西子灣海風"], key="region_selector")

# 根據選擇的地區篩選數據
filtered_data = data if selected_region == "所有地區" else data[data["author"] == selected_region]

# 選擇種類
selected_category = st.selectbox("景點種類", ["所有種類", "美食介紹", "景點遊玩"], key="category_selector")

# 根據選擇的種類再次篩選數據
filtered_data = filtered_data if selected_category == "所有種類" else filtered_data[filtered_data["genre"] == selected_category]

# 輸出結果
for i, row in filtered_data.iterrows():
    st.write(f"{row['title']}")
    st.image(row["image"], caption=row["title"], width=300)
    st.write(f"位置: {row['author']}")
    st.write(f"類型: {row['genre']}")
    st.write(f"金額: {row['price']}")
