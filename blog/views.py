from django.views.generic import ListView, DetailView
from django.http import Http404
from models import *

class PostDetailView(DetailView):
	model = Post
	
	def get_object(self, *args, **kwargs):
		obj = super(DetailView, self).get_object(*args, **kwargs)
		if not obj.public:
			raise Http404
		return obj

class PostListView(ListView):
	model = Post
	
	def get_queryset(self):
		return self.model.objects.exclude(public=False)
