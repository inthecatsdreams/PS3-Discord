import requests
from bs4 import BeautifulSoup
from pypresence import Presence
import time

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
    strings = soup.findAll('font', attrs={'size': 3})
    if strings == None:
        game = "Nothing"
        return game
    else:
        try:
            game = strings[-1].text
        except IndexError:
            game = "Nothing"
    
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


print("Welcome to PS3 Rich presence by Yowai-dev\n")
ps3_ip = input("Please enter your PS3 local IP address:")

if connect_to_console(ps3_ip):
    print("Connection established with your console.")
    print(get_game(ps3_ip))
    client_id = '718828414525505588'  
    RPC = Presence(client_id)
    RPC.connect()

    while True:  
        ps3_info = get_console_info(ps3_ip)
        temps = get_temps(ps3_info[0])
        fw = get_firmware(ps3_info[4])
        game = get_game(ps3_ip)
        status = "🎮: {}".format(game)
        RPC.update(large_image="logo", large_text=status, small_image="logo", small_text=status, details="CFW: {}".format(fw), state= status)
        time.sleep(15) 

else:
    print("Something went wrong, aborting...")
    exit()
