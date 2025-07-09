from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    url(r'^$', views.all_blogs, name="Blogs"),
    url(r'^upvote/$', views.upvote),
    url(r'^create/$', views.create_blog),
    url(r'^see/1/$', views.blog_single,name="blog"),
    url(r'^see/2/$', views.blog_more,name="blog"),
    path('see/3/$', views.blog_single3,name="blog"),
]

