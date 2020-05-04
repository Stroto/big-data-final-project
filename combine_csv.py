# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import csv

def combine_csv(string="combined_songs_csv.csv"):
    
    extension = 'csv'
    
    all_filenames = [f'songs_{2006 + i}.csv' for i in range(14)]
    
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    #export to csv
    combined_csv.to_csv(string, index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    
    with open("combined_songs_csv.csv", 'r', encoding='utf-8-sig') as inp, open("final_songs.csv", 'w', newline='', encoding='utf-8-sig') as out:
        
        writer = csv.writer(out)
        
        for row in csv.reader(inp):
            if (row[3].strip("\[\]").split(',') == ['']) == False and row[7] != "":
                writer.writerow(row)
            