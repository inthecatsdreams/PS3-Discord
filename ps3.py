import requests
from bs4 import BeautifulSoup
from pypresence import Presence
import time
import sys
import os
import json
import re

def connect_to_console(console_ip):
    url = f"http://{console_ip}/cpursx.ps3?/sman.ps3"
    is_connected = False
    try:
        html = requests.get(url).text
        is_connected = True
        return is_connected
    except ConnectionError:
        return is_connected


def get_console_info(console_ip):
    url = f"http://{console_ip}/cpursx.ps3?/sman.ps3"
    html = requests.get(url).text.encode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    strings = soup.findAll('a', attrs={'class': 's'})
    return strings

def get_game(console_ip):
    url = f"http://{console_ip}/cpursx.ps3?/sman.ps3"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    strings = soup.findAll('h2')
    res = strings[0].text
    game = None
    if res.startswith("BL") or res.startswith("NP") or res.startswith("BC"):
        game = res.split(' ', 1)[1].encode("ascii","ignore").decode()
    else:
        game = "XMB"


    return game
    


def get_temps(div):
    temps = div.text.replace("Â", "")
    return temps

def get_firmware(div):
    clutter = div.text
    formatted_fw = ""
    for l in clutter:
        if l != "P":
            formatted_fw += l
        else:
            break
    return formatted_fw


def clean_buffer(user_os):
    if user_os.startswith('freebsd') or user_os.startswith('linux') or user_os.startswith("darwin"):
        os.system("clear")
    elif user_os.startswith('win'):
        os.system("cls")
        
    else:
        return

ps3_ip = None
fw_temp_cycle = False

with open("config.json", "r") as config_file:
    data = json.load(config_file)
    if data["cycle-temps"] == 0:
        fw_temp_cycle = False
    else:
        fw_temp_cycle = True
    
    if data["ps3-ip"] == "" or data["ps3-ip"] == None:
        print("Please add your PS3 ip to config.json and then restart the script.")
        exit(-1)
    else:

        ps3_ip = data["ps3-ip"]
        
print("Welcome to PS3 Rich presence by inthecatsdreams\n")


if connect_to_console(ps3_ip):
    print("Connection established with your console.")
    client_id = '718828414525505588'  
    RPC = Presence(client_id)
    RPC.connect()
    
    
    while True:  
        ps3_info = get_console_info(ps3_ip)
        
        if(fw_temp_cycle):
            fw_temp = get_temps(ps3_info[0]).replace("[Fan control: Disabled]", '')
            fw_temp_cycle = False
        else:
            fw_temp = get_firmware(ps3_info[4]).split(': ', 1)[1]
            fw_temp_cycle = True
        
        
        game = get_game(ps3_ip)
        game = game.split(" ")
        del game[-1]
        game = ' '.join(game)



        status = f"🎮: {game}"
        RPC.update(large_image="logo", large_text=status, small_text=status, details=fw_temp, state=status)
        clean_buffer(sys.platform)
        print(f"Status updated with {game}") 

        time.sleep(10)

else:
    print("Couldn't establish a connection, exiting...")
    exit()
