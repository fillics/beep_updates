from time import sleep
import os, time, smtplib, os.path, pickle
from settings import pi_mode, notif_push, notif_email, codice_utente, password_utente, refresh_rate, anno_accademico, savefile_path, headless_mode, corso_scelto

if pi_mode == 'true':
	from selenium import webdriver
	from selenium.webdriver import Firefox
else:
	from selenium.webdriver import Chrome



if notif_push == 'true':
	from notify_run import Notify
	notify = Notify()

if notif_email == 'true':
	from settings import email_user, email_pass, email_send
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from email.mime.base import MIMEBase
	from email import encoders


controllo = 0
volte = 0

# Apertura Browser
browser = webdriver.Firefox() if pi_mode == 'true' else Chrome()
url = 'https://beep.metid.polimi.it/'
browser.get(url) # connessione a beep
if pi_mode == 'true': browser.minimize_window() # iconizzare il browser
sleep(2)

# Click del pulsante Login
button = browser.find_element_by_xpath("//a[contains(text(), 'Login')]")
button.click()
sleep(2)

# Riempimento con le credenziali
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

print("I tuoi corsi disponibili sono i seguenti")
sleep(0.5)
print('\n'.join(corsi_disponibili))
sleep(2)

if headless_mode == 'true':
	corso = corso_scelto.upper()
else:
	testo = input("Quale corso vuoi tenere sotto controllo? ") # Chiedere quale corso controllare
	corso = testo.upper()


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
	print("Non è stata trovata una pre-esistente lista di documenti su beep")

print("\nSalvo lista documenti...")
with open(savefile_path, 'wb') as file:
	pickle.dump(lista, file) # salva i dati su file
print("fatto!\n")

sleep(3)
browser.close()
