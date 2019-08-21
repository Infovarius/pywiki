import pywikibot
from pywikibot import pagegenerators as pg
import requests

prop2delete='P4828'

query='select ?item where {?item wdt:%s ?iets}' % prop2delete

def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass
x=0
for item in wd_sparql_query(query):
  claim=item.claims[prop2delete][0]
  item.removeClaims(claim,summary='https://www.wikidata.org/w/index.php?title=Wikidata:Bot_requests&oldid=997885832')
  x=x+1
  y= (12-x)
