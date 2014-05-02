from django.db import models
from django.contrib.auth.models import User  #django default userclass
#from jsonfield import JSONField
#from picklefield.fields import PickledObjectField
#from taggit.managers import TaggableManager

# Job Choices
JOB_CHOICES = (
#http://pluralsight.com/training/Player?author=reindertjan-ekker&name=django-fundamentals-m4-models&mode=live&clip=0&course=django-fundamentals
('Executive Assistant to CEO','Executive Assistant to CEO'),
('Accounting and Audit Clerk',' Accounting and Audit Clerk'),
('Convention and Event Planner',' Convention and Event Planner'),
('Accountant','Accountant'),
('Administrative Assistant','Administrative Assistant'),
('Architect','Architect'),
('Art Director','Art Director'),
('Auto Mechanic','Auto Mechanic'),
('Bill Collector','Bill Collector'),
('Bookkeeping','Bookkeeping'),
('Business Operations Manager','Business Operations Manager'),
('Civil Engineer','Civil Engineer'),
('Clinical Laboratory Technician','Clinical Laboratory Technician'),
('Clinical Social Worker','Clinical Social Worker'),
('Compliance Officer','Compliance Officer'),
('Computer Programmer','Computer Programmer'),
('Computer Support Specialist','Computer Support Specialist'),
('Computer Systems Administrator','Computer Systems Administrator'),
('Computer Systems Analyst','Computer Systems Analyst'),
('Construction Manager','Construction Manager'),
('Cost Estimator','Cost Estimator'),
('Customer Service Representative','Customer Service Representative'),
('Database Administrator','Database Administrator'),
('Dental Assistant','Dental Assistant'),
('Dental Hygienist','Dental Hygienist'),
('Dentist','Dentist'),
('Diagnostic Medical Sonographer','Diagnostic Medical Sonographer'),
('Dietitian and Nutritionist','Dietitian and Nutritionist'),
('Elementary School Teacher','Elementary School Teacher'),
('Epidemiologist','Epidemiologist'),
('Esthetician','Esthetician'),
('Exterminator','Exterminator'),
('Financial Advisor','Financial Advisor'),
('Financial Analyst','Financial Analyst'),
('Financial Manager','Financial Manager'),
('Glazier','Glazier'),
('Hairdresser','Hairdresser'),
('High School Teacher','High School Teacher'),
('Home Health Aide','Home Health Aide'),
('HR Specialist','HR Specialist'),
('Information Security Analyst','Information Security Analyst'),
('Insurance Agent','Insurance Agent'),
('Interpreter & Translator','Interpreter & Translator'),
('Interpreter and Translator','Interpreter and Translator'),
('IT Manager','IT Manager'),
('Landscaper and Groundskeeper','Landscaper and Groundskeeper'),
('Lawyer','Lawyer'),
('Licensed Practical and Licensed Vocational Nurse','Licensed Practical and Licensed Vocational Nurse'),
('Logistician','Logistician'),
('Maintenance and Repair Worker','Maintenance and Repair Worker'),
('Management Analyst','Management Analyst'),
('Market Research Analyst','Market Research Analyst'),
('Marketing Manager','Marketing Manager'),
('Marriage and Family Therapist','Marriage and Family Therapist'),
('Massage Therapist','Massage Therapist'),
('Mechanical Engineer','Mechanical Engineer'),
('Medical Assistant','Medical Assistant'),
('Medical Equipment Repairer','Medical Equipment Repairer'),
('Medical Secretary','Medical Secretary'),
('Meeting','Meeting'),
('Mental Health Counselor','Mental Health Counselor'),
('Middle School Teacher','Middle School Teacher'),
('Nail Technician','Nail Technician'),
('Nurse Practitioner','Nurse Practitioner'),
('Nursing Aide','Nursing Aide'),
('Occupational Therapist','Occupational Therapist'),
('Occupational Therapy Assistant','Occupational Therapy Assistant'),
('Office Clerk','Office Clerk'),
('Operations Research Analyst','Operations Research Analyst'),
('Optician','Optician'),
('Painter','Painter'),
('Paralegal','Paralegal'),
('Paramedic','Paramedic'),
('Patrol Officer','Patrol Officer'),
('Personal Care Aide','Personal Care Aide'),
('Pharmacist','Pharmacist'),
('Pharmacy Technician','Pharmacy Technician'),
('Phlebotomist','Phlebotomist'),
('Physical Therapist Assistant','Physical Therapist Assistant'),
('Physical Therapist','Physical Therapist'),
('Physician Assistant','Physician Assistant'),
('Physician','Physician'),
('Plumber','Plumber'),
('Preschool Teacher','Preschool Teacher'),
('Public Relations Specialist','Public Relations Specialist'),
('Radiologic Technologist','Radiologic Technologist'),
('Real Estate Agent','Real Estate Agent'),
('Recreation and Fitness Worker','Recreation and Fitness Worker'),
('Registered Nurse','Registered Nurse'),
('Respiratory Therapist','Respiratory Therapist'),
('Sales Manager','Sales Manager'),
('Sales Representative','Sales Representative'),
('School Counselor','School Counselor'),
('School Psychologist','School Psychologist'),
('Software Developer','Software Developer'),
('Speech-Language Pathologist','Speech-Language Pathologist'),
('Structural Iron and Steelworker','Structural Iron and Steelworker'),
('Substance Abuse Counselor','Substance Abuse Counselor'),
('Surgical Technologist','Surgical Technologist'),
('Taxi Driver and Chauffeur','Taxi Driver and Chauffeur'),
('Veterinarian','Veterinarian'),
('Veterinary Technologist and Technician','Veterinary Technologist and Technician'),
('Web Developer','Web Developer')
)


class Post(models.Model):
        title = models.CharField(max_length = 100)
        body = models.TextField()
        created = models.DateTimeField()
        #tags = TaggableManager()

        def __unicode__(self):
            return self.title

class Best(models.Model):
        company_rank = models.IntegerField()
        company_name = models.CharField(max_length=100)
        abbreviation = models.CharField(max_length=50, null=True)

class Links(models.Model):
        job_name = models.CharField(max_length=200)
        job_url = models.CharField(max_length=200)

        def __unicode__(self):
            return self.job_name

class Search(models.Model):
	    from_user = models.ForeignKey(User)
	    job_searched = models.CharField(max_length=100, choices=JOB_CHOICES)
	    timestamp = models.DateTimeField(auto_now_add = True)

	#Need to add these later ------------
	#job_listed = JSONField()
	#job_searched = models.ForeignKey(Links)
	#http://stackoverflow.com/questions/6836740/django-admin-change-foreignkey-display-text

# -----  importing data -------
#http://stackoverflow.com/questions/4003034/execute-sql-script-to-create-tables-and-rows

#checking whats in DB
#mysql> SELECT DATABASE();   (Tables_in_db_name)
#mysql> SHOW TABLES;
#mysql> DESCRIBE pet;

# to import into SQL table you want to
   #  a create table
   #  create SQL script
   #  connect to SQL from bash (see here - "mysql -uUSERNAME -hmysql.server -p")
   #  use "source file.sql"

#----- pickling objects ------------

#... class SomeObject(models.Model):
#...     args = PickledObjectField()

#and assign whatever you like (as long as it's picklable) to the field:

# obj = SomeObject()
# obj.args = ['fancy', {'objects': 'inside'}]
# obj.save()

# serializing an object
# http://docs.python.org/2/library/pickle.html


#---------- migrating database ---------
# Note, syncDB does not do database migrations  - they are looking to add this in Django 1.7
# If you need to alter tables, use South
# or drop table  (python manage.py dbshell - to get shell)
# "drop table XX;"
# syncDB

#------- linked in ---------
# authentication - https://github.com/PrincessPolymath/django-linkedin-simple
# linked in API - https://github.com/ozgur/python-linkedin
    #http://nbviewer.ipython.org/github/ptwobrussell/Mining-the-Social-Web-2nd-Edition/blob/master/ipynb/Chapter%203%20-%20Mining%20LinkedIn.ipynb
    #https://developer.linkedin.com/thread/1902


# --- git ----
# to pull files down - https://github.com/ozgur/python-linkedin
# use git pull o master  (o is what you specified form /Metten  - master is the branch)
# change settings - http://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings