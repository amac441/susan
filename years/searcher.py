from __future__ import division
from datetime import datetime
from urllib import quote
from json import loads
from threading import Thread, RLock
from Queue import Queue
import requests as r
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import urllib2  #maybe python3
from xmltodict import parse
from linkedin import linkedin
import amazonproduct


#site   title   desc    url author  location    length  date
#alltop title   need desc   url TBD N/A length? need date?
#amazon title   need desc   need url    author  N/A length? pub date?
#coursera   title   need desc   url (change name)   N/A N/A length  date
#indeed title   need desc   need url    company(change) location(change)    sal(as length)  N/A
#itunes change(trackName)   change(genres)  change (trackViewUrl)   change(collectionName)      TBD change(release-date)
#linkedin   change(name)    change(??)  url N/A change(location)    sal(as length)  TBD
#meetup title   description url N/A change(location)    need end time   date
#unl    title   change(descriptions)    need url    N/A change(location)    need end time   date (and time)



def __init__(self):
    self.data = []

def get_json(url):
    return loads(r.get(url).content)


def flatten(lst):
    return [item for sublist in lst for item in sublist]


# --------- ALL TOP --------------------------


class Alltop(object):
    # need to add code to determine which URL to hit.
    URL = 'http://database.alltop.com/'
    #URL = newFunction(object):

    @staticmethod
    def get_results(*args):
        html = urllib2.urlopen(Alltop.URL)
        soup = BeautifulSoup(html)
        topular_ul = soup.find('ul', {'id': 'top-five'})
        results = []
        if len(topular_ul) > 0:
            #page has topular sites, for some topics it's empty
            for idx, entries in enumerate(topular_ul.find_all('li', {'class':  'hentry'})):
                a = entries.find('a')
                en = a.get_text().encode('ascii', 'ignore')
                hr = a.get('href')
            for entry in entries.find_all('div', {'class':  'full-post'}):
                site = entry.find('div', {'class':  'site-title'}).get_text().encode('ascii', 'ignore')
                date = entry.find('div', {'class':  'published'}).get_text().encode('ascii', 'ignore')
                desc = entry.find('div', {'class':  'entry-bound'}).get_text().encode('ascii', 'ignore')
                results.append({
                    'title': en,
                    'url': hr,
                    'desc': desc,
                    'date':'',  #took out date
                    'content_type':'Article',
                    'author': site,
                    'id': '',
                })
        return results


# --------- AMAZON -----------------------------

class Amazon():


    @staticmethod
    def get_results(job_title):

        config = {
        'access_key' : 'AKIAIAW7JXESRBCM2BLA',
        'secret_key' : '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',
        'associate_tag' : '4319-1549-2008',
        'locale' : 'us'
        }
        api = amazonproduct.API(cfg=config)
        #amazonproduct.API(access_key_id=Amazon.ACCESS_KEY, secret_access_key=Amazon.SECRET_KEY,associate_tag=Amazon.ASSOCIATE_TAG, locale='us')
        items = api.item_search('Books', Keywords=job_title)
        results = []

        #price = api.item_lookup('B00008OE6I', ResponseGroup='OfferFull', Condition='All')

        for x, item in enumerate(items):
            #try:

            try:
                ansi = str(item.ASIN)
                offer = api.item_lookup(ansi, ResponseGroup='OfferFull', Condition='All')
                price = str(offer.Items.Item.Offers.Offer.OfferListing.Price.FormattedPrice)
                a=1
            except:
                price = "Price Unkown"

                title = str(item.ItemAttributes.Title)
                author = str(item.ItemAttributes.Author)
                url = str(item.DetailPageURL)

                results.append({
                             'author': author,
                             'title': title,
                             'url': url,
                             'description':price,
                             'id': '',
                             'content_type':'Article',
                             }
                )
            if x == 5:
                break

            #For Price:
            #<Items>
            #...
            #<Item>
            #...
            #<Offers>
            #    ...
            #    <Offer>
            #        ...
            #        <OfferListing>

            #Some rows don't have the author or title attributes
            #except AttributeError:
            #    pass
        return results

# ------- COURSERA --------------------------------

class Coursera(object):
    URL = 'https://api.coursera.org/api/catalog.v1/courses?q=search&query=%s&includes=sessions'
    SESSION_URL = 'https://api.coursera.org/api/catalog.v1/sessions?ids=%s&fields=startYear,startMonth,startDay,name,durationString,shortDescription'

    @staticmethod
    def get_results(job_title):
        searched_items = get_json(Coursera.URL % quote(job_title))['elements']
        results = []
        for item in searched_items:
            session_ids = [session_id for session_id in item['links']['sessions']]
            session_id = session_ids[0]
            session_id = str(session_id)
            url = Coursera.SESSION_URL % (''.join(session_id))
            sessions_json = get_json(url)['elements']
            for session_json in sessions_json:
                try:
                    course_date = datetime(int(session_json['startYear']), int(session_json['startMonth']),
                                           int(session_json['startDay']))
                except KeyError:
                    course_date = datetime(10, 1, 1, 1, 1, 1)  #some rows don't specify dates, ignore those
                #if datetime.today() < course_date:
                if datetime.today() < course_date:
                    start_date = course_date
                else:
                    start_date = ''
                results.append({'title': item['name'],
                                'length': session_json['durationString'],
                                'url': session_json['homeLink'],
                                'date': course_date,
                                'start_date':start_date,
                                'description': str(session_ids),
                                'content_type':'Course',
                                'id': ''
                                                               })     #'desc':session_json['shortDescription']

        return results


# -------- INDEED ------------------------------------
# -------- NEED TO PULL THIS AND THE ODESK THING OUT ---------

class Indeed():
    URL = 'http://api.indeed.com/ads/apisearch?publisher=9988125764049772&q=&l=austin%2C+tx&sort=&radius=&st=&jt=&start=&limit=&fromage=&filter=&latlong=1&co=us&chnl=&userip%20=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'

    @staticmethod
    def get_results(job_title):
        url = Indeed.URL.replace('&q=', '&q=' + quote(job_title))
        content = r.get(url).content
        result_dict = parse(content)
        jobs = result_dict['response']['results']['result'][:3]
        results = [{'title': job['jobtitle'],
                    'location': job['formattedLocationFull'],
                    'author': job['source'],
                    'url':job['url'],
                    'desc':job['snippet'],
                    'date':job['date'],
                    'content_type':'Meeting',
                    'id':''}
                    for job in jobs]
        return results


# -------- ITUNES --------------------------------

class ItunesU(object):
    URL = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch?term=%s&media=iTunesU&entity=podcast'

    @staticmethod
    def get_results(job_title):
        url = ItunesU.URL % quote(job_title)
        json = get_json(url)
        results = []
        for row in json['results'][0:5]:
            results.append({'title': row['trackName'],
                            'desc':row['genres'],
                            'url':row['trackViewUrl'],
                            'author': row['collectionName'],
                            'date': row['releaseDate'],
                            'content_type':'Podcast',
                            'id':'' } )

        return results


#class ItunesPodcasts(object):
#    URL = 'https://itunes.apple.com/search?term=%s&entity=podcast'

#    @staticmethod
#    def get_results(job_title):
#        results = []
#        url = ItunesPodcasts.URL % quote(job_title)
#        results.append({'title': item['trackName'], 'desc':session_json['genres'], 'url':session_json['trackViewUrl'],
#                        'author': session_json['collectionName'], 'length': session_json['durationString'],
#                        'date': session_json['releaseDate'] } )

#        return results

# -------- LINKEDIN --------------------------------

class LinkedInner(object):

    @staticmethod
    def get_results(job_title, zip_code):

        API_KEY = '75i3mk2maw6ogl'
        SECRET_KEY = 'MDasUmDtjPbYa1I9'
        USER_TOKEN = '8faba2a7-e3a6-4727-b06b-a291ebbf8032'
        USER_SECRET = '99fde265-7fd3-4d53-8eb8-d0f6f979388c'
        RETURN_URL = ''

        authentication = linkedin.LinkedInDeveloperAuthentication(API_KEY, SECRET_KEY,
                                                                    USER_TOKEN, USER_SECRET,
                                                                    RETURN_URL,
                                                                    linkedin.PERMISSIONS.enums.values())


        application = linkedin.LinkedInApplication(authentication)
        selectors = [{'people': ['first-name', 'last-name', 'headline', 'picture-url', 'public-profile-url']}]
        params = {'keywords': job_title, 'postal-code': zip_code, 'country-code': 'us'}
        linked = application.search_profile(selectors=selectors, params=params)

        links = linked['people']['values']

        results = []
        #application = linkedin.LinkedInApplication(authentication)
        #results = application.search_profile(selectors=[{'people': ['first-name', 'last-name', 'headline']}], params={'keywords': job_title})
        #res = application.search_profile(selectors=[{'people': ['first-name', 'last-name']}], params={'keywords': 'Analyst'})
        #print linkedin.LinkedInApplication.search_profile.url
        #results = application.search_job(selectors=[{'jobs': ['id', 'customer-job-code', 'posting-date']}], params={'title': 'python', 'count': 2})

        for link in links:
            try:
                results.append({

                    'title' : link['firstName'] + " " + link['lastName'],
                    'desc' : link['headline'],
                    'image' : link['pictureUrl'],
                    'url' : link['publicProfileUrl'],
                    'content_type':'Meeting',
                    'id': ''
                        })
            except:
                 a=1
        return results


# ---------- MEETUP -------------------

class Meetup():
    API_KEY = '7369551518c62716596b04c10b57'
    TOPIC_URL = 'http://api.meetup.com/recommended/group_topics?text=%s&page=20&sign=true&key=%s'
    EVENTS_URL = 'https://api.meetup.com/2/open_events?&sign=true&topic=%s&page=20&radius=%s&zip=%s&key=%s'
    GROUPS_URL = 'http://api.meetup.com/2/groups?zip=11211&topic=moms3&order=members4&key=ABDE12456AB23244455'

    GROUPS = 'http://api.meetup.com/find/groups?zip=%s&text=%s&radius=%s&key=%s'


    @staticmethod
    # JUST GETS YOU A LIST OF TOPICS.  SENDS THAT TOPIC TO THE EVENT SEARCH
    def get_topic(job_title):
        url = Meetup.TOPIC_URL % (quote(job_title), Meetup.API_KEY)
        json = get_json(url)
        try:
            return json[0]['urlkey']
        except IndexError:
            return ''

    #NEED THIS SEARCH TO BE VERRY 'FUZZY'  - TRY THIS OUT!

    @staticmethod
    def get_group(job_title):
        url = Meetup.GROUP_URL % (quote(job_title), Meetup.API_KEY)
        json = get_json(url)
        try:
            return json[0]['urlkey']
        except IndexError:
            return ''

    @staticmethod
    def get_results(job_title, radius, zip_code):
        keywords = job_title.split(' ')
        radiuses = [radius for k in keywords]
        zip_codes = [zip_code for k in keywords]
        result = map(Meetup.get_single_event, keywords, radiuses, zip_codes)
        return flatten(result)

    @staticmethod
    def get_single_event(split_job_title, radius, zip_code):
        topic = Meetup.get_topic(split_job_title)
        url = Meetup.EVENTS_URL % (topic, radius, zip_code, Meetup.API_KEY)
        json = get_json(url)
        results = []
        for result in json['results']:
            cleaned_epoch = (result['time'] + result['utc_offset']) / 1000
            formatted_date = datetime.utcfromtimestamp(cleaned_epoch)

            try:
                if result['venue']:
                    venue = result['venue']
                else:
                    venue = ""
                if result['group']:
                    group = result['group']
                else:
                    group = ""

                single_res = {'description': result['description'],
                              'title': result['name'],
                              'date': formatted_date,
                              'url': result['event_url'],
                              'location':venue['city'],
                              'author':group['name'],
                              'content_type':'Meeting',
                              'id': ''
                              }
                results.append(single_res)
            except:
                 a = 1

    #    return results

    #@staticmethod
    #def get_group_event(split_job_title, radius, zip_code):

        url2 = Meetup.GROUPS % (zip_code, topic, radius, Meetup.API_KEY)
        json2 = get_json(url2)
        results = []
        for res in json2:
            group = res['category']

            try:
                single_res = res['next_event']

                time = single_res['time']
                cleaned_epoch = (time - 18000000) / 1000
                dat = datetime.utcfromtimestamp(cleaned_epoch)

                rezults = {
                'date' : dat,
                'location' : res['city'],
                'desc' : res['description'],
                'url' : res['link'],
                'author' : res['name'],
                'title' : single_res['name'],
                #'start_date': dat,
                #'end_date': end,
                'content_type':'Meeting',
                'id': ''
                }

                results.append(rezults)
            except:
                a=1

        return results


# --------- ONET ------------------------------------

class Onet(object):
    URL = 'http://services.onetcenter.org/ws/mnm/search?keyword=%s'

    @staticmethod
    def get_jobs(keyword):
        xml_result = r.get(Onet.URL % quote(keyword), auth=HTTPBasicAuth('metro_community', 'jnf8739')).content
        doc = parse(xml_result)
        try:
            careers = doc['careers']['career']
            if isinstance(careers, dict):
                #the job is an exact match, example keyword - lumberjack
                return [dict(title=careers['title'])]
            else:
                results = [
                    dict(title=career['title'])
                    for career in careers]
        except KeyError:
            results = []
        return results

# ----------- UNL -------------------------------------

class UNL():
    URL = 'https://events.unl.edu/search/?q=%s&submit=Search&search=search'

    @staticmethod
    def get_results(job_title):
        keywords = job_title.split(' ')
        result = map(UNL.get_single_result, keywords)
        return flatten(result)

    @staticmethod
    def get_single_result(keyword):
        url = UNL.URL % quote(keyword)
        content = r.get(url).content
        soup = BeautifulSoup(content)
        dates = soup.find_all('td', attrs={'class': 'date'})[:5]
        titles = soup.find_all('a', attrs={'class': 'url summary'})[:5]
        descriptions = soup.find_all('blockquote', attrs={'class': 'description'})[:5]
        locations = soup.find_all('span', attrs={'class':'location'})[:5]
        results = []
        for i in range(len(dates)):
            single_result = {'title': titles[i].get_text().encode('ascii', 'ignore'),
                             'desc': descriptions[i].get_text().encode('ascii', 'ignore'),
                             'date': dates[i].get_text().encode('ascii', 'ignore'),
                             'location': locations[i].get_text().encode('ascii','ignore'),
                             'content_type':'Meeting',
                             'id': ''
                             }
            results.append(single_result)
        return results



# ------ GENERAL SCRAPER CLASS -----------------------


queue = Queue()
lock = RLock()
result = {}


class ScraperThread(Thread):
    def __init__(self, site_name, site, job_title, radius, zip_code):
        Thread.__init__(self)
        self.site = site
        self.job_title = job_title
        self.site_name = site_name
        self.radius = radius
        self.zip_code = zip_code

    def run(self):
        try:
            if self.site_name == "LinkedIn":
                site_result = self.site.get_results(self.job_title, self.zip_code)
            elif (self.site != Meetup):
                site_result = self.site.get_results(self.job_title)
            else:
                site_result = self.site.get_results(self.job_title, self.radius, self.zip_code)
            queue.put((self.site_name, site_result))

        except:
            #In case opf rare errors, ignore site and return empty list
            queue.put((self.site_name, []))



class SearchClass():
    """description of class"""
    def __init__(self, *args, **kw):
        pass

    def scrape_jobs(self, keyword):
        return Onet.get_jobs(keyword)


    def scrape_sites(self, siter, job_title, radius, zip_code):

        result = {}

        # sites = {'UNL': ['UNL', UNL], 'Amazon':['Amazon', Amazon], 'Alltop':['Alltop', Alltop],
        #     'Meetup':['Meetup', Meetup], 'Coursera':['Coursera', Coursera],
        #     'ItunesU':['ItunesU', ItunesU], 'LinkedIn':['LinkedIn', LinkedInner]}

        sites = [
        ('UNL', UNL), ('Amazon', Amazon), ('Alltop', Alltop),
        ('Meetup', Meetup), ('Coursera', Coursera),
        ('ItunesU', ItunesU), ('LinkedIn', LinkedInner)
        ]

        #'Indeed':['Indeed', Indeed],

        # site_name = sites[siter][0]
        # site = sites[siter][1]


        threads = []


        for site_name, site in sites:
            t = ScraperThread(site_name, site, job_title, radius, zip_code)
            t.start()
            with lock:
                threads.append(t)

        for thread in threads:
            thread.join()
            with lock:
                site_name, site_result = queue.get()
                result[site_name] = site_result
        return result



        #def scrape_sites(self, siter, job_title, radius, zip_code):
        #sites = {'unl': ['UNL', UNL], 'amazon':['Amazon', Amazon], 'alltop':['Alltop', Alltop],
        #    'meeetup':['Meetup', Meetup], 'indeed':['Indeed', Indeed], 'coursera':['Coursera', Coursera],
        #    'itunes':['ItunesU', ItunesU], 'linked':['LinkedIn', LinkedIn]}

        #site_name = sites[siter][0]
        #site = sites[siter][1]

        #site_result = ScraperThread(site_name, site, job_title, radius, zip_code)

        #result[site_name] = site_result
        #return result


# job_title = "science workshop"
# radius = 50
# zip_code = 68106
# l = LinkingIn()
# a = l.scrape_sites(job_title, radius, zip_code)
# print a
