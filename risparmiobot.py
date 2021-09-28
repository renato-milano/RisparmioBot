TOKEN ='2013213860:AAGj-G5Ku9gTB6izss1fAW8zVyicga2Fm9s'
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import string
import random
from selenium import webdriver
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup, element
from telegram import ParseMode

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="UELA'")

def search(update,context,result,driver):

        context.bot.send_message(chat_id=update.effective_chat.id, text='PRODOTTO RICONOSCIUTO.\n\nCERCO ...')
        driver.get("https://www.google.com/search?tbm=shop&q="+result)
        element= driver.find_elements_by_class_name("VfPpkd-Jh9lGc")[3]
        driver.execute_script("arguments[0].scrollIntoView();", element)
        action = ActionChains(driver)
        action.move_to_element(element)
        time.sleep(3)
        action.click()
        action.perform()
        time.sleep(3)
        if len(driver.find_elements_by_class_name('iXEZD'))>0:
            #CONFRONTA PREZZI
            driver.find_element_by_class_name('iXEZD').click()
            time.sleep(1)
            driver.find_element_by_class_name('sh-osd__total-price').click()
            time.sleep(1)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=driver.get_screenshot_as_png())
            elements= driver.find_elements_by_class_name("sh-osd__offer-row")
            title=driver.find_element_by_class_name('sh-t__title').get_attribute('innerHTML')
            context.bot.send_message(chat_id=update.effective_chat.id, text='LINK RISULTATO:\nhttps://www.google.com/search?tbm=shop&q='+result)
            context.bot.send_message(chat_id=update.effective_chat.id, text='RISULTATI IN ORDINE DI PREZZO')
            for elem in elements:
                result=''
                soup = BeautifulSoup(elem.get_attribute('innerHTML'), 'lxml')
                result+='Nome: '+title+'\n'
                result+='Prezzo: '+soup.find('span',class_='_-dN').get_text()+'\n'
                result+='Venduto da: '+soup.find('a',class_='_-dQ').get_text().replace('Si apre in una nuova finestra','')+'\n'
                result+=soup.find('td',class_='_-eE').get_text()+'\n'
                result+='TOTALE: '+soup.find('div',class_='_-e5').get_text()+'\n'
                
                #result+='Vedi: '+str(soup.find('a',class_='eaGTj').attrs.get('src'))+'\n'
                #resultFinale+= elem.get_attribute('innerHTML')context.bot.send_photo(chat_id=update.effective_chat.id, photo=dir_path+'.png')
                context.bot.send_message(chat_id=update.effective_chat.id, text=result)

        else:        
            elements= driver.find_elements_by_class_name("sh-dgr__content")
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=driver.get_screenshot_as_png())
            context.bot.send_message(chat_id=update.effective_chat.id, text='https://www.google.com/search?tbm=shop&q='+result)
            k=0
            im =''
            for elem in elements:
                result=''
                soup = BeautifulSoup(elem.get_attribute('innerHTML'), 'lxml')
                result+='Nome: '+soup.find('h4',class_='Xjkr3b').get_text()+'\n'
                result+='Prezzo: '+soup.find('span',class_='a8Pemb').get_text()+'\n'
                result+='Venduto da: '+soup.find('div',class_='aULzUe').get_text()+'\n'
                result+=soup.find('div',class_='vEjMR').get_text()+'\n'
                #result+='Vedi: '+str(soup.find('a',class_='eaGTj').attrs.get('src'))+'\n'
                #resultFinale+= elem.get_attribute('innerHTML')
                #context.bot.send_photo(chat_id=update.effective_chat.id, photo=dir_path+'.png')
                context.bot.send_message(chat_id=update.effective_chat.id, text=result)
            
        if len(elements)==0:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Come non detto... Prodotto riconosciuto ma non presente sui diversi comparatori di prezzo')
        driver.close()
        driver.quit()

def searchTrovaprezzi(update,context,result,driver):
    context.bot.send_message(chat_id=update.effective_chat.id, text='       PRODOTTO RICONOSCIUTO.      \n\n      INIZIA LO SHOW ...      ')
    driver.get('https://www.trovaprezzi.it/')
    element = driver.find_element_by_id('libera')
    element.send_keys(result)
    driver.find_elements_by_class_name("search_button")[0].click()
    time.sleep(1)
    driver.get(driver.current_url+'?sort=prezzo_totale')
    time.sleep(1)
    
    if len(driver.find_elements_by_class_name("listing_item"))>0:
        element=driver.find_elements_by_class_name("listing_item")[0]
        driver.execute_script("arguments[0].scrollIntoView();",element)
        action = ActionChains(driver)
        action.move_to_element(element)
        action.click()
        action.perform()
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=driver.get_screenshot_as_png())
        #context.bot.send_message(chat_id=update.effective_chat.id, text='LINK RISULTATO:\n'+driver.current_url)
        context.bot.send_message(chat_id=update.effective_chat.id, text='       RISULTATI IN ORDINE DI PREZZO       ')
        elements=driver.find_elements_by_class_name("listing_item")
        for elem in elements:
            result=''
            soup = BeautifulSoup(elem.get_attribute('innerHTML'), 'lxml')
            result+='Nome: '+soup.find('a',class_='item_name').get_text().strip()+'\n'
            link= 'trovaprezzi.it'+soup.find('a', {'class': 'item_name'})['href']
            result+='Prezzo: '+soup.find('div',class_='item_basic_price').get_text().strip()+'\n'
            seller= soup.find('span',class_='merchant_name').get_text().strip()
            result+='Venduto da: '+soup.find('span',class_='merchant_name').get_text().strip()+'\n'
            result+=soup.find('div',class_='item_delivery_price').get_text().strip().replace('+ Sped.','Spedizione:')+'\n'
            result+=soup.find('div',class_='item_total_price').get_text().strip().replace('Tot.','\nTotale: ')+'\n'
            #result+='Vedi: '+str(soup.find('a',class_='eaGTj').attrs.get('src'))+'\n'
            #resultFinale+= elem.get_attribute('innerHTML')
            #context.bot.send_photo(chat_id=update.effective_chat.id, photo=dir_path+'.png')
            context.bot.send_message(chat_id=update.effective_chat.id, text=result)
            context.bot.send_message(chat_id=update.message.chat_id, text="<a href='"+link+"'>Clicca per visualizzare l'offerta di "+seller+"  </a>",parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Come non detto... Prodotto riconosciuto ma non presente sui diversi comparatori di prezzo.\n')

    driver.close()
    driver.quit()       
    

def searchProductIMG(update,context):
    opts = Options()
   # opts.headless=True
    opts.binary_location='/app/vendor/firefox/firefox'

    context.bot.send_message(chat_id=update.effective_chat.id, text='       RICONOSCIMENTO PRODOTTO ...     ')
    driver = webdriver.Firefox(executable_path='/app/vendor/geckodriver/geckodriver',options=opts)
    file = context.bot.getFile(update.message.photo[-1].file_id)
    obj = context.bot.get_file(file)
    nomefile= randomword(6)
    with open("foto/"+nomefile+".jpg", 'wb') as f:
        context.bot.get_file(update.message.photo[-1]).download(out=f)
    img = cv2.imread('foto/'+nomefile+'.jpg')
    code= decode(img)
    os.remove('foto/'+nomefile+'.jpg')
    if(len(code)>0):
        result=str(code[0].data).replace('b\'','').replace('\'','')
        print(result)
        searchTrovaprezzi(update,context,result,driver)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Non Trovato :( \n- Non è stato possibile reperire le informazioni\n- Inquadra meglio il codice a barre\nRiprova!')

    results = driver

def searchProductText(update,context):
    if update.message.text.startswith('Cerca'):
        dati= update.message.text.split('erca ')
        opts = Options()
        #opts.headless=True
        opts.binary_location='/app/vendor/firefox/firefox'
        context.bot.send_message(chat_id=update.effective_chat.id, text='       RICONOSCIMENTO PRODOTTO ...     ')
        driver = webdriver.Firefox(executable_path='/app/vendor/geckodriver/geckodriver',options=opts)
        result=dati[1].replace(' ','%20')
        searchTrovaprezzi(update,context,result,driver)
        results = driver




photoHandler =  MessageHandler(Filters.photo, searchProductIMG)
TextHandler =  MessageHandler(Filters.text, searchProductText)


start_handler = CommandHandler('start', start)

dispatcher.add_handler(TextHandler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(photoHandler)    
updater.start_polling()
