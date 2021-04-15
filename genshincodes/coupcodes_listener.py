#!/usr/bin/python3

import requests
import os
import time
from bs4 import BeautifulSoup

from colorama import Fore, Style

source = "https://theaxo.com/2021/genshin-impact-redemption-code/"
genshin_gift = "https://hk4e-api-os.mihoyo.com/common/apicdkey/api/webExchangeCdkey"
already_found = []

player_data = dict()
cookies = dict()

def load_player_data():
	print(f"[{Fore.CYAN}*{Style.RESET_ALL}] Loading login cookied and tickets...")
	with open("login.txt", "r") as file:
		lines = file.readlines()
		for line in lines:
			line = line.replace("\n", "")
			if line.startswith("data/"):
				entry = line.split("/")[1].split(":")
				key = entry[0]
				value = entry[1]
				player_data[key] = value
			elif line.startswith("cookies/"):
				entry = line.split("/")[1].split(":")
				key = entry[0]
				value = entry[1]
				cookies[key] = value
	print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Successfully connected to genshin api !")



def get_codes():
	req = requests.get(source)
	soup = BeautifulSoup(req.content, "html.parser")

	potential_codes = soup.find_all("tr")
	for code in potential_codes:
		content = code.find_all("td")
		rawCodeValue = content[0].find("strong")
		if rawCodeValue == None:
			continue

		value = rawCodeValue.get_text()
		isActive = content[2].get_text() == "Active"
		if isActive and not (value in already_found) and len(value) >= 10:
			already_found.append(value)
			print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Found code \"{Fore.CYAN}" + value + f"{Style.RESET_ALL}\".")

def useCodes():
	data = player_data
	for code in already_found:
		data["cdkey"] = code
		req = requests.get(genshin_gift, params=data, cookies=cookies)
		print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Using code {Fore.CYAN}\"{code}\"{Style.RESET_ALL}...")
		response = req.json()["message"]
		print(f"[{Fore.CYAN}*{Style.RESET_ALL}] {response}")
		print(f"[{Fore.CYAN}*{Style.RESET_ALL}] Waiting 5 seconds api delay...")
		time.sleep(5)
		
def helpTab():
	print("All available commands :")
	print("help - Shows this help menu.")
	print("grabcodes - Try to grab new codes.")
	print("codes - Show currently available codes.")
	print("useallcodes - Use all gift codes. ")
	print("quit - Closes this shell.")

def open_shell():
	running = True
	while running:
		cmd = input("> ")
		if cmd == "help":
			helpTab()
		elif cmd == "grabcodes":
			get_codes()
		elif cmd == "codes":
			for code in already_found:
				print("-", code)
		elif cmd == "quit":
			running = False
		elif cmd == "useallcodes":
			useCodes()
		else:
			print("Unknown command.")
	#Shell ended
	print("		Goodbye !")

def main():
	load_player_data()
	get_codes()
	open_shell()

if __name__ == "__main__":
	main()
