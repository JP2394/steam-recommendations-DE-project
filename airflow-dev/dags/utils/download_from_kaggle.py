import os
import logging

from time import time
from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage
import pyarrow.csv as pv
import pyarrow.parquet as pq
import pandas as pd 



def download_from_kaggle(downloadpath):
    dataset = 'antonkozyriev/game-recommendations-on-steam'
    path = downloadpath
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path,unzip=True)




