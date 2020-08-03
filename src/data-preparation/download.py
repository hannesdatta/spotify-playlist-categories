import requests
import os

print('Downloading raw data... please wait.')

data = requests.get('https://www.dropbox.com/s/9ufn2t4nn7og0wn/20200803_data.zip?dl=1')

print('Writing raw data to file')

os.makedirs('../../data', exist_ok=True)

f = open('../../data/data.zip', 'wb')

f.write(data.content)

f.close()

print('Done.')