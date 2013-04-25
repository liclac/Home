import logging
from datetime import datetime
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.http import Http404
from models import *

class PostListView(ListView):
	model = Post
	
	def get_queryset(self):
		return self.model.objects.exclude(public=False)
	
	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		context['no_badge'] = True #TODO: Make this actually take effect!
		return context
	
	def dispatch(self, request, *args, **kwargs):
		response = super(PostListView, self).dispatch(request, *args, **kwargs)
		response.set_cookie('last_blog_visit', str(timezone.now()), max_age=60*60*24*365*10)
		return response

class PostDetailView(DetailView):
	model = Post
	
	def get_object(self, *args, **kwargs):
		obj = super(DetailView, self).get_object(*args, **kwargs)
		if not obj.public:
			raise Http404
		return obj
