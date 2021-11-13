import configparser
from datetime import date
import glob
import fnmatch
import os
from pathlib import Path
from  PIL import Image
import requests
import time
import json

def fetch_memories():
    config = configparser.ConfigParser()
    config.read('piwigo.ini')
    url = config.get('connection', 'url')
    port = config.get('connection', 'port')
    username = config.get('auth', 'username')
    password = config.get('auth', 'password')


    base_location = config.get('pictures','location')
    memories_location = os.path.join(base_location, "memories/*")
    for f in glob.glob(memories_location):
        os.remove(f)

    with requests.Session() as s:

        login = s.post(url + ':' + port + '/ws.php?method=pwg.session.login', data = {"username": username, "password": password})
        print(login.content)

        page_nr = 0
        count = 1
        while (count):
            #request_data = s.get(url + ':' + port + '/ws.php?format=json&method=pwg.categories.getImages&recursive=true')
            request_data = s.get(url + ':' + port + '/ws.php?format=json&method=pwg.categories.getImages&recursive=true&per_page=500&page=' + str(page_nr))
            page_nr = page_nr + 1

            try:
                request_data.json()
            except:
                continue

            print(request_data.json()['result']['paging'])
            count = request_data.json()['result']['paging']['count']

            all_pictures = request_data.json()['result']['images']
            #print(json.dumps(all_pictures))

            today = date.today()
            memories_wildcard = '????-' + str(today.month).zfill(2) + '-' + str(today.day).zfill(2) + '*'
            memories_pictures = [picture for picture in all_pictures if picture.get('date_creation') and fnmatch.fnmatch(picture['date_creation'], memories_wildcard)]

            base_location = config.get('pictures','location')
            memories_location = os.path.join(base_location, "memories")
            for picture in memories_pictures:
                file_name = os.path.join(memories_location, picture['file'])
                print (file_name)
                if (not os.path.exists(file_name)):
                    f = open (file_name, 'wb')
                    f.write(s.get(picture['element_url']).content)
                    f.close()

        s.get(url + ':' + port + '/ws.php?format=rest&method=pwg.session.logout')

#TODO
def resize_picture():
    config = configparser.ConfigParser()
    config.read('piwigo.ini')

    base_location = config.get('pictures','location')
    memories_location = os.path.join(base_location, "memories/*")
    for f in glob.glob(memories_location):
        if (os.path.isfile(f)):
          picture = Image.open(f)

          file_name = os.path.join(Path(f).parent.absolute(), 'resized/')
          file_name += Path(f).stem
          file_name += Path(f).suffix
          print(file_name)
          resized_picture = picture.resize((1920, 1080))
          resized_picture.save(file_name)


if __name__ == '__main__':
    #fetch_memories()
    resize_picture()
