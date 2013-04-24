from django.contrib import admin
from django import forms
from models import *

class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'posted_on', 'public']
	list_filter = ['posted_on', 'author__username', 'public']
	date_hierachy = 'posted_on'

	readonly_fields = ['posted_on', 'edited_on']
	fieldsets = (
		(None, {
			'fields': ('title', 'content', 'public')
		}),
		('Timestamps', {
			'classes': ('collapse',),
			'fields': ('posted_on', 'edited_on')
		}),
	)

	def save_model(self, request, obj, form, change):
		#if getattr(obj, 'author', None) is None:
		if not change: # If this is a new post...
			obj.author = request.user
		super(PostAdmin, self).save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)

