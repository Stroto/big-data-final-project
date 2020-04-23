# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:44:25 2020

@author: Joshua
"""

import scrapper






def main():
    
    url = "https://www.billboard.com/charts/year-end/2019/hot-100-songs"
    
    song_list = scrapper.getSongs(url, 2019)
    
    
    for song in song_list:
        print(song)
    
    
if __name__ == "__main__":
    main()
    