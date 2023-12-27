import streamlit as st

# 在session state中存儲widget的初始值
# 如果 "visibility" 不在 session_state 中，則將其初始化為 "visible"
#session_state 設定 "共同變數"控制 col1, col2，讓彼此間可以溝通
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = False

# 使用 `st.columns` 函數將畫面分為兩列
col1, col2 = st.columns(2)

# 在第一列顯示兩個Checkbox
with col1:
    st.checkbox("Disable radio widget", key="disabled")
    st.checkbox("Orient radio options horizontally", key="horizontal")

# 在第二列顯示一個Radio組件
with col2:
    st.radio(
        "Set label visibility 👇",
        ["visible", "hidden", "collapsed"],
        key="visibility",
        label_visibility=st.session_state.visibility,  # 使用session state中的值作為label_visibility參數
        disabled=st.session_state.disabled,  # 使用session state中的值作為disabled參數
        horizontal=st.session_state.horizontal,  # 使用session state中的值作為horizontal參數
    )