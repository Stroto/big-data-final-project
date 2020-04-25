# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:44:25 2020

@author: Joshua
"""

import scrapper
import requests
from bs4 import element
import re

CLIENT_ACCESS_TOKEN = 'x7D_HFMdSpFStJddZOmfavjW8ExkdNZnzABkCQGM7zyv7yWAPmdVS8iV1LgsK1VW'

def request_song_info(song_title, artist):
    
  
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist}
    response = requests.get(search_url, data=data, headers=headers)

    return response
    
def scrapeTrackProducers(url):
    "Gets the Track Info HTML Section from the song's genius page"
    
    res = scrapper.getResponseSoup(url)

    # Go to the metadata section where the Title, Artist, Features, and Produced By Info is
    meta_data = res.find("div", class_="header_with_cover_art-primary_info")
    metadata_units = meta_data.find_all("div", "metadata_unit")
    
    # Get all metadata div sections and find the "Produced By" units
    metadata_units = [metadata_unit for metadata_unit in metadata_units if metadata_unit.span.text == "Produced by"]
    
    # Get producers
    producer_metadata_units = [producer_unit.text.strip() for metadata_unit in metadata_units for producer_unit in metadata_unit.find_all("span", class_ = "metadata_unit-info")]
    
    # Clean producer names
    producer_metadata_units = [re.sub(r'\s*&\s*[0-9]\s*more\s*', "", unit) for unit in producer_metadata_units]
    producers = re.split(r'\s*[,&]\s*', ",".join(producer_metadata_units))
        
    # producer_metadata_units = [ for metadata_unit in metadata_units]
    # print(url, "\n", producers)
          
    return producers

def getProducers_Lyrics(song: tuple, i):
    
    song_title, artists, song_rank, song_year = song
    found_page = False
    producers = []
    lyrics = ""
    view_count = 0
    
    # Search the song on genius with the song title and one of the artists
    # If search does not produce a list of producers, then search with the next available artist
    # If song is not in genius, mark song data as NONE
    count = 0
    while(found_page == False and count < len(artists)):
        json_res = request_song_info(song_title, artists[count]).json()
        
        
        for hit in json_res['response']['hits']:
            if artists[count].lower() in hit['result']['primary_artist']['name'].lower():
                song_page = hit['result']["url"]
                producers = scrapeTrackProducers(song_page)
                lyrics = scrapeLyrics(song_page)
                view_count = scrapeViewCount(song_page)
                print(f"COUNT: {i}\nSong: {song[0]}, Artists: {song[1]}, Rank: {song[2]}, Year: {song[3]}")
                print(f"", producers, "\n--------")
                found_page = True
            break
        count += 1
        
    return producers, lyrics

def scrapeViewCount(url):
    
    res = scrapper.getResponseSoup(url)

    # Go to the metadata section where the Title, Artist, Features, and Produced By Info is
    meta_data = res.select("body > routable-page > ng-outlet > song-page > div > div > div.song_body.column_layout > div.column_layout-column_span.column_layout-column_span--secondary.u-top_margin.column_layout-flex_column > div.column_layout-column_span-initial_content > div > defer-compile:nth-child(4) > div.song-metadata")
    #views = meta_data.contents[1].text.strip()
    
    print(meta_data)
    
    
def scrapeLyrics(url):
    "Gets the lyrics from the song's genius page. Lyrics is labeled by sections!"
    res = scrapper.getResponseSoup(url)

    # Go to the metadata section where the Title, Artist, Features, and Produced By Info is
    meta_data = res.find("div", class_="lyrics")
    
    lyrics = meta_data.text.strip()
    print(lyrics)
    
    return lyrics

def main():
    
    url = "https://www.billboard.com/charts/year-end/2019/hot-100-songs"
    
    song_list = scrapper.getSongs(url, 2019)
    
    
    for i, song in enumerate(song_list):
        producers, lyrics = getProducers_Lyrics(song, i)
        
    
if __name__ == "__main__":
    main()
    