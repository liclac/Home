import os
import re
import string
import random
from datetime import datetime
from operator import attrgetter
import jsonpickle
from markdown2 import Markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

timestamp_exp = re.compile(r'\! ([^\r\n]+)\r?\n')
syntax_exp = re.compile(r'\!s ([^\r\n]+)\r?\n')
title_exp = re.compile(r'([^\r\n]+)\r?\n[=-]+(\r?\n)*')

USE_CACHE = True

def make_path_to(path):
	dirpath = os.path.dirname(path)
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

class Post(object):
	_sortkey = 'created'
	_extension = 'md'
	
	# Defaults
	title = "Untitled"
	
	def __init__(self, posts_path, slug, full=True):
		self.slug = slug
		self.is_full = full
		path = os.path.join(posts_path, self.slug + '.' + self._extension)
		
		with open(path) as f:
			text = f.read().decode('utf-8')
		
		text = self.extract_meta(text, path)
		text = self.extract_title(text)
		self.extract_content(text, full)
	
	def extract_meta(self, text, path):
		text = self.extract_timestamp(text, path)
		return text
	
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
		return text
	
	def extract_content(self, text, full=True):
		self.is_full = full
		if not self.is_full:
			text = text.split('\n\n')[0]
		
		# Extract the metadata, then 'demote' the text to an unicode
		# object. Without the demotion, it won't serialize properly.
		markdowner = Markdown(extras=['metadata', 'fenced-code-blocks'])
		attributed_html = markdowner.convert(text)
		for key, value in attributed_html.metadata.iteritems():
			setattr(self, key, value)
		self.html = unicode(attributed_html)
	
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
		cachepath = os.path.join(cache_dir, cls.__name__.lower() + 's', slug + '.json')
		should_cache = USE_CACHE and not slug.startswith('_') and not slug.startswith('.')
		if should_cache:
			try:
				with open(cachepath) as f:
					post = jsonpickle.decode(f.read().decode('utf-8'))
					return post
			except:
				pass
		post = cls(posts_dir, slug, full)
		if should_cache:
			make_path_to(cachepath)
			with open(cachepath, 'w') as f:
				f.write(jsonpickle.encode(post))
		return post
	
	@classmethod
	def list(cls, posts_dir, cache_dir):
		index_cache_filename = cls.__name__.lower() + 's.json'
		cachepath = os.path.join(cache_dir, index_cache_filename)
		if USE_CACHE:
			try:
				with open(cachepath) as f:
					posts = jsonpickle.decode(f.read().decode('utf-8'))
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
			f.write(jsonpickle.encode(posts).encode('utf-8'))
		return posts

class Page(Post):
	_sortkey = None
	
	# Pages don't need timestamps
	def extract_timestamp(self, text, path):
		return text
	def write_timestamp(self, path):
		pass

class Paste(Post):
	_extension = 'txt'
	_slug_length = 5
	_slug_chars = string.ascii_uppercase + \
				string.ascii_lowercase + \
				string.digits
	
	title = None
	syntax = None
	
	def extract_title(self, text):
		return text
	
	# Extract information for Pygments highlighting
	def extract_meta(self, text, path):
		text = self.extract_timestamp(text, path)
		text = self.extract_syntax(text)
		return text
	
	def extract_syntax(self, text):
		match = syntax_exp.match(text)
		if match:
			text = text[match.end():]
			self.syntax = match.group(1)
		return text
	
	def extract_content(self, text, full=True):
		self.text = text
		if self.syntax:
			lexer = get_lexer_by_name(self.syntax)
			formatter = HtmlFormatter(linenos=False)
			self.html = highlight(text, lexer, formatter)
		else:
			self.html = "<pre>%s</pre>" % text
	
	@classmethod
	def create(cls, pastes_path, text, syntax, return_full=False):
		if syntax:
			text = "!s %s\n%s" % (syntax, text)
		
		# Keep generating IDs until we find one that's not taken
		while True:
			slug = ''.join(random.choice(cls._slug_chars) for x in range(cls._slug_length))
			path = os.path.join(pastes_path, slug + '.' + cls._extension)
			if not os.path.exists(path):
				break
		with open(path, 'w') as f:
			f.write(text.encode('utf-8'))
		
		paste = Paste(pastes_path, slug, return_full)
		return paste
