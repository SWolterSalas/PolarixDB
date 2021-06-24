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

image_antarctica = Image.open('C:\\Users\\Wolter\\Desktop\\PolarixDB\\Images\\antarctica.jpg')
image_expedicion1= Image.open('C:\\Users\\Wolter\\Desktop\\PolarixDB\\Images\\expedicion1.jpg')

def app():
    st.markdown("<h1 style='text-align: center; color: black;'>Welcome to Polarix!</h1>", unsafe_allow_html=True)    
    #st.title('Welcome to Polarix!')
    #st.subheader('We investigate the transport of microorganisms and pollutants to and from Antarctica')
    st.subheader('Study on Antarctica')
    
    col1, mid, col2 = st.beta_columns([6,1,8])
    with col1:
        st.write('We are a multidisciplinary group of scientists dedicated to studying the long-range transport of microorganisms and pollutants to Antarctica, and how this can affect terrestrial biota.')
        st.subheader('Our Goals for Polarix')
        st.write('Our objective is to understand the teleconnections between Antarctica and the rest of the planet through the transport of microorganisms and pollutants, to evaluate their reservoirs, possible origins, and potential impact on the endemic vascular plants of Antarctica.')
        st.subheader('Our mission')
        st.write('Our mission is to elucidate how microorganisms and pollutants travel through the atmosphere. For this we use a combination of genomic and metabolomic analytical tools, as well as atmospheric and climate modeling in an integrative scope.')
    with col2:
        st.image(image_antarctica, use_column_width=False)
    
    col1, mid, col2 = st.beta_columns([6,2,8])
    with col1:
        st.subheader('Our vision')
        st.write('Our vision is to strengthen a multidisciplinary group of scientists in Chile and the world to understand and predict the movement of microorganisms and particles in the atmosphere in a climate change scenario. ')
    with col2:
        st.image(image_expedicion1, use_column_width=False, width = 600)
