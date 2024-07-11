import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from current_location import latitude, longitude
from models import Kraje_df, Regiony_df, Atrakcje_df, Kontynenty_df,Redaktorzy_df,Opinie_df
import subprocess
import os
from users import login_as_user


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

st.set_page_config(initial_sidebar_state="collapsed",layout="wide")

st.title("Zaplanuj swoją podróż")






login = st.sidebar.text_input("login")
password = st.sidebar.text_input("password",type="password")

if  st.sidebar.button("zaloguj sie"):

     if login in list(Redaktorzy_df.login):

         try :
             login_as_user(login,password)
             if list(Redaktorzy_df[Redaktorzy_df.login==login].administrator)[0] == 1:
                 run_command("streamlit run C:/Users/skyri/PycharmProjects/MAM/admin_panel.py")

             else:
                 os.environ[f"login"] = login
                 run_command("streamlit run C:/Users/skyri/PycharmProjects/MAM/editor_panel.py")

         except:
             st.sidebar.text("Nie dziala")

     else:
         st.sidebar.text("to tez")







import streamlit as st
import plotly.graph_objs as go

# Inicjalizacja list współrzędnych
if 'longitude_list' not in st.session_state:
    st.session_state.longitude_list = []
if 'latitude_list' not in st.session_state:
    st.session_state.latitude_list = []


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.selectbox("Kontynent", list(Kontynenty_df.kontynent), key="kont")


with col2:
    st.selectbox("Kraj", list(Kraje_df[Kraje_df.parent_id == st.session_state.kont].kraj), key="kraj")


with col3:
    st.selectbox("Region", list(Regiony_df[Regiony_df.parent_id == st.session_state.kraj].region), key="region")


with col4:
    temp = Atrakcje_df[Atrakcje_df.parent_id == st.session_state.region]
    st.selectbox("Atrakcja", list(temp.atrakcja), key="atrakcja")


if st.button("Dodaj"):
    st.session_state.longitude_list.extend(temp[temp.atrakcja == st.session_state.atrakcja].dlugosc.tolist())
    st.session_state.latitude_list.extend(temp[temp.atrakcja == st.session_state.atrakcja].szerokosc.tolist())


fig = go.Figure(go.Scattermapbox(
    mode="lines+markers",
    lon=st.session_state.longitude_list,
    lat=st.session_state.latitude_list,
    marker={'size': 10}
))

fig.update_layout(
    mapbox={
        'accesstoken': 'pk.eyJ1IjoicGF3ZWxwbHV0YSIsImEiOiJjbHdieG9mNm0wcGYzMnFxbWhxdjFsdnhqIn0.pe2esrKvIHXNUJX_GnO5xA',  # Tutaj wstaw swój klucz API Mapbox
        'style': "streets",
        'center': {'lon': 10.0, 'lat': 50.0},
        'zoom': 3
    },
    showlegend=False
)




st.plotly_chart(fig)

cola,colb = st.columns(2)

with cola:
    try:
     st.text_area("Opinia",list(Opinie_df[Opinie_df.parent_id == list(Atrakcje_df[Atrakcje_df.atrakcja==st.session_state.atrakcja].id)[0]].opinia)[0])
    except:
        st.text_area("Park Krajobrazowy Orlich Gniazd jest wyjątkowym obszarem chronionym w południowej Polsce, charakteryzującym się malowniczymi krajobrazami i bogatą historią. Rozciąga się on na Jurze Krakowsko-Częstochowskiej i zawiera szereg wapiennych skał, jaskiń oraz głębokich wąwozów. Park jest również znany z licznych zamków i ruin, które są częścią tzw. Szlaku Orlich Gniazd – linii obronnej z czasów średniowiecza. Przyroda parku jest różnorodna, z licznymi gatunkami roślin i zwierząt, które przyciągają zarówno naukowców, jak i turystów. Szczególnie popularne są tu trasy piesze i rowerowe, które pozwalają na pełne docenienie krajobrazu i dziedzictwa kulturowego regionu.")
with colb:

    directory_path = f"uploaded_files/{st.session_state.kraj}/{st.session_state.region}/{st.session_state.atrakcja}"

    # Get a list of all files in the directory
    files_in_directory = os.listdir(directory_path)

    # Filter out directories, keeping only files
    files_only = [f for f in files_in_directory if os.path.isfile(os.path.join(directory_path, f))]



    st.image(f"uploaded_files/{st.session_state.kraj}/{st.session_state.region}/{st.session_state.atrakcja}/{files_only[0]}",width=500)

