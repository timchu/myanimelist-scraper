"""A scraper to identify shared voice actors/actresses in myanimelist."""

import utils
import scraper as s
import sys

def printUsageAndExit():
  print '''Usage: python {prog} [anime url] [anime url] [anime url] ...

Example: python {prog} 'shingeki' 'gurren' 'FMA brotherhood' '''.format(prog=sys.argv[0])
  sys.exit(1)
def main():
  if len(sys.argv) <= 1:
    printUsageAndExit()

  animes = sys.argv[1:]
  anime_urls = [utils.getPageUrl(anime) for anime in animes]
  s.scrape(anime_urls)

if __name__ == '__main__':
  main()
