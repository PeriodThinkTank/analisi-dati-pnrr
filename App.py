import json
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
def fetch_data(path:str)->pd.DataFrame:
    """
        Raccoglie il dato CIG
    """
    data = pd.DataFrame(pd.read_parquet(path, engine="pyarrow"))
    return data

@st.cache_data
def fetch_geojson(path:str)->dict:
    """
        Raccoglie e pre-processa il dato geografico per la mappatura 
    """
    with open(path, "r") as file:
        geojson = json.load(file)
    return geojson

def convert_df(df):
    return df.to_csv().encode('utf-8')


### LOADING DATA ###
# dati CIG-CUP
st.session_state["data"] = fetch_data(path="data/cig_cup_final.parquet")
st.session_state["data_charts"] = st.session_state["data"]
# geo-data
st.session_state["province"] = fetch_geojson(path="data/geojson_province_IT.json")


### SIDEBAR FILTRI ###
st.sidebar.image("assets/period_logo.png", use_column_width=True)

st.session_state["flag_premiali"] = st.sidebar.checkbox(
    label="Visualizzare solo quei bandi che prevedono **Misure Premiali**?"
)

st.session_state["flag_urgenza"] = st.sidebar.checkbox(
    label="Visualizzare solo quei bandi la cui realizzazione è contrassegnata come **urgente**?"
)

st.session_state["filtro_quota_femminile"] = st.sidebar.radio(
    label="Filtra sulla **Quota Femminile** prevista dal bando",
    options=("Includi tutti", "Maggiore del 30%", "Inferiore al 30%")
)

st.session_state["filtro_quota_giovanile"] = st.sidebar.radio(
    label="Filtra sulla **Quota Giovanile** prevista dal bando",
    options=("Includi tutti", "Maggiore del 30%", "Inferiore al 30%")
)
st.session_state["filtro_missioni"] = st.sidebar.multiselect(
    label="Per quali **Missioni** vorresti monitorare i dati PNRR?",
    options = st.session_state["data"].MISSIONE.sort_values().unique()
)

st.session_state["filtro_importo_finanziato"] = st.sidebar.multiselect(
    label="Entità dell'**importo** del singolo CIG",
    options = ["BASSA", "MEDIA", "ALTA"],
    help="BASSA: minore di 100.000€, MEDIA è compresa tra 100.000€ e 1.000.000€, ALTA è oltre 1.000.000.000€"
)

st.session_state["filtro_regioni"] = st.sidebar.multiselect(
    label="Per quali **Regioni** vorresti monitorare i dati PNRR?",
    options = st.session_state["data"].REGIONE.sort_values().unique()
)

st.session_state["filtro_province"] = st.sidebar.multiselect(
    label="Per quali **Province** vorresti monitorare i dati PNRR?",
    options = st.session_state["data"].PROVINCIA.sort_values().unique()
)

st.session_state["filtro_comuni"] = st.sidebar.text_input(
    label="Puoi anche selezionare il nome del **Comune** di tuo interesse"
)

st.session_state["filtro_motivo_urgenza"] = st.sidebar.multiselect(
    label="Ti interessa monitorare un **motivo di urgenza** specifico?",
    options = st.session_state["data"].MOTIVO_URGENZA.sort_values().unique()
)

st.session_state["filtro_esito"] = st.sidebar.multiselect(
    label="Ti interessa monitorare bandi con un **esito** specifico?",
    options = st.session_state["data"].ESITO.sort_values().unique()
)


### MANIPOLAZIONE DATI ###
## mappa ##  
if st.session_state["flag_premiali"]:
    st.session_state["data"] = st.session_state["data"].query("FLAG_MISURE_PREMIALI=='S'")

if st.session_state["flag_urgenza"]:
    st.session_state["data"] = st.session_state["data"].query("FLAG_URGENZA==1")

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

if st.session_state.filtro_motivo_urgenza:
    st.session_state["data"] = st.session_state["data"][st.session_state["data"].MOTIVO_URGENZA.isin(st.session_state["filtro_motivo_urgenza"])]

if st.session_state.filtro_esito:
    st.session_state["data"] = st.session_state["data"][st.session_state["data"].ESITO.isin(st.session_state["filtro_esito"])]

if st.session_state.filtro_importo_finanziato:
    st.session_state["data"] = st.session_state["data"][st.session_state["data"].CLASSE_IMPORTO.isin(st.session_state["filtro_importo_finanziato"])]


## pie+bar charts##
if st.session_state.filtro_regioni:
    st.session_state["data_charts"] = st.session_state["data_charts"][st.session_state["data_charts"].REGIONE.isin(st.session_state["filtro_regioni"])]

if st.session_state.filtro_province:
    st.session_state["data_charts"] = st.session_state["data_charts"][st.session_state["data_charts"].PROVINCIA.isin(st.session_state["filtro_province"])]

if st.session_state.filtro_comuni:
     st.session_state["data_charts"] = st.session_state["data_charts"][st.session_state["data_charts"].COMUNE == st.session_state["filtro_comuni"].upper()]

if st.session_state.filtro_missioni:
    st.session_state["data_charts"] = st.session_state["data_charts"][st.session_state["data_charts"].MISSIONE.isin(st.session_state["filtro_missioni"])]

if st.session_state.filtro_motivo_urgenza:
    st.session_state["data_charts"] = st.session_state["data_charts"][st.session_state["data_charts"].MOTIVO_URGENZA.isin(st.session_state["filtro_motivo_urgenza"])]

if st.session_state.filtro_esito:
    st.session_state["data_charts"] = st.session_state["data_charts"][st.session_state["data_charts"].ESITO.isin(st.session_state["filtro_esito"])]

if st.session_state.filtro_importo_finanziato:
    st.session_state["data_charts"] = st.session_state["data_charts"][st.session_state["data_charts"].CLASSE_IMPORTO.isin(st.session_state["filtro_importo_finanziato"])]


### FINE APPLICAZIONI FILTRI ###
st.info(
    f"Stai visualizzando un totale di {st.session_state.data.CIG.nunique()} CIG distribuiti su {st.session_state.data.CUP.nunique()} CUP e su {st.session_state.data.COMUNE.nunique()} Comuni", 
    icon="ℹ️"
)

### TABELLA FILTRATA ###
with st.expander("Espandi per visualizzare i dati filtrati"):
    st.dataframe(data=st.session_state["data"])
    csv = convert_df(st.session_state["data"])
    st.download_button(label="Clicca qui per scaricare i dati secondo i filtri impostati", 
                       data=csv,
                       file_name="period_analisi_pnrr.csv",
                       mime="text/csv",
                       use_container_width=True
                       )

### MAPPA ###
cig_x_prov = pd.DataFrame(st.session_state["data"]["PROVINCIA"].value_counts())
cig_x_prov['COUNT'] = cig_x_prov['PROVINCIA']
cig_x_prov['PROVINCIA'] = cig_x_prov.index
cig_x_prov['PROVINCIA'] = cig_x_prov['PROVINCIA'].map(lambda x:str.title(x))

with st.container():
    st.subheader("Numero di Bandi - Distribuzione Provinciale")
    mappa_provinciale = px.choropleth(
                                data_frame=cig_x_prov, 
                                geojson=st.session_state["province"], 
                                locations='PROVINCIA', 
                                color='COUNT', 
                                featureidkey='properties.prov_name', 
                                color_continuous_scale='PurD', 
                                range_color=(0, max(cig_x_prov['COUNT'])),
                                labels={'COUNT':'Bandi PNRR per Provincia'}
                                )
    mappa_provinciale.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    mappa_provinciale.update_geos(fitbounds="locations", visible=False)
    mappa_provinciale.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    st.plotly_chart(mappa_provinciale, use_container_width=True)

### CHARTs ###
with st.container():
    
    col1, col2 = st.columns(2)
    with col1: 
        st.write("Bandi che prevedono quote premiali")
        temp_df = st.session_state["data_charts"].query("FLAG_MISURE_PREMIALI=='S'")
        df = pd.DataFrame(temp_df['REGIONE'].value_counts())
        df['COUNT'] = df['REGIONE']
        df['REGIONE'] = df.index
        df['REGIONE'] = df['REGIONE'].map(lambda x:str.title(x))
        best_reg = list(df.head(5).index)
        worst_reg = list(df.tail(5).index)
        st.plotly_chart(
            px.pie(df, values="COUNT", 
                   names=df.index, color_discrete_sequence=px.colors.sequential.PuRd),
            use_container_width=True
        )
    with col2:
        st.write("Regioni e numero di bandi con premialità") 
        tab1, tab2 = st.tabs(["Migliori", "Peggiori"])
        with tab1:
            st.plotly_chart(
                px.bar(
                    temp_df.query(f"REGIONE=={best_reg}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack(),
                    color_discrete_sequence=px.colors.sequential.PuRd
                ).update_layout(xaxis={'categoryorder':'total descending'})
            )
        with tab2: 
            st.plotly_chart(
                px.bar(
                    temp_df.query(f"REGIONE=={worst_reg}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack(),
                    color_discrete_sequence=px.colors.sequential.PuRd
                ).update_layout(xaxis={'categoryorder':'total ascending'})
            )   

with st.container():
    col12, col22 = st.columns(2)
    with col12: 
        st.write("Bandi che prevedono quote femminili > 30%")
        temp_df2 = st.session_state["data_charts"].query("QUOTA_FEMMINILE=='>30%'")
        df2 = pd.DataFrame(temp_df2['REGIONE'].value_counts())
        df2['COUNT'] = df2['REGIONE']
        df2['REGIONE'] = df2.index
        df2['REGIONE'] = df2['REGIONE'].map(lambda x:str.title(x))
        best_reg2 = list(df2.head(5).index)
        worst_reg2 = list(df2.tail(5).index)
        st.plotly_chart(
            px.pie(df2, values="COUNT", 
                   names=df2.index, color_discrete_sequence=px.colors.sequential.PuRd),
            use_container_width=True
        )
    with col22: 
        st.write("Regioni e bandi con quota femminile > 30%") 
        tab12, tab22 = st.tabs(["Migliori", "Peggiori"])
        with tab12:
            st.plotly_chart(
                px.bar(
                    temp_df2.query(f"REGIONE=={best_reg2}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack(),
                    color_discrete_sequence=px.colors.sequential.PuRd
                ).update_layout(xaxis={'categoryorder':'total descending'})
            )
        with tab22:
            st.plotly_chart(
                px.bar(
                    temp_df2.query(f"REGIONE=={worst_reg2}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack(),
                    color_discrete_sequence=px.colors.sequential.PuRd
                ).update_layout(xaxis={'categoryorder':'total ascending'})
            )   

with st.container():
    col13, col23 = st.columns(2)
    with col13: 
        st.write("Bandi che prevedono quote giovanili > 30%")
        temp_df3 = st.session_state["data_charts"].query("QUOTA_GIOVANILE=='>30%'")
        df3 = pd.DataFrame(temp_df3['REGIONE'].value_counts())
        df3['COUNT'] = df3['REGIONE']
        df3['REGIONE'] = df3.index
        df3['REGIONE'] = df3['REGIONE'].map(lambda x:str.title(x))
        best_reg3 = list(df3.head(5).index)
        worst_reg3= list(df3.tail(5).index)
        st.plotly_chart(
            px.pie(df3, values="COUNT", 
                   names=df3.index, color_discrete_sequence=px.colors.sequential.PuRd),
            use_container_width=True
        )
    with col23: 
        st.write("Regioni e bandi con quota giovanile > 30%") 
        tab13, tab23 = st.tabs(["Migliori", "Peggiori"])
        with tab13:
            st.plotly_chart(
                px.bar(
                    temp_df3.query(f"REGIONE=={best_reg3}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack(),
                    color_discrete_sequence=px.colors.sequential.PuRd
                ).update_layout(xaxis={'categoryorder':'total descending'})
            )
        with tab23:
            st.plotly_chart(
                px.bar(
                    temp_df3.query(f"REGIONE=={worst_reg3}")[["REGIONE", "MISSIONE"]].groupby("REGIONE")["MISSIONE"].value_counts().unstack(),
                    color_discrete_sequence=px.colors.sequential.PuRd
                ).update_layout(xaxis={'categoryorder':'total ascending'})
            )


# Set up the filters and store them in st.session_state["filter"]
st.session_state["filters"] = {
                            "flag_premiali":st.session_state["flag_premiali"],
                            "flag_urgenza":st.session_state["flag_urgenza"],
                            "filtro_quota_femminile":st.session_state["filtro_quota_femminile"],
                            "filtro_quota_giovanile":st.session_state["filtro_quota_giovanile"],
                            "filtro_missioni":st.session_state["filtro_missioni"],
                            "filtro_importo":st.session_state["filtro_importo_finanziato"],
                            "filtro_regioni":st.session_state["filtro_regioni"], 
                            "filtro_province":st.session_state["filtro_province"],
                            "filtro_comuni":st.session_state["filtro_comuni"],
                            "filtro_motivo_urgenza":st.session_state["filtro_motivo_urgenza"],
                            "filtro_esito":st.session_state["filtro_esito"]
}

# Display a table with the filters and their values
with st.expander("Espandi per visualizzare un riassunto dei filtri selezionati"):
    filter_df = pd.DataFrame.from_dict(st.session_state["filters"], orient="index", columns=["Value"])
    st.dataframe(data=filter_df)
            