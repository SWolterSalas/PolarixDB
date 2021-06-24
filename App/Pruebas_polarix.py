##### Modulos #####
import sqlite3
import os
import streamlit as st
import pandas as pd
import datetime
#from PIL import Image
import base64
from streamlit_folium import folium_static
import folium
import numpy as np
#import altair as alt
import plotly.express as px
from typing import List, Optional
import markdown
#import basemap
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def app():
    m = Basemap(projection='stere', resolution='c',
            lat_0=-77, lon_0=280,  lat_ts=(50.+15.)/2., width=9000000, height=9000000)
    # (width, height) is the plot extents in meters
    
    #m.drawmeridians(np.arange(0, 360, 30), labels=[1,1,1,0])
    m.drawparallels(np.arange(0, 90, 10), labels=[0,0,0,1])
    #m.drawcoastlines()
    m.shadedrelief()
    st.pyplot(use_column_width=True)

