# Beep Updates [![](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/)
Rimani aggiornato sugli ultimi file caricati su Beep dei corsi che vuoi seguire.

Quante volte vi è capitato di continuare ad *aggiornare* la pagina di Beep per controllare la pubblicazione di un file? E quante volte siete rimasti *delusi* dalla non pubblicazione del file degli esiti che state aspettando da giorni?

Per rendere il tutto più automatico e senza perdite di tempo, abbiamo creato un bot che aggiorna in automatico la pagina dei corsi che vuoi controllare e ti avvisa se è stato caricato qualcosa.

## Che cos'è
È un semplice bot che si logga nel sito di Beep e ti chiede a quali corsi sei interessato a ricevere aggiornamenti sul caricamento di file. Se è stato caricato qualcosa nella pagina del corso che hai deciso di seguire, il bot ti avvisa:
- con un'email all'indirizzo che vuoi, sfruttando il protocollo [SMTP](https://docs.python.org/3/library/smtplib.html#module-smtplib)
- con una notifica WebPush direttamente sul cellulare, usando [notify.run](https://notify.run/)


## Come funziona
Per programmare questo bot, abbiamo usato **Python** e **Selenium**, un tool per l'automazione di pagine Web capace di simulare le attività di un utente.

Lo script ammette due modalità di funzionamento:
- **headless**: le impostazioni vengono recuperate principalmente da variabili d'ambiente della shell da cui viene lanciato lo script, i dati relativi ai file di BeeP vengono letti/scritti su files remoti, e non viene visualizzato graficamente il browser: avviene tutto in riga di comando
- **standard**: le impostazioni vengono recuperate interamente dal file di configurazione `settings.py`, i dati relativi ai file di BeeP vengono salvati su files locali, ed è possibile vedere il browser animarsi di vita propria


### Modalità Standard
1. Impostare le proprie preferenze e dati di login nel file `settings.py`
2. Avviare lo script con: `python3 beep_updates.py`
3. _(opzionale)_ Automatizzare l'avvio periodico del programma, ad esempio con un cronjob appropriato

### Modalità Headless
1. Impostare le preferenze della prima sezione in `settings.py`
2. Impostare le variabili d'ambiente necessarie: `export NOME_VARIABILE=valore`

Variabile | Significato
--------- | -----------
BEEP_CODICE_UTENTE | Codice Persona per l'accesso a BeeP
BEEP_PASSWORD | Password di Beep
CHROME_BIN | Percorso all'eseguibile di Google Chrome, che viene usato come browser
CHROMEDRIVER_PATH | Percorso all'eseguibile di `chromedriver`
HTTP_GET_ENDPOINT | URL della cartella remota che ospita (/ospiterà) i file di salvataggio
HTTP_POST_ENDPOINT | URL allo script remoto che accetta [richieste POST](#caricamento-di-file-remoti) per salvare i file prodotti dallo script
CORSO_SCELTO_1 | Nome del primo corso che si intende seguire
CORSO_SCELTO_2 | Nome del secondo corso che si intende seguire
... | ...
CORSO_SCELTO_n | Nome dell'n-esimo corso che si intende seguire

3. Avviare lo script con: `python3 beep_updates.py`
4. _(opzionale)_ Automatizzare l'avvio periodico del programma, ad esempio con un cronjob appropriato


## Caricamento di File Remoti
In modalità headless, lo script proverà a caricare i file di salvataggio inviando richieste http `POST` al link specificato nella variabile d'ambiente `HTTP_POST_ENDPOINT`.

In particolare, il programma invia dati di tipo `multipart/form-data`: è necessario che l'endpoint accetti questo tipo di richieste, e si aspetti un file al parametro `fileToUpload`.

Un [esempio di un simile script](esempi/upload.php) è disponibile nella cartella `esempi`.


## Deployment su Heroku [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
Per caricare lo script su [Heroku](https://heroku.com), è necessario attivare i buildpack:
- heroku/python
- https://github.com/heroku/heroku-buildpack-google-chrome
- https://github.com/heroku/heroku-buildpack-chromedriver

e seguire poi le istruzioni per la [modalità headless](#modalità-headless).

Per generare automaticamente un progetto basato sul template standard, è possibile sfruttare il bottone qui sopra.
