from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from Metten.blog.models import Post
from django.contrib.syndication.views import Feed

class BlogFeed(Feed):
    title = "Metten Tot"
    description = "Some ramblings"
    link = "/blog/feed"

    def items(self):
        return Post.objects.all().order_by("-created")[:2]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.body
    def item_link(self, item):
        return u"/blog/%d" % item.id

urlpatterns = patterns('blog.views',

    url(r'^$', ListView.as_view(
                               queryset=Post.objects.all().
                               order_by("-created")[:4],
                               context_object_name = "blog_list",
                               template_name="blog.html")),
    url(r'^(?P<pk>\d+)$', DetailView.as_view(
                               model=Post,
                               context_object_name = "post",
                               template_name="post.html")),
    url(r'^archives/$', ListView.as_view(
                               queryset=Post.objects.all().
                               order_by("-created"),
                               context_object_name = "archive_list",
                               template_name="archives.html")),
    #url(r'^tag/(?P<tag>\w+)$', 'tagpage'),
    url(r'^feed/$', BlogFeed()),

    #generic views
)