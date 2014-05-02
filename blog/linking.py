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


def __init__(self):
    self.data = []

def get_json(url):
    return loads(r.get(url).content)


def flatten(lst):
    return [item for sublist in lst for item in sublist]


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


class ItunesU(object):
    URL = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch?term=%s&media=iTunesU&entity=podcast'

    @staticmethod
    def get_results(job_title):
        url = ItunesU.URL % quote(job_title)
        json = get_json(url)
        results = [row for row in json['results']]
        return results


class ItunesPodcasts(object):
    URL = 'https://itunes.apple.com/search?term=%s&entity=podcast'

    @staticmethod
    def get_results(job_title):
        url = ItunesPodcasts.URL % quote(job_title)
        json = get_json(url)
        result = [row for row in json['results']]
        return result


class Coursera(object):
    URL = 'https://api.coursera.org/api/catalog.v1/courses?q=search&query=%s&includes=sessions'
    SESSION_URL = 'https://api.coursera.org/api/catalog.v1/sessions?ids=%s&fields=startYear,startMonth,startDay,name,durationString'

    @staticmethod
    def get_results(job_title):
        searched_items = get_json(Coursera.URL % quote(job_title))['elements']
        results = []
        for item in searched_items:
            session_ids = [session_id for session_id in item['links']['sessions']]
            url = Coursera.SESSION_URL % (','.join(map(str, session_ids)))
            sessions_json = get_json(url)['elements']
            for session_json in sessions_json:
                try:
                    course_date = datetime(int(session_json['startYear']), int(session_json['startMonth']),
                                           int(session_json['startDay']))
                except KeyError:
                    course_date = datetime(10, 1, 1, 1, 1, 1)  #some rows don't specify dates, ignore those
                if datetime.today() < course_date:
                    results.append({'title': item['name'], 'length': session_json['durationString'],
                                    'course_page': session_json['homeLink'],
                                    'date': course_date})
        return results


class LinkedIn(object):
    API_KEY = '75i3mk2maw6ogl'
    SECRET_KEY = 'MDasUmDtjPbYa1I9'
    USER_TOKEN = '6b759135-60ec-4885-81e3-8bc025ac3591'
    USER_SECRET = '344b6e0c-0a22-4896-baaa-9457ffdb621c'
    RETURN_URL = ''

    @staticmethod
    def get_results(job_title, zip_code, country_code):
        authentication = linkedin.LinkedInDeveloperAuthentication(LinkedIn.API_KEY, LinkedIn.SECRET_KEY,
                                                                  LinkedIn.USER_TOKEN, LinkedIn.USER_SECRET,
                                                                  LinkedIn.RETURN_URL,
                                                                  linkedin.PERMISSIONS.enums.values())
        application = linkedin.LinkedInApplication(authentication)
        selectors = [{'people': ['first-name', 'last-name', 'headline']}]
        params = {'keywords': job_title, 'postal-code': zip_code, 'country-code': country_code}
        results = application.search_profile(selectors=selectors, params=params)
        return results


class Amazon():
    ACCESS_KEY = 'AKIAIAW7JXESRBCM2BLA'
    SECRET_KEY = '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'
    ASSOCIATE_TAG = '4319-1549-2008'

    @staticmethod
    def get_results(job_title):
        api = amazonproduct.API(access_key_id=Amazon.ACCESS_KEY, secret_access_key=Amazon.SECRET_KEY,associate_tag=Amazon.ASSOCIATE_TAG, locale='us')
        items = api.item_search('Books', Keywords=job_title)
        results = []
        for item in items:
            try:
                tite = item.ItemAttributes.Title
                tite = "Book"
                book_info = {'author': item.ItemAttributes.Author, 'title': tite}
                results.append(book_info)
            #Some rows don't have the author or title attributes
            except AttributeError:
                pass
        return results


class Indeed():
    URL = 'http://api.indeed.com/ads/apisearch?publisher=9988125764049772&q=&l=austin%2C+tx&sort=&radius=&st=&jt=&start=&limit=&fromage=&filter=&latlong=1&co=us&chnl=&userip%20=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'

    @staticmethod
    def get_results(job_title):
        url = Indeed.URL.replace('&q=', '&q=' + quote(job_title))
        content = r.get(url).content
        result_dict = parse(content)
        jobs = result_dict['response']['results']['result'][:3]
        results = [{'title': job['jobtitle'], 'location': job['formattedLocationFull'], 'company': job['source']} for
                   job in jobs]
        return results


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
        dates = soup.find_all('td', attrs={'class': 'date'})[:3]
        titles = soup.find_all('a', attrs={'class': 'url summary'})[:3]
        descriptions = soup.find_all('blockquote', attrs={'class': 'description'})[:3]
        results = []
        for i in range(len(dates)):
            single_result = {'title': titles[i].get_text().encode('ascii', 'ignore'),
                             'descriptions': descriptions[i].get_text().encode('ascii', 'ignore'),
                             'date': dates[i].get_text().encode('ascii', 'ignore')}
            results.append(single_result)
        return results


class Meetup():
    API_KEY = '7369551518c62716596b04c10b57'
    TOPIC_URL = 'http://api.meetup.com/recommended/group_topics?text=%s&page=20&sign=true&key=%s'
    EVENTS_URL = 'https://api.meetup.com/2/open_events?&sign=true&topic=%s&page=20&radius=%s&zip=%s&key=%s'
    #GROUPS_URL = 'http://api.meetup.com/2/groups?zip=11211&topic=moms3&order=members4&key=ABDE12456AB23244455

    @staticmethod
    def get_topic(job_title):
        url = Meetup.TOPIC_URL % (quote(job_title), Meetup.API_KEY)
        json = get_json(url)
        try:
            return json[0]['urlkey']
        except IndexError:
            return ''

    #@staticmethod
    #def get_group(job_title):
    #    url = Meetup.GROUP_URL % (quote(job_title), Meetup.API_KEY)
    #    json = get_json(url)
    #    try:
    #        return json[0]['urlkey']
    #    except IndexError:
    #        return ''

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
            single_res = {'description': result['description'], 'title': result['name'],
                          'date': formatted_date, 'url': result['event_url']}
            results.append(single_res)
        return results


class Alltop(object):
    URL = 'http://database.alltop.com/'

    @staticmethod
    def get_results(*args):
        html = urllib2.urlopen(Alltop.URL)
        soup = BeautifulSoup(html)
        topular_ul = soup.find('ul', {'id': 'top-five'})
        results = []
        if len(topular_ul) > 0:
            #page has topular sites, for some topics it's empty
            for idx, entries in enumerate(topular_ul.find_all('a')):
                en = entries.get_text().encode('ascii', 'ignore')
                hr = entries.get('href')
                results.append({
                    'title': en,
                    'url': hr
                })
        return results


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
            if self.site != Meetup:
                site_result = self.site.get_results(self.job_title)
            else:
                site_result = self.site.get_results(self.job_title, self.radius, self.zip_code)
            queue.put((self.site_name, site_result))

        except:
            #In case opf rare errors, ignore site and return empty list
            queue.put((self.site_name, []))


class LinkingIn():
    def scrape_jobs(self, keyword):
        return Onet.get_jobs(keyword)


    def scrape_sites(self, job_title, radius, zip_code):
        sites = [
            ('UNL', UNL), ('Amazon', Amazon), ('Alltop', Alltop),
            ('Meetup', Meetup), ('Indeed', Indeed), ('Coursera', Coursera),
            ('ItunesU', ItunesU)]
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


# job_title = "science workshop"
# radius = 50
# zip_code = 68106
# l = LinkingIn()
# a = l.scrape_sites(job_title, radius, zip_code)
# print a
