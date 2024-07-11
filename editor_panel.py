import streamlit as st
from models import Kontynenty_df,Kraje_df,Regiony_df,Atrakcje_df,Redaktorzy_df,Opinie_df,engine
from users import login_as_user, admin_connection
import os
import pandas as pd

login = os.getenv('login', 'default_value')

st.set_page_config(layout="wide")
if "atrakcja" not in st.session_state:
    st.session_state["atrakcja"] = None

if st.session_state.atrakcja == None:

    col1, col2, col3, col4 = st.columns(4)



    with col1:
        st.selectbox("Kontynent", list(Kontynenty_df.kontynent), key="kont")

    with col2:
        st.selectbox("Kraj", list(Kraje_df[Kraje_df.parent_id == st.session_state.kont].kraj), key="kraj")

    with col3:
        st.selectbox("Region", list(Regiony_df[Regiony_df.parent_id == st.session_state.kraj].region), key="region")

    with col4:
        temp = Atrakcje_df[Atrakcje_df.parent_id == st.session_state.region]
        atrakcja = st.selectbox("Atrakcja", list(temp.atrakcja), key="atrakcja")


    if atrakcja!=None:

        st.text("\n")
        st.text("\n")
        st.text("\n")
        st.text("\n")

        col1, col2 = st.columns(2)

        with col1:

            st.text_input("TEKST","HEJ")

        with col2:

            pass


else:

    cola,colb = st.columns([1,3],gap="large")

    with cola:

        st.selectbox("Kontynent", list(Kontynenty_df.kontynent), key="kont")


        st.selectbox("Kraj", list(Kraje_df[Kraje_df.parent_id == st.session_state.kont].kraj), key="kraj")


        st.selectbox("Region", list(Regiony_df[Regiony_df.parent_id == st.session_state.kraj].region), key="region")


        temp = Atrakcje_df[Atrakcje_df.parent_id == st.session_state.region]
        atrakcja = st.selectbox("Atrakcja", list(temp.atrakcja), key="atrakcja")



    with colb:

        opinia = list(Opinie_df[Opinie_df.parent_id == list(Atrakcje_df[Atrakcje_df.atrakcja==st.session_state.atrakcja].id)[0]].opinia)


        redaktor = list(Redaktorzy_df[Redaktorzy_df.login==login].id)[0]

        text = opinia[0] if len(opinia)>0 else ""

        opinia_input = st.text_input("opinion",text)

        import streamlit as st
        import os

        # Define the directory where you want to save the uploaded files
        save_directory = f"uploaded_files/{st.session_state.kraj}/{st.session_state.region}/{st.session_state.atrakcja}"

        # Ensure the save directory exists
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # File uploader to accept multiple files
        uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

        # Loop through each uploaded file
        for uploaded_file in uploaded_files:
            # Read the file data
            bytes_data = uploaded_file.read()

            # Define the full path to save the file
            save_path = os.path.join(save_directory, uploaded_file.name)

            # Save the file
            with open(save_path, "wb") as f:
                f.write(bytes_data)

            # Display the filename and the save path
            st.write("File saved as:", save_path)

        if st.button("Dodaj"):

            conn = admin_connection
            cur = conn.cursor()

            if len(opinia) > 0:

                cur.execute(f"UPDATE \"Opinie\" SET opinia = '{opinia_input}' WHERE parent_id = {int(list(Atrakcje_df[Atrakcje_df.atrakcja==st.session_state.atrakcja].id)[0])};")
                conn.commit()
                st.text("opinia dodana")

                st.experimental_rerun()
                Opinie_df = pd.read_sql("SELECT * FROM \"Opinie\"", engine)


            else:


                cur.execute(f"insert into \"Opinie\"(parent_id,redaktor_id,opinia) values({int(list(Atrakcje_df[Atrakcje_df.atrakcja==st.session_state.atrakcja].id)[0])},{int(redaktor)},\'{opinia_input}\')")
                conn.commit()

                st.text("opinia dodana")
                st.experimental_rerun()
                st.text("opinia dodana")


            st.dataframe(Opinie_df)

            conn.close()





