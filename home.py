import os
from urlparse import urljoin
from functools import wraps
from flask import Flask, render_template, request, abort, url_for
from fileblog import Post
from middleware import PathFix
from werkzeug.contrib.cache import SimpleCache
from werkzeug.contrib.atom import AtomFeed

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

CACHE_TIMEOUT = 60*60

def make_external(url):
	return urljoin(request.url_root, url)



# http://flask.pocoo.org/snippets/9/
@app.before_request
def return_cached():
	# Don't cache things with GET or POST values
	if not request.values:
		response = cache.get(request.path)
		if response:
			return response

@app.after_request
def cache_response(response):
	if not request.values:
		try:
			cache.set(request.path, response, CACHE_TIMEOUT)
		except:
			# If we're dealing with an uncacheable type...
			pass
	return response



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/blog/')
def blog():
	return render_template('blog.html', posts=Post.list(posts_path))

@app.route('/blog/<slug>/')
def blog_post(slug):
	try:
		post = Post.slug(posts_path, slug)
	except:
		abort(404)
	return render_template('blog_post.html', slug=slug, post=post)

# http://flask.pocoo.org/snippets/10/
@app.route('/blog/feed.atom')
def blog_feed():
	feed = AtomFeed('MacaroniCode',
			feed_url=request.url, url=request.url_root)
	posts = Post.list(posts_path)
	for post in posts:
		feed.add(
			unicode(post.title), unicode(post.html),
			content_type='html',
			author='uppfinnarn',
			url=make_external(url_for('blog_post', slug=post.slug)),
			updated=post.modified,
			published=post.created
		)
	return feed.get_response()



@app.errorhandler(404)
def error404(error):
	return render_template('404.html')

@app.errorhandler(500)
def error500(error):
	return render_template('500.html')



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
	
