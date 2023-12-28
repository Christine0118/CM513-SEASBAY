import streamlit as st
import pandas as pd

def generate_google_maps_link(coordinates):
    waypoints = '|'.join([f"{lat},{lon}" for lat, lon in coordinates])
    return f'https://www.google.com/maps/dir/?api=1&destination={waypoints}'

def display_map_with_coordinates(coordinates):
    st.subheader("多個座標地圖")

    # Create a DataFrame with explicit column names
    map_df = pd.DataFrame(coordinates, columns=['lat', 'lon'])

    # Display the map with specified column names
    st.map(map_df, use_container_width=True)

    # Return the DataFrame, so it can be used later
    return map_df

def automatic_input_navigation(coordinates):
    st.subheader("自動輸入座標並導航")
    
    # 显示多选框以选择座标
    selected_coordinates = st.multiselect("選擇要導航的座標", coordinates, default=coordinates)

    if st.button('開啟 Google 地圖導航'):
        # 生成 Google 地图导航链接
        google_maps_link = generate_google_maps_link(selected_coordinates)
        st.markdown(f'[開啟 Google 地圖導航]({google_maps_link})')

def Payment_page(shopping_cart):
    # 假設你有多個座標值
    coordinates = [
        (22.62492385821083, 120.2648231633996),
        (24.62492385821083, 120.2648231633996),
        (23.62492385821083, 120.2648231633996),
        (25.62492385821083, 120.2648231633996)
    ]

    # 顯示多個座標地圖
    displayed_coordinates = display_map_with_coordinates(coordinates)

    # 自動輸入座標並開啟 Google 地圖導航
    automatic_input_navigation(coordinates)

# 呼叫 Payment_page 函數
Payment_page([])
