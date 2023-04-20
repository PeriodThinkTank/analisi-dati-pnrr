import geopandas as gpd
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

### CONFIGURAZIONE PAGINA ###
st.set_page_config(
    page_title="Welcome",
    page_icon="🩸",
)
st.title("🩸 :red[Period] Think Tank")
st.header("PNRR Data Monitoring App")
### INFO SUI DATI VISUALIZZATI ###
st.markdown(
    """
        App per la visualizzazione dei dati provenienti da OpenPNRR e da ANAC, 
        e rielaborati da [Period Think Tank](https://www.thinktankperiod.org/)
        con lo scopo di indagarne gli impatti di genere.

        Fonti dati:
        * [OpenPNRR](https://openpnrr.it/)
        * [ANAC](https://pnrr.datibenecomune.it/fonti/anac/)     
    """
)


### FUNZIONI UTILI###
@st.cache_data
def fetch_data(path):
    """
        Raccoglie e pre-processa il dato CIG
    """
    data = pd.DataFrame(pd.read_excel(path))
    # data["MISSIONE"] = data["NOME_TEMATICA"].apply(lambda x: x[:2])
    # data["MISSIONE_LONG"] = data["NOME_TEMATICA"].apply(lambda x: x[:4])
    return data

@st.cache_data
def fetch_geodata(path):
    """
        Raccoglie e pre-processa il dato geografico per la mappatura 
    """
    geodata = gpd.read_file(filename=path)
    return geodata

def convert_df(df):
    return df.to_csv().encode('utf-8')


### LOADING DATA ###
# dati CIG-CUP
st.session_state["data"] = fetch_data(path="data/cig_cup_final.xlsx")
st.session_state["data_unfiltered"] = st.session_state["data"]
# geo-data
st.session_state["geodata"] = fetch_geodata(path="data/limits_IT_regions.geojson")


### SIDEBAR FILTRI ###
st.sidebar.image("assets/period_logo.png", use_column_width=True)

st.session_state["filtro_quota_femminile"] = st.sidebar.radio(
    label="Filtra sulla **Quota Femminile** prevista dal bando",
    options=("Includi tutti", "Maggiore del 30%", "Inferiore al 30%")
)

st.session_state["filtro_quota_giovanile"] = st.sidebar.radio(
    label="Filtra sulla **Quota Giovanile** prevista dal bando",
    options=("Includi tutti", "Maggiore del 30%", "Inferiore al 30%")
)
st.session_state["filtro_missioni"] = st.sidebar.multiselect(
    label="Per quali Missioni vorresti monitorare i dati PNRR?",
    options = st.session_state["data"].MISSIONE.unique()
)

st.session_state["filtro_importo_finanziato"] = st.sidebar.slider(
    label="Frazione **massima** di importo finanziato (1 = 100\% di finanziamento)",
    min_value=0.00,
    max_value=1.00,
    step = 0.05
)

st.session_state["filtro_regioni"] = st.sidebar.multiselect(
    label="Per quali Regioni vorresti monitorare i dati PNRR?",
    options = st.session_state["data"].REGIONE.unique()
)

st.session_state["filtro_province"] = st.sidebar.multiselect(
    label="Per quali Province vorresti monitorare i dati PNRR?",
    options = st.session_state["data"].PROVINCIA.unique()
)

st.session_state["filtro_comuni"] = st.sidebar.text_input(
    label="Puoi anche selezionare il nome del Comune di tuo interesse"
)


### MANIPOLAZIONE DATI ###
if st.session_state.filtro_quota_femminile != "Includi tutti":
        if st.session_state.filtro_quota_femminile == "Maggiore del 30%":
            st.session_state["data"] = st.session_state["data"][st.session_state["data"].QUOTA_FEMMINILE==">30%"]
        elif st.session_state.filtro_quota_femminile == "Inferiore al 30%":
             st.session_state["data"] = st.session_state["data"][st.session_state["data"].QUOTA_FEMMINILE!=">30%"]    

if st.session_state.filtro_quota_giovanile != "Includi tutti":
        if st.session_state.filtro_quota_giovanile == "Maggiore del 30%":
            st.session_state["data"] = st.session_state["data"][st.session_state["data"].QUOTA_GIOVANILE==">30%"]
        elif st.session_state.filtro_quota_giovanile == "Inferiore al 30%":
             st.session_state["data"] = st.session_state["data"][st.session_state["data"].QUOTA_GIOVANILE!=">30%"]

if st.session_state.filtro_regioni:
    st.session_state["data"] = st.session_state["data"][st.session_state["data"].REGIONE.isin(st.session_state["filtro_regioni"])]

if st.session_state.filtro_province:
    st.session_state["data"] = st.session_state["data"][st.session_state["data"].PROVINCIA.isin(st.session_state["filtro_province"])]

if st.session_state.filtro_comuni:
     st.session_state["data"] = st.session_state["data"][st.session_state["data"].COMUNE == st.session_state["filtro_comuni"].upper()]

if st.session_state.filtro_missioni:
    st.session_state["data"] = st.session_state["data"][st.session_state["data"].MISSIONE.isin(st.session_state["filtro_missioni"])]

st.session_state["data"] = st.session_state["data"][st.session_state["data"].IMPORTO_FINANZIATO_PCT>=st.session_state["filtro_importo_finanziato"]]


### TABELLA FILTRATA ###
with st.expander(f"Dati Filtrati"):

    st.write(f"Dati visualizzati in questo momento: {len(st.session_state.data)} righe")
    st.write(f"Stai visualizzando un totale di {st.session_state.data.CIG.nunique()} CIG distribuiti su {st.session_state.data.CUP.nunique()} CUP e su {st.session_state.data.COMUNE.nunique()} Comuni")
    st.dataframe(data=st.session_state["data"])
    csv = convert_df(st.session_state["data"])
    st.download_button(label="Clicca qui per scaricare i dati secondo i filtri che hai impostato", 
                       data=csv,
                       file_name="period_analisi_pnrr.csv",
                       mime="text/csv",
                       use_container_width=True
                       )

### MAPPA ###
cig_x_reg = pd.DataFrame(st.session_state["data"]['REGIONE'].value_counts())
cig_x_reg['COUNT'] = cig_x_reg['REGIONE']
cig_x_reg['REGIONE'] = cig_x_reg.index
cig_x_reg['REGIONE'] = cig_x_reg['REGIONE'].map(lambda x:str.title(x))
cig_x_reg['REGIONE'] = cig_x_reg['REGIONE'].str.replace('Trentino-Alto Adige','Trentino-Alto Adige/Südtirol')
cig_x_reg['REGIONE'] = cig_x_reg['REGIONE'].str.replace("Valle D'Aosta","Valle d'Aosta/Vallée d'Aoste")
st.session_state["geodata"] = pd.merge(left=st.session_state["geodata"], right=cig_x_reg, how='left', left_on='reg_name', right_on='REGIONE')
st.session_state["geodata"].set_index(st.session_state["geodata"]['reg_name'], inplace=True)

with st.container(): 
    st.subheader("Numero di Bandi - Distribuzione Regionale (dati filtrati)")
    fig = st.session_state["geodata"].plot(
        column="COUNT",
        legend=True,
        cmap='OrRd',
        missing_kwds={'color': 'lightgrey'}
    )
    fig.set_axis_off()
    st.pyplot(fig.figure, use_container_width=True)


### CHARTs ###
st.subheader("Visualizzazione dei dati priva di filtri")

with st.container():
    
    col1, col2 = st.columns(2)
    with col1: 
        st.write("Bandi che prevedono quote premiali")
        temp_df = st.session_state["data_unfiltered"].query("FLAG_MISURE_PREMIALI=='S'")
        df = pd.DataFrame(temp_df['REGIONE'].value_counts())
        df['COUNT'] = df['REGIONE']
        df['REGIONE'] = df.index
        df['REGIONE'] = df['REGIONE'].map(lambda x:str.title(x))
        best_reg = list(df.head(5).index)
        worst_reg = list(df.tail(5).index)
        st.plotly_chart(
            px.pie(df, values="COUNT", names=df.index),
            use_container_width=True
        )
    with col2:
        st.write("Regioni e numero di bandi con premialità") 
        tab1, tab2 = st.tabs(["Migliori", "Peggiori"])
        with tab1:
            st.plotly_chart(
                px.bar(
                    temp_df.query(f"REGIONE=={best_reg}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack()
                )
            )
        with tab2: 
            st.plotly_chart(
                px.bar(
                    temp_df.query(f"REGIONE=={worst_reg}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack()
                )
            )   

with st.container():
    col12, col22 = st.columns(2)
    with col12: 
        st.write("Bandi che prevedono quote femminili > 30%")
        temp_df2 = st.session_state["data_unfiltered"].query("QUOTA_FEMMINILE=='>30%'")
        df2 = pd.DataFrame(temp_df['REGIONE'].value_counts())
        df2['COUNT'] = df2['REGIONE']
        df2['REGIONE'] = df2.index
        df2['REGIONE'] = df2['REGIONE'].map(lambda x:str.title(x))
        best_reg2 = list(df2.head(5).index)
        worst_reg2 = list(df2.tail(5).index)
        st.plotly_chart(
            px.pie(df2, values="COUNT", names=df2.index),
            use_container_width=True
        )
    with col22: 
        st.write("Regioni e bandi con quota femminile > 30%") 
        tab12, tab22 = st.tabs(["Migliori", "Peggiori"])
        with tab12:
            st.plotly_chart(
                px.bar(
                    temp_df2.query(f"REGIONE=={best_reg2}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack()
                )
            )
        with tab22:
            st.plotly_chart(
                px.bar(
                    temp_df2.query(f"REGIONE=={worst_reg2}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack()
                )
            )   

with st.container():
    col13, col23 = st.columns(2)
    with col13: 
        st.write("Bandi che prevedono quote giovanili > 30%")
        temp_df3 = st.session_state["data_unfiltered"].query("QUOTA_GIOVANILE=='>30%'")
        df3 = pd.DataFrame(temp_df['REGIONE'].value_counts())
        df3['COUNT'] = df3['REGIONE']
        df3['REGIONE'] = df3.index
        df3['REGIONE'] = df3['REGIONE'].map(lambda x:str.title(x))
        best_reg3 = list(df3.head(5).index)
        worst_reg3= list(df3.tail(5).index)
        st.plotly_chart(
            px.pie(df3, values="COUNT", names=df3.index),
            use_container_width=True
        )
    with col23: 
        st.write("Regioni e bandi con quota giovanile > 30%") 
        tab13, tab23 = st.tabs(["Migliori", "Peggiori"])
        with tab13:
            st.plotly_chart(
                px.bar(
                    temp_df3.query(f"REGIONE=={best_reg3}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack()
                )
            )
        with tab23:
            st.plotly_chart(
                px.bar(
                    temp_df3.query(f"REGIONE=={worst_reg3}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack()
                )
            )