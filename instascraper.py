import regex as re
import pandas as pd
import scraper_helper
import requests
import json
import random
def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
proxy_ports = [1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023
               ]
def get_proxy():
    port = random.choice(proxy_ports)
    print(port)
    proxy = {
        'http': f'http://s67:BKKproxies874529@bkk-project.cyberalps.com:{port}',
        'https': f'http://s67:BKKproxies874529@bkk-project.cyberalps.com:{port}'
    }
    return proxy
headers = """accept: */*
accept-encoding: gzip, deflate, br
accept-language: en-GB,en;q=0.9
sec-ch-prefers-color-scheme: dark
sec-ch-ua: "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
viewport-width: 1119
x-ig-app-id: 936619743392459
x-ig-www-claim: 0
x-requested-with: XMLHttpRequest"""
headers = scraper_helper.get_dict(headers)

def profile_scraper(user):
    print(user)
    while True:
        try:
            req = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user}',headers=headers,proxies=get_proxy(),verify=False)
            print(req.status_code)
            if req.status_code == 200:
                js = json.loads(req.text)
                if js['data']['user']:
                    b = js['data']['user']['biography']
                    b = re.finditer(r'(https?://\S+)',str(b))
                    websites = [x.group() for x in b]
                    try:
                        b = re.finditer(r'(https?://\S+)',str(js['data']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['edge_media_to_caption']['edges'][0]['node']['text']))
                        websites.extend([x.group() for x in b])
                    except:
                        pass
                        
                    all_locs = [x for x in js['data']['user']['edge_owner_to_timeline_media']['edges'] if x['node']['location'] and ',' in x['node']['location']['name']]
                    data = {}
                    data['username'] = user
                    data['userid'] = js['data']['user']['id']
                    data['fbid'] = js['data']['user']['fbid']
                    data['full_name'] = js['data']['user']['full_name']
                    data['id'] = js['data']['user']['id']
                    data['biography'] = js['data']['user']['biography']
                    data['stories'] = js['data']['user']['highlight_reel_count']
                    data['business_category_name'] = js['data']['user']['business_category_name']
                    data['followers'] = js['data']['user']['edge_followed_by']['count']
                    data['follows'] = js['data']['user']['edge_follow']['count']
                    data['full_name'] = js['data']['user']['full_name']
                    data['is_private'] = js['data']['user']['is_private']
                    data['is_verified'] = js['data']['user']['is_verified']
                    data['posts'] = js['data']['user']['edge_owner_to_timeline_media']['count']
                    data['email'] = ','.join(scraper_helper.extract_emails(js['data']['user']['biography']))
                    data['website'] = websites
                    try:data['location'] = all_locs[0]['node']['location']['name']
                    except:data['location'] = None
                    return data
                else:
                    return None
            break
        except Exception as e:
            print(e)
            pass
        
        