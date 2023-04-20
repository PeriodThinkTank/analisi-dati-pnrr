## Dati Da Visualizzare
* misure premiali
* quota femminile
* quota giovanile 
* missioni = M1-M6 della colonna "NOME_TEMATICA"
* regione/provincia associate alle quote
* tematica
* settore/sottosettore intervento --> https://plotly.com/python/radar-chart/
* anno decisione
* importo lavori? vs finanziamento?
* totale CIG e totale CUP (bisogna andare in distinct?)

## Filtri da impostare
- [x] quota femminile >30%? --> https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
- [x] quota giovanile?
- [x] premialità quota
- [x] regione
- [x] provincia
- [] codice tematica
- [x] importo finanziato

## To do
- [] utilizzare geopandas per leggere gli shapefile ISTAT
- [x] utilizzare tutto il dataset (con associazione CIG su CUP) per poi filtrare nella App
- [x] implementazione bottone di download per scaricare i dati manipolati
- [x] utilizzare tutti i filtri 
- [x] aggiungere filtro Comune
- [x] aggiungere filtro flag_premialità
- [x] diagrammi a torta per tutte le regioni -> se clicchi un pulsante "top" ti appaiono le migliori regioni (barchart con la divisione in missioni) se clicchi un pulsante "worst" ti appaiono le peggiori

## Note
* valori Null/NaN/Missing --> come comportarsi? 

## Esempi domande:
1. solo alcuni settori hanno premialità? 
2. come si incrociano le premialità sulle provincie? 
3. misure di intervento (M1-M6 come categorie)