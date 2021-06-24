#Home_polarix
import Home_polarix
import Data_polarix
import Downloads_polarix
import Pruebas_polarix
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

image = Image.open('C:\\Users\\Wolter\\Desktop\\PolarixDB\\Images\\Polarix.jpg')
st.sidebar.image(image, use_column_width=True)
st.sidebar.title('Navigation')

PAGES = {
    "Home": Home_polarix,
    "Data": Data_polarix,
    "Downloads": Downloads_polarix,
    "Test": Pruebas_polarix}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))

print(selection)
page = PAGES[selection]

page.app()
