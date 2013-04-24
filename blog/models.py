from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	author = models.ForeignKey(User, editable=False, related_name="posts")
	
	title = models.CharField(max_length=140)
	content = models.TextField()
	public = models.BooleanField(default=True)
	
	posted_on = models.DateTimeField(auto_now_add=True)
	edited_on = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ['-posted_on']
	
	def slug(self):
		return self.title.lower().replace(" ", "-")
	
	def excerpt(self):
		return self.content.replace("\r\n", "\n").split("\n\n")[0]
	
	def has_more(self):
		return len(self.content.replace("\r\n", "\n").split("\n\n")) > 0
	
	def __unicode__(self):
		return self.title
	