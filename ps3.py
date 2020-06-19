import requests
from bs4 import BeautifulSoup
from pypresence import Presence
import time
import sys
import os

def connect_to_console(console_ip):
    url = "http://{}/cpursx.ps3?/sman.ps3".format(console_ip)
    connected = False
    try:
        html = requests.get(url).text
        connected = True
        return connected
    except TimeoutError:
        return connected


def get_console_info(console_ip):
    url = "http://{}/cpursx.ps3?/sman.ps3".format(console_ip)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    strings = soup.findAll('a', attrs={'class': 's'})
    return strings

def get_game(console_ip):
    url = "http://{}/cpursx.ps3?/sman.ps3".format(console_ip)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    strings = soup.findAll('h2')
    res = strings[0].text
    game = None
    if res.startswith("BL") or res.startswith("NP"):
        game = res.split(' ', 1)[1]
    else:
        game = "XMB"


    return game
    


def get_temps(div):
    temps = div.text.replace("Â", "")
    return temps

def get_firmware(div):
    crap = div.text
    formatted_fw = ""
    for l in crap:
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
    
if not os.path.exists("ip.txt"):
    ps3_ip_file = open("ip.txt",'w+')
    ps3_ip = input("Please enter your PS3 local IP address:")
    ps3_ip_file.write(f"{ps3_ip}")
    ps3_ip_file.close()
else:
    ps3_ip_file = open("ip.txt",'r+')
    ps3_ip = ps3_ip_file.read()
    ps3_ip_file.close()

print("Welcome to PS3 Rich presence by Yowai-dev\n")


if connect_to_console(ps3_ip):
    print("Connection established with your console.")
    client_id = '718828414525505588'  
    RPC = Presence(client_id)
    RPC.connect()

    while True:  
        ps3_info = get_console_info(ps3_ip)
        temps = get_temps(ps3_info[0])
        fw = get_firmware(ps3_info[4]).split(': ', 1)[1]
        game = get_game(ps3_ip)
        print("Playing {}".format(game))
        status = "🎮: {}".format(game)
        RPC.update(large_image="logo", large_text=status, small_text=status, details=fw, state=status)
        time.sleep(10)
        clean_buffer(sys.platform) 

else:
    print("Something went wrong, aborting...")
    exit()
