
import requests
from bs4 import BeautifulSoup
import smtplib
import time
import schedule
from tkinter import *

headers = {"user-agent": "--x--x--x"}
     
def checagem_preco():

    verificador = True

    URL = UrlEnt.get()
    preco_requerido = int(PriceEnt.get())
    intervalo = int(TimeEnt.get())


    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content,"html.parser")

    preco = soup.find(class_='src__BestPrice-sc-1jvw02c-5 cBWOIB priceSales').get_text()
    titulo = soup.find(class_='src__Text-sc-154pg0p-0 product-title__Title-sc-1hlrxcw-0 hoBeMD').get_text()

    indice_virgula = preco.find(',')
    preco = (preco[3:indice_virgula])

    if preco.find('.') != -1:
        preco = preco.replace('.','')

    preco = int(preco)

    if (preco < preco_requerido):
        try:
            print('enviando email')
            send_mail()
            verificador = False
        except Exception as e:
            print(e)
            
    
    while verificador:
        time.sleep(intervalo*60*60)

    
def send_mail():
    preco_requerido = int(PriceEnt.get())
    URL = UrlEnt.get()
    destinatario = MailEnt.get()
    server = smtplib.SMTP('protocolo-smtp',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('seu-email','sua-senha')
    subject = 'Encontramos o que você deseja!'
    body = ('O produto que você deseja está com o preco menor ou igual a R$%d, de uma olhada:\n\n%s '%(preco_requerido,URL))
    msg = ('Subject: %s \n\n\n%s'%(subject,body))
    server.sendmail('remetente@email',destinatario,msg.encode("utf-8"))
    server.quit()


#configurações iniciais da GUI
gui = Tk()
gui.title('Rastreador de preços Americanas')
gui.resizable(False, False)
gui.geometry('350x200')

#URL
UrlLabel = Label(text='Link: ',font=('Arial',12))
UrlLabel.grid(row=0, column=0)


UrlEnt = Entry(font=('Arial',12))
UrlEnt.grid(row=0, column=1,sticky='W')

#preço
PriceLabel = Label(text='Preço ideal: ',font=('Arial',12))
PriceLabel.grid(row=1, column=0,pady=10)

PriceEnt = Entry(font=('Arial',12))
PriceEnt.grid(row=1, column=1)

#Intervalo de tempo 
TimeLabel = Label( text='Intervalo(em horas): ',font=('Arial',12))
TimeLabel.grid(row=2,column=0, pady=10)

TimeEnt = Entry(font=('Arial',12))
TimeEnt.grid(row=2,column=1)

#Email
MailLabel = Label(text='Informe seu e-mail: ',font=('Arial',12))
MailLabel.grid(row=3,column=0,pady=10)

MailEnt= Entry(font=('Arial',12))
MailEnt.grid(row=3,column=1)

#Botão 
btn = Button(text='Enviar',command=checagem_preco)
btn.grid(row=4,column=1,columnspan=3)


gui.mainloop()