import sys
from bs4 import BeautifulSoup
from requests import session


if len(sys.argv) is not 4:
  print("nh-fave-dl username password last_page_of_favorites_to_download")
  sys.exit(0)


get_url = 'https://nhentai.net/login/'
login_url = 'https://nhentai.net/login/'
fave_url = 'https://nhentai.net/favorites/?page={}'
download_url = 'https://nhentai.net/g/{}/download'
fave_page = sys.argv[3]
path = './downloads/{}.torrent'
payload = {
  'username_or_email': sys.argv[1],
  'password': sys.argv[2],
}

with session() as c:
  #get csrf token
  resp = c.get(get_url)
  html = BeautifulSoup(resp.content, "html.parser")
  payload['csrfmiddlewaretoken'] = html.find('input', {'name':'csrfmiddlewaretoken'})['value']
  #login
  resp = c.post(login_url, data=payload, headers=dict(Referer=login_url))
  #get all favorites 
  fave_ids = []
  while (fave_page > 0):
    resp = c.get(fave_url.format(fave_page))

    html = BeautifulSoup(resp.content, "html.parser")
    faves = html.find_all('div', {'class':'gallery-favorite'})
    fave_ids.extend([f['data-id'] for f in faves])
    fave_page -= 1
  #download faves
  for i in fave_ids:
    resp = c.get(download_url.format(i))

    with open(path.format(i), 'wb') as fd:
      for chunk in resp.iter_content(chunk_size=128):
        fd.write(chunk)

  # print(fave_ids)