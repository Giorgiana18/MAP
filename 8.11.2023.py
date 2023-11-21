import string
import requests
from bs4 import BeautifulSoup
#from apscheduler.schedulers.blocking import BlockingScheduler
from hashlib import new
import smtplib
sender='giorgianamariamarangoci@gmail.com'    
subject='Pretul a scazut la:'
to_addr_list = ['giorgianamarangoci@gmail.com'] 
cc_addr_list = ['']
def sendemail(sender,message, subject,to_addr_list, cc_addr_list=[]):
    try:
        smtpserver='smtp.gmail.com:587'
        header  = 'From: %s\n' % sender
        header += 'To: %s\n' % ','.join(to_addr_list)
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        message = header + message
        server = smtplib.SMTP(smtpserver)
        server.starttls()
#Parola este de pe myaccount.google.com/apppasswords
        server.login(sender,"dyvx jxls hbmm fohm")
        problems = server.sendmail(sender, to_addr_list, message)
        server.quit()
        return True
    except:
        print("Error: unable to send email")
        return False
 
sendemail(sender, "Pretul a scazut la: ", subject, to_addr_list, cc_addr_list)
 
def data_scraping ():
    req=requests.get("https://www.emag.ro/placa-video-gigabyte-geforce-rtx-4070-windforce-oc-12gb-gddr6x-192-bit-gv-n4070wf3oc-12gd/pd/DZ5M78MBM/")
    soup=BeautifulSoup(req.text,"html.parser")
    price=soup.find('p', attrs={'class': 'product-new-price'}).text
    new_price=price[0:5]
    new_price=new_price.replace(".","")
    new_price=int(new_price)
    pret_referinta = 8000
    if ( new_price<pret_referinta ):
        sendemail(sender,"Pretul a scazut la: "+str(new_price),subject,to_addr_list, cc_addr_list=[])
        print ("Pretul a scazut ")
    else:
       print ("Pretul nu a scazut")
#sendemail(sender, "Pretul a scazut la: ", subject, to_addr_list, cc_addr_list)
# # scheduler = BlockingScheduler()
# # scheduler.add_job(data_scraping, 'interval', seconds=10)
# # scheduler.start()
data_scraping()#