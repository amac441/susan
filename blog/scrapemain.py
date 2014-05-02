# READ THIS -- https://medium.com/cs-math/f29f6080c131

from threading import Thread
import urllib2  #maybe python3
from bs4 import BeautifulSoup
import time
from scraping import Scraper
from rcode import Rcode
from grapher import Graph
from django.conf import settings
from mechanize import Browser
from Metten.blog.models import Links
import os

class ScrapeMain:

    def __init__(self):
        self.data = []

#====== INPUTS =================
    def scrape_main(self, jb):

        #job = business-analyst
        #city = omaha-ne
        #local = raw_input("Local or Web (L/W): ")
        #job = raw_input("Job title with + as spaces: ")

        #-----need a method to scrub job title --------

        job = jb.split()
        local = "W"
        #city = ""
        #pages = 1
        path1 = settings.MEDIA_ROOT
        #path1 = ''
        path2 = '/jobs_' + jb.replace(" ","_")
        path3 = '.txt'
        filename = path1 + path2 + path3

        #===== CHECK IF FILE EXISTS ========

        if os.path.exists(filename):
            filename = filename
        else:
            #===== CREATE FILE IF IT DOESNT EXISTS ========

            file = open(filename, 'w+')
            header = 'Res' + ';' + "URL" + ';' +  "Job_num" + ';' +  "Job_Title" + ';' +  "Company" + ';' + "Location" + ';' +  "End_Date" + ';' +  "Duration" + ';' + "Avg_Sal" + ';' + "Company_Prestige" + ';' + "Work_Description" + '\n'
            file.write(header)


            #===== GRAB LIST OF RESUMES FOR INPUTS ABOVE ======

            # if job[1]:
            #     file.write(job[0] + "---" + job[(len(job)-1)] + jb )
            #     resume_links = Links.objects.filter(job_name__icontains=job[1])  #.filter(job_name__contains=job[1])
            #     file.write(resume_links[0])
            # else:
            #file.write('hello')

            resume_links = Links.objects.filter(job_name__icontains=jb.replace(" ","-"))

            #file.write(resume_links)
            #======= GRAB SPECIFIC RESUME BY HYPERLINK AND SCRAPE DATA ============

            pers = 0
            threadlist = []
            s2 = Scraper()

            for res in resume_links:
                print 'Resume' + res.job_url
                pers = pers + 1

        #---------- THREADING CODE -----------------
            # --- so that we dont kick off more than 10 threads ------
                if pers % 10 == 0:
                    time.sleep(1)

                try:
                    t = Thread(target=s2.person, args=(res.job_url,pers,file))
                    t.start()
                    threadlist.append(t)

                except:
                    time.sleep(1)
                    try:
                        t = Thread(target=s2.person, args=(res.job_url,pers,file))
                        t.start()
                        threadlist.append(t)
                    except:
                        print "this person didnt work"

            # -- rejoining the threads -----

            for b in threadlist:
                b.join()

            file.close()

        #-------- DO PLOTTING -----------

        job_cluster = []

        if local == "L":
            print "local"
            #plots(filename)  -  ADD FOR LOCAL  - https://bitbucket.org/njs/rnumpy/wiki/API
        elif local == "W":
            r = Rcode()
            r_data = r.rots(filename, jb)
            med = r_data['median']
            for i in range(1,(med+2)):
                print "-----------JOB " + str(i) + " ----------------"
                plots = r_data['plot_files'][i-1]
                #plot_listing.append(plots)
                job_list = []
                for j in range(1,4):
                    print '--cluster '+ str(j) + "--"
                    job = r_data['jobz'][(i*j)-1]
                    job1 = tuple(job)
                    title = job1[3][0]
                    company = job1[4][0]
                    sal = job1[8][0]
                    #{'title' 'company''sal'}
                    tup = [title, company, sal, plots]
                    job_list.append(tup)

                job_cluster.append(job_list)


        return {'stat':"done", 'jobs_cluster':job_cluster, 'med':range((med+2))}
    # when doing multithreading you need to define a function and give seperate memory allocation for each thread


#sc = ScrapeMain()
#sc.scrape_main('architect')