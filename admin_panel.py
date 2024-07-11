import streamlit as st
from models import Kontynenty_df,Kraje_df,Regiony_df,Atrakcje_df,Redaktorzy_df,Opinie_df
from users import admin_connection





panel = st.selectbox("Panele",["Zarządzaj zawartością","Dodaj redaktora"])

if panel == "Zarządzaj zawartością":
    st.text("Tablice")
    col1, col2, col3, col4 = st.columns(4)

    query = st.text_input("SQL query")
    if st.button("ok"):
        cur = admin_connection.cursor()
        cur.execute(query)
        st.text(f"{query}")
        admin_connection.commit()
        admin_connection.close()
        st.experimental_rerun()



    with col1:
        st.selectbox("Kontynent", list(Kontynenty_df.kontynent), key="kont")

    with col2:
        st.selectbox("Kraj", list(Kraje_df[Kraje_df.parent_id == st.session_state.kont].kraj), key="kraj")

    with col3:
        st.selectbox("Region", list(Regiony_df[Regiony_df.parent_id == st.session_state.kraj].region), key="region")

    with col4:
        temp = Atrakcje_df[Atrakcje_df.parent_id == st.session_state.region]
        st.selectbox("Atrakcja", list(temp.atrakcja), key="atrakcja")



    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(Kraje_df[Kraje_df.parent_id == st.session_state.kont])

    with col2:
        st.dataframe(Regiony_df[Regiony_df.parent_id == st.session_state.kraj],width=30000)


    st.dataframe(Atrakcje_df[Atrakcje_df.parent_id == st.session_state.region],width=30000)

    st.dataframe(Redaktorzy_df)
    st.dataframe(Opinie_df)

else:
    login = st.text_input("login")
    haslo = st.text_input("haslo")
    email = st.text_input("email")
    warunek = st.checkbox("Admin")
    admin =   1 if warunek else 0

    if st.button("dodaj") :
     try:
        cur = admin_connection.cursor()
        cur.execute("SELECT create_user_and_assign_role( \'"+login+"\',\'" +haslo+"\');")
        cur.execute(f"insert into \"Redaktorzy\"(email,administrator,login) values(\'{email}\',\'{admin}\',\'{login}\')")
        admin_connection.commit()
        admin_connection.close()
        st.experimental_rerun()
     except:

        st.text("Uzytkownik o podanym loginie istnieje!")
