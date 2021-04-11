import requests 

def send_request(sat_num):
    url = 'https://data.ivanstanojevic.me/api/tle/{}'.format(sat_num)
    print('requesting data from: {}'.format(url))
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux armv6l) AppleWebKit/537.36 (KHTML, like Gecko) Raspbian Chromium/78.0.3904.108 Chrome/78.0.3904.108 Safari/537.36'}
    
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print('successfully retrived TLE for {}'.format(sat_num))
    else:
        print('Error: received {} status code'.format(r.status_code))
        return None
    return r.json()

def get_tle_dict(sat_num):
    res = send_request(sat_num)
    return res

