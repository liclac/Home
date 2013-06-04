import os
import json
from flask import Flask, render_template, abort
from middleware import PathFix
from fileblog import Page
from common import *

from modules.blog import blog
from modules.paste import paste

app = Flask(__name__)
# I want this on /, even though mod_rewrite/mod_wsgi doesn't.
# Remove the following line to let it mount where WSGIScriptAlias
# says it should be.
app.wsgi_app = PathFix(app.wsgi_app, '/')



# These two were growing huge, so they got their own modules
# Mount them as Blueprints!
app.register_blueprint(blog, url_prefix='/blog')
app.register_blueprint(paste, url_prefix='/p')



@app.context_processor
def inject_pages():
	return { 'pages': get_list(Page) }

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/projects/')
def projects():
	with open(os.path.join(data_path, 'projects.json')) as f:
		projects = json.load(f)
	return render_template('projects.html', projects=projects)

@app.route('/<path:path>/')
def page(path):
	if path == 'favicon.ico':
		abort(404)
	
	page = get_or_404(Page, path)
	return render_template('page.html', page=page)



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



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
