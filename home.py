import os
import json
from urlparse import urljoin
from operator import itemgetter
from flask import Flask, render_template, request, abort, redirect, url_for
from werkzeug.contrib.atom import AtomFeed
from middleware import PathFix
from fileblog import Post, Page, Paste
from pygments.lexers import get_all_lexers

app = Flask(__name__)
# I want this on /, even though mod_rewrite/mod_wsgi doesn't.
# Remove the following line to let it mount where WSGIScriptAlias
# says it should be.
app.wsgi_app = PathFix(app.wsgi_app, '/')

path_for = lambda p: os.path.join(os.path.abspath(os.path.dirname(__file__)), p)
posts_path = path_for('posts')
pages_path = path_for('pages')
pastes_path = path_for('pastes')
data_path = path_for('data')
cache_path = path_for('cache')

make_external = lambda url: urljoin(request.url_root, url)

def get_or_404(cls, path, slug, full=True):
	try:
		p = cls.with_slug(path, cache_path, slug, full)
	except Exception as e:
		print e
		abort(404)
	return p



@app.context_processor
def inject_pages():
	return {
		'pages': Page.list(pages_path, cache_path)
	}



@app.errorhandler(401)
def error401(error):
	return render_template('error.html', errcode=401, errname="Unauthorized",
							errmsg="You're not supposed to be here.")

@app.errorhandler(404)
def error404(error):
	return render_template('error.html', errcode=404, errname="Not Found",
							errmsg="These are not the pages you are looking for.")

@app.errorhandler(500)
def error500(error):
	return render_template('error.html', errcode=500, errname="Server Error",
							errmsg="Whoops, looks like something made the server blow up...")



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/blog/')
def blog():
	return render_template('blog.html', posts=Post.list(posts_path, cache_path))

@app.route('/blog/<slug>/')
def blog_post(slug):
	try:
		post = Post.with_slug(posts_path, cache_path, slug)
	except Exception as e:
		print e
		abort(404)
	return render_template('blog_post.html', post=post)

@app.route('/p/', methods=['GET', 'POST'])
def paste_new():
	if request.method == 'POST':
		text = request.form['text'].strip()
		syntax = request.form['syntax'].strip()
		
		if not text:
			return redirect(url_for('paste_new'))
		
		paste = Paste.create(pastes_path, text, syntax)
		return redirect(url_for('paste', slug=paste.slug))
	
	return render_template('paste_new.html')

@app.route('/p/<slug>/')
def paste(slug):
	try:
		paste = Paste.with_slug(pastes_path, cache_path, slug)
	except Exception as e:
		print e
		abort(404)
	return render_template('paste.html', paste=paste)

@app.route('/p/<slug>/raw/')
def paste_raw(slug):
	paste = get_or_404(Paste, pastes_path, slug, False)
	return (paste.text, 200, {'Content-Type': 'text/plain'})

@app.route('/projects/')
def projects():
	with open(os.path.join(data_path, 'projects.json')) as f:
		projects = json.load(f)
	return render_template('projects.html', projects=projects)

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

@app.route('/<path:path>/')
def page(path):
	if path == 'favicon.ico':
		abort(404)
	
	try:
		page = Page.with_slug(pages_path, cache_path, path)
	except Exception as e:
		#print e
		abort(404)
	return render_template('page.html', page=page)



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
