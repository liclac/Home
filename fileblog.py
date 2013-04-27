import os
import re
import markdown2
from datetime import datetime
from operator import attrgetter

markdowner = markdown2.Markdown(extras=['metadata', 'fenced-code-blocks'])

title_exp = re.compile(r'([^\r\n]+)\r?\n[=-]+(\r?\n)*')
def extract_title(text):
	match = title_exp.match(text)
	if match:
		text = text[match.end():]
		title = match.group(1)
		return (title, text)
	return ('Untitled', text)

class Post(object):
	def __init__(self, path, full=True):
		self.path = path
		self.created = datetime.fromtimestamp(os.path.getctime(path))
		
		with open(path) as f:
			text = f.read()
			title, text = extract_title(text)
			if not full:
				text = text.split('\n\n')[0]
			
			self.html = markdowner.convert(text)
			self.slug = '.'.join(os.path.basename(path).split(os.extsep)[:-1])
			self.title = title
			#for key, value in self.html.metadata.iteritems():
			#	setattr(self, key, value)
	
	@classmethod
	def list(cls, path):
		posts = [ cls(os.path.join(path, filename), False) for filename in os.listdir(path)
					if filename.endswith('.md') and not filename.startswith('_') ]
		posts.sort(key=attrgetter('created'), reverse=True) # sort() is slightly more efficient than sorted()
		return posts
	
	@classmethod
	def slug(cls, path, slug):
		return cls(os.path.join(path, slug + '.md'))
