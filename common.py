import os
from flask import abort

root_path_for = lambda p: os.path.join(os.path.abspath(os.path.dirname(__file__)), p)
content_path = root_path_for('content')
cache_path = root_path_for('cache')

paths = {
	'Post': os.path.join(content_path, 'posts'),
	'Page': os.path.join(content_path, 'pages'),
	'Paste': os.path.join(content_path, 'pastes')
}
path_for_class = lambda cls: paths[cls.__name__]
data_path = os.path.join(content_path, 'data')

def get_or_404(cls, slug, full=True):
	try:
		p = cls.with_slug(path_for_class(cls), cache_path, slug, full)
	except Exception as e:
		print e
		abort(404)
	return p

def get_list(cls):
	return cls.list(path_for_class(cls), cache_path)
