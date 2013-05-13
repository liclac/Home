import os
import re
import markdown2
import jsonpickle
from datetime import datetime
from operator import attrgetter

markdowner = markdown2.Markdown(extras=['metadata', 'fenced-code-blocks'])
timestamp_exp = re.compile(r'\! ([^\r\n]+)\r?\n')
title_exp = re.compile(r'([^\r\n]+)\r?\n[=-]+(\r?\n)*')

USE_CACHE = True

def make_path_to(path):
	dirpath = os.path.dirname(path)
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

class Post(object):
	_index_cache_filename = '__posts.json'
	_sortkey = 'created'
	
	def __init__(self, posts_path, slug, full=True):
		self.slug = slug
		path = os.path.join(posts_path, self.slug + '.md')
		
		with open(path) as f:
			text = f.read()
		
		text = self.extract_timestamp(text, path)
		text = self.extract_title(text)
		
		self.is_full = full
		if not full:
			text = text.split('\n\n')[0]
		
		# Extract the metadata, then 'demote' the text to an unicode
		# object. Without the demotion, it won't serialize properly.
		attributed_html = markdowner.convert(text)
		for key, value in attributed_html.metadata.iteritems():
			setattr(self, key, value)
		self.html = unicode(attributed_html)
	
	def extract_timestamp(self, text, path):
		match = timestamp_exp.match(text)
		ctime = datetime.fromtimestamp(os.path.getctime(path))
		
		if match:
			text = text[match.end():]
			self.created = datetime.strptime(match.group(1), '%d %b %Y, %H:%M')
		else:
			self.created = ctime
			self.write_timestamp(path)
		return text
	
	def extract_title(self, text):
		match = title_exp.match(text)
		if match:
			text = text[match.end():]
			self.title = match.group(1)
		else:
			self.title = 'Untitled'
		return text
	
	def write_timestamp(self, path):
		metaline = '! %s\n' % self.created.strftime('%d %b %Y, %H:%M')
		
		with open(path, 'rU') as in_:
			lines = in_.readlines()
			
			if lines[0].startswith('! '):
				lines[0] = metaline
			else:
				lines.insert(0, metaline)
		
		with open(path, 'w') as out:
			out.writelines(lines)
	
	@classmethod
	def with_slug(cls, posts_dir, cache_dir, slug, full=True):
		cachepath = os.path.join(cache_dir, slug + '.json')
		if USE_CACHE and not slug.startswith('_') and not slug.startswith('.'):
			try:
				with open(cachepath) as f:
					post = jsonpickle.decode(f.read())
					return post
			except:
				pass
		post = cls(posts_dir, slug, full)
		make_path_to(cachepath)
		with open(cachepath, 'w') as f:
			f.write(jsonpickle.encode(post))
		return post
	
	@classmethod
	def list(cls, posts_dir, cache_dir):
		cachepath = os.path.join(cache_dir, cls._index_cache_filename)
		if USE_CACHE:
			try:
				with open(cachepath) as f:
					posts = jsonpickle.decode(f.read())
					return posts
			except:
				pass
		
		posts = [ cls(posts_dir, '.'.join(filename.split(os.extsep)[:-1]), False) \
					for filename in os.listdir(posts_dir) \
					if filename.endswith('.md') \
					and not filename.startswith('_') \
					and not filename.startswith('.') ]
		
		# Note: sort() is slightly more efficient than sorted()
		if cls._sortkey:
			posts.sort(key=attrgetter(cls._sortkey), reverse=True)
		
		make_path_to(cachepath)
		with open(cachepath, 'w') as f:
			f.write(jsonpickle.encode(posts))
		return posts

class Page(Post):
	_index_cache_filename = '__pages.json'
	_sortkey = None
	
	# Pages don't need timestamps
	def extract_timestamp(self, text, path):
		return text
	def write_timestamp(self, path):
		pass
