from selenium import webdriver
from selenium.webdriver import Firefox
from time import sleep
import os, time, smtplib
from settings import notif_push, notif_email, codice_utente, password_utente, refresh_rate, anno_accademico

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
browser = webdriver.Firefox()
url = 'https://beep.metid.polimi.it/'
browser.get(url)
browser.minimize_window()
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
corsi = browser.find_elements_by_xpath("//*[contains(text(), '[2020-21]')]")
for x in corsi:
	corsi_disponibili.append(x.text)

corsi_disponibili = list(dict.fromkeys(corsi_disponibili))

print("I tuoi corsi disponibili sono i seguenti")
sleep(0.5)
print('\n'.join(corsi_disponibili))
sleep(2)

# Chiedere quale corso controllare
testo = input("Quale corso vuoi tenere sotto controllo? ")
corso = testo.upper()


# Click della pagina del corso che si vuole controllare
button = browser.find_element_by_xpath("//*[contains(text(),'"+ corso +"')]")
button.click()

while(controllo!=2):

	lista = []
	elements = browser.find_elements_by_xpath("//a[contains(@href, 'https://beep.metid.polimi.it/c/document_library/get_file?groupId=')]")
	for a in elements:
	    lista.append(a.text)

	
	if controllo==0:
		new_lista = list(lista)

	controllo=1

	if lista != new_lista:
		print("Il nuovo file e': ")
		print(''.join(lista[0]))

		# Invia notifica WebPush
		if notif_push == 'true':
			notify.send('Nuovo file caricato su Beep: ', lista[0])
			link = browser.find_element_by_link_text(lista[0]).get_attribute("href")

		#Invia notifica Email
		if notif_email == 'true':
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

	browser.refresh()
	time.sleep(refresh_rate)
	volte= volte + 1
	print('Ho refreshato ', volte, 'volte')

sleep(5)
browser.close()
