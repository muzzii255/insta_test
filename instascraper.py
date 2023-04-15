import regex as re
import pandas as pd
import scraper_helper
import requests
import json
import random
import logging
import warnings
import time

warnings.simplefilter('ignore')
log_level = logging.INFO
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m-%d-%Y %H:%M:%S',
                    filename='InstaLogs.logs',
                    level=log_level
                    )


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


proxies = [
    'http://baysocial1:69np2nxxm7jb@73.127.11.222:1001',
    'http://baysocial1:69np2nxxm7jb@73.127.11.222:1004',
    'http://baysocial1:69np2nxxm7jb@73.127.11.222:1005',
    'http://baysocial1:69np2nxxm7jb@73.127.11.222:1008',
    'http://proxy:doctor@pxdr.io:56246',
    'http://proxy:doctor@pxdr.io:31696',
    'http://proxy:doctor@pxdr.io:36788',
    'http://proxy:doctor@pxdr.io:41081',
    'http://proxy:doctor@pxdr.io:21515',
    'http://proxy:doctor@pxdr.io:29231',
    'http://proxy:doctor@pxdr.io:28389',
    'http://proxy:doctor@pxdr.io:22364',
    'http://proxy:doctor@pxdr.io:53412',
    'http://proxy:doctor@pxdr.io:38964',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1009',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1011',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1012',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1013',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1004',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1005',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1002',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1003',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1006',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1007',
    'http://francepr:FranceProxies273819@france-proxies.cyberalps.com:1015',
    'http://dimi27:dimi27@polproxiesgdansk.cyberalps.com:1041',
]
def get_proxy():
    port = random.choice(proxies)
    proxy = {
        'http': port,
        'https': port
    }
    return proxy


headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)"
    }
sess = requests.Session()

def profile_scraper(user):
    username = user.split(':')[0]
    proxy = get_proxy()
    try:
        a = time.perf_counter()
        req = sess.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}',headers=headers,proxies=proxy,verify=False)
        b = time.perf_counter()
        print(req.status_code, user,proxy,b-a)
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
                data['user'] = user
                data['username'] = username
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
                data['profile_picture'] = js['data']['user']['profile_pic_url_hd']
                data['posts'] = js['data']['user']['edge_owner_to_timeline_media']['count']
                data['email'] = ','.join(scraper_helper.extract_emails(js['data']['user']['biography']))
                data['website'] = ','.join(websites)
                try:data['location'] = all_locs[0]['node']['location']['name']
                except:data['location'] = None
                return data
                # pd.DataFrame(data,index=[0]).to_csv('instadata_new.csv',index=False,mode='a',header=False)
            
            else:
                # print(req.text)
                return {'error': '404 error, Profile Doesnt Exists'}
            
    except Exception as e:
        # print(e)
        return {'error': str(e)}


            