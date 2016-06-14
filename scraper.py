"""A scraper to identify shared voice actors/actresses in myanimelist."""

from lxml import html
import requests
import sys


# """ Takes as input a page, and outputs a list of (actor, character). """
# def getChars(tree):
#     char_list = tree.xpath('//td/a[contains(@href, "/character/")]')
#     chars = [s.text for s in char_list]
#     return chars

def getLanguage(actor_html):
   return actor_html.getparent().getchildren()[2].text

""" Gets the list of Japanese actors from a page."""
def getJActorsHtml(page):
    tree = html.fromstring(page.text)
    eng_and_jap_actors_html = tree.xpath('//td/a[contains(@href, "/people/")]')
    return [e for e in eng_and_jap_actors_html if getLanguage(e) == 'Japanese']

""" Gets the character HTML from an actor HTML."""
def getChar(actor_html):
    common_root_html = actor_html
    for i in range(5):
        common_root_html = common_root_html.getparent()
    return common_root_html.getchildren()[1].getchildren()[0]

# output: actor : [chars played by actor]
# adds to an existing acmap
def ActorCharMap(page, acmap, title):
    tree = html.fromstring(page.text)
    for actor_html in getJActorsHtml(page):
        name = actor_html.text
        char = getChar(actor_html).text
        if name not in acmap:
            acmap[name] = {title: [char]}
        elif title not in acmap[name]:
            acmap[name][title] = [char]
        else:
            acmap[name][title].append(char)

# output: {actor : { title : characters played in title}}
def ActorCharacterMap(pages, anime_titles):
  acmap = {}
  for i in xrange(len(pages)):
    title = anime_titles[i]
    page = pages[i]
    ActorCharMap(page, acmap, title)
  return acmap

# counts the number of keys in a map
def numKeys(m):
    keyCount = 0
    for key in m:
        keyCount += 1
    return keyCount

# removes keys in a map whos value is a map with <= 1 key.
def pruneMap(mapOfMaps):
    pruned_map = {}
    for key in mapOfMaps:
        if numKeys(mapOfMaps[key]) > 1:
            pruned_map[key] = mapOfMaps[key]
    return pruned_map

# Some formatting on the output.
def PrintMap(m):
  for i in m:
    PrintMap2(m[i])
    print "Voiced By: (", i, ")"
    print ""

def PrintMap2(m):
    for i in m:
        print m[i], " : ", i

# Helper function to get the anime title from the list of URLs.
def getAnimeName(a_url):
  last_slash = a_url.rfind('/')
  second_last_slash = a_url.rfind('/',0, last_slash)
  return a_url[second_last_slash+1:last_slash][0:5]

def print_usage_and_exit():
  print '''Usage: python {prog} [anime url] [anime url] [anime url] ...

Example: python {prog} http://myanimelist.net/anime/10165/Nichijou http://myanimelist.net/anime/10620/Mirai_Nikki_(TV) http://myanimelist.net/anime/26165/Yuri_Kuma_Arashi'''.format(prog=sys.argv[0])
  sys.exit(1)

def main():
  if len(sys.argv) <= 1:
    print_usage_and_exit()

  anime_urls = sys.argv[1:]
  print anime_urls
  character_urls = [url + '/characters' for url in anime_urls]
  pages = [requests.get(url) for url in character_urls]
  anime_titles = [getAnimeName(url) for url in character_urls]

  prunedMap = pruneMap(ActorCharacterMap(pages, anime_titles))
  PrintMap(prunedMap)

if __name__ == '__main__':
  main()
