from flask import Blueprint, render_template
from werkzeug.contrib.atom import AtomFeed
from fileblog import Post
from common import get_list, get_or_404

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/')
def index():
	return render_template('blog/index.html', posts=get_list(Post))

@blog.route('/<slug>/')
def post(slug):
	post = get_or_404(Post, slug)
	return render_template('blog/post.html', post=post)

# http://flask.pocoo.org/snippets/10/
@blog.route('/feed.atom')
def feed():
	feed = AtomFeed('MacaroniCode',
			feed_url=request.url, url=request.url_root)
	posts = get_list(Post)
	for post in posts:
		feed.add(
			unicode(post.title), unicode(post.html),
			content_type='html',
			author='uppfinnarn',
			url=make_external(url_for('blog.post', slug=post.slug)),
			updated=post.created,
			published=post.created
		)
	return feed.get_response()
