import os
import re
import markdown2
from datetime import datetime
from operator import attrgetter

markdowner = markdown2.Markdown(extras=['metadata', 'fenced-code-blocks'])
timestamp_exp = re.compile(r'\! ([^\r\n]+)\r?\n')
title_exp = re.compile(r'([^\r\n]+)\r?\n[=-]+(\r?\n)*')

class Post(object):
	def __init__(self, path, full=True):
		self.path = path
		
		with open(self.path) as f:
			text = f.read()
		
		text = self.extract_timestamp(text)
		text = self.extract_title(text)
		self.slug = '.'.join(os.path.basename(path).split(os.extsep)[:-1])
		
		self.is_full = full
		if not full:
			text = text.split('\n\n')[0]
		
		self.html = markdowner.convert(text)
		#for key, value in self.html.metadata.iteritems():
		#	setattr(self, key, value)
	
	def extract_timestamp(self, text):
		match = timestamp_exp.match(text)
		if match:
			text = text[match.end():]
			self.created = datetime.strptime(match.group(1), '%d %b %Y, %H:%M')
		else:
			self.created = datetime.fromtimestamp(os.path.getctime(self.path))
			self.write_timestamp()
		return text
	
	def extract_title(self, text):
		match = title_exp.match(text)
		if match:
			text = text[match.end():]
			self.title = match.group(1)
		else:
			self.title = 'Untitled'
		return text
	
	def write_timestamp(self):
		metaline = '! %s\n' % self.created.strftime('%d %b %Y, %H:%M')
		
		with open(self.path, 'rU') as in_:
			lines = in_.readlines()
			
			if lines[0].startswith('! '):
				lines[0] = metaline
			else:
				lines.insert(0, metaline)
		
		with open(self.path, 'w') as out:
			out.writelines(lines)
	
	@classmethod
	def list(cls, path):
		posts = [ cls(os.path.join(path, filename), False) for filename in os.listdir(path)
					if filename.endswith('.md') and not filename.startswith('_') ]
		posts.sort(key=attrgetter('created'), reverse=True) # sort() is slightly more efficient than sorted()
		return posts
	
	@classmethod
	def slug(cls, path, slug):
		return cls(os.path.join(path, slug + '.md'))
