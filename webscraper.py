import requests
import time
from bs4 import BeautifulSoup
from csv import writer
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#GLOBAL VARIABLES
wr_highthreshold = 70
wr_threshold = 60
games_threshold = 25
m_player_name = 'animbot'
smurfs = list()

def print_player(player_name):
	if player_name is None:
		return

	url = 'https://na.op.gg/summoner/userName='
	url += player_name
	
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')

	name = soup.find(class_='Name').contents[0]
	rank = soup.find(class_='TierRank').contents[0]
	winstemp = soup.find(class_='wins')
	if winstemp is None:
		return
	wins = winstemp.contents[0]
	losses = soup.find(class_='losses').contents[0]
	winratio = soup.find(class_='winratio').contents[0]

	#print(name + ' | ' + rank + ' | ' + wins + ' | ' + losses + ' | ' + winratio)

	winratio = winratio[-3:-1]
	wr_int = int(winratio)
	games = int(wins[:-1]) + int(losses[:-1])

	if(wr_int >= wr_highthreshold) or ((games >= games_threshold) and (wr_int >= wr_threshold)):
		smurfs.append(name + ' | ' + rank + ' | ' + wins + ' | ' + losses + ' | ' + winratio)
		print(name + ' | ' + rank + ' | ' + wins + ' | ' + losses + ' | ' + winratio + '%')


player_url = 'https://na.op.gg/summoner/userName=' + m_player_name
with closing(Firefox()) as driver:
    driver.get(player_url)
    button = driver.find_element_by_id('right_gametype_soloranked')
    button.click()
    # wait for the page to load
    time.sleep(5)
    # store it to string variable
    response = driver.page_source

soup = BeautifulSoup(response, 'html.parser')
players = soup.find_all(class_='SummonerName')

#for each player, print their name and winrate in the csv

for player in players:
	url = player.find('a')
	if url is not None:
		temp = ''+url.contents[0]
		if temp != m_player_name:
			print_player(url.contents[0])


print(str(len(smurfs)) + " in 20 games | Average " + str(len(smurfs)/20))

