from bs4 import BeautifulSoup as bs
from selenium import webdriver
import smtplib
import ssl
from dotenv import load_dotenv
import os 
from datetime import datetime
import json
from email.mime.text import MIMEText
from selenium.webdriver.chrome.options import Options
from dbmanager import DatabaseManager

load_dotenv()
pwd = os.getenv("pwd")
sender = os.getenv("sender_email")
receiver = os.getenv("receiver_email")
mongodb_uri = os.getenv('MONGODB_URI')



def price_check():
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    url = "https://www.boots.com/clinique-moisture-surge-100h-auto-replenishing-hydrator-50ml-10292729?cm_mmc=bmm-buk-google-ppc-_-PLAs_HeroCompare-_-Beauty_Premium_Clinique-_-UK_Smart_Shopping_Beauty_Premium_Clinique&gclid=Cj0KCQjw852XBhC6ARIsAJsFPN2fEcoTeY-lAdI7jLEOkEMdJxgEv8iEXUnzTX7tNE-m-RZC4xHogP0aAimhEALw_wcB&gclsrc=aw.ds"
    driver.get(url)
    page = driver.page_source
    soup = bs(page, "html.parser")
    price = soup.find("div", {"class": "price price_redesign"})
    current_price = price.text
    print('Current price : ', current_price)
    current_time = datetime.now()
    current_time = current_time.strftime("%Y/%m/%d")
    driver.close()
    
    dbmanager = DatabaseManager(mongodb_uri)
        
    info_count = dbmanager.count_price_info_mongoDB()

    if info_count == 0:
        last_time = 'None'
        last_price = 'None'
        info_dict = {
            'date': current_time,
            'price': current_price
        }
        dbmanager.insert_price_info_mongoDB(info_dict)
        send_mail_price(last_time, last_price, current_time, current_price)
        print('Price recored in DB, email sent!')
        
    else:
        info_dict = dbmanager.extract_price_info_mongoDB()
        last_time = info_dict['date']
        last_price = info_dict['price']
    
        if last_price != current_price:
            info_dict = {
                'date': current_time,
                'price': current_price
            }
            dbmanager.insert_price_info_mongoDB(info_dict)
            send_mail_price(last_time, last_price, current_time, current_price)
            print('Price updated in DB, email sent!')
        else:
            print('Price unchanged')
            
            


    
    
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
    price_check()