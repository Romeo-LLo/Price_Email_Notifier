from bs4 import BeautifulSoup as bs
from selenium import webdriver
import smtplib
import ssl
from dotenv import load_dotenv
import os 
from datetime import datetime
import json
from email.message import EmailMessage
from email.mime.text import MIMEText


load_dotenv()
pwd = os.getenv("pwd")
sender = os.getenv("sender_email")
receiver = os.getenv("receiver_email")


def check_moisture():
    info_file = 'lastest_price.json'
        
    url = "https://www.boots.com/clinique-moisture-surge-100h-auto-replenishing-hydrator-50ml-10292729?cm_mmc=bmm-buk-google-ppc-_-PLAs_HeroCompare-_-Beauty_Premium_Clinique-_-UK_Smart_Shopping_Beauty_Premium_Clinique&gclid=Cj0KCQjw852XBhC6ARIsAJsFPN2fEcoTeY-lAdI7jLEOkEMdJxgEv8iEXUnzTX7tNE-m-RZC4xHogP0aAimhEALw_wcB&gclsrc=aw.ds"

    driver = webdriver.Chrome()
    driver.get(url)
    page = driver.page_source
    soup = bs(page, "html.parser")
    price = soup.find("div", {"class": "price price_redesign"})
    current_price = price.text
    current_time = datetime.now()
    current_time = current_time.strftime("%Y/%m/%d")
    driver.close()
    

    if os.path.exists(info_file):
        
        with open(info_file, 'r') as json_file:
            info_dict = json.load(json_file)
            last_time = info_dict['date']
            last_price = info_dict['price']
            
        if last_price != current_price:
            info_dict = {
                'date': current_time,
                'price': current_price
            }
            with open(info_file, 'w') as json_file:
                json.dump(info_dict, json_file)
            
            send_mail_price(last_time, last_price, current_time, current_price)
            print('Price updated, email sent!')
        else:
            print('Price unchanged')
            
            
    else:
        last_time = 'None'
        last_price = 'None'
        info_dict = {
            'date': current_time,
            'price': current_price
        }
        with open(info_file, 'w') as json_file:
            json.dump(info_dict, json_file)
            
        send_mail_price(last_time, last_price, current_time, current_price)
        print('Price recored, email sent!')

    
    
def send_mail_price(last_time, last_price, current_time, current_price):
        
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = sender
    password = pwd
    receiver_email = receiver
     

    
    body = f"""
    Price on {last_time} was {last_price}. 
    Price on {current_time} is {current_price}. 
    """

    
    # body = body.encode('utf-8')


    msg = MIMEText(body)
    msg['Subject'] = 'Price notification'
    msg['From'] = sender
    msg['To'] = receiver


    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        
if __name__ == '__main__':
    check_moisture()