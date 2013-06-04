import cgi
from flask import Blueprint, request, url_for, redirect, render_template
from pygments.lexers import get_lexer_by_name
from fileblog import Paste
from common import path_for_class, get_or_404

paste = Blueprint("paste", __name__, template_folder='templates')

@paste.route('/', methods=['GET', 'POST'])
def new():
	if request.method == 'POST':
		text = cgi.escape(request.form['text'].strip())
		syntax = cgi.escape(request.form['syntax'].strip())
		
		# No empty pastes >_>
		if not text:
			return redirect(url_for('paste.new'))
		
		# Make sure we have a correct lexer name, otherwise the view crashes!
		try:
			lexer = get_lexer_by_name(syntax)
		except:
			syntax = ''
		
		paste = Paste.create(path_for_class(Paste), text, syntax)
		return redirect(url_for('paste.view', slug=paste.slug))
	
	return render_template('paste/new.html')

@paste.route('/<slug>/')
def view(slug):
	paste = get_or_404(Paste, slug)
	return render_template('paste/view.html', paste=paste)

@paste.route('/<slug>/raw/')
def view_raw(slug):
	paste = get_or_404(Paste, slug, False)
	return (paste.text, 200, {'Content-Type': 'text/plain'})
