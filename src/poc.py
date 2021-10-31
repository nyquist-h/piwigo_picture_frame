import configparser
import fnmatch
import os
import requests

def poc():
    config = configparser.ConfigParser()
    config.read('piwigo.ini')

    url = config.get('connection', 'url')
    port = config.get('connection', 'port')
    with requests.Session() as s:
        myobj = {"username": config.get('auth', 'username'), "password": config.get('auth', 'password')}
        login = s.post(url + ':' + port + '/ws.php?method=pwg.session.login', data = myobj)
        print(login.status_code)
        print(login.content)

        x = s.get(url + ':' + port + '/ws.php?format=json&method=pwg.categories.getImages&cat_id=17&recursive=true')
        data = x.json()
        print(x.status_code)
        print(x.content)

        images = data['result']['images']
        filtered_data = [x for x in images if fnmatch.fnmatch(x['date_creation'], '????-12-03*')]
        for image in filtered_data:
            location = os.path.join(config.get('pictures','location'), image['file'])
            if (not os.path.exists(location)):
                print (location)
                f = open (location, 'wb')
                f.write(s.get(image['element_url']).content)
                f.close()

        s.get(url + ':' + port + '/ws.php?format=rest&method=pwg.session.logout')


if __name__ == '__main__':
    poc()
