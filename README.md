# PolarixDB

This is PolarixDB, a public repository of a Web App to study and analyze data of the Antartic Stations associated with AWS, SCAR and POLENET.

To start, we need to create an SQL database. We have one compiled that takes the historic record of every Antartic stations to april of 2021. The link is here:

```
https://uandresbelloedu-my.sharepoint.com/:u:/g/personal/s_woltersalas_uandresbello_edu/EZKDp7dxN5FGmsXRWmNtbKIB4h55s7QzkxugGSyTZDA8ZA?e=fZFTkS
```

To run this page it is necesary to build a conda environment with the next apps:

- sqlite3
- os
- streamlit
- pandas
- datetime
- base64
- folium
- numpy
- plotly.express
- markdown
- matplotlib

Next step to be fully functional is to change the route of every script to the download site of this repository and the file the it is needed:

| Script  | Lines of the code |
|     :---:             |  :---:      |
| Polarix_app.py        | 11          |
| Home_polarix.py       | 15, 16      |
| Data_polarix.py       | 67, 230, 231|
| Downloads_polarix.py  | 39, 40      |

Next, you only need to activate the environment and run the next comands in bash:

```
cd <the directory where you download this repository>
streamlit run Polarix_app.py
```

Open the page of PolarixDB using the IP showed in the console in your favorite web browser and analyze all the historic data of the Antarctic Stations. This contemplate Temperature, Pressure, Wind Direction and Wind Speed.
