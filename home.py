import os
from urlparse import urljoin
from functools import wraps
from flask import Flask, render_template, request, abort, url_for
from werkzeug.contrib.cache import SimpleCache
from werkzeug.contrib.atom import AtomFeed
from fileblog import Post
from middleware import PathFix

app = Flask(__name__)
# I want this on /, even though mod_rewrite/mod_wsgi doesn't.
# Remove the following line to let it mount where WSGIScriptAlias
# says it should be.
app.wsgi_app = PathFix(app.wsgi_app, '/')

path = os.path.abspath(os.path.dirname(__file__))
posts_path = os.path.join(path, 'posts')
cache_path = os.path.join(path, 'cache')

make_external = lambda url: urljoin(request.url_root, url)



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/blog/')
def blog():
	return render_template('blog.html', posts=Post.list(posts_path, cache_path))

@app.route('/blog/<slug>/')
def blog_post(slug):
	try:
		#post = Post.slug(posts_path, cache_path, slug)
		post = Post.with_slug(posts_path, cache_path, slug)
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
	return render_template('error.html', errcode=404, errname="Not Found",
							errmsg="These are not the pages you are looking for.")

@app.errorhandler(500)
def error500(error):
	return render_template('error.html', errcode=500, errname="Server Error",
							errmsg="Whoops, looks like something made the server blow up...")



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
