import json
import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
conn = sqlite3.connect('/Users/bclark66/musi7100/sp_data.db')
conn2 = sqlite3.connect('/Users/bclark66/musi7100/sp_data.db')
c = conn.cursor()
c1 = conn2.cursor()

driver = webdriver.Chrome(ChromeDriverManager().install())

def get_chords(title,song,store):
    url = 'https://chordify.net/chords/' + song

    #driver = webdriver.Chrome()
    driver.get(url)
    timeout = 10

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'chord'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    html = driver.page_source
    # response = urllib.request.urlopen(url)
    # html = response.read().decode("utf-8") 

    soup = BeautifulSoup(html, "html.parser")
    rs3 = soup.find("div", {"id": "chordsArea"})
    #print("rrrrr",rs3)
    if store:
        c1.execute('insert into chordify_songs values(?,?) ', (song, title))
        conn2.commit()
    chordlist = []
    for chord in rs3.children:
        if type(chord) == type(rs3):
            if chord['class'][0] == 'chords':
                #print("bar ",chord['class'][1])
                for child in chord.children:
                    #print("child ",child)
                    if child['class'][0] == 'chord':
                        if len(child['class']) > 1:
                            if child['class'][1] == 'nolabel':
                                chordlist.append('N')
                        else:
                                    
                            for label in child.descendants:
                                #print("lab ",label)
                                if label['class'][0] == 'chord-label':
                                    #print(label['class'][1][0:6])
                                    if label['class'][1][0:6] == 'label-':
                                        #print(label)
                                        chordlist.append(label['class'][1][6:])
    ms_nbr = 1                                
    for chord in chordlist:
        if store:
            c1.execute('insert into chordify_song_chords values(?,?,?,?)', (song,ms_nbr,chord," "))
            conn2.commit()
        else:
            print(song," ",ms_nbr," ",chord)
        ms_nbr += 1



# name = 'bastille'
# title = 'happier'
#searchtext = name + ' ' + title
url = 'https://chordify.net/search/'
searches = []
for artist,title in c1.execute("select artist,song_title from mcgill_billboard_songs limit 5"):
    searches.append(url + title + " " + artist)
#for search in searches:
    # rs = get_search_results(search,True)
    #     print("rs ",rs)
    #driver = webdriver.Chrome()
for search in searches:
    driver.get(search)
    html = driver.page_source
    done = False
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a'):
        #print("llll ",link.get('href'))
        if len(link.get('href')) > 5:
            #print("type ",type(link.get('href')))
            ch = link.get('href')
            #print("ch ")
            if ch[0:6] == '/chord' and ch[6] != '-' and ch[6:14] != 's/artist' and ch[6:15] !='s/archive':
                print("ch ",ch)
                #get_chords(ch)
                done = True
        if done:
            break
# title = 'Love and Happiness'
# song = 'the-police-every-breath-you-take-thepolicevevo'
# get_chords(title,song,True)



    


