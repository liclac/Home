from datetime import datetime
from django.utils.dateparse import parse_datetime
from django import template
from django.core import urlresolvers
from blog.models import Post

register = template.Library()

@register.inclusion_tag('new_posts_badge.html', takes_context=True)
def new_posts_badge(context):
	latest_post = Post.objects.latest()
	last_visit_cookie = context['request'].COOKIES.get('last_blog_visit')
	has_new = False
	if last_visit_cookie:
		try:
			has_new = parse_datetime(last_visit_cookie) < latest_post.posted_on
		except:
			pass
	return {'has_new': has_new}
