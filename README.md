# Price Email Notifier
Price_Email_Notifier scrapes the price of the product. Once the current price is different from last time, an email containing the price information is sent.

## Description
1. Chromedriver and selenium
* Here is an example of finding the element, inspect the information you are interested in on the web page.
    ```
        driver.get(url)
        page = driver.page_source
        soup = bs(page, "html.parser")
        price = soup.find("div", {"class": "price price_redesign"})
        current_price = price.text
        print('Current price : ', price)
    ```
 

2. Save price information in dictionary
    ```
    info_dict = {
        'date': current_time,
        'price': current_price
    }
    ```
- If runnuing locally, save to a json file.
- If deployed to heroku, so that the program could check for the price periodically. We need to connect to cloud database, here mongoDB Atlas is used. 
    - Deploy cluster on mongoDB Atlas and copy the connection string for later usage. [Detailed instruction](https://www.mongodb.com/developer/products/atlas/use-atlas-on-heroku/)
    - In requirements.txt, add pymongo[tls,srv] instead of pymongo
    - MongoDB operations are covered in dbmanager.py





3. Sending email via gmail
- Firstly, go to google account and activate "App Passwords", the generated code is used as password afterwards. [Detailed instruction](https://support.google.com/accounts/answer/185833?hl=en)

- Secondly, save your password that generated from the previuos step in .env file. In my case,  I save sender and receiver's email as well.
    ```
    from dotenv import load_dotenv
    load_dotenv()
    pwd = os.getenv("pwd")
    ```

    - Finally, send email with SMTP and TLS. Although there are a lot ways to send an email, this is the only one that works for me.
    ```
    port = 587  
    smtp_server = "smtp.gmail.com"
    body = " Body of email"
    msg = MIMEText(body)
    msg['Subject'] = 'Price notification'
    msg['From'] = sender
    msg['To'] = receiver
    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    ```

4. Deployment
- If you want to run locally, notifier_local.py is enough.
- Alternatively, let's deploy it to heroku.
    1. Prepare runtime.txt and requirements.txt
    2. Deploy to heroku. [Detailed instruction](https://devcenter.heroku.com/articles/github-integration)
    3. Install chromedriver and chrome for heroku, open "Settings" on heroku page. Sroll down to "Buildpacks" section. Add the following 2 links.
    * https://github.com/heroku/heroku-buildpack-google-chrome
    * https://github.com/heroku/heroku-buildpack-chromedriver
    ![Buildpacks](/Instrusction%20image/Buildpacks.png)
    4. Sroll up to "Config Vars" section. Add the following 4 variables. pwd is your generated code. MONGODB_URI is the connection string.
    ![Config Vars](/Instrusction%20image/Config%20vars.png)
    5. Open "Resources" on heroku page and search for "Advanced Scheduler" adds up. Set up the time period. Press activate trigger.
        ![Scheduler](/Instrusction%20image/Scheduler.png)
    6. Done!