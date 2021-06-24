##### Modulos #####
import sqlite3
import os
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import base64
from streamlit_folium import folium_static
import folium
import numpy as np
#import altair as alt
import plotly.express as px
from zipfile import ZipFile
from io import BytesIO


def load_data(option2):
    st.write(option2)
    option3=option2.replace('.csv','')
    #st.write(option3)
    conn = sqlite3.connect('Antarctica.db')
    query = 'SELECT * FROM {}'.format(option3)
    data = pd.read_sql(query, conn)
    return data

def download_data():
    ZipfileDotZip = "Selected_stations.zip"
    with open(ZipfileDotZip, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        download_filename = "Selected_stations.zip"
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}"><input type="button" value="Download"></a>'

def app():
    st.markdown("<h1 style='text-align: center; color: black;'>Download Data of multiple station of Antarctica</h1>", unsafe_allow_html=True)    
    #st.title('Download Data of multiple station of Antarctica')
    st.write('Here you can download the data of the station you need')
    ruta = 'C:\\Users\\Wolter\\Desktop\\PolarixDB\\Data_Stations'
    lista = os.listdir('C:\\Users\\Wolter\\Desktop\\PolarixDB\\Data_Stations')
    rutas = []
    for i in lista:
        rutas.append(os.path.join(ruta, i))
    AWS = []
    SCAR = []
    POLENET = []
    for j in rutas:
        if 'AWS' in j:
            AWS = os.listdir(j)
        if 'SCAR' in j:
            SCAR = os.listdir(j)
        if 'POLENET' in j:
            POLENET = os.listdir(j)
    
    descargas = []

    col1, col2, col3 = st.beta_columns([3,3,3])
    with col1:
        check_number=0

        st.subheader('AWS stations')
        check_boxes_AWS = [st.checkbox(estacion, key=estacion) for estacion in AWS]
        x = ([i for i, checked in zip(AWS, check_boxes_AWS) if checked])
        for i in x:
            ruta2 = os.path.join(rutas[check_number], i)
            descargas.append(ruta2)    
    with col2:
        check_number=1
        st.subheader('POLENET stations')
        check_boxes_POLENET = [st.checkbox(estacion, key=estacion) for estacion in POLENET]
        x = ([i for i, checked in zip(POLENET, check_boxes_POLENET) if checked])
        for i in x:
            ruta2 = os.path.join(rutas[check_number], i)
            descargas.append(ruta2)
    with col3:
        check_number=2
        st.subheader('SCAR stations')
        check_boxes_SCAR = [st.checkbox(estacion, key=estacion) for estacion in SCAR]
        x = ([i for i, checked in zip(SCAR, check_boxes_SCAR) if checked])
        for i in x:
            ruta2 = os.path.join(rutas[check_number], i)
            descargas.append(ruta2)
    
    zipObj = ZipFile("Selected_stations.zip", "w")
        
    for i in descargas:
        zipObj.write(i)
    zipObj.close()
    st.markdown(download_data(), unsafe_allow_html=True)

