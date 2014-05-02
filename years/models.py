from django.db import models
import re
from gooser import Gooser
from calendar import timegm
from datetime import timedelta


# ---- ADMIN STUFF -------


# ---- USER STUFF ----------

# - extending the profile  - http://www.turnkeylinux.org/blog/django-profile

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    max_items_per_week = models.IntegerField(blank=True)
    zip_code = models.IntegerField(blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# --- later you can add custom city model field ---

# from models import City
# import strings
# from registration.forms import RegistrationForm

# class UserRegistrationForm(RegistrationForm):
#     city = forms.ModelChoiceField(queryset=City.objects, label=strings.city, empty_label=strings.notDefined)

# ---- TASK ADDITIONS ---------

CONTENT_CHOICES = (
    ('Article', 'Article'),
    ('Podcast', 'Podcast'),
    ('Course', 'Course'),
    ('Meeting', 'Meeting')
                   )

class AddersManager(models.Manager):
    def items_for_user(self, user):
        return super(AddersManager, self).get_queryset().filter(
            Q(user_id=user.id))

    def new_adder(self, user, title, description):
        adder = Adder(user = user,
                      title = title,
                      description = description
                      )
        return adder

class Adder(models.Model):
    user = models.ForeignKey('auth.User', related_name='adder')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text=(
        "If omitted, the description will be the post's title."))
    is_completed = models.BooleanField(default=True, blank=True)
    content_type = models.CharField(max_length=10, default='Article', choices = CONTENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    #start_date = models.DateTimeField()
    #end_date = models.DateTimeField()
    url = models.CharField(max_length=200)
    is_scheduled = models.BooleanField(default=True, blank=False)

    objects = AddersManager()

    class Meta:
        get_latest_by = 'timestamp'
        unique_together = ["title", "date", "url", "content_type"]

    #python manage.py sql appname
    #python manage.py syndb  - doesnt do DB migration
        #it will not alter tables  - in Django 1.7 they will have migrations

    #python manage.py dbshell
        #drop table posts_adder
        #exit
        #then run syncdb again

    def __str__(self):
        return "{0}".format(self.title)


    def start(self):
        d = timegm(self.date.utctimetuple())*1000
        return d

    def end(self):
        #eventually delta will be "Length" of the course
        ender = self.date + timedelta(0,3600)
        d = timegm(ender.utctimetuple())*1000
        return d

    def item_in(self,data,user):

        query = Adder.objects.create(
            user = user,
            title = data.get('title'),
            description = data.get('desc'),
            is_completed = False,
            date = data.get('date'),
            url = data.get('url'),
            #start_date = data.get('start_date'),
            #end_date = data.get('end_date'),
            content_type = data.get('content_type')
            )
        #query.save()
        return query.id
        #need to add something here about deleting if "unique" peice fails


    def email_in(self, data, user):

        g = Gooser()

        #---parse data---

        sender    = data.get('sender')
        recipient = data.get('recipient')
        subject   = data.get('subject', '')
        body_plain = data.get('body-plain', '')


        #---perform logic---

        # bounce sender address off users table to find match (later)
        user_email = user

        # check recipient

        if recipient == 'loggit@mettentot.com':

        # check if article was read
            if subject == 'done':
                is_comp_email = True
            elif subject == 'later':
                is_comp_email = False
            else:
                return 'Bad Subject'

        # check if the description is a website

            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body_plain)

            if len(urls) > 1:
            #do something  - like call the GOOSE and SAVE methods twice for each thing
                a = 1

                #query = Adder.objects.create(user = user_email,
                #title=title_email,
                #description = des_email,
                #is_completed = is_comp_email
                #)

               #query.save()

            else:
            #call goose

                response = g.goosing(str(urls[0]))
                title_email = response['title']
                des_email = response['text']


            #save it
                query = Adder.objects.create(user = user_email,
                          title=title_email,
                          description = des_email,
                          is_completed = is_comp_email
                          )
               #query.save()

        else:
            return 'Bad Recipient'

        return 'OK'

