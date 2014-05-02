from django.contrib import admin
from Metten.blog.models import Post, Links, Best, Search
from Metten.years.models import Adder

admin.site.register(Post)
admin.site.register(Links)
admin.site.register(Best)
admin.site.register(Search)
admin.site.register(Adder)
#takes care of admin.PY and models