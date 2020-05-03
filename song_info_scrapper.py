# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:44:25 2020

@author: Joshua
"""

import scrapper
import requests
from bs4 import element
import re
import numpy as np
from collections import defaultdict
import operator
import pandas as pd

CLIENT_ACCESS_TOKEN = 'x7D_HFMdSpFStJddZOmfavjW8ExkdNZnzABkCQGM7zyv7yWAPmdVS8iV1LgsK1VW'

def search_song_info(song_title, artist):
    
  
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def getSongInfo(song: tuple, i):
    
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
        json_res = search_song_info(song_title, artists[count]).json()
        
        
        for hit in json_res['response']['hits']:
            if artists[count].lower() in hit['result']['primary_artist']['name'].lower():
                song_page = hit['result']["url"]
                song_api_path = hit['result']['api_path']
                song_artist_page = hit['result']["primary_artist"]['url']                
                
                producers, view_count = getProducers_and_ViewCount(song_api_path)
                lyrics = scrapeLyrics(song_page)
                # popular_songs = getPopularSongs(artists[count])
                
                #print(f"COUNT: {i}\nSong: {song[0]}, Artists: {song[1]}, Rank: {song[2]}, Year: {song[3]}")
                #print(f"", producers, "\n--------")
                found_page = True
            break
        count += 1
        
    return producers, lyrics, view_count

def getProducers_and_ViewCount(api_path):
    
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN}
    search_url = base_url + api_path
    
    response = requests.get(search_url, headers=headers)
    
    json_res = response.json()
    
    producers = [producer['name'] for producer in json_res['response']['song']["producer_artists"]]
    view_count = json_res['response']['song']['stats']['pageviews']
    
    return producers, view_count

def scrapeLyrics(url):
    "Gets the lyrics from the song's genius page. Lyrics is labeled by sections!"
    res = scrapper.getResponseSoup(url)

    # Go to the metadata section where the Title, Artist, Features, and Produced By Info is
    meta_data = res.find("div", class_="lyrics")
    
    lyrics = meta_data.text.strip()
 
    return lyrics

def re_strip(string):
    new_string = re.sub(r'^(\u200b)+', "", string)
    new_string = re.sub(r'(\u200b)+$', "", new_string)

    return new_string

def getPopularSongs(artist):
    
    
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN}
    search_url = base_url + '/search'
    data = {'q': artist}
    json_res = requests.get(search_url, data=data, headers=headers).json()
    
    url = ""
    
    for hit in json_res['response']['hits']:
        if artist.lower() in hit['result']['primary_artist']['name'].lower():
            url = hit['result']['primary_artist']['url']
            break
        
    res = scrapper.getResponseSoup(url)
    
    popular_songs_html_grid = res.find_all("div", class_ = "mini_card-title_and_subtitle")
    popular_songs = [(grid.find("div", class_="mini_card-title").text.strip(), grid.find("div", class_="mini_card-subtitle").text.strip()) for grid in popular_songs_html_grid]
    
    popular_songs = [(re_strip(song[0]), re.split(r'\s*[,&)]\s*', song[1])) for song in popular_songs]
    popular_songs = [(song[0], song[1]) for song in popular_songs if "Remix" not in song[0]]
    
    print(popular_songs)   
        
        
        
def main():
    
    url = "https://www.billboard.com/charts/year-end/2019/hot-100-songs"
    
    song_list = scrapper.getSongs(url, 2019)
    songs_with_metadata = []
    

    
    # Track songs, artists, and producers via set for ID Tagging:
    songs_artists_producers = defaultdict(set)
    
    # Shape is number of songs by number of metadata (6): Artists, Producers, Genius View Count, Lyrics, Year
    songs_matrix = [[0]*7]*len(song_list)
    
    
    for i, song in enumerate(song_list):
        song_name, song_artists, song_rank, year = song
        producers, lyrics, view_count = getSongInfo(song, i)
        
        songs_artists_producers['songs'].add(song_name)
        
        for artist in song_artists:
            songs_artists_producers['artists'].add(artist)
        for producer in producers:
            songs_artists_producers['producers'].add(producer)
        
        songs_with_metadata.append((song_name, song_artists, producers, view_count, lyrics, song_rank, year))
    print(len(songs_with_metadata))
    
    # Sort the Song Names via songs_with_metadata
    # Sort the Artists, and Producers
    # Enumerate and make the index the ID Representation of the Song, replace artists and prducers w. IDS too
    songs_with_metadata.sort(key = operator.itemgetter(0))
    artists = list(songs_artists_producers['artists'])
    artists.sort()
    producers = list(songs_artists_producers['producers'])
    producers.sort()
    
    # Set up ID's
    id_to_artists_and_producers = defaultdict(dict)
    id_to_artists_and_producers['artists'] = defaultdict(str)
    id_to_artists_and_producers['producers'] = defaultdict(str)
    
    
    artists_and_producers_to_id = defaultdict(dict)
    artists_and_producers_to_id['artists'] = defaultdict(int)
    artists_and_producers_to_id['producers'] = defaultdict(int)
    
    for i, artist in enumerate(artists):
        id_to_artists_and_producers['artists'][i] = artist
        artists_and_producers_to_id['artists'][artist] = i
    
    for i, producers in enumerate(producers):
        id_to_artists_and_producers['producers'][i] = artist
        artists_and_producers_to_id['producers'][artist] = i
    
    # Structure data into a np array and finally a Pandas Dataframe
    for i, song in enumerate(songs_with_metadata):
        for j, metadata in enumerate(song):
            songs_matrix[i][j] = metadata
    
    df = pd.DataFrame(songs_matrix, columns = ['Song Title', "Artists", "Producers", "Genius ViewCount", "Lyrics", "Song Rank", "Year"]) 
    df.to_csv('songs.csv')

    
if __name__ == "__main__":
    main()
    