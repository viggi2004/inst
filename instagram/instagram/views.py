import bs4
from scrapkit.browser import Browser, Session
import re
from django.conf.urls import url
import operator
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .Exceptions import *
from selenium import webdriver
import urllib
import json
from selenium.webdriver.common.keys import Keys
urlpatterns = []
def request_map(name, url_pattern):
    print name, ':  ', url_pattern

    def url_router(func):
        urlpatterns.append(url(str(url_pattern), func, name=name))
        return func

    return url_router


@request_map('home', r'^$')
def home(request):
    browser = Browser()
    #url = 'https://www.instagram.com'
    #loginUrl = 'https://www.instagram.com/accounts/login/ajax/'
    location_url = 'https://www.instagram.com/explore/locations/215822965/cambridge-massachusetts'
    session = Session()
    html = session.get(location_url)
    #re.findall('<script type="text/javascript">(.*)</script>', html.text)
    js = ''
    #re.search('(?<=name\':\')[a-z]*', a)
    #gr=re.search('(?<=viewport_width": ")([a-zA-Z0-9]*)', html.text)
    gr = re.findall('<script type="text/javascript">(.*)</script>', html.text)
    for item in gr:
        if 'window._sharedData' in item:
            js = re.sub("window._sharedData[ ]+=[ ]+","",item)
    userids = []
    js = json.loads(urllib.unquote(js.strip(';')))
    for feed in js['entry_data']['LocationsPage']:
        for item in feed['location']['media']['nodes']:
            print userids.append(item['code'])

    print userids

    user_url = 'https://www.instagram.com/p/USER-ID/?taken-at=215822965'
    for userid in userids:
        link = user_url.replace('USER-ID', userid)
        userpage = session.get(link)
        gr = re.findall('<script type="text/javascript">(.*)</script>', userpage.text)
        js = ''
        for item in gr:
            if 'window._sharedData' in item:
                js = re.sub("window._sharedData[ ]+=[ ]+","",item)
        js = json.loads(urllib.unquote(js.strip(';')))

        for item in js['entry_data']['PostPage']:
            print item['media']['owner']['username']

    #vw = gr.group(1)
    # gr=re.search('(?<=pixel_ratio": ")([a-zA-Z0-9]*)', html.text)
    # pr = gr.group(1)
    #print vw
    ##if csrf_token is None:
    #    raise CsrfNotFoundException
    #print csrf_token
    #for key, val in html.cookies.items():
    #    session.cookies[key] = val
    #session.cookies['ig_pr']='2.0'
    #session.cookies['ig_vw']='360'

    #print session.cookies
    #login_payload = {
    #     'username': 'balavigneshshanmugam',
    #     'password': '*********'
    # }
    # headers = {
    #     'content-type':'application/x-www-form-urlencoded',
    #     'origin':'https://www.instagram.com',
    #     'pragma':'no-cache',
    #     'referer':'https://www.instagram.com/',
    #     'x-instagram-ajax':'1',
    #     'x-requested-with':'XMLHttpRequest',
    #     'x-csrftoken': session.cookies['csrftoken']
    # }
    #print html.text
    # if session.cookies['sessionid'] is None:
    #     response = session.post(loginUrl, data=login_payload, headers=headers)
    #     print response.request.headers
    #     print response.status_code
    #     print response.cookies
    # response = session.get(url)
    return HttpResponse('success')

@request_map('scrape',r'scrape$')
def scrape(request):
    url = 'https://www.instagram.com/explore/locations/215822965/cambridge-massachusetts/'
    driver = webdriver.PhantomJS()

    driver.get(url)
    content = driver.find_element_by_css_selector('body')
    #------fetch all links
    top_posts = content.find_elements_by_css_selector('._myci9')
    for elem in top_posts:
        links = elem.find_elements_by_tag_name('a')
        for link in links:
            href = link.get_attribute('href')
            driver = webdriver.PhantomJS()
            driver.get(href)
            popup_page = driver.find_element_by_css_selector('._ook48')
            print popup_page.text

    #------fetch one link
    # top_post = content.find_element_by_css_selector('._myci9')
    # link = top_post.find_element_by_tag_name('a')
    # href = link.get_attribute('href')
    # page = driver.get(href)
    # popup_page = driver.find_element_by_css_selector('._ook48')
    # print popup_page.text
    # driver.quit()

    #print popup_page.get_attribute('innerHTML')
    #name_a = name_div.find_element_by_tag_name('a')
    #print name_a.text
    #print top_posts.get_attribute('innerHTML')
    #html = content.get_attribute('innerHTML')


    #print content.text
    #browser = Browser()
    #html = browser.get(url)
    return HttpResponse('success')