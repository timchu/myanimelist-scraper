from lxml import html
import requests

# No error handling.

def getTopUrl(search_page):
    search_page_tree = html.fromstring(search_page.text)
    return search_page_tree.xpath('//div[@class="information di-tc va-t pt4 pl8"]')[0].getchildren()[0].attrib['href']

def getPageUrl(anime_name):
    search_term = anime_name.replace(" ", "+")
    search_url = "http://myanimelist.net/search/all?q=" + search_term
    search_page = requests.get(search_url)
    if search_page.status_code == 200:
        return getTopUrl(search_page)
    else: 
      print anime_name
      raise RuntimeError('MyAnimeList denied you from searching for the anime:' + anime_name)
