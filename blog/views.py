from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from Metten.blog.models import Post, Search #need to import the model for the blog
from Metten.blog.forms import SearchForm, LinkedinForm
from Metten.blog.scrapemain import ScrapeMain
from Metten.blog.graph_main import Graph
from Metten.blog.linking import LinkingIn
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.contrib.auth import authenticate, login

from django.views.decorators.cache import never_cache


def index(request):
    # user = authenticate(username='buddy', password='garity')
	#user = authenticate()
	#login(request, user)
	if request.method == 'POST':

		if 'job_search' in request.POST:
			search = Search(from_user=request.user)
			form = SearchForm(data=request.POST, instance=search)
			if form.is_valid():   #calls the clean method
				form.save()
				request.session['job'] = form.cleaned_data
				return redirect('/plots')
		elif 'linkedin_search' in request.POST:
			form1 = LinkedinForm(request.POST)
			if form1.is_valid():
				request.session['linked'] = form1.cleaned_data
				return redirect('/linker')

	else:
		form = SearchForm()
		form_l = LinkedinForm()
		dater = datetime.now() + relativedelta(years=5)
		#dater = date.today() + datetime.timedelta(days=(5*365.24))
		return render(request, 'index.html', {'date':dater, 'form':form, 'form_l':form_l})
        #takes a parameter, request, which is an object that has information about the
        #user requesting the page from the browser.
        #The function's response is to simply render the index.html template

#def tagpage(request, tag):
#    posts = Post.objects.filter(tags__name=tag)
#    return render_to_response("tagpage.html", {"posts":posts, "tag": tag})

@never_cache
def plots(request):
	job = request.session['job']
	job = job['job_searched']
	s = ScrapeMain()
	s_main = s.scrape_main(job)

	l = LinkingIn()
 	l_jobs = l.scrape_jobs(job)

	#, 'res':status[1][0]
	return render_to_response('plots.html', {'job':job, 'stat':s_main['stat'], 'jobs_cluster':s_main['jobs_cluster'], 'med':s_main['med'], 'jobs':l_jobs})


@never_cache
def graph(request):
	job = request.session['job']
	job = job['job_searched']
	g = Graph()
	g_main = g.graph_main(job)
	return render_to_response('graph.html', {'png_graph':g_main['png_graph'], 'matches':g_main['matches'], 'jb_title':g_main['title']})


	   # <h3>&nbsp;</h3>
    # <!------ JOB 1 ------->
    # {% for cluster in jobs_cluster %}
    #     <h3>&nbsp;</h3>
    #     <h3>Job {{forloop.counter}}</h3>
    # <!-- gives you path for plots -->
    #     {% for jobs in cluster %}
    #     <ul type="circle">
    #             <li>{{jobs.0}}, {{jobs.1}}, {{jobs.2}} </li>
    #     </ul>
    #     {% endfor %}
    #     <img src="{{cluster.0.3}}" />
    # {% endfor %}


def linker(request):
 	link = request.session['linked']
 	job_title = link['search_for']
 	zip_code = 68106
 	radius = 100

# 	searched = link['search_for']
 	l = LinkingIn()
 	l_results = l.scrape_sites(job_title, radius, zip_code)
	#, 'res':status[1][0]
	return render_to_response('linked_html.html', {'results':l_results})