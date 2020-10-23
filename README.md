# Beep Updates
Rimani aggiornato sugli ultimi file caricati su Beep dei corsi che vuoi seguire.

## Motivo
Quante volte vi è capitato di continuare ad *aggiornare* la pagina di Beep per controllare la pubblicazione di un file? E quante volte siete rimasti *delusi* dalla non pubblicazione del file degli esiti che state aspettando da giorni?
Per rendere il tutto più automatico e senza perdite di tempo, ho creato un bot che aggiorna in automatico la pagina del corso che vuoi controllare e ti avvisa se è stato caricato qualcosa. 

## Che cos'è
È un semplice bot che si logga nel sito di Beep e ti chiede a quale dei corsi, alla quale siamo iscritti, sei interessato a ricevere aggiornamenti sul caricamento di file. Se è stato caricato qualcosa nella pagina del corso che hai deciso di seguire, il bot ti avvisa:
- con un'email all'indirizzo che vuoi, sfruttando il protocollo [SMTP](https://docs.python.org/3/library/smtplib.html#module-smtplib)
- con una notifica direttamente sul cellulare, usando [notify.run](https://notify.run/)


## Come funziona
Per programmare questo bot, ho usato **Python** e **Selenium**, un tool per l'automazione di pagine Web capace di simulare le attività di un utente. 
Per prima cosa, si devono inserire le proprie credenziali di accesso nel file [secrets.py](secrets.py), sia quelle di Beep sia quelle dell'email. (*le credenziali inserite sono e rimarranno private, non vengono in alcun modo condivise con altre persone*)

Successivamente, lanciando il file [beep_updates.py](beep_updates.py) *(consiglio di usare **Linux** o un **Raspberry**, che può rimanere sempre accesso senza troppi problemi, usando il file [raspberry.py](raspberry.py))*, il bot si collegherà direttamente alla pagina Beep inserendo in automatico le credenziali, per poi chiedere quale corso controllare, inserendo il nome del prof o il nome della materia.

```
testo = raw_input("Quale corso vuoi tenere sotto controllo? ")
```

Si può impostare ogni quanto fargli aggiornare la pagina, andando a inserire, al posto della x, l'intervallo di aggiornamento espresso in secondi. 
```
browser.refresh()
time.sleep(x)
```

Ogni x secondi, la pagina viene aggiornata e controlla se sono stati caricati nuovi file. Se è presente un nuovo file, il bot manda un'**email** con il nome del file aggiunto e il link per scaricarlo, oppure una **notifica** con il comando: ```notify.send('Nuovo file caricato su Beep')```. (*per ricevere la notifica, si dovranno eseguire due istruzioni molto facili e veloci, trovabili sul sito [notify.run](https://notify.run/)*)

## Note
Funziona con Python 3
