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
import plotly.graph_objects as go

##### Funciones #####

# Carga desde  SQL Database
def load_data(option2):
    option3=option2.replace('.csv','')
    conn = sqlite3.connect('Antarctica.db')
    query = 'SELECT * FROM {}'.format(option3)
    data = pd.read_sql(query, conn)
    return data

# Seleccion de fechas iniciales
@st.cache
def seleccion_dates(csv):
    x = min(list(range(len(csv['Dates']))))
    y = max(list(range(len(csv['Dates']))))
    z = x+200
    mini_1 = csv['Dates'][x]
    mini_2 = csv['Dates'][z]
    return mini_1,mini_2,y

# Formacion de tabla con fechas iniciales y finales de cada estacion
@st.cache
def get_min_max_dates(lista2, option2):
    lista_dates = []
    co = 0 
    co_d = []
    for estacion in lista2:
            option3=estacion.replace('.csv','')
            conn = sqlite3.connect('Antarctica.db')
            query = 'SELECT Dates FROM {}'.format(option3)
            data = pd.read_sql(query, conn)
            mini_date = min(list(range(len(data['Dates']))))
            maxi_date = max(list(range(len(data['Dates']))))
            mini_1 = data['Dates'][mini_date]
            mini_2 = data['Dates'][maxi_date]
            lista_dates.append([option3,mini_1,mini_2])
            estat_eleg = option2.replace('.csv','')
            if option3 == estat_eleg:
                co_d=co
            co +=1
    lista_dates2 = pd.DataFrame(lista_dates, columns =['Station','Min_Date','Max_Date'])
    return lista_dates2, co_d

# Seleccion de tabla de bases Antarticas
@st.cache
def coord_data(option):
    ruta = 'C:\\Users\\Wolter\\Desktop\\PolarixDB\\Metadata_Stations'
    coor = os.path.join(ruta,option)
    df_c = pd.read_csv(coor)
    df_c = df_c.rename({
        'Latitude': 'lat',
        'Longitude': 'lon'}, axis=1)
    return df_c

# Boton de descarga de Data Frame
def get_table_download_link(df, option2):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    download_filename = option2
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}"><input type="button" value="Download"></a>'

# Eleccion de mes o año para cambiar el formato del tiempo
@st.cache
def transform_month_year(date, month=True):
    co = 0
    if month is True:
        for i in date:
            mes = i[:-9]
            date[co] = mes
            co += 1
    else:
        for i in date:
            year = i[:-12]
            date[co] = year
            co += 1

# Contador de datos por estacion elegida
@st.cache
def counter(option2):
    option3=option2.replace('.csv','')
    conn = sqlite3.connect('Antarctica.db')
    query = 'SELECT * FROM {}'.format(option3)
    data = pd.read_sql(query, conn)
    date = list(data['Dates'])
    largo = len(date)
    if largo > 50000:
        transform_month_year(date, month=False)
        tiempo = 'Years'
    else:
        transform_month_year(date)
        tiempo = 'Months'
    co = 0
    co_datos = 0
    cant_datos = []
    for i in date:
        if (co+1) < largo:
            if i == date[co+1]:
                co_datos += 1
            elif i != date[co+1]:
                cant_datos.append([i, co_datos])
                co_datos = 0
        co +=1
    df = pd.DataFrame(cant_datos)
    df.columns = [tiempo, 'Count of data per Date']
    return df

# Obtencion de valores promedios de temperatura por dia
@st.cache
def mean_temp(option2):
    option3=option2.replace('.csv','')
    
    conn = sqlite3.connect('Antarctica.db')
    query = 'SELECT * FROM {}'.format(option3)
    data = pd.read_sql(query, conn)
    new_data_d = list(data['Dates'])
    new_data_t = list(data['Temperature_(Celsius)'])
    new_data = list(zip(new_data_d,new_data_t))
    largo = len(new_data)
    co = 0
    lista_temp_avg = []
    for i in list(new_data):
        x = i[0]
        dia = x[:-6]
        t = i[1]
        lista_temp_avg.append([dia,t])
        co += 1
    co = 0
    temp = []
    datos = []
    for i in lista_temp_avg:
        if (co+1) < largo:
            if i[0] == lista_temp_avg[co+1][0]:
                if i[1] != '':
                    #i[1]= np.nan
                    #continue
                    #break
                    temp.append(i[1])
                    #print(temp)
                #data = data.replace('',np.nan)
            elif i != new_data[co+1]:
                temp1=np.array(temp).astype(np.float)
                mean = "%.1f" %np.mean(temp1)
                datos.append([i[0], float(mean)])
                temp = []
        co +=1
    df = pd.DataFrame(datos)
    return df

def minmax_temp(option2):
    option3=option2.replace('.csv','')
    conn = sqlite3.connect('Antarctica.db')
    query = 'SELECT * FROM {}'.format(option3)
    data = pd.read_sql(query, conn)
    new_data_d = list(data['Dates'])
    new_data_t = list(data['Temperature_(Celsius)'])
    new_data = list(zip(new_data_d,new_data_t))
    largo = len(new_data)
    co = 0
    lista_temp_min = []
    lista_temp_max = []
    for i in list(new_data):
        x = i[0]
        dia = x[:-6]
        t = i[1]
        lista_temp_min.append([dia,t])
        #lista_temp_max.append([dia,t])
        co += 1
    co = 0
    temp = []
    datos = []
    for i in lista_temp_min:
        if (co+1) < largo:
            #st.write(i[0])
            if i[0] == lista_temp_min[co+1][0]:
                #st.write(i[0],lista_temp_min[co+1][0])
                if i[1] != '':
                    #st.write(i[0],i[1])
                    #i[1]= np.nan
                    #continue
                    #break
                    temp.append(i[1])
                    #print(temp)
                #data = data.replace('',np.nan)
            elif i != new_data[co+1]:
                temp1=np.array(temp).astype(np.float)
                if temp1.size != 0: 
                #temp2=np.array(temp).astype(np.float)
                    #st.write(temp1)
                    minim = "%.1f" %np.min(temp1)
                    maxim = "%.1f" %np.max(temp1)
                    datos.append([i[0], float(minim), float(maxim)])
                    #datos[1].append([i[0], ])
                    temp = []
        co +=1
    df = pd.DataFrame(datos)
    #df_T= df.T
    #st.dataframe(df)
    return df


st.set_option('deprecation.showPyplotGlobalUse', False)

def app():
##### Titulos e imagen Polarix #####
    st.markdown("<h1 style='text-align: center; color: black;'>Data of Antarctic Stations</h1>", unsafe_allow_html=True)    

    #st.title('')
    st.write('Here you can display the data of the station you need')
    st.sidebar.header('Polar Station')
    ruta = 'C:\\Users\\Wolter\\Desktop\\PolarixDB\\Data_Stations'
    lista = os.listdir('C:\\Users\\Wolter\\Desktop\\PolarixDB\\Data_Stations')
    option = st.sidebar.selectbox("Select station group:", lista)
    ruta2 = os.path.join(ruta, option)
    lista2 = os.listdir(os.path.join(ruta, option))
    option2 = st.sidebar.selectbox("Select station:", lista2)
    print(option2)
    lista_dates2, co_d = get_min_max_dates(lista2, option2)
    csv_elegido = os.path.join(ruta2, option2)
    df = load_data(option2)

##### Seleccion de datos para mapa
    
    data_coord = coord_data(option)
    data_coord = pd.DataFrame(data_coord)
    latlong = [(data_coord['lat'][co_d]), (data_coord['lon'][co_d])]
    data_coord = pd.concat([data_coord, lista_dates2], axis=1, join="inner")
    latlon = data_coord[['lat','lon']]
    latlon_l = latlon.values.tolist()
    tabla_coord = option2.replace('.csv','')
    tabla_coord = tabla_coord.replace('_aws','')
    
    ##### Formacion de mapa
    m = folium.Map(width=650,height=500, location=latlong, zoom_start=6)
    for punto in range(len(latlon_l)):
        folium.Marker(latlon_l[punto], popup=(data_coord['Name'][punto], 
                                              "\nMin_Date",data_coord['Min_Date'][punto], 
                                              "\nMax_Date",data_coord['Max_Date'][punto])).add_to(m)
    

##### Seleccion de columnas para tabla

    st.sidebar.subheader('Parameters')
    columnas = st.sidebar.multiselect('Columns:', options = list(df.columns), default=('Dates','Temperature_(Celsius)','Pressure_(hPa)'))
    
    ##### Seleccion de fechas y cambio de formato de 'string' a 'datetime.datetime'
    st.sidebar.subheader('Dates')
    mini_1_d, mini_2, max_d = seleccion_dates(df)
    
    co = 0
    for fecha in df['Dates']:
        if mini_1_d == fecha:
            fecha1 = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M')
            df['Dates'][co] = fecha1
            mini_1_d = fecha1
            co += 1
        elif mini_2 == fecha:
            fecha1 = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M')
            df['Dates'][co] = fecha1
            mini_2 = fecha1
            co += 1
        elif max_d == fecha:
            fecha1 = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M')
            df['Dates'][co] = fecha1
            max_d = fecha1
            co += 1        
        else:
            co += 1
    
    ##### Seleccion de fechas mediante Strealit
    start_date = st.sidebar.date_input('Start Date:', mini_1_d)
    end_date = st.sidebar.date_input('End Date:', mini_2)
    start_date = str(start_date)
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = str(end_date)
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    
    if start_date < end_date:
        st.subheader('You have selected:')
        st.success('Start Date: `%s`\n\nEnd Date: `%s`' % (start_date, end_date))
    else:
        st.error('Error: The "End Date" must be after the "Start Date"')
    
    ##### Cambio de formato de 'datetime.datetime' a 'string'
    co=0
    for fecha in df['Dates']:
        if isinstance(fecha, datetime.datetime) is True:
            fecha1 = str(fecha)
            df['Dates'][co] = fecha1
            co += 1
        else:
            co +=1
    
    ##### Display de datos exclusivos entre las fechas elegidas
    #mask = (df['Dates'] > str(start_date)) & (df['Dates'] <= str(end_date))
    df = df[(df['Dates'] > str(start_date)) & (df['Dates'] <= str((end_date)))]
    
    ##### Escritura de tabla 
    #st.write(df[columnas])
    
    c1, c2 = st.beta_columns([2,2])
    with c1:
        st.subheader("Station table from "+ option2.replace('.csv','') +"")
        st.dataframe(df[columnas],width=650,height=500)
    with c2:
        st.subheader('Map of '+option+' stations')
        folium_static(m)
    
    ##### Boton de descarga
    st.subheader('Download the station data with parameters and dates selected:')
    st.markdown(get_table_download_link(df, option2), unsafe_allow_html=True)
    st.sidebar.subheader('Other statistics')
    ##### Conteo de datos por estacion
    conteo_dato_estacion=st.sidebar.checkbox('Show count of Data:',value=False)
    if conteo_dato_estacion == True:
        df = counter(option2)
        tiempo = df.columns[0]
        y_header = df.columns[1]
        st.subheader('Data Count Timeline')
        fig = px.line(df, x=tiempo,y=y_header, width=1300, height=500)
        fig.update_traces(connectgaps=False)
        st.plotly_chart(fig)
    
    ##### Promedio de temperatura por dia
    avg_estacion=st.sidebar.checkbox('Show Mean of Temperature along time of sampling:',value=False)
    if avg_estacion == True:
        df = mean_temp(option2)
        df.columns = ['Days', 'Mean Temperature']
        x_header = df.columns[0]
        y_header = df.columns[1]
        st.subheader('Mean Temperature Timeline')
        fig2 = px.line(df, x=x_header,y=y_header, width=1300, height=500)
        fig2.update_traces(connectgaps=True)
        #a1, a2 = st.beta_columns([2,2])
        st.plotly_chart(fig2)
   
    minmax_estacion=st.sidebar.checkbox('Show minimum and maximum Temperature along time of sampling:',value=False)
    if minmax_estacion == True:
        df = minmax_temp(option2)
        df.columns = ['Days', 'Min Temperature', 'Max Temperature']
        #st.dataframe(df)
        x_header = df['Days']
        y_header = df['Min Temperature']
        y_header2 = df['Max Temperature']
        st.subheader('Min and Max Temperature Timeline')
        #fig3 = px.line(df, x=x_header,y=['Min Temperature','Max Temperature'], width=1300, height=500, color="Temperature")
        #fig3.add_scatter(x=df['Days'],y=df['Max Temperature'])

        #fig3.update_traces(connectgaps=False)
    
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=x_header, y=y_header,
                            mode='lines',
                            name='Min Temperature',
                            connectgaps=False))
        fig3.add_trace(go.Scatter(x=x_header, y=y_header2,
                            mode='lines',
                            name='Max Temperature',
                            connectgaps=False))

        fig3.update_layout(autosize=False, width=1300, height=500)
        st.plotly_chart(fig3)
    


    

