import streamlit as st
from datetime import datetime
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import copy
import os
import json
import numpy as np
import webbrowser


# 讀取設定檔
with open('./config.yaml', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

import toml
from toml import TomlDecodeError

# 初始化身份驗證
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
#global login
#login = 0


# 初始化使用者資訊，
# Login 進來的人的購買紀錄
if "user_info" not in st.session_state:
    st.session_state.user_info = {
        "name": None,
        "shopping_cart": [],
        "order_history": []
    }

# 用戶訂單歷史檔案路徑
orders_path = "./orders/"

# 確保訂單目錄存在
if not os.path.exists(orders_path):
    os.makedirs(orders_path)

# 加載用戶訂單歷史
def load_user_order_history(username):
    order_history_file = f"{orders_path}/{username}.csv"
    if os.path.exists(order_history_file):
        return pd.read_csv(order_history_file)
    return pd.DataFrame(columns=["title", "quantity"])

# 保存用戶訂單歷史
def save_user_order_history(username, current_orders):
    order_history_file = f"{orders_path}/{username}.csv"
    if os.path.exists(order_history_file):
        # 如果檔案已存在，則讀取並附加新訂單
        existing_orders = pd.read_csv(order_history_file)
        updated_orders = pd.concat([existing_orders, pd.DataFrame(current_orders)], ignore_index=True)
    else:
        # 如果檔案不存在，則創建新的 DataFrame
        updated_orders = pd.DataFrame(current_orders)

    
    # 保存更新後的訂單歷史
    updated_orders.to_csv(order_history_file, index=False)



def login_page():
    # 在登入頁面以對話框的形式顯示用戶消息
    page = st.sidebar.radio("選擇頁面", ["所有景點","私房遊程" ,"歷史景點", "景點搜搜搜", "留言板"])
    if page == "所有景點":
        popular_attractions()
    elif page == "私房遊程":
        private_tours()
    elif page == "歷史景點":
        order_history()
    elif page == "景點搜搜搜":
        shopping_cart_page()
    elif page == "留言板":
        message_board()




import csv

csv_file_path = 'book.csv'

# 讀取CSV檔案，將資料存入DataFrame

books = pd.read_csv(csv_file_path)


# 初始化 session_state
if "shopping_cart" not in st.session_state:
    st.session_state.shopping_cart = []

# 定義各頁面
    
# 首頁
def home():
    st.subheader("TOP5熱門景點")
    cols = st.columns(5)  
    for i in range(0, min(5, len(books))):  # Display up to the first 6 entries
        with cols[i % 5]: 
            st.image(books.at[i, "image"], caption=books.at[i, "title"])
    st.subheader("私房遊程")
    st.subheader("高雄景點搜搜搜，想怎麼玩就怎麼玩🔥")
    st.image("orders/Screenshot 2023-12-23 002157.png")


 
#購買按鈕
def buy_button(book_index):
    titlename = books.at[book_index, 'title']
    is_selected = any(item['景點'] == titlename for item in st.session_state.shopping_cart)

    if is_selected:
        if st.button(f"取消選取 {titlename}", key=f"cancel_button_{book_index}"):
            st.session_state.shopping_cart = [item for item in st.session_state.shopping_cart if item['景點'] != titlename]
            st.write(f"已取消選取 {titlename}")
            st.experimental_rerun()  # 重新渲染頁面
    else:
        if st.button(f"選取 {titlename}", key=f"buy_button_{book_index}"):
            st.session_state.shopping_cart.append({
                "景點": books.at[book_index, "title"],
                "地區": books.at[book_index, "author"],
                "類型": books.at[book_index, "genre"],  
            })
            st.write(f"已將 {titlename} 加入景點搜搜搜")
            st.experimental_rerun()  # 重新渲染頁面

# 顯示訂單
def display_order():
    st.title("訂單明細")
    # 顯示景點搜搜搜中的商品
    for item in st.session_state.shopping_cart:
        st.write(f"{item['gender']} 本 {item['title']}")


    # 顯示其他訂單相關資訊，例如總金額、訂單時間等
    total_expense = sum(item["total_price"] for item in st.session_state.shopping_cart)
    st.write(f"總金額: {total_expense}")

    order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"訂單時間: {order_time}")

# 景點搜搜搜頁面
def shopping_cart_page():
    st.title("景點搜搜搜")
       
    if not st.session_state.shopping_cart:
        st.write("景點搜搜搜是空的，快去選有興趣的景點吧！")
    else:
        # Create a Pandas DataFrame from the shopping cart data
        st.subheader("景點安排")
        df = pd.DataFrame(st.session_state.shopping_cart)
        
        # Display the DataFrame as a table
        st.table(df)

        if st.button('重選景點'):
            # Reset the shopping cart (delete the DataFrame)
            st.session_state.shopping_cart = []
            st.experimental_rerun()#重新刷新頁面


        Payment_page(st.session_state.shopping_cart)
#google map 規劃路線
def generate_google_maps_link(latitude, longitude):
    return f'https://www.google.com/maps?q={latitude},{longitude}'

def open_google_maps(latitude, longitude):
    google_maps_link = generate_google_maps_link(latitude, longitude)
    webbrowser.open_new_tab(google_maps_link)


# 結帳頁面
def Payment_page(shopping_cart):
    st.subheader("景點地圖")
    all_map_data = []    
    # Collect map data for all locations
    for item in shopping_cart:
        location_name = item["景點"] 
        matching_book = books[books['title'] == location_name].iloc[0]
        lat, lon = matching_book['lat'], matching_book['lon']
        location_data = [lat, lon, location_name]
        all_map_data.append(location_data)

    # Display all locations on the same map
    if all_map_data:
        all_map_data.append([22.62492385821083, 120.2648231633996, "西子灣沙灘會館"])
        map_df = pd.DataFrame(all_map_data, columns=['lat', 'lon', 'location_name'])
        st.map(map_df,size=50, use_container_width=True )
    if st.button("開啟 Google 地圖:西子灣沙灘會館"):
        # 用于示例的经度和纬度坐标
        latitude, longitude = 22.62492385821083, 120.2648231633996
        order_history_df = pd.DataFrame(st.session_state.shopping_cart)
        save_user_order_history(st.session_state.user_info["name"], order_history_df)
        open_google_maps(latitude, longitude)

# 留言頁
def message_board():
    # 初始化 session_state
    if "past_messages" not in st.session_state:
        st.session_state.past_messages = []
    # 在應用程式中以對話框的形式顯示用戶消息
    with st.chat_message("user"):
        st.write("歡迎來到留言板！")
    # 接收用戶輸入
    prompt = st.text_input("在這裡輸入您的留言")
    # 如果用戶有輸入，則將留言加入 session_state 中
    if prompt:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.past_messages.append({"user": "user", "message": f"{timestamp} - {prompt}"})
    # 留言板中顯示過去的留言
    with st.expander("過去的留言"):
        # 顯示每條留言
        for message in st.session_state.past_messages:
            with st.chat_message(message["user"]):
                st.write(message["message"])



# 訂單歷史頁面
def order_history():
    st.title("景點歷史")
    # 將訂單資料轉換為 DataFrame
    df = load_user_order_history(st.session_state.user_info["name"])
    # 顯示表格
    st.table(df)
    if st.button('刪除景點'):
        # 刪除整個 DataFrame
        df.drop(df.index, inplace=True)
        
        # 將刪除後的 DataFrame 保存到文件
        order_history_file = f"{orders_path}/{st.session_state.user_info['name']}.csv"
        df.to_csv(order_history_file, index=False)


# 所有景點頁面
def popular_attractions():
    st.title("所有景點")

    # Get selected region and category from the sidebar
    cols = st.columns(2)
    with cols[0]:
        selected_region = st.selectbox("景點地區", ["所有地區", "旗津海港", "駁二時尚", "鹽埕風格", "西子灣海風"], key="region_selector")
    with cols[1]:
        selected_category = st.selectbox("景點種類", ["所有種類", "美食介紹", "景點遊玩"], key="category_selector")

    if selected_region == "所有地區" and selected_category == "所有種類":
        st.subheader("所有景點")
    # 使用 st.beta_columns 將一行分為兩列
        cols = st.columns(2)  # 新增
        for i in range(0, len(books)): 
                with cols[i % 2]:  # 新增
                    st.write(f"**{books.at[i, 'title']}**")
                    st.image(books.at[i, "image"], caption=books.at[i, "title"], width=300)
                    st.write(f"位置: {books.at[i, 'author']}")
                    st.write(f"類型: {books.at[i, 'genre']}")
                    buy_button(i)
    else:
        # 根據選擇的地區篩選數據
        filtered_data = books if selected_region == "所有地區" else books[books["author"] == selected_region]
        # 根據選擇的種類再次篩選數據
        filtered_data = filtered_data if selected_category == "所有種類" else filtered_data[filtered_data["genre"] == selected_category]
        # 輸出結果

        cols = st.columns(2)  # 新增
        for i, (_, row) in enumerate(filtered_data.iterrows()):  # Iterate over rows in filtered_data
            with cols[i % 2]:  # Switch columns for each iteration
                titlename = st.write(f"**{row['title']}**")
                st.image(row["image"], width=300)
                st.write(f"位置: {row['author']}")
                st.write(f"類型: {row['genre']}")
                        # 使用 buy_button 函數處理按鈕邏輯
                titlename = row['title']
                if st.button(f"選取 {titlename}", key=f"buy_button_{i}"):
                    if any(item['景點'] == titlename for item in st.session_state.shopping_cart):
                        st.warning("此景點已經加入景點搜搜搜")
                    else:
                        st.session_state.shopping_cart.append({
                            "景點": row["title"],
                            "地區": row["author"],
                            "類型": row["genre"],  
                        })
                        st.write(f"已將 {row['title']} 加入景點搜搜搜")

#私房景點
def private_tours():
    st.title("私房遊程")
    st.write("尋找獨特的私房遊程，打造屬於您的旅程！")
    # 使用 st.container 創建一個容器
    with st.container():
    # 在容器內部顯示文字
    

    # 使用 st.columns 分割容器為三列，分別賦值給 col1, col2, col3


    # 在第一列（col1）顯示鹽埕區半日遊的圖片跟簡短介紹

        st.header("一日遊")
        st.subheader("鹽埕風格的美食與景點探索")
        st.image("orders\鹽埕-景點-文武聖殿.jpg")
        st.write("上午")
        st.markdown(" 前往參拜「文武聖殿」，這是一座具有悠久歷史的廟宇，充滿宗教文化氛圍。在這裡，你可以感受到當地居民的信仰和傳統。") 
        with st.expander("繼續閱讀"):    
            st.image("orders\鹽埕-景點-高雄市立歷史博物館.jpg")
            st.markdown("前往參觀「高雄市立歷史博物館」，深入了解高雄市的豐富歷史。博物館展示了許多珍貴的文物和歷史資料，是一個了解城市發展的絕佳場所。")
            st.image("orders\鹽埕-美食-港園牛肉麵.jpg")
            st.markdown("來到鹽埕風格區的「港園牛肉麵」。這家餐廳以濃郁的牛肉湯底和彈牙的麵條聞名，是當地的美食代表之一。品嚐一碗熱騰騰的牛肉麵，開啟美好的一天。")
            st.image("orders\鹽埕-景點-高雄市電影館.jpg")
            st.markdown("隨後，探訪「高雄市電影館」，這裡是影視愛好者的天堂。不僅有豐富的電影放映，還有特展和活動，讓你沉浸在電影的世界中。")
            st.image("orders\鹽埕-景點-愛河親水徒步區.jpg")
            st.markdown("漫步「愛河親水徒步區」，欣賞愛河風光。這裡有美麗的河畔風景、悠閒的散步道，讓你放鬆心情，感受愛河的浪漫氛圍。")
    # 在第二列（col2）顯示三民區半日遊的圖片跟簡短介紹

        st.header("半日遊")
        st.subheader("西子灣美食與自然探險")
        st.image("orders\西子灣-美食-鴨肉珍.jpg")
        st.write("下午：")
        st.markdown(" 開啟你的半日遊行程，首先在木葉粗食品嚐當地特色的粗食料理。這家餐廳以木葉為名，營造出自然、清新的用餐環境。你可以品嚐到新鮮、簡單而美味的台灣傳統料理，感受當地飲食文化的精髓。") 
        with st.expander("繼續閱讀"):    
            st.image("orders\西子灣-景點-打狗英國領事館文化園區.jpg")
            st.markdown("前往打狗英國領事館文化園區，這是一個融合歷史、文化和藝術的地方。在這裡，你可以漫遊於保存完整的英國領事館建築中，了解高雄的歷史背景。文化園區也經常舉辦各種藝術展覽和文化活動，為遊客提供多元的體驗。")
            st.image("orders\西子灣-景點-夕照觀景坡堤.jpg")
            st.markdown("午後時光，前往夕照觀景坡堤，這裡是西子灣海風的最佳觀景點之一。站在坡堤上，你可以俯瞰整個西子灣，欣賞到海天一色的美景，特別是在夕陽西下的時刻，風景更是令人陶醉。攜帶相機，記錄下這片美麗的風光。")
            st.markdown("這趟半日遊行程結合了美食、自然和文化，讓你在西子灣海風中度過一個豐富而難忘的時光。")
    # 在第三列（col3）顯示旗津全日遊的圖片跟簡短介紹

        st.header("半日遊")
        st.subheader("駁二時尚藝術與美食探險")
        st.image("orders\駁二-景點- 金馬賓館當代美術館.jpg")
        st.markdown(" 開啟你的半日遊行程，首先參觀「金馬賓館當代美術館」，這座當代藝術館位於駁二時尚區，展示著豐富的藝術收藏品。在這裡，你可以欣賞到來自不同藝術家的作品，感受當代藝術的獨特魅力。") 
        with st.expander("繼續閱讀"):
            st.image("orders\駁二-景點-哈瑪星鐵道文化園區.jpg")
            st.markdown("隨後前往「哈瑪星鐵道文化園區」，這個充滿歷史氛圍的地方曾經是一座火車站，現在轉變成文化園區。在這裡，你可以探索保存完好的鐵道建築，了解高雄的鐵道歷史。")
            st.image("orders\駁二-美食-紅瀰.jpg")
            st.markdown("午後時光，前往夕照觀景坡堤，這裡是西子灣海風的最佳觀景點之一。站在坡堤上，你可以俯瞰整個西子灣，欣賞到海天一色的美景，特別是在夕陽西下的時刻，風景更是令人陶醉。攜帶相機，記錄下這片美麗的風光。")
            st.markdown("這趟半日遊行程結合了美食、自然和文化，讓你在西子灣海風中度過一個豐富而難忘的時光。")

def main():
    
    st.title("西子灣沙灘會館")
    st.image("https://s3-alpha-sig.figma.com/img/152b/406a/1a0e94e7a9c64f497bdd72615b2568d2?Expires=1704067200&Signature=hGOM2q7F2ObaczZ5E26wBxXMbdFhesgJLR0pbknF3hyI8ft0a72ZglpKQ408~8Gg~clBh-IaaEFcATTJoFa6w7a4X9-k--W53oJND1vkgKTwn0tsjsaIOAuohTl3AYm89I~x7XblQBrDR2e-Yp7z4J20QeCTQturkAfIsc3BSyyUSU-bWwdMQHj651uoZSD04GtM2ODhG3bXOCSq6s9DjDJoTYw1y3kjwFU8VxD9j3oqe3NolB3j2IcCsuQ2ePcFa1s~bIFm9pwuxCi22jqE2nxcE1s0ASVU8b6o3FzERTWgYVOCPqbczCCTJ1TIfJJKHBKxUtXCcZlAxY5j8Jtg3Q__&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4")
    st.session_state.login = False
    
    # 登入
    name, authentication_status, username = authenticator.login('Login', 'main')
    st.session_state.login = authentication_status
    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.session_state.user_info["name"] = name
        # 加載用戶訂單歷史
        st.session_state.user_info["order_history"] = load_user_order_history(username)
        st.write(f'Welcome *{name}*')  
        login_page()
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

if __name__ == "__main__":
    main()



