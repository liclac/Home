import os
from functools import wraps
from flask import Flask, render_template, request, abort
from fileblog import Post
from middleware import PathFix
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
# I want this on /, even though mod_rewrite/mod_wsgi doesn't.
# Remove the following line to let it mount where WSGIScriptAlias
# says it should be.
app.wsgi_app = PathFix(app.wsgi_app, '/')

# I don't need memcached for such a simple project.
# Local memory is also far easier to nuke.
cache = SimpleCache()

path = os.path.dirname(__file__)
posts_path = os.path.join(path, 'posts')



# Decorators
def cached(timeout=10*60, key='view/%s'):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			cache_key = key % request.path
			rv = cache.get(cache_key)
			if rv is not None:
				return rv
			rv = f(*args, **kwargs)
			cache.set(cache_key, rv, timeout=timeout)
			return rv
		return decorated_function
	return decorator



# Templates
@app.context_processor
def blog_processor():
	return {
		'get_posts': lambda: Post.list(posts_path),
		'get_post': lambda slug: Post.slug(posts_path, slug),
	}



# Routes
@app.route('/')
@cached()
def home():
	return render_template('home.html')

@app.route('/blog/')
@cached()
def blog():
	return render_template('blog.html')

@app.route('/blog/<slug>/')
@cached()
def blog_post(slug):
	try:
		post = Post.slug(posts_path, slug)
	except:
		abort(404)
	return render_template('blog_post.html', slug=slug, post=post)

@app.errorhandler(404)
def error404(error):
	return render_template('404.html')

@app.errorhandler(500)
def error500(error):
	return render_template('500.html')



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
	
