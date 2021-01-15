"""
    i'll comment the code later. Lazy !!! 😂😂😂
"""
from decouple import config
from selenium import webdriver
from time import sleep
import winsound
import datetime
import requests
import os

def main():
    GATEWAY_IP_ADDRESS = config("GATEWAY_IP_ADDRESS")
    THRESHOLD_GB = config("THRESHOLD_GB")
    file_name = './storage/bx_consumption-'+ str(datetime.date.today())   

    if not os.path.isfile(file_name):
        with open(file_name, 'w') as box_consumption_f:
            box_consumption_f.write("0,0")

    browser = webdriver.Chrome(executable_path="./resources/chromedriver.exe")

    check_bx_connection(GATEWAY_IP_ADDRESS, browser)

    browser.get(GATEWAY_IP_ADDRESS)

    while True:

        with open(file_name, 'r') as box_consumption_f:
            total_download, total_upload = box_consumption_f.read().split(",")
            total_download, total_upload = float(total_download), float(total_upload) 
        
        downloaded_el = browser.find_element_by_xpath("//label[@id='TotalDownload']")
        uploaded_el = browser.find_element_by_xpath("//label[@id='TotalUpload']")
        downloaded, uploaded = to_megabyte(downloaded_el.text), to_megabyte(uploaded_el.text)
        
        if downloaded < total_download or uploaded < total_upload :
            total_download += downloaded
            total_upload += uploaded
        else:
            total_download +=  downloaded - total_download 
            total_upload += uploaded - total_upload 

        print("________________________________________")
        print(f"Total data downloaded ⬇⬇⬇⬇ = {format(total_download/1000, '4f')} GB")
        print(f"Total data uploaded ⬆⬆⬆⬆ = {format(total_upload/1000, '4f')} GB")
        print(f"Threshold = {THRESHOLD_GB} GB")

        # Save new downloaded and uploaded amount of data in the file storage of the day 
        with open(file_name, 'w') as box_consumption_f:
            box_consumption_f.write(f"{total_download},{total_upload}")
        
        if total_download + total_upload < float(THRESHOLD_GB)*1000 :
            print(f"data consumed = {format((total_download + total_upload)/1000, '4f')} GB --> Threshold not exceeded ✅✅✅")
        else:
            print(f"data consumed = {format((total_download + total_upload)/1000, '4f')} GB --> Threshold exceeded ❗❗❗")
            print("Alert started....")
            winsound.Beep(2000, 2000)
            winsound.Beep(2000, 2000)
            winsound.Beep(2000, 2000)
            winsound.Beep(2000, 2000)
        print("________________________________________")


        sleep(5)
        check_bx_connection(GATEWAY_IP_ADDRESS, browser)

def to_megabyte(data: str) -> float:
    unit = data[-2:]
    data = float(data[:-3])
    if unit == "GB": 
        return data*1000
    return data 

def to_gigabyte(data: str) -> float:
    unit = data[-2:]
    data = float(data[:-3])
    if unit == "MB": 
        return data/1000
    return data 

def check_bx_connection(gateway_url, browser):
    resp = requests.get(gateway_url)
    was_disconnected = not resp.ok
    while not resp.ok : 
        print("Connection unavailable 🚫🚫🚫")
        try:
            resp = requests.get(gateway_url)
        except Exception as e:
            pass
        sleep(5)
    if was_disconnected : 
        browser.get(gateway_url)

if __name__ == "__main__":
    main()
