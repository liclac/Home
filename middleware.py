import posixpath

class PathFix(object):
	def __init__(self, app, script_name):
		self.app = app
		self.script_name = script_name
	
	def __call__(self, environ, start_response):
		environ['SCRIPT_NAME'] = posixpath.dirname(environ['SCRIPT_NAME'])
		if environ['SCRIPT_NAME'] == '/':
			environ['SCRIPT_NAME'] = ''
		return self.app(environ, start_response)

