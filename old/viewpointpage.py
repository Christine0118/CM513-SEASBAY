import streamlit as st

# 使用 `st.container` 創建一個容器
with st.container():
    # 在容器內部顯示文字
    

    # 使用 `st.columns` 分割容器為三列，分別賦值給 col1, col2, col3
    col1, col2, col3 = st.columns(3)

    # 在第一列（col1）顯示一個標題和貓的圖片
    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")
        st.write("This is inside the container 1.")
        st.markdown("The cat (Felis catus), commonly referred to as the domestic cat or house cat, \
            is the only domesticated species in the family Felidae. Recent advances in archaeology and \
            genetics have shown that the domestication of the cat occurred in the Near East around 7500 BC.") 

    # 在第二列（col2）顯示一個標題和狗的圖片
    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")
        st.write("This is inside the container 2.")
        st.markdown("The dog (Canis familiaris[4][5] or Canis lupus familiaris[5]) is a domesticated descendant of the wolf. \
            Also called the domestic dog, it is derived from extinct Pleistocene wolves,[6][7] \
            and the modern wolf is the dog's nearest living relative.[8] \
            The dog was the first species to be domesticated[9][8] by humans. ") 

    # 在第三列（col3）顯示一個標題和貓頭鷹的圖片
    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")
        st.write("This is inside the container 3.")
        st.markdown("Owls are birds from the order Strigiformes[1] (/ˈstrɪdʒəfɔːrmiːz/), which includes over 200 species of mostly solitary \
            and nocturnal birds of prey typified by an upright stance, a large, broad head, binocular vision, \
            binaural hearing, sharp talons, and feathers adapted for silent flight.  ") 

# 在容器外顯示文字
st.header("This is outside the container")
