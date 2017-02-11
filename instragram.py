# coding: utf-8
'''

Instagram scraper

'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    import Cookie
    import cookielib
    import mechanize
    import time
    import os
    import sys
    import pprint
    import json
    from getpass import getpass
    from bs4 import BeautifulSoup
    import urllib
    import urllib2
    import requests
    from urllib import urlretrieve
    print bcolors.OKGREEN+'Import: OK'+bcolors.ENDC
except:
    print bcolors.FAIL+'Import: FAILED'+bcolors.ENDC
time.sleep(1)


'''

Below code is used to login into instagram account and save cookies.

NOTE: COOKIES WILL BE SAVED IN YOUR LOCAL STORAGE SO MAKE SURE YOU TAKE EXTRA CARE
ELSE ANYONE CAN ACCESS YOUR ACCOUNT BY THAT.

'''
print 'Currently it scrapes the homepage of Instagram'
def insta_scrape(soup):
    #print ' | ',
    l= soup.find_all('script')[6].text
    jsonValue = '{%s}' % (l.split('{', 1)[1].rsplit('}', 1)[0],)
    value = json.loads(jsonValue)
    length = len(value['entry_data']['FeedPage'][0]['feed']['media']['nodes'])
    s = 0
    for i in xrange(length):
        sys.stdout.write('\r')
        sys.stdout.write("[%-50s] %d%%" % ('='*(int(s)/2), s))
        sys.stdout.flush()
        #sys.stdout.write("█")
        #sys.stdout.flush()
        try:
            download_link = str(value['entry_data']['FeedPage'][0]['feed']['media']['nodes'][i]['display_src'])
        except:
            z = 0
            while True:
                if z == 3:
                    print 'Failed'
                    break
                try:
                    download_link = str(value['entry_data']['FeedPage'][0]['feed']['media']['nodes'][i]['display_src'])
                except:
                    print 'Failing ...'
                z+=1

        s = ((i+2)/float(length))*100
        #user = str(value['entry_data']['FeedPage'][0]['feed']['media']['nodes'][0]['owner']['username'])
        urlretrieve(download_link, str(i+1)+'.jpg')
        #sys.stdout.write("\r" + '| '+ str(((i+1)/length)*100)+'%')



if os.path.isfile('./.cookies.txt'):
    print bcolors.OKGREEN+'Compiled: Successfully'+bcolors.ENDC
    time.sleep(1)
    print bcolors.OKGREEN+'Cookies: FOUND'+bcolors.ENDC
    time.sleep(1)
    try:
        br = mechanize.Browser()
        print bcolors.OKGREEN+'Mechanize Browser: OK'+bcolors.ENDC
    except:
        print bcolors.FAIL+'Browser Setting: FAILED'+bcolors.ENDC
    time.sleep(1)
    cookiejar =cookielib.LWPCookieJar()
    br.set_cookiejar(cookiejar)
    cookiejar.load('.cookies.txt', ignore_discard=True, ignore_expires=True)
    br.set_handle_robots(False)
    print bcolors.OKGREEN+'Robots settings: OK'+bcolors.ENDC
    print bcolors.OKGREEN+'\nStatus: ACCESS GRANTED'+bcolors.ENDC
    try:
        br.open('http://instagram.com/')
        print bcolors.OKGREEN+'Connection: OK'+bcolors.ENDC
    except:
        cou = 0
        print bcolors.FAIL+'Connection: Not Connected'+bcolors.ENDC
        while True:
            print bcolors.WARNING+'Trying again: '+str(cou+1)+'/3'+bcolors.ENDC
            try:
                br.open('http://instagram.com/')
                print bcolors.OKGREEN+'Connection: OK'+bcolors.ENDC
                break
            except:
                cou+=1
            if cou >= 3:
                print bcolors.FAIL+'Failed Quitting'+bcolors.ENDC
                failno = 1
                break
    soup = BeautifulSoup(br.response().read())

else:
    cookiejar =cookielib.LWPCookieJar('.cookies.txt')
    print bcolors.OKGREEN+'Compiled: Successfully'+bcolors.ENDC
    print bcolors.OKGREEN+'Cookies.txt: NOT FOUND'+bcolors.ENDC
    time.sleep(1)
    try:
        br = mechanize.Browser()
        print bcolors.OKGREEN+'Mechanize Browser: OK'+bcolors.ENDC
    except:
        print bcolors.FAIL+'Browser Setting: FAILED'+bcolors.ENDC
        failno = 1
    time.sleep(1)
    try:
        br.set_cookiejar(cookiejar)
        print bcolors.OKGREEN+'Browser cookies: OK'+bcolors.ENDC
    except:
        print bcolors.FAIL+'Browser cookies: FAILED'+bcolors.ENDC
        failno = 1
    time.sleep(1)
    # Robots is not false
    #br.set_handle_robots(False)
    print bcolors.OKGREEN+'Robots settings: OK'+bcolors.ENDC
    failno = 0
    try:
        br.open('https://www.instagram.com/accounts/login/?force_classic_login')
        print bcolors.OKGREEN+'Connection: OK'+bcolors.ENDC
    except:
        cou = 0
        print bcolors.FAIL+'Connection: Not Connected'+bcolors.ENDC
        while True:
            print bcolors.WARNING+'Trying again: '+str(cou+1)+'/3'+bcolors.ENDC
            try:
                br.open('https://www.instagram.com/accounts/login/?force_classic_login')
                print bcolors.OKGREEN+'Connection: OK'+bcolors.ENDC
                break
            except:
                cou+=1
            if cou >= 3:
                print bcolors.FAIL+'Failed Quitting'+bcolors.ENDC
                failno = 1
                break
    if failno == 0:
        br._factory.is_html = True
        try:
            br.select_form(nr = 0)
            print bcolors.OKGREEN+'Form selected: OK'+bcolors.ENDC
        except:
            print bcolors.FAIL+'Form selected: FAILED'+bcolors.ENDC
        print bcolors.BOLD + "Email:" + bcolors.ENDC,
        email = raw_input()
        br['username'] = 'shashank.py'
        passw = getpass()
        print bcolors.OKBLUE+'\nSubmitting:'+ bcolors.ENDC,
        br['password'] = passw
        try:
            br.submit()
            print bcolors.OKGREEN+'OK'+bcolors.ENDC
        except:
            cou = 0
            print bcolors.FAIL+'FAILED'+bcolors.ENDC
            while True:
                print bcolors.WARNING+'Trying again: '+str(cou+1)+'/3'+bcolors.ENDC
                try:
                    br.submit()
                    print bcolors.OKGREEN+'OK'+bcolors.ENDC
                except:
                    cou += 1
                if cou>= 3:
                    print bcolors.FAIL+'Failed Quitting'+bcolors.ENDC
                    failno = 1
                    break

        cookiejar.save()
        soup = BeautifulSoup(br.response().read())

if 'case-sensitive' in str(soup):
    print bcolors.FAIL+'Log in: Failed'+bcolors.ENDC
else:
    print bcolors.OKGREEN+bcolors.BOLD+'Log in: Accepted'+bcolors.ENDC
    print bcolors.OKGREEN+'Mythical Bot is ready'+bcolors.ENDC
    check = raw_input('Press Enter to continue')
    insta_scrape(soup)