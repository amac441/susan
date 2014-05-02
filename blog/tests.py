"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from Metten.blog.models import Links

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


            #===== GRAB LIST OF RESUMES FOR INPUTS ABOVE ======

    def testing():
        job = ['a','b']
        jb = 'cat'
        if job[1]:
            print "hello"
            resume_links = Links.objects.filter(job_name__icontains=job[1])  #.filter(job_name__contains=job[1])
            print resume_links
        else:
            print "hell no"
            resume_links = Links.objects.filter(job_name__icontains=jb)