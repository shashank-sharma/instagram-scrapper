# coding: utf-8
'''

Instagram scraper

It scrapes user profile to get all images from it

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
    # For saving your login session
    import Cookie
    import cookielib
    import mechanize
    import time
    import os
    import sys
    # To get script and manipulate it
    import json
    # To get password in much secured way
    from getpass import getpass
    from bs4 import BeautifulSoup
    # To save images locally
    from urllib import urlretrieve
    print bcolors.OKGREEN+'Import: OK'+bcolors.ENDC
except:
    print bcolors.FAIL+'Import: FAILED'+bcolors.ENDC
time.sleep(1)


def tags_scrape():
    # To scrape given tag and download all images from it

    start = 0
    name = 0
    print 'Enter the tag name you wish to download',
    tag = raw_input()
    print bcolors.WARNING+'Getting data related tag'+bcolors.ENDC
    try:
        br.open('https://www.instagram.com/explore/tags/'+tag)
        soup = BeautifulSoup(br.response().read())
        print bcolors.OKGREEN+'Data: OK'.bcolors.ENDC
    except:
        zz = 0
        while True:
            try:
                br.open('https://www.instagram.com/explore/tags/'+tag)
                soup = BeautifulSoup(br.response().read())
                print bcolors.OKGREEN+'Data: OK'+bcolors.ENDC
                break
            except:
                zz+=1

    # To get particular script so that we can get all image/media link.
    # Currently it supports image download not videos
    try:
        ss = 0
        l = soup.find_all('script')
        for i in l:
            if i.text[:18] == 'window._sharedData':
                break
            else:
                ss+=1
        l= soup.find_all('script')[ss].text
    except:
        print soup.find_all('script')

    jsonValue = '{%s}' % (l.split('{', 1)[1].rsplit('}', 1)[0],)
    value = json.loads(jsonValue)
    print 'Want to download [H]D images or [N]ormal'
    choice = raw_input()
    if choice == 'n' or choice == 'N':
        quality = 'thumbnail_src'
    else:
        quality = 'display_src'
    print bcolors.BOLD+bcolors.WARNING+'\n\n[INSTAGRAM]: Getting data '+bcolors.ENDC

    load = 0
    while True:
        # Get data and represent it in list
        data = value['entry_data']['TagPage'][0]['tag']['media']['nodes']
        count = len(data)
        print bcolors.WARNING+str(count)+' images'+bcolors.ENDC
        page = value['entry_data']['TagPage'][0]['tag']['media']['page_info']['has_next_page']
        for i in xrange(len(data)):
            sys.stdout.write('\r')
            sys.stdout.write("[%-50s] %.2f%%" % ('='*(int(load)/2), load))
            sys.stdout.flush()
            link = str(data[i][quality])
            try:
                # This is where images get downloaded
                urlretrieve(link, str(name+1)+'.jpg')
            except:
                if '.jpg' not in link:
                    print 'Not a jpg file - Testing'    # Testing case to test if there comes any error or not
                    break
                else:
                    z = 1
                    if z%3==0:
                        print 'Trying again after '+str(60*(z/3))+' seconds'   # Need to remove this but it is for testing
                        time.sleep(60*(z/3))
                    while True:
                        try:
                            urlretrieve(link, user_id+str(i+1)+'.jpg')
                            break
                        except:
                            z+=1
            start+=1
            name+=1
            load = ((start+1)/float(count))*100
        if not page:
            print bcolors.OKGREEN+'\n\nStatus: Completed'+bcolors.ENDC
            break
        else:
            print '\n'
            start = 0
            load = 0
            ss = 0
            next = str(value['entry_data']['TagPage'][0]['tag']['media']['page_info']['end_cursor'])
            br.open('https://www.instagram.com/explore/tags/'+tag+'/?max_id='+next)
            try:
                soup = BeautifulSoup(br.response().read())
            except:
                x = 0
                while True:
                    try:
                        soup = BeautifulSoup(br.response().read())
                        break                    
                    except:
                        if x == 3:
                            break
                        x+=1
            try:
                l = soup.find_all('script')
                for i in l:
                    if i.text[:18] == 'window._sharedData':
                        break
                    else:
                        ss+=1
                l= soup.find_all('script')[ss].text
                jsonValue = '{%s}' % (l.split('{', 1)[1].rsplit('}', 1)[0],)
                value = json.loads(jsonValue)
            except:
                print soup.find_all('script') # To analyze the error as if why it is breaking



def profile_scrape():
    # Use to scrape given profile user and get all images from it

    start = 0
    print 'Enter user name to scrape: ',
    # username not email id
    user = raw_input()
    print bcolors.WARNING+'Checking availability'+bcolors.ENDC
    try:
        br.open('https://www.instagram.com/'+user)
        soup = BeautifulSoup(br.response().read())
        print bcolors.OKGREEN+'Data: OK'.bcolors.ENDC
    except:
        zz = 0
        while True:
            try:
                br.open('https://www.instagram.com/'+user)
                soup = BeautifulSoup(br.response().read())
                print bcolors.OKGREEN+'Data: OK'+bcolors.ENDC
                break
            except:
                zz+=1
    if 'This Account is Private' in str(soup):
        print bcolors.FAIL+'ACCOUNT: PRIVATE'+bcolors.ENDC
        return ''
    else:
        print bcolors.OKGREEN+'ACCOUNT: PUBLIC'+bcolors.ENDC

    # To get particular script so that we can get all image/media link.
    # Currently it supports image download not videos
    try:
        ss = 0
        l = soup.find_all('script')
        for i in l:
            if i.text[:18] == 'window._sharedData':
                break
            else:
                ss+=1
        l= soup.find_all('script')[ss].text
    except:
        print soup.find_all('script')

    # To get script and convert it into json object which helps to get data
    jsonValue = '{%s}' % (l.split('{', 1)[1].rsplit('}', 1)[0],)
    value = json.loads(jsonValue)
    # Total count of images/media inside
    count = value['entry_data']['ProfilePage'][0]['user']['media']['count']
    # User id
    user_id = str(value['entry_data']['ProfilePage'][ 0 ]['user']['username'])

    print bcolors.OKGREEN+'Total count '+str(count)+bcolors.ENDC
    print 'Want to download [H]D images or [N]ormal'
    choice = raw_input()
    if choice == 'n' or choice == 'N':
        quality = 'thumbnail_src'
    else:
        quality = 'display_src'
    print bcolors.BOLD+bcolors.WARNING+'\n\n[INSTAGRAM]: Getting data '+bcolors.ENDC

    load = 0
    while True:
        # Get data and represent it in list
        data = value['entry_data']['ProfilePage'][0]['user']['media']['nodes']
        page = value['entry_data']['ProfilePage'][0]['user']['media']['page_info']['has_next_page']
        for i in xrange(len(data)):
            sys.stdout.write('\r')
            sys.stdout.write("[%-50s] %.2f%%" % ('='*(int(load)/2), load))
            sys.stdout.flush()
            link = str(data[i][quality])
            try:
                # This is where images get downloaded
                urlretrieve(link, user_id+str(start+1)+'.jpg')
            except:
                if '.jpg' not in link:
                    print 'Not a jpg file - Testing'    # Testing case to test if there comes any error or not
                    break
                else:
                    z = 0
                    if z%3==0:
                        print 'Trying again after '+str(60*(z/3))+' seconds'   # Need to remove this but it is for testing
                        time.sleep(60*(z/3))
                    while True:
                        try:
                            urlretrieve(link, user_id+str(i+1)+'.jpg')
                            break
                        except:
                            z+=1
            start+=1
            load = ((start+1)/float(count))*100
        if not page:
            print bcolors.OKGREEN+'\n\nStatus: Completed'+bcolors.ENDC
            break
        else:
            ss = 0
            next = str(value['entry_data']['ProfilePage'][0]['user']['media']['nodes'][len(data)-1]['id'])
            br.open('https://www.instagram.com/'+user+'?&max_id='+next)
            try:
                soup = BeautifulSoup(br.response().read())
            except:
                x = 0
                while True:
                    try:
                        soup = BeautifulSoup(br.response().read())
                        break                    
                    except:
                        if x == 3:
                            break
                        x+=1
            try:
                l = soup.find_all('script')
                for i in l:
                    if i.text[:18] == 'window._sharedData':
                        break
                    else:
                        ss+=1
                l= soup.find_all('script')[ss].text
                jsonValue = '{%s}' % (l.split('{', 1)[1].rsplit('}', 1)[0],)
                value = json.loads(jsonValue)
            except:
                print soup.find_all('script') # To analyze the error as if why it is breaking





def insta_scrape(soup):
    #print ' | ',
    l= soup.find_all('script')[6].text #18 for user
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


'''

Below code is used to login into instagram account and save cookies.

NOTE: COOKIES WILL BE SAVED IN YOUR LOCAL STORAGE SO MAKE SURE YOU TAKE EXTRA CARE
ELSE ANYONE CAN ACCESS YOUR ACCOUNT BY THAT.

'''


print bcolors.WARNING+bcolors.BOLD+'\n\nDo you wish to log in ? [Y]es or [N]o'+bcolors.ENDC
print bcolors.WARNING+'Note: Log in may give access to some selected profile which you are following.'
print bcolors.WARNING+'>>>'+bcolors.ENDC
lo = raw_input()
if lo == 'y' or 'Y':
    flag = 0
else:
    flag = 1

if os.path.isfile('./.cookies.txt') and flag == 0:
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

elif flag == 0:
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

if 'case-sensitive' in str(soup) and flag == 0:
    print bcolors.FAIL+'Log in: Failed'+bcolors.ENDC
else:
    if flag == 0:
        print bcolors.OKGREEN+bcolors.BOLD+'Log in: Accepted'+bcolors.ENDC
    time.sleep(2)
    print bcolors.WARNING+'Welcome to Instagram scraper\nCurrently you can scrape:\n1. Home page of your instagram\n2. Any particular profile (all images)'+bcolors.ENDC,
    print bcolors.WARNING+'\n3. Download images from tags'
    while True:
        time.sleep(1)
        print('Type your choice [1], [2] or [3]')
        check = raw_input()
        if check == '2':
            profile_scrape()
        elif check == '1':
            insta_scrape()
        elif check == '0':
            exit()
        elif check == '3':
            tags_scrape()
        else:
            print 'Type [0] to quit'
