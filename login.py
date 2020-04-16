import requests
from bs4 import BeautifulSoup

import config

site = config.amazon_login_url

'''initiate session'''
session = requests.Session()

'''define session headers'''
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,en;q=0.5',
    'Referer': site
}

resp = session.get(site)
html = resp.text

form = BeautifulSoup(html, 'html.parser').find('form', {'name': 'signIn'})
data = {field.get('name'): field.get('value') for field in form.find_all('input')}

data[u'email'] = config.amazon_login_user
data[u'password'] = config.amazon_login_pass

post_resp = session.post(site, data = data)

post_soup = BeautifulSoup(post_resp.content , 'html.parser')

with open(f'responses/login_response.html', 'w') as file:
    file.write(post_resp.text)

if post_soup.find_all('title')[0].text == 'Your Account':
    print('Login Successfull')
else:
    print('Login Failed')

session.close()