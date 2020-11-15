def send_email_notif(link, corso):
	print("Invio email...")
	subject = 'Nuovo file caricato su '+corso
	msg = MIMEText("Ciao, e' appena stato caricato su Beep un file. Il link per scaricarlo e' il seguente: ", link)
	msg['From'] = email_user
	msg['To'] = email_send
	msg['subject'] = subject
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.ehlo()
	server.login(email_user, email_pass)
	server.sendmail(email_user, email_send, msg.as_string())
	server.quit()

def send_webpush_notif(link, listaDocumenti):
	print("Invio notifica push...")
	notify.send('Nuovo file caricato su Beep: '+str(listaDocumenti[0]), link)

def send_notifs(link, corso, listaDocumenti):
	if notif_push == 'true': send_webpush_notif(link, listaDocumenti)
	if notif_email == 'true': send_email_notif(link, corso)

def init_browser(): # -> browser
	print("Let's go!\n")
	l.info("\nOpening browser...")
	if headless == 'true' and pi_mode != 'true':
		browser = webdriver.Chrome(executable_path=chromedriver_bin, options=chrome_options)
	else:
		browser = webdriver.Firefox() if pi_mode == 'true' else Chrome()

	return browser

def connect_to_beep(browser):
	url = 'https://beep.metid.polimi.it/'
	l.info("\nNavigating...")
	browser.get(url) # connessione a beep
	if pi_mode == 'true': browser.minimize_window() # iconizzare il browser
	sleep(2)

def do_beep_login(browser):
	# Click del pulsante Login
	button = browser.find_element_by_xpath("//a[contains(text(), 'Login')]")
	button.click()
	sleep(2)

	# Riempimento con le credenziali
	print("\nEseguo il login...")
	login_field = browser.find_element_by_xpath("//input[@name=\"login\"]").send_keys(codice_utente)
	pw_field = browser.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password_utente)
	sleep(2)

	# Click del pulsante di Login
	button = browser.find_element_by_xpath("//button[@name=\"evn_conferma\"]")
	button.click()
	sleep(3)

def cerca_corsi(browser): # -> corsi_disponibili
	print("\nI tuoi corsi disponibili sono i seguenti:")
	corsi_disponibili = []
	#corsi = browser.find_elements_by_xpath("//*[contains(text(), anno_accademico)]")
	corsi = browser.find_elements_by_xpath("//*[contains(text(), '[2020-21]')]")
	for x in corsi:
		corsi_disponibili.append(x.text)

	corsi_disponibili = list(dict.fromkeys(corsi_disponibili))
	print('\n'.join(corsi_disponibili))
	return corsi_disponibili

def get_corsi_desiderati(quanti_corsi): # -> corsi_desiderati
	print("\nHai specificato di voler seguire " + str(quanti_corsi) + " corsi.\nLi cercherò come specificato nelle impostazioni.\n")
	corsi_desiderati = []
	# costruisco la lista dei nomi dei corsi
	if headless == 'true': # se siamo headless, cercali nelle variabili d'ambiente
		for i in range(1, quanti_corsi+1):
			corsi_desiderati.append(os.environ.get('CORSO_SCELTO_'+str(i)))
	else: # altrimenti, prendili dal file di Configurazione
		corsi_desiderati = [corso_scelto_1, corso_scelto_2, corso_scelto_3, corso_scelto_4, corso_scelto_5, corso_scelto_6, corso_scelto_7]

	return corsi_desiderati










print("-o-o-o-o- Beep Updates -o-o-o-o-o-")


import logging as l
l.info("\nImporting...")
from time import sleep
import os, time, smtplib, os.path, pickle
from settings import pi_mode, notif_push, notif_email, headless, anno_accademico, percorso, base_filename, quanti_corsi, corso_scelto_1, corso_scelto_2, corso_scelto_3, corso_scelto_4, corso_scelto_5, corso_scelto_6, corso_scelto_7
if headless == 'true': import requests


# Import dei browser
if pi_mode == 'true':
	l.info("pi mode is ON")
	from selenium import webdriver
	from selenium.webdriver import Firefox
else:
	l.info("pi mode is OFF")
	from selenium.webdriver import Chrome

# Import Utilità di Notifiche
if notif_push == 'true':
	l.info("push notifs ON")
	from notify_run import Notify
	from settings import notify_channel
	notify_endpoint = "https://notify.run/" + notify_channel
	print("Notifiche WebPush attivate presso: " + notify_endpoint)
	notify = Notify(endpoint=notify_endpoint)

if notif_email == 'true':
	l.info("email notifs ON")
	from settings import email_user, email_pass, email_send
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from email.mime.base import MIMEBase
	from email import encoders
l.info("Done importing!\n")

## _-_-_-_  ENV VARS _-_-_-_
if headless == 'true' and pi_mode != 'true':
	print("Headless mode detected!")

	# Recupero variabili d'ambiente
	l.info("getting environment variables...")
	chrome_bin = os.environ.get('CHROME_BIN')
	chromedriver_bin = os.environ.get('CHROMEDRIVER_PATH')
	codice_utente = int(os.environ.get("BEEP_CODICE_UTENTE"))
	password_utente = os.environ.get("BEEP_PASSWORD")
	http_get_endpoint = os.environ.get("HTTP_GET_ENDPOINT")
	http_post_endpoint = os.environ.get("HTTP_POST_ENDPOINT")
	print("Got variables:\n  - CHROME_BIN = " + chrome_bin + "\n  - CHROMEDRIVER_PATH = " + chromedriver_bin + "\n  - BEEP_CODICE_UTENTE = " + str(codice_utente) + "\n  - BEEP_PASSWORD: _mica te la scrivo, scemo!_" + "\n  - HTTP_GET_ENDPOINT: " + http_get_endpoint + "\n  - HTTP_POST_ENDPOINT: " + http_post_endpoint + "\n\n")

	# Configurazione del webdriver
	l.info("Configuring Chrome...")
	from selenium import webdriver
	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = chrome_bin
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")

else:
	from settings import codice_utente, password_utente



# Inizializzazione browser
browser = init_browser()

# Connessione a BeeP e login
connect_to_beep(browser)
do_beep_login(browser)

# Ottieni liste dei corsi
corsi_disponibili = cerca_corsi(browser)
corsi_desiderati = get_corsi_desiderati(quanti_corsi)

# Verifiche updates
for i in range(0, quanti_corsi):
	corso = corsi_desiderati[i].upper() # seleziono il corso

	# costruisco il percorso al file di salvataggio
	filename = base_filename + '_' + str(i+1) + '.txt'
	savefile_path_local = percorso + filename
	savefile_path_remote = http_get_endpoint + filename

	l.info("Local file path is: " + savefile_path_local + ".\nRemote file path is: " + savefile_path_remote)

	# Click della pagina del corso che si vuole controllare
	print("Mi dirigo verso:" + corso)
	button = browser.find_element_by_xpath("//*[contains(text(),'"+ corso +"')]")
	button.click()

	# Verifica Novità
	lista = []
	documenti = browser.find_elements_by_xpath("//a[contains(@href, 'https://beep.metid.polimi.it/c/document_library/get_file?groupId=')]") # ottieni documenti
	for a in documenti:
		lista.append(a.text) # inserisci i documenti nella lista

	# Recupero vecchia lista documenti
	gotfile = False
	if headless != 'true':
		if os.path.isfile(savefile_path_local):
			l.info("Loading from local")
			with open(savefile_path_local, 'rb') as file: #apri il file
				vecchi_dati = pickle.load(file) # recupera i dati
				gotfile = True
		else: # è la prima volta che runniamo il programma
			print("Non è stata trovata una pre-esistente lista di documenti su beep: provvedo a generarne una.")
			gotfile = False
	else: # siamo headless
		l.info("Loading from remote")
		r = requests.get(savefile_path_remote) # prova a recuperare il file remoto
		if r.status_code == 200: # se abbiamo ottenuto un file
			with open('fil.pkl', 'wb') as f: # scriviamo i dati su un file locale temporaneo
				f.write(r.content)
				f.truncate()
			with open('fil.pkl', 'rb') as f: # riapro quel file e ne carico i dati
				vecchi_dati = pickle.load(f)
			gotfile = True
		else:
			gotfile = False

	# Confrontiamo liste documenti, se l'abbiamo trovata
	if gotfile:
		if lista != vecchi_dati : # ci sono stati cambiamenti su beep
			print("Dati difformi!\n")
			print("Il nuovo file e': ")
			print(''.join(lista[0]))

			link = browser.find_element_by_link_text(lista[0]).get_attribute("href")

			# Invia Notifiche
			send_notifs(link, corso, lista)

		else: # non ci sono stati cambiamenti su beep
			print("Dati corrispondenti --> niente di nuovo su beep.")


	print("Salvo lista documenti...")
	with open(savefile_path_local, 'wb') as file:
		pickle.dump(lista, file) # salva i dati su file
		l.info("Lista documenti salvata in Locale.")
	if headless == 'true':
		print("Carico online la lista aggiornata...")
		dati = { 'fileToUpload': (filename, open(savefile_path_local, 'rb'))}
		pReq = requests.post(http_post_endpoint, files=dati)
		pReq.raise_for_status() # quitta in errore se abbiamo ricevuto una risposta HTTP diversa dal 200
	print("Fatto! Al prossimo corso!\n")

	browser.back()
	sleep(2)


print("\n\nFinito! Buono Studio!\n\n\nSaluti al Magnifico Ferruccio!")
sleep(2)
browser.close()
