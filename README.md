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

## URGENTE
**COUNT DISTINCT** su tutti i grafici che esibisci.
## filtri da inserire
- [x] FLAG_URGENZA
- [x] MOTIVO_URGENZA
- [x] ESITO
- [x] importo gara (colonna importo_complessivo_gara)
- [x] togliere il filtro sulla percentuale finanziamento

## To do - UI 
- [ ] ALTRA PAGINA grafico con possibilità di scelta variabile master + dimensione figlia --> radar chart con tra le variabili (i) settore (ii) descrizione natura (iii) tipologia--> "altro"
- [ ] COSA SCRIVERE nel front-end? 
- [x] tabella riassuntiva filtri impostati
- [ ] il bar chart deve dare valori % -> quanti CIG su una missione ha una regione in percentuale rispetto al numero di cig assoluto per quella regione?

## To do - Performance
- [x] file parquet anziché .json e .xlsx
- [ ] verificare cosa può essere messo in cache

## Esempi domande:
1. solo alcuni settori hanno premialità? 
2. come si incrociano le premialità sulle provincie? 
3. misure di intervento (M1-M6 come categorie)
4. vorrei vedere la combo flag premialità, regione=EmiliaRomagna e distribuzione delle province/settori