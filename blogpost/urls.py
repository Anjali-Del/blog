import views

from django.conf.urls import url

urlpatterns = [
    url(r'^blog/list/$', views.ListBlogposts.as_view({'get': 'get'}),
    	name='list-blogs'),
    url(r'^blog/add/$', views.AddBlogposts.as_view({'post': 'post'}),
    	name='add-blog'),
    url(r'^comment/add/(?P<blog_id>[\w-]+)/(?P<para_no>\d+)/$',
    	views.AddComments.as_view({'post': 'post'}), name='add-comment'),
    url(r'^post/view/(?P<blog_id>[\w-]+)/$',
    	views.GetBlogpost.as_view({'get': 'get'}), name='get-blog'),
]
