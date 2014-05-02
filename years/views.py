# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from searcher import SearchClass
from django.http import HttpResponse
from django.conf import settings
from Metten.years.models import Adder
from Metten.years.serializers import AdderSerializer


#@api_view(['GET', 'POST'])

def home(request, template_name="indexer.html"):
    """
    A index view.
    """
    return render_to_response(template_name,
                              context_instance=RequestContext(request))


class SearchRest(APIView):
    def get(self, request, job, *args, **kw):
        search_data = str(job)

        if search_data:
            myClass = SearchClass()
            result = myClass.scrape_jobs(search_data, *args, **kw)
            response = Response(result, status=status.HTTP_200_OK, content_type='json')
        else:
           response = Response(status = status.HTTP_404_NOT_FOUND)

        return response

class SearchStay(APIView):
    def get(self, request, job, site, *args, **kw):
        search_data = str(job)
        site = str(site)

        if search_data:
            myClass = SearchClass()
            result = myClass.scrape_sites(site, search_data, 50, 68106 *args, **kw)
            response = Response(result, status=status.HTTP_200_OK, content_type='json')
        else:
           response = Response(status = status.HTTP_404_NOT_FOUND)

        return response

# Receives Email from MailGun
#http://www.mettentot.com/years/api/messages/
class EmailIn(APIView):
    def post(self, request):

         a = Adder()
         user = request.user

         if request.method == 'POST':

             #request.POST = data
             data = {
             'sender' : 'bob@mettentot.com',
             'recipient' : 'loggit@mettentot.com',
             'subject' : 'done',
             'body-plain' : 'http://www.businessinsider.com/inside-story-of-clinkle-2014-4'
             }

             response = a.email_in(data, user)

             #------ THIS BREAK OUT WILL GO IN THE MODEL -----
             #sender    = request.POST.get('sender')
             #recipient = request.POST.get('recipient')
             #subject   = request.POST.get('subject', '')
             #body_plain = request.POST.get('body-plain', '')
             #body_without_quotes = request.POST.get('stripped-text', '')
             # note: other MIME headers are also posted here...


         # Returned text is ignored but HTTP status code matters:
         # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
         return HttpResponse(response)

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of profile to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user and
            request.method in ['GET', 'PATCH'])

class AdderList(generics.ListCreateAPIView):
    """
    List all added items, or create a new item.
    """
    model = Adder
    serializer_class = AdderSerializer
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        return Adder.objects.filter(user=user)

    def put(self,request):
        a = Adder()
        user = request.user
        if request.method == 'PUT':
            data = request.DATA
            response = a.item_in(data, user)

        return Response(response)

class AdderAdd(generics.DestroyAPIView):

    model = Adder
    serializer_class = AdderSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

