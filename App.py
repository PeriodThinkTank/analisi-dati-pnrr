import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

### CONFIGURAZIONE PAGINA ###
st.set_page_config(
    page_title="Period PNRR Monitoring App",
    page_icon="🩸",
)
st.title("🩸 :red[Period] Think Tank")
st.header("PNRR Data Monitoring App")
### INFO SUI DATI VISUALIZZATI ###
st.markdown(
    """
        App per la visualizzazione e l'analisi dei dati aperti riguardanti i bandi di gara finanziati dal PNRR provenienti da OpenPNRR, ANAC e OpenCUP, 
        e rielaborati da [Period Think Tank](https://www.thinktankperiod.org/), associazione femminista che promuove l'equità di genere attraverso un approccio femminista ai dati.  

        Lo scopo dell'app è di indagare la presenza e la distribuzioni sul territorio e sulle missioni, 
        delle quote occupazionali minime o misure premiali per donne e giovani nei bandi di gara emessi.  

        **ATTENZIONE**  
        questa è una prima versione della nostra App, pertanto qualsiasi segnalazione bug o problematiche è caldamente incoraggiata.
        Per segnalazioni scrivere a info@thinktankperiod.org.

        #### Fonti dati:
        * [OpenPNRR](https://openpnrr.it/)
        * [OpenCUP](https://www.opencup.gov.it/portale/web/opencup/opendata)
        * [ANAC](https://pnrr.datibenecomune.it/fonti/anac/)
        * [Guida ai dati aperti sul PNRR](https://pnrr.datibenecomune.it/)     

        Le informazioni geografiche sono state ottenute dal merge tra CIG e CUP. La realazione tra questi due codici è "molti a molti", ovvero un CIG può essere associato a più CUP e viceversa.
        Poichè non sono disponibili le informazioni sulla distribuzione dell’importo economico e su differenti comuni per i CUP associati, si sono considerati i CIG in conteggio distinto.  
        Per avere informazioni sui progetti collegati ai bandi di gara è sufficiente utilizzare il codice CUP all'interno della banca dati di OpenCup. 

        I valori mostrati sono valori percentuali, si confronta il totale dei cig con l'attributo mostrato (misure premiali, quote>30%) ecc, 
        sul totale dei CIG per quel raggruppamento. I grafici a torta rappresentano la distribuzione dei CIG per regione sul totale dei CIG.  
        I grafici a barre rappresentano la percentuale dei CIG con premialità (quota femminile >30%, quota giovanile>30%..) sul totale dei CIG per Regione/Missione nel primo tab, e per Missione/Componente nel secondo tab. 

        #### Note sui Filtri:
        * I filtri impattano su tutti i grafici.
        * I grafici sulla presenza di misure premiali e sulle quote femminili/giovanili mostreranno sempre i dati filtrati per queste caratteristiche.
        * In fondo alla pagina è possibile visualizzare il riepilogo dei filtri selezionati
        * Possibilità di esportare il dataset in formato csv tramite la app.     
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
    options = st.session_state["data"].REGIONE.dropna().sort_values().unique()
)

st.session_state["filtro_province"] = st.sidebar.multiselect(
    label="Per quali **Province** vorresti monitorare i dati PNRR?",
    options = st.session_state["data"].PROVINCIA.dropna().sort_values().unique()
)

st.session_state["filtro_comuni"] = st.sidebar.text_input(
    label="Puoi anche selezionare il nome del **Comune** di tuo interesse"
)

st.session_state["filtro_motivo_urgenza"] = st.sidebar.multiselect(
    label="Ti interessa monitorare un **motivo di urgenza** specifico?",
    options = st.session_state["data"].MOTIVO_URGENZA.sort_values().unique(),
)

st.session_state["filtro_esito"] = st.sidebar.multiselect(
    label="Ti interessa monitorare bandi con un **esito** specifico?",
    options = st.session_state["data"].ESITO.sort_values().unique()
)

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

if any(v=="None" for v in st.session_state["filters"].values()):
    st.warning(body="Per visualizzare correttamente l'analisi, rimuovere '**None**' dai filtri",
                icon="⚠️")

### MANIPOLAZIONE DATI ### 
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
cig_x_prov = pd.DataFrame(st.session_state["data"][["CIG","PROVINCIA"]].groupby(['PROVINCIA'])['CIG'].nunique())
cig_x_prov['PROVINCIA'] = cig_x_prov.index
cig_x_prov['PROVINCIA'] = cig_x_prov['PROVINCIA'].map(lambda x:str.title(x))

with st.container():
    st.subheader("Numero di Bandi - Distribuzione Provinciale")
    mappa_provinciale = px.choropleth(
                                data_frame=cig_x_prov, 
                                geojson=st.session_state["province"], 
                                locations='PROVINCIA', 
                                color='CIG', 
                                featureidkey='properties.prov_name', 
                                color_continuous_scale='PurD', 
                                range_color=(0, max(cig_x_prov['CIG'])),
                                labels={'COUNT':'Bandi PNRR per Provincia'}
                                )
    mappa_provinciale.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    mappa_provinciale.update_geos(fitbounds="locations", visible=False)
    mappa_provinciale.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    st.plotly_chart(mappa_provinciale, use_container_width=True)

### DIVISIONE REGIONI/MISSIONI ###
full_count = pd.DataFrame(st.session_state.data_charts[["CIG","REGIONE","MISSIONE"]].groupby(["REGIONE", "MISSIONE"])["CIG"].nunique())
full_count.columns = ["NUMERO_CIG"]
full_count['PCT_CIG_MISSIONE_REGIONE'] = full_count['NUMERO_CIG'] / full_count.groupby('REGIONE')['NUMERO_CIG'].transform('sum') * 100
full_count['PCT_CIG_MISSIONE_REGIONE'] = full_count['PCT_CIG_MISSIONE_REGIONE'].apply(lambda x: f'{x:.2f}%')

### DIVISIONE MISSIONI/COMPONENTI ###
full_count2 = pd.DataFrame(st.session_state.data_charts[["CIG","COMPONENTE","CODICE_MISSIONE"]].groupby(["CODICE_MISSIONE", "COMPONENTE"])["CIG"].nunique())
full_count2.columns = ["NUMERO_CIG"]
full_count2['PERCENTAGE_TOTAL_CIG'] = full_count2['NUMERO_CIG'] / full_count2.groupby('CODICE_MISSIONE')['NUMERO_CIG'].transform('sum') * 100
full_count2['PERCENTAGE_TOTAL_CIG'] = full_count2['PERCENTAGE_TOTAL_CIG'].apply(lambda x: f'{x:.2f}%')

### GRAFICI ###
with st.container():
    
    st.write("**Bandi che prevedono quote premiali**")
    temp_df = st.session_state["data_charts"].query("FLAG_MISURE_PREMIALI=='S'")[["CIG","REGIONE","MISSIONE"]]
    counts = pd.DataFrame(temp_df[["CIG","REGIONE"]].groupby(['REGIONE'])['CIG'].nunique())
    st.plotly_chart(
        px.pie(counts, 
                values="CIG", 
                names=counts.index, 
                color_discrete_sequence=px.colors.sequential.PuRd
                ),
        use_container_width=True
    )
    tab1, tab2 = st.tabs(["Regioni e numero di bandi con premialità", "Componenti dei bandi con premialità"])
    with tab1:
        regioni_filtered = pd.DataFrame(temp_df.groupby(["REGIONE", "MISSIONE"])["CIG"].nunique())
        regioni_filtered.columns = ["CIG_FILTRATI"]
        regioni_filtered['PCT_CIG_FILT_MISS_REG'] = regioni_filtered['CIG_FILTRATI'] / regioni_filtered.groupby('REGIONE')['CIG_FILTRATI'].transform('sum') * 100
        regioni_filtered['PCT_CIG_FILT_MISS_REG'] = regioni_filtered['PCT_CIG_FILT_MISS_REG'].apply(lambda x: f'{x:.2f}%')
        regioni_recap = pd.merge(full_count, regioni_filtered, left_index=True, right_index=True, how="outer")
        regioni_recap["PRESENCE_ON_TOTAL_CIGS"] = round((regioni_recap["CIG_FILTRATI"] / regioni_recap["NUMERO_CIG"])*100)
        regioni_sum = regioni_recap.groupby(['REGIONE'])['CIG_FILTRATI', 'NUMERO_CIG'].sum()
        regioni_sum['RATIO'] = regioni_sum['CIG_FILTRATI'] / regioni_sum['NUMERO_CIG']
        fig = px.bar(
            regioni_recap.reset_index(), 
            x="REGIONE", y="CIG_FILTRATI", 
            color="MISSIONE",
            color_discrete_sequence=px.colors.sequential.PuRd,
            hover_data=["MISSIONE","PRESENCE_ON_TOTAL_CIGS"]
        )
        fig.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
        for i, r in regioni_sum.iterrows():
            fig.add_annotation(x=i, y=r['CIG_FILTRATI']+20, text=f"{r['RATIO']:.2%}", showarrow=False, textangle=90)
        fig.update_traces(hovertemplate=
                        'Missione: %{customdata[0]} <br>'+
                        'Numero di CIG (filtrati) per Missione nella Regione: %{y} <br>'+
                        'Percentuale rispetto al totale dei CIG per Missione nella Regione: %{customdata[1]}%'
                        )
        st.plotly_chart(fig)
    with tab2: 
        temp_df_a = st.session_state["data_charts"].query("FLAG_MISURE_PREMIALI=='S'")[["CIG","CODICE_MISSIONE", "COMPONENTE"]]
        missioni_filtered = pd.DataFrame(temp_df_a.groupby(["CODICE_MISSIONE", "COMPONENTE"])["CIG"].nunique())
        missioni_filtered.columns = ["CIG_FILTRATI"]
        missioni_filtered['PERCENTAGE'] = missioni_filtered['CIG_FILTRATI'] / missioni_filtered.groupby('CODICE_MISSIONE')['CIG_FILTRATI'].transform('sum') * 100
        missioni_filtered['PERCENTAGE'] = missioni_filtered['PERCENTAGE'].apply(lambda x: f'{x:.2f}%')
        missioni_recap = pd.merge(full_count2, missioni_filtered, left_index=True, right_index=True, how="outer")
        missioni_recap["PRESENCE_ON_TOTAL_CIGS"] = round((missioni_recap["CIG_FILTRATI"] / missioni_recap["NUMERO_CIG"])*100)
        missioni_sum = missioni_recap.groupby(['CODICE_MISSIONE'])['CIG_FILTRATI', 'NUMERO_CIG'].sum()
        missioni_sum['RATIO'] = missioni_sum['CIG_FILTRATI'] / missioni_sum['NUMERO_CIG']
        fig_a = px.bar(
            missioni_recap.reset_index(), 
            x="CODICE_MISSIONE", 
            y="CIG_FILTRATI", 
            color="COMPONENTE",
            color_discrete_sequence=px.colors.sequential.PuRd,
            hover_data=["COMPONENTE", 'PRESENCE_ON_TOTAL_CIGS']
        )
        fig_a.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
        for i, r in missioni_sum.iterrows():
            fig_a.add_annotation(x=i, y=r['CIG_FILTRATI']+40, text=f"{r['RATIO']:.2%}", showarrow=False, textangle=90)
        fig_a.update_traces(hovertemplate=
                        'Componente: %{customdata[0]}<br>'+
                        'Numero di CIG filtrati per Componente nella Missione: %{y} <br>'+
                        'Percentuale rispetto al totale dei CIG per Componente nella Missione: %{customdata[1]}%'
                        )
        st.plotly_chart(fig_a)

with st.container():
    st.write("**Bandi che prevedono quote femminili > 30%**")
    temp_df2 = st.session_state["data_charts"].query("QUOTA_FEMMINILE=='>30%'")[["CIG","REGIONE","MISSIONE"]]
    counts2 = pd.DataFrame(temp_df2[["CIG","REGIONE"]].groupby(['REGIONE'])['CIG'].nunique())
    st.plotly_chart(
        px.pie(counts2, 
                values="CIG", 
                names=counts2.index, 
                color_discrete_sequence=px.colors.sequential.PuRd
                ),
        use_container_width=True
        )
    tab3, tab4 = st.tabs(["Regioni e bandi con quota femminile > 30%", "Componenti dei bandi con quota femminile > 30%"])
    with tab3:    
        regioni_filtered2 = pd.DataFrame(temp_df2.groupby(["REGIONE", "MISSIONE"])["CIG"].nunique())
        regioni_filtered2.columns = ["CIG_FILTRATI"]
        regioni_filtered2['PCT_CIG_FILT_MISS_REG'] = regioni_filtered2['CIG_FILTRATI'] / regioni_filtered2.groupby('REGIONE')['CIG_FILTRATI'].transform('sum') * 100
        regioni_filtered2['PCT_CIG_FILT_MISS_REG'] = regioni_filtered2['PCT_CIG_FILT_MISS_REG'].apply(lambda x: f'{x:.2f}%')
        regioni_recap2 = pd.merge(full_count, regioni_filtered2, left_index=True, right_index=True, how="outer")
        regioni_recap2["PRESENCE_ON_TOTAL_CIGS"] = round((regioni_recap2["CIG_FILTRATI"] / regioni_recap2["NUMERO_CIG"])*100)
        regioni_sum2 = regioni_recap2.groupby(['REGIONE'])['CIG_FILTRATI', 'NUMERO_CIG'].sum()
        regioni_sum2['RATIO'] = regioni_sum2['CIG_FILTRATI'] / regioni_sum2['NUMERO_CIG']
        fig2 = px.bar(
            regioni_recap2.reset_index(), 
            x="REGIONE", y="CIG_FILTRATI", 
            color="MISSIONE",
            color_discrete_sequence=px.colors.sequential.PuRd,
            hover_data=["MISSIONE", "PRESENCE_ON_TOTAL_CIGS"]
        )
        fig2.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
        for i, r in regioni_sum2.iterrows():
            fig2.add_annotation(x=i, y=r['CIG_FILTRATI']+100, text=f"{r['RATIO']:.2%}", showarrow=False, textangle=90)
        fig2.update_traces(hovertemplate=
                        'Missione: %{customdata[0]} <br>'+
                        'Numero di CIG (filtrati) per Missione nella Regione: %{y} <br>'+
                        'Percentuale rispetto al totale dei CIG per Missione nella Regione: %{customdata[1]}%'
                        )
        st.plotly_chart(fig2)
    with tab4:
        temp_df_b = st.session_state["data_charts"].query("QUOTA_FEMMINILE=='>30%'")[["CIG","CODICE_MISSIONE", "COMPONENTE"]]
        missioni_filtered2 = pd.DataFrame(temp_df_b.groupby(["CODICE_MISSIONE", "COMPONENTE"])["CIG"].nunique())
        missioni_filtered2.columns = ["CIG_FILTRATI"]
        missioni_filtered2['PERCENTAGE'] = missioni_filtered2['CIG_FILTRATI'] / missioni_filtered2.groupby('CODICE_MISSIONE')['CIG_FILTRATI'].transform('sum') * 100
        missioni_filtered2['PERCENTAGE'] = missioni_filtered2['PERCENTAGE'].apply(lambda x: f'{x:.2f}%')
        missioni_recap2 = pd.merge(full_count2, missioni_filtered2, left_index=True, right_index=True, how="outer")
        missioni_recap2["PRESENCE_ON_TOTAL_CIGS"] = round((missioni_recap2["CIG_FILTRATI"] / missioni_recap2["NUMERO_CIG"])*100)
        missioni_sum2 = missioni_recap2.groupby(['CODICE_MISSIONE'])['CIG_FILTRATI', 'NUMERO_CIG'].sum()
        missioni_sum2['RATIO'] = missioni_sum2['CIG_FILTRATI'] / missioni_sum2['NUMERO_CIG']
        fig_b = px.bar(
            missioni_recap2.reset_index(), 
            x="CODICE_MISSIONE", 
            y="CIG_FILTRATI", 
            color="COMPONENTE",
            color_discrete_sequence=px.colors.sequential.PuRd,
            hover_data=["COMPONENTE", 'PRESENCE_ON_TOTAL_CIGS']
        )
        fig_b.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
        for i, r in missioni_sum2.iterrows():
            fig_b.add_annotation(x=i, y=r['CIG_FILTRATI']+150, text=f"{r['RATIO']:.2%}", showarrow=False, textangle=90)
        fig_b.update_traces(hovertemplate=
                        'Componente: %{customdata[0]}<br>'+
                        'Numero di CIG filtrati per Componente nella Missione: %{y} <br>'+
                        'Percentuale rispetto al totale dei CIG per Componente nella Missione: %{customdata[1]}%'
                        )
        st.plotly_chart(fig_b)

with st.container():
    st.write("**Bandi che prevedono quota giovanile > 30%**")
    temp_df3 = st.session_state["data_charts"].query("QUOTA_GIOVANILE=='>30%'")[["CIG","REGIONE","MISSIONE"]]
    counts3 = pd.DataFrame(temp_df3[["CIG","REGIONE"]].groupby(['REGIONE'])['CIG'].nunique())
    st.plotly_chart(
        px.pie(counts3, 
                values="CIG", 
                names=counts3.index, 
                color_discrete_sequence=px.colors.sequential.PuRd
                ),
        use_container_width=True
        )
    tab5, tab6 = st.tabs(["Regioni e bandi con quota giovanile > 30%", "Componenti dei bandi con quota giovanile > 30%"])
    with tab5:
        regioni_filtered3 = pd.DataFrame(temp_df3.groupby(["REGIONE", "MISSIONE"])["CIG"].nunique())
        regioni_filtered3.columns = ["CIG_FILTRATI"]
        regioni_filtered3['PCT_CIG_FILT_MISS_REG'] = regioni_filtered3['CIG_FILTRATI'] / regioni_filtered3.groupby('REGIONE')['CIG_FILTRATI'].transform('sum') * 100
        regioni_filtered3['PCT_CIG_FILT_MISS_REG'] = regioni_filtered3['PCT_CIG_FILT_MISS_REG'].apply(lambda x: f'{x:.2f}%')
        regioni_recap3 = pd.merge(full_count, regioni_filtered3, left_index=True, right_index=True, how="outer")
        regioni_recap3["PRESENCE_ON_TOTAL_CIGS"] = round((regioni_recap3["CIG_FILTRATI"] / regioni_recap3["NUMERO_CIG"])*100)
        regioni_sum3 = regioni_recap3.groupby(['REGIONE'])['CIG_FILTRATI', 'NUMERO_CIG'].sum()
        regioni_sum3['RATIO'] = regioni_sum3['CIG_FILTRATI'] / regioni_sum3['NUMERO_CIG']
        fig3 = px.bar(
            regioni_recap3.reset_index(), 
            x="REGIONE", y="CIG_FILTRATI", 
            color="MISSIONE",
            color_discrete_sequence=px.colors.sequential.PuRd,
            hover_data=["MISSIONE", "PRESENCE_ON_TOTAL_CIGS"]
        )
        fig3.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
        for i, r in regioni_sum3.iterrows():
            fig3.add_annotation(x=i, y=r['CIG_FILTRATI']+100, text=f"{r['RATIO']:.2%}", showarrow=False, textangle=90)
        fig3.update_traces(hovertemplate=
                            'Missione: %{customdata[0]} <br>'+
                            'Numero di CIG (filtrati) per Missione nella Regione: %{y} <br>'+
                            'Percentuale rispetto al totale dei CIG per Missione nella Regione: %{customdata[1]}%'
                        )
        st.plotly_chart(fig3)
    with tab6:
        temp_df_c = st.session_state["data_charts"].query("QUOTA_GIOVANILE=='>30%'")[["CIG","CODICE_MISSIONE", "COMPONENTE"]]
        missioni_filtered3 = pd.DataFrame(temp_df_c.groupby(["CODICE_MISSIONE", "COMPONENTE"])["CIG"].nunique())
        missioni_filtered3.columns = ["CIG_FILTRATI"]
        missioni_filtered3['PERCENTAGE'] = missioni_filtered3['CIG_FILTRATI'] / missioni_filtered3.groupby('CODICE_MISSIONE')['CIG_FILTRATI'].transform('sum') * 100
        missioni_filtered3['PERCENTAGE'] = missioni_filtered3['PERCENTAGE'].apply(lambda x: f'{x:.2f}%')
        missioni_recap3 = pd.merge(full_count2, missioni_filtered3, left_index=True, right_index=True, how="outer")
        missioni_recap3["PRESENCE_ON_TOTAL_CIGS"] = round((missioni_recap3["CIG_FILTRATI"] / missioni_recap3["NUMERO_CIG"])*100)
        missioni_sum3 = missioni_recap3.groupby(['CODICE_MISSIONE'])['CIG_FILTRATI', 'NUMERO_CIG'].sum()
        missioni_sum3['RATIO'] = missioni_sum3['CIG_FILTRATI'] / missioni_sum3['NUMERO_CIG']
        fig_c = px.bar(
            missioni_recap3.reset_index(), 
            x="CODICE_MISSIONE", 
            y="CIG_FILTRATI", 
            color="COMPONENTE",
            color_discrete_sequence=px.colors.sequential.PuRd,
            hover_data=["COMPONENTE", 'PRESENCE_ON_TOTAL_CIGS']
        )
        fig_c.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
        for i, r in missioni_sum3.iterrows():
            fig_c.add_annotation(x=i, y=r['CIG_FILTRATI']+200, text=f"{r['RATIO']:.2%}", showarrow=False, textangle=90)
        fig_c.update_traces(hovertemplate=
                        'Componente: %{customdata[0]}<br>'+
                        'Numero di CIG filtrati per Componente nella Missione: %{y} <br>'+
                        'Percentuale rispetto al totale dei CIG per Componente nella Missione: %{customdata[1]}%'
                        )
        st.plotly_chart(fig_c)


### RECAP FILTRI IMPOSTATI ###
with st.expander("Espandi per visualizzare un riassunto dei filtri selezionati"):
    filter_df = pd.DataFrame.from_dict(st.session_state["filters"], orient="index", columns=["Value"])
    st.dataframe(data=filter_df, use_container_width=True)
            