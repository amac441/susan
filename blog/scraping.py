#import statements
import urllib2  #maybe python3
from bs4 import BeautifulSoup
from threading import Lock
from datetime import datetime
import time
from models import Best
from django.conf import settings

path1 = settings.MEDIA_ROOT
filename2 = path1 + '/testing_it_up.txt'
file2 = open(filename2, 'w+')

#-----------scrape main page for resume links----------------

class Scraper:


    def __init__(self):
        self.data = []


    def test(self):
        return "hello"


    #----------  SALARY FINDER --------------
    def salary(self, job,city):

        # job must be 'business+analyst' string

        salary = "NA"

        if city == "NA":
            city = ""


        sal_url =  'http://www.indeed.com/salary?q1=' + job + '&l1=' + city + '&tm=1'
        #url = 'http://www.indeed.com/salary?q1=business+analyst&l1=omaha&tm=1'

        # ---- SAMPLE URLS -------
        # http://www.indeed.com/salary?q1=business+analyst&l1=omaha%2C+ne&tm=1
        # http://www.indeed.com/salary?q1=business+analyst&l1=68106&tm=1
        #url = 'http://www.espn.com'

        request = urllib2.Request(sal_url)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response)

        #for a_soup in soup.find_all('div', attrs={'class':'salary_display_table_wrapper'}):
        #use the above if you want salaries for 'similar jobs'

        for a_soup in soup.find_all('div', {'id':'salary_display'}):

            for b in a_soup.find_all('span', attrs={'class':'salary'}):
                salary = b.getText().encode('ascii', 'ignore')

        if salary == 'No Data ':
            salary = "NA"

        return salary


    #-------- GET DATES BETWEEN ---------

    def days_between(self, dates):

        date_list = dates.split(" to ",1)

        try:
            d1 = datetime.strptime(date_list[0], "%B %Y")

            if date_list[1] == "Present":
                date_list[1] = time.strftime("%B %Y")

            d2 = datetime.strptime(date_list[1], "%B %Y")

            diff = abs((d2 - d1).days)
        except:
            a = 1
            #print "not M Y"
            try:
                d1 = datetime.strptime(date_list[0], "%b %Y")

                if date_list[1] == "Present":
                    date_list[1] = time.strftime("%b %Y")

                d2 = datetime.strptime(date_list[1], "%b %Y")
                diff = abs((d2 - d1).days)
            except:
                a = 1
                #print "not m Y"
                try:
                    d1 = datetime.strptime(date_list[0], "%Y")

                    if date_list[1] == "Present":
                        date_list[1] = time.strftime("%Y")

                    d2 = datetime.strptime(date_list[1], "%Y")
                    diff = abs((d2 - d1).days)
                except:
                    #print "not Y"
                    d1 = date_list[0]
                    d2 = date_list[1]
                    diff = 365

        days = float(diff)
        duration = days/365
        return {'start':d1,'end':d2,'duration':duration}


    #---------BEST COMPANIES -------
    #---------NEED TO PUT THIS LOGIC IN THE MODEL---------

    def company_pres(self, name):

        company = Best.objects.filter(company_name__icontains=name)
        print(company)

        if company:
            company = company
        else:
            company = Best.objects.filter(abbreviation__icontains=name)
            print(company)

        #print company

        if company:
            company = int(company[0][0])
            if company < 2:
                 company_prestige = 1
            elif company < 20:
                company_prestige = 2
            elif company < 100:
                company_prestige = 1.8
            elif company < 300:
                company_prestige = 1.6
            elif company < 500:
                company_prestige = 1.5
            elif company < 1000:
                company_prestige = 1.3
        else:
            company_prestige = 1

        return company_prestige



    #-------- LINK FINDER ---------------



    def links(self,job,city,pages):

        resume_links = []

        for page in range(0,pages):
            #resume_url = 'http://www.indeed.com/resumes/' + job + '/in-' + city + '?co=US&start=' + str(page*10+1)
            # additional pages http://www.indeed.com/resumes/business-analyst/in-Omaha-NE?co=US&start=10
            #url = 'http://www.indeed.com/resumes/business-analyst/'
            url2 = 'http://www.indeed.com/resumes?q=title%3A(' + job + ')&co=US&start=' + str(page*10+1)

            request = urllib2.Request(url2)
            response = urllib2.urlopen(request)
            soup = BeautifulSoup(response)


            for a in soup.find_all('div', attrs={'class':'app_name'}):
                #print a
                for link in a.find_all('a'):
                    resume_links.append(link.get('href'))

        return resume_links


    #---------SCRAPE RESUMES--------------------

    def person(self, res, pers, file):

        file2.write("testing_it  person")
        title = []
        company = []
        location = []
        comp_prestige = []
        end_date = []
        duration = []
        avg_salary = []
        description = []
        wrk_desc = []
        person = pers
        sc = Scraper()

        resume_url = 'http://www.indeed.com' + res
        #resume_url2 = 'http://www.indeed.com/r/Tony-Heard/6da0be4fdb87cad6'
        resume_html = urllib2.urlopen(resume_url) #.read()
        soup = BeautifulSoup(resume_html)

        #------ GET JOB, COMPANY, DURATION, SALARY FOR ALL JOBS IN RESUME -----------
        #todo - need to get Education as well!

        for a_soup in soup.find_all('div', attrs={'class':'data_display'}):
            #print a_soup
            #a_soup = BeautifulSoup(a)

            for b in a_soup.find_all('p', attrs={'class':'work_title title'}):

                # --- job_title needed for salary -----
                job_title = b.getText().encode('ascii', 'ignore')
                title.append(job_title.replace("'",""))

                company_section = ""
                company_section = a_soup.find_all('div', attrs={'class':'work_company'})
                if company_section:
                    for company_section in a_soup.find_all('div', attrs={'class':'work_company'}):
                #comp_sect_text = company_section.getText()

                # == get job, company, and company prestige ===
                # Company is a list for that person
                # Comp_Prestige is prestige factor for each company
                # company_pres() is a function in BestCompanys

                        company_name = ""
                        company_name = company_section.find('span', attrs={'class':'bold'})
                        if company_name:
                            comp_name = company_name.getText().encode('ascii', 'ignore')
                            company.append(comp_name.replace("'",""))

                            # ---- company_pres calls database of fortune 1000 -----
                            try:
                                prestige = sc.company_pres(comp_name)
                                print "Prestige for " + res
                            except:
                                prestige = "1"

                            comp_prestige.append(prestige)

                        else:
                            company.append("NA")
                            comp_prestige.append("1")

                    #===== get job location ======
                        location_name = ""
                        location_name = company_section.find('div', attrs={'class':'inline-block'})
                        if location_name:
                            loca = location_name.getText().encode('ascii', 'ignore')
                            location.append(loca.replace("'",""))

                            #--- needed for salary ----
                            city = loca.split(",",1)[0]
                            a=1
                        else:
                            location.append("NA")
                            city = "NA"

                    #====== get dates ========
                        work_dates = ""
                        work_dates = a_soup.find('p', attrs={'class':'work_dates'})
                        if work_dates:
                            dates = work_dates.getText().encode('ascii', 'ignore')
                            dates_return = sc.days_between(dates)
                            end_date.append(dates_return['end'])
                            duration.append(dates_return['duration'])
                            print "workdates for " + res
                        else:
                            end_date.append('NA')
                            duration.append("1")

                    # ===== call to get location salary factor =======
                        avg_salary.append(sc.salary(job_title,city))



                    #====== get description ======
                        work_desc = ""
                        work_desc = a_soup.find('p', attrs={'class':'work_description'})
                        if work_desc:
                            desc = work_desc.getText().encode('ascii', 'ignore')
                            print desc
                            wrk_desc.append(desc)
                        else:
                            wrk_desc.append('N/A')


                    # ------ incase company section isnt in resume ----
                else:
                    end_date.append("NA")
                    duration.append("1")
                    location.append("NA")
                    avg_salary.append("NA")
                    company.append("NA")
                    comp_prestige.append("1")
                    wrk_desc.append('N/A')



        #--------------write to file------------------------
        lock = Lock()
        for i in range(0, len(title)):

            lock.acquire()
            try:
                stringer = str(person) + ';' + resume_url.replace("'","") + ';' +  str(i+1) + ';' +  title[i] + ';' +  company[i] + ';' + location[i] + ';' +  str(end_date[i]) + ';' +  str(duration[i]) + ';' + avg_salary[i] + ';' + str(comp_prestige[i]) + ';' + wrk_desc[i].replace(";",".") + '\n'
                #print stringer
                file.write(stringer)
                print "printed file for " + res
            finally:
                lock.release() # release lock, no matter what

        #return person




