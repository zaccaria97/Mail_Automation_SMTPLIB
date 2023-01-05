from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart 
import smtplib 
import datetime

import imaplib

import os 
import csv
import time
 
''' 
GESTIONE INVIO MAIL 
''' 
 

def invioMail(oggetto,testo,to, mittente, password, ccnascosto, ccnascosto2):

    #smtp = smtplib.SMTP('smtp.office365.com', 587)
    smtp = smtplib.SMTP('out.monema.it', 587)   
    smtp.ehlo() 
    smtp.starttls() 
    smtp.login(mittente.strip(), password.strip()) 
     
     
    msg = MIMEMultipart('alternative')
    msg['From'] = mittente
    msg['To'] = to
    msg['Subject'] = oggetto
    msg['Body'] = testo
    msg['Bcc'] = ccnascosto
    msg['Disposition-Notification-To'] = mittente

    msg.attach(MIMEText(msg['Body']))
    if ccnascosto2 != '':
        to=[to]+[ccnascosto] + [ccnascosto2]
    else:
        to=[to]+[ccnascosto]
    
    smtp.sendmail(msg['From'], to, msg.as_string())
    smtp.quit()
        
    '''
    f = open("log.txt", "a")
    f.write(msg.as_string())
    f.write("\n\n----------------------------\n\n")
    f.close()
    '''
    with open("log.txt","a") as file:
        now = datetime.datetime.now()
        file.write("timestamp: "+str(now)+'\n')
        file.write("destinatario: "+msg['To']+'\n')
        file.write("oggetto: "+msg['Subject']+'\n')
        file.write("corpo: "+msg['Body']+'\n')
        file.write("-------------------------------------------------\n")
    
    time.sleep(1)

##lettura credenziali
with open('CredenzialiMittente.txt',"r") as f:
    credenziali = f.readlines()
if credenziali[0]=='' or credenziali[1]=='' or credenziali[2]=='':
    print('inserire i dati nel file delle credenziali!')
    exit
    
with open('mail_counter.txt',"r") as f:
    ultimoIndice = f.read()  
'''
with open("semaforo.txt","w") as file:
    file.write("false")
'''
list_of_column_names=[]
with open('Target.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
# loop to iterate through the rows of csv
    index=0
    for row in csv_reader: 
        # adding the first row
        if index==0: 
            list_of_column_names.append(row)
            index=index+1
        else:
            if row[0]!='' and row[1]!='' and row[2]!='':
                if index>int(ultimoIndice)+1:
                    invioMail(row[0],row[1],row[2],credenziali[0],credenziali[1],credenziali[2], credenziali[3])
                    with open("mail_counter.txt","w") as file:
                        file.write(str(index))
                    time.sleep(30)
            index=index+1     
        #if index%10==10:
        #time.sleep(30)   #10 minuti 

    f.close()
'''
with open("semaforo.txt","w") as file:
    file.write("true")
'''
with open("mail_counter.txt","w") as file:
    file.write("-1")


  