# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:27:18 2020

Scrapper Code Usage Path:
    
    1.Go to Billboard Year End Chart Page
    2.Get each year end chart page link for each year available
    3.Go to each year's page (years specified by user)'
        Go to song list elements of page
            Get song element and extract info
    

@author: Joshua
"""

import requests
import re
from bs4 import BeautifulSoup
from bs4 import element
from collections import defaultdict
import re

def re_strip(string):
    new_string = re.sub(r'^(\u200b)+', "", string)
    new_string = re.sub(r'(\u200b)+$', "", new_string)

    return new_string
def getResponseSoup(url: str):
    
    res = requests.get(url)
    
    res = BeautifulSoup(res.content, 'html.parser')
    
    return res

def getSongLinks(res):
    """"Given a BeautifulSoup obj of targeted page, get links for each year chart
    from the data range"""
    
    billboard_home_dir = "https://www.billboard.com"
    
    css_selector = "#main > div.container.container--xxlight-grey.container--no-side-padding > div > div:nth-child(1) > div.chart-year-selection__wrapper > div.chart-year-selection.chart-year-selection--mini > div > span > label ul"
    
    year_lists_html = res.select(css_selector)
        
    year_to_url = defaultdict(str)
    for year_list in year_lists_html[0].find_all('a'):
    
        if type(year_list) == element.Tag:
            year = int(year_list.text)
            link =  billboard_home_dir + year_list.attrs['href']
            
            year_to_url[year] = link
                    
    return year_to_url

def cleanSongArtistsTexts(artists_text):
    "Seperates artists into a tuple. Assumes first artist is primary artist and the rest are featuring artists"
    
    artists = re.split(r'\s*[,&)] | \s*Featuring\s* | \s*X\s*', artists_text)
    
    artists = [re_strip(artist) for artist in artists]
    artists = [re.sub(r'^(Featuring)+\s*', "", artist) for artist in artists]
    
    return tuple(artists)
    

def getSongList(res, year):
    "Gets songs and billboard rank from year-end html page"
    
    # List is broken down into 5 sections, each one divided with class below
    song_list_sections = res.find_all("div", class_ = "chart-details__item-list")
    
    
    for section in song_list_sections:
        for song in section.find_all("div", class_ = "ye-chart-item__primary-row"):
            song_name = song.find("div", class_ = "ye-chart-item__title").text.strip()
            song_name = re.sub("\s*\((.)*\)\s*", "", song_name)
            song_name = re_strip(song_name)
            
            song_rank = int(song.find("div", class_ = "ye-chart-item__rank" ).text.strip())
            song_artists = song.find("div", class_ = "ye-chart-item__artist" ).text.strip()
            
            # Seperate artists if there are multiple artists in the song
            # Assumes that the first artist is the primary artists and the rest are featuring
            song_artists = cleanSongArtistsTexts(song_artists)
            yield (song_name, song_artists, song_rank, year)
    

def getSongListYears(links: dict, start_year: int, end_year = None):
    """Retrieves songs for the given year range from the links
    If there is a missing ranked song, song list will add a placeholder tuple
    (None, None, None)"""
    
    song_list = []
    
    if end_year == None:
        end_year = start_year
        
    for year in range(start_year, end_year+1):
        link = links[year]
        res = getResponseSoup(link)
        

        for song in getSongList(res, year):
            song_list.append((song[0], song[1], song[2], song[3]))

            
    return song_list

def getSongs(url, start_year, end_year = None):
    
    res = getResponseSoup(url)
    
    song_List_links = getSongLinks(res)
    
    song_list = getSongListYears(song_List_links, start_year, end_year)
    
    return song_list

def main():
   
    billboard_url = "https://www.billboard.com/charts/year-end/2019/hot-100-songs"
    res = getResponseSoup(billboard_url)
    
    
    song_List_links = getSongLinks(res)
    
    for song in getSongListYears(song_List_links, 2019):
        print(f"Song: {song[0]}, Artists: {song[1]}, Rank: {song[2]}, Year: {song[3]}")

    

if __name__ == "__main__":
    main()