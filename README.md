# Period Think Tank
![alt text](assets/period_logo.png)

## PNRR Data Monitoring App
App per la visualizzazione e l'analisi dei dati aperti riguardanti il PNRR provenienti da OpenPNRR, ANAC e OpenCUP, 
e rielaborati da [Period Think Tank](https://www.thinktankperiod.org/), associazione femminista che promuove l'equità di genere attraverso un approccio femminista ai dati.  

La App è accessibile da questo [link](https://periodthinktank-analisi-dati-pnrr-app-6tk6o2.streamlit.app/).  

Lo scopo dell'app è di indagare la presenza e la distribuzioni sul territorio e sulle missioni, 
delle quote occupazionali minime o misure premiali per donne e giovani nei bandi di gara emessi.  

### Fonti dati:
* [OpenPNRR](https://openpnrr.it/)
* [OpenCUP](https://www.opencup.gov.it/portale/web/opencup/opendata)
* [ANAC](https://pnrr.datibenecomune.it/fonti/anac/)     

Le informazioni geografiche sono state ottenute dal merge tra CIG e CUP. La realazione tra questi due codici è "molti a molti", ovvero un CIG può essere associato a più CUP e viceversa.
Poichè non sono disponibili le informazioni sulla distribuzione dell’importo economico e su differenti comuni per i CUP associati, si sono considerati i CIG in conteggio distinto.  

I valori mostrati sono valori percentuali, si confronta il totale dei cig con l'attributo mostrato (misure premiali, quote>30%) ecc, 
sul totale dei CIG per quel raggruppamento.

### Note sui Filtri:
* I filtri impattano su tutti i grafici.
* I grafici sulla presenza di misure premiali e sulle quote femminili/giovanili mostreranno sempre i dati filtrati per queste caratteristiche.
* In fondo alla pagina è possibile visualizzare il riepilogo dei filtri selezionati
* Possibilità di esportare il dataset in formato csv tramite la app.

#### Note degli autori
L'applicativo mostrato è realizzato in [Streamlit](https://streamlit.io/), quindi il nostro tool di sviluppo è principalmente Python.    
Per utilizzare la App anche in locale, clonare la repository, installare il virtual environment con le librerie in ```requirements.txt```.
In seguito, da terminale e con l'ambiente virtuale attivo, eseguire il comando  
```streamlit run App.py```.  
Pull request da altri branch sul principale verranno valutate e integrate. L'apertura di issue per proposte di miglioramento sono ben accette.
