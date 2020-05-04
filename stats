#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:45:02 2020

@author: joshpc
"""

import csv
import pandas as pd
import re
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
sns.set(style="ticks", color_codes=True)


def makeList(string):
    "Takes string that is in a list or tuple format into a list"
    
    
    li = re.sub(r"^[\[\()]", "", string)
    li = re.sub(r"[\]\)]$", "", li)

    li = [word.strip("' ") for word in li.split(',') if word != '']
        
    return li
    


def primary_and_features_Artists_List(df):
    
    
    primary_artists = []
    feature_artists = []
    
    for artists_list in df["Artists"]:
        li = makeList(artists_list)
        
        primary_artists.append(li[0])
        
        if len(li) > 1:
            for feature_artist in li[1:]:
                feature_artists.append(feature_artist)
    
    primary_artists = {'Primary Artists': primary_artists}
    feature_artists = {'Feature Artists': feature_artists}
    
    
    return primary_artists, feature_artists

def get_top_artists_year(df, year):
    
    prim, features= primary_and_features_Artists_List(df[df.Year.eq(year)])
    
    
    sns.distplot(prim['Primary Artists'], kde=False);
    #print(pd.DataFrame(prim))
    
    
def draw_Artists_Count_year(df, yaer):
    g = sns.catplot(x="Primary Artists", kind="count", palette="ch:.25", data=pd.DataFrame(df), height=4, aspect=3)
    g.set_titles(f"Primary Artist Mentions {year}")
    
    axes = g.axes.flatten()
   
    axes[0].set_xticklabels(axes[0].get_xticklabels(), fontsize = 10, rotation=65, ha="right")
  
    

    
    
def get_top_artists(df):
    
    
    prim, features = primary_and_features_Artists_List(df)
    
    
    
    
if __name__ == "__main__":
    
    df = pd.read_csv("final_songs.csv")
    
    
    
    get_top_artists_year(df, 2015)
    #print(df.iloc[1232])
    

 
    #print(df["Artists"][0])
    #print(makeList(df.iloc[1232][3]))
        
        
        
    