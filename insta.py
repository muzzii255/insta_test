import regex as re
import pandas as pd
import scraper_helper
import requests
import json
import random

proxy_ports = [1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023
               ]

def get_proxy():
    port = random.choice(proxy_ports)
    print(port)
    # PROXIES
    proxy = {
          'http': f'http://{port}',
          'https': f'http://{port}'
      }
    
    return proxy



def get_account(change=False):
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
    headers = scraper_helper.get_dict(headers,strip_cookie=False)
    
    if change:
        df = pd.read_csv('cookies.csv',names=['u','c'])
        rows = df.to_dict('records')
        new_account = rows[0]
        pd.DataFrame(rows[1:]).to_csv('cookies.csv',index=False,header=False)
        cookies = new_account['c']
        with open('cookies.txt','w') as f:
            f.write(cookies)
        f.close()
        headers['cookie'] = cookies
    else:
        with open('cookies.txt','r') as c:
            cookies = c.read()
        c.close()
        headers['cookie'] = cookies
    
    return headers
    
def get_followers(user_id):
    usernames = []
    headers = get_account()
    main_data = []    
    req = requests.get(f'https://www.instagram.com/api/v1/friendships/{user_id}/followers/?max_id=100&search_surface=follow_list_page',headers=headers)
    print(req.status_code,'page ',1)
    for row in req.json()['users']:
        # if row['latest_reel_media'] != 0:
        # print(row[''])
        data = {}
        data['username'] = row['username']
        data['userid'] = row['strong_id__']
        data['full_name'] = row['full_name']
        data['latest story'] = row['latest_reel_media']
        main_data.append(data)
    for x in range(100,1100,100):
        req = requests.get(f'https://www.instagram.com/api/v1/friendships/{user_id}/followers/?count={x}&max_id=100&search_surface=follow_list_page',headers=headers)
        print(req.status_code,'page ',x/100)
        for row in req.json()['users']:
            # if row['latest_reel_media'] != 0:
            if row['username'] in usernames:
                break
            else:
                data = {}
                data['username'] = row['username']
                data['userid'] = row['strong_id__']
                data['full_name'] = row['full_name']
                data['latest story'] = row['latest_reel_media']
                main_data.append(data)
                usernames.append(data['username'])
                
    return main_data

user_data = get_followers('18067386776')

with open('test.json','w',encoding='utf-8') as f:
    json.dump(user_data,f)
f.close()
        
