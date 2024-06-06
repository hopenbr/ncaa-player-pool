import glob
import os 

import pandas as pd
from xlsx2csv import Xlsx2csv


def converto_csv(xs):
    '''one time file convert from data.ncaa.org xlsx exports 
    converto_csv(glob.glob('/workspaces/ncaa-player-pool/data/prediction/NCAA*.xlsx'))'''
    for x in xs:
        newName = (os.path.basename(x)
                    .replace('xlsx', 'csv')
                    .replace(' ', '_')
                    .replace('(', '')
                    .replace(')','')
                    .lower())
        p = os.path.dirname(x)

        csv = f'{p}/{newName}'
        Xlsx2csv(x, outputencoding="utf-8").convert(csv)

def move_xlsx(xs):
    '''one time file move for data xlsx files
    move_xlsx((glob.glob('/workspaces/ncaa-player-pool/data/prediction/NCAA*.xlsx')'''
    for x in xs:
        p = os.path.dirname(x)
        n = os.path.basename(x)
        np = f'{p}/xlsx/{n}'
        os.rename(x, np)


def read_data(file):
    df = pd.read_csv(file, dtype=str)
    print(df)


read_data('/workspaces/ncaa-player-pool/data/prediction/ncaa_statistics_2022-23.csv')
