print("-o-o-o-o- Beep Updates -o-o-o-o-o-")

import logging as l

l.info("\nImporting...")
from time import sleep
import os, time, smtplib, os.path, pickle
from settings import pi_mode, notif_push, notif_email, headless, anno_accademico, percorso, quanti_corsi, corso_scelto_1, corso_scelto_2, corso_scelto_3, corso_scelto_4, corso_scelto_5, corso_scelto_6, corso_scelto_7

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

# Browser Setup specifico per applicazioni headless
if headless == 'true' and pi_mode != 'true':
	print("Headless mode detected!")

	# Recupero variabili d'ambiente
	l.info("getting environment variables...")
	chrome_bin = os.environ.get('CHROME_BIN')
	chromedriver_bin = os.environ.get('CHROMEDRIVER_PATH')
	codice_utente = int(os.environ.get("BEEP_CODICE_UTENTE"))
	password_utente = os.environ.get("BEEP_PASSWORD")
	print("Got variables:\n  - CHROME_BIN = " + chrome_bin + "\n  - CHROMEDRIVER_PATH = " + chromedriver_bin + "\n  - BEEP_CODICE_UTENTE = " + str(codice_utente) + "\n  - BEEP_PASSWORD: _mica te la scrivo, scemo!_" + "\n\n")

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


# Apertura Browser
print("Let's go!\n")
l.info("\nOpening browser...")
if headless == 'true' and pi_mode != 'true':
	browser = webdriver.Chrome(executable_path=chromedriver_bin, options=chrome_options)
else:
	browser = webdriver.Firefox() if pi_mode == 'true' else Chrome()

url = 'https://beep.metid.polimi.it/'
l.info("\nNavigating...")
browser.get(url) # connessione a beep
if pi_mode == 'true': browser.minimize_window() # iconizzare il browser
sleep(2)

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

# Chiedere quale corso seguire
corsi_disponibili = []
#corsi = browser.find_elements_by_xpath("//*[contains(text(), anno_accademico)]")
corsi = browser.find_elements_by_xpath("//*[contains(text(), '[2020-21]')]")
for x in corsi:
	corsi_disponibili.append(x.text)

corsi_disponibili = list(dict.fromkeys(corsi_disponibili))

print("\nI tuoi corsi disponibili sono i seguenti:")
sleep(0.5)
print('\n'.join(corsi_disponibili))
sleep(2)

corsi_desiderati = []
print("\nHai specificato di voler seguire " + str(quanti_corsi) + " corsi.\nLi cercherò come specificato nelle impostazioni.\n")

# costruisco la lista dei nomi dei corsi
if headless == 'true': # se siamo headless, cercali nelle variabili d'ambiente
	for i in range(1, quanti_corsi+1):
		corsi_desiderati.append(os.environ.get('CORSO_SCELTO_'+str(i)))
else: # altrimenti, prendili dal file di Configurazione
	corsi_desiderati = [corso_scelto_1, corso_scelto_2, corso_scelto_3, corso_scelto_4, corso_scelto_5, corso_scelto_6, corso_scelto_7]


for i in range(0, quanti_corsi):
	corso = corsi_desiderati[i].upper() # seleziono il corso
	savefile_path = percorso + '_' + str(i) + '.txt' # costruisco il percorso al file di salvataggio
	l.info("File path is: " + savefile_path)

	# Click della pagina del corso che si vuole controllare
	print("Mi dirigo verso:" + corso)
	button = browser.find_element_by_xpath("//*[contains(text(),'"+ corso +"')]")
	button.click()

	# Verifica Novità
	lista = []
	documenti = browser.find_elements_by_xpath("//a[contains(@href, 'https://beep.metid.polimi.it/c/document_library/get_file?groupId=')]") # ottieni documenti
	for a in documenti:
		lista.append(a.text) # inserisci i documenti nella lista

	if os.path.isfile(savefile_path): # se esiste già un file coi dati
		with open(savefile_path, 'rb') as file:
			vecchi_dati = pickle.load(file) # recupera i dati

		if lista != vecchi_dati : # ci sono stati cambiamenti su beep
			print("Dati difformi!\n")
			print("Il nuovo file e': ")
			print(''.join(lista[0]))

			# Invia notifica WebPush
			if notif_push == 'true':
				print("Invio notifica push...")
				notify.send('Nuovo file caricato su Beep: ', lista[0])
				link = browser.find_element_by_link_text(lista[0]).get_attribute("href")

			#Invia notifica Email
			if notif_email == 'true':
				print("Invio email...")
				msg = MIMEText("Ciao, e' appena stato caricato su Beep un file. Il link per scaricarlo e' il seguente: ", link)
				msg['From'] = email_user
				msg['To'] = email_send
				msg['subject'] = subject
				subject = 'Nuovo file caricato su '+corso
				server = smtplib.SMTP('smtp.gmail.com:587')
				server.starttls()
				server.ehlo()
				server.login(email_user, email_pass)
				server.sendmail(email_user, email_send, msg.as_string())
				server.quit()

		else: # non ci sono stati cambiamenti su beep
			print("Dati corrispondenti --> niente di nuovo su beep.")

	else: # è la prima volta che runniamo il programma
		print("Non è stata trovata una pre-esistente lista di documenti su beep: provvedo a generarne una.")

	print("Salvo lista documenti...")
	with open(savefile_path, 'wb') as file:
		pickle.dump(lista, file) # salva i dati su file
	print("Fatto! Al prossimo corso!\n")
	sleep(2)

	browser.back()

print("\n\nFinito! Buono Studio!\n\n\nSaluti al Magnifico Ferruccio!")


sleep(3)
browser.close()
