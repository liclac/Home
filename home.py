import os
from flask import Flask, render_template, abort
from fileblog import Post
from middleware import PathFix

app = Flask(__name__)
# I want this on /, even though mod_rewrite/mod_wsgi doesn't.
# Remove the following line to let it mount where WSGIScriptAlias
# says it should be.
app.wsgi_app = PathFix(app.wsgi_app, '/')

path = os.path.dirname(__file__)
posts_path = os.path.join(path, 'posts')



@app.context_processor
def blog_processor():
	return {
		'get_posts': lambda: Post.list(posts_path),
		'get_post': lambda slug: Post.slug(posts_path, slug),
	}



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/blog/')
def blog():
	return render_template('blog.html')

@app.route('/blog/<slug>/')
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
	
