# Std Libs
import requests
import logging
from datetime import datetime

# 3rd Party Libs
import dateparser
from bs4 import BeautifulSoup
import pandas as pd

# Local Libs
from dropbox_ops import read_file,write_file

#Config
file_path = '/BrentOilPrice.csv'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.StreamHandler()])

# --------------------------------------------------------------------------------

def get_data():

    r = requests.get('https://www.bbc.co.uk/news/topics/cmjpj223708t/oil')
    soup = BeautifulSoup(r.text, 'html.parser')

    update_date = soup.findAll(class_="nw-c-md-chart-date gel-brevier")[0].text.replace("As of","")
    update_date = str(dateparser.parse(update_date).date())

    price = soup.findAll(class_="gel-paragon nw-c-md-commodity-summary__value")[0].text

    return update_date,price

# --------------------------------------------------------------------------------

def update_dropbox(file_path,date,price):
    
    logging.info("Reading file from DB")
    df = read_file(file_path)
    df = df.append({'date':date,'price':price,'update_date':str(datetime.now())},ignore_index=True)
    logging.info("Saving file to DB")
    write_file(df=df,path=file_path)

    return

# --------------------------------------------------------------------------------


def run_script():
    logging.info("Getting data from BBC")
    date,price = get_data()
    logging.info("Saving to Dropbox")
    update_dropbox(file_path,date,price)
    logging.info('File saved')
    return

# --------------------------------------------------------------------------------


if __name__ == "__main__":
    run_script()