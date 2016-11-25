import json
import re
import urllib
from models import *
def get_username(userid, session):
 	user_url = 'https://www.instagram.com/p/USER-ID/?taken-at=215822965'
	link = user_url.replace('USER-ID', userid)
	username = ''
	userpage = session.get(link)
	gr = re.findall('<script type="text/javascript">(.*)</script>', userpage.text)
	js = ''
	for item in gr:
	    if 'window._sharedData' in item:
	        js = re.sub("window._sharedData[ ]+=[ ]+","",item)
	js = json.loads(urllib.unquote(js.strip(';')))

	for item in js['entry_data']['PostPage']:
	        username = item['media']['owner']['username']
	return username

def scrape_users(session):
	users = []
	location_url = 'https://www.instagram.com/explore/locations/215822965/cambridge-massachusetts'
	location_response = session.get(location_url)
	gr = re.findall('<script type="text/javascript">(.*)</script>', location_response.text)
	for item in gr:
		if 'window._sharedData' in item:
			js = re.sub("window._sharedData[ ]+=[ ]+","",item)
	js = json.loads(urllib.unquote(js.strip(';')))

	for feed in js['entry_data']['LocationsPage']:
	    has_next_page = feed['location']['media']['page_info']['has_next_page']
	    end_cursor = feed['location']['media']['page_info']['end_cursor']   
	    for item in feed['location']['media']['nodes']:
	    	username = get_username(item['code'], session)
	    	user = User(id=item['code'], username=username)
	    	user.save()