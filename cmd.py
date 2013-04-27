import re
import sys, os
import shutil
from datetime import datetime

def timestamp(path):
	ctime = datetime.fromtimestamp(os.path.getctime(path))
	metaline = '! %s\n' % ctime.strftime('%d %b %Y, %H:%M')
	with open(path, 'rU') as f:
		lines = f.readlines()
	
	if lines[0].startswith('! '):
		lines[0] = metaline
	else:
		lines.insert(0, metaline)
	
	with open(path, 'w') as f:
		f.writelines(lines)

def collectstatic(dstpath):
	srcpath = os.path.join(os.path.dirname(__file__), 'static')
	for filename in os.listdir(srcpath):
		shutil.copy(os.path.join(srcpath, filename), dstpath)

if __name__ == '__main__':
	handlers = {
		'timestamp': timestamp,
		'collectstatic': collectstatic,
	}
	
	if len(sys.argv) <= 1 or sys.argv[1] not in handlers:
		print "-- Commands --"
		print " "
		
		print "timestamp <file>"
		print "    Embeds the file's ctime into it, overwriting any existing."
		print "    embedded timestamp. Posts without embedded timestamps will"
		print "    be dated using their ctime on visit, which is rather"
		print "    fragile - any change to the file will reset it."
		print " "
		
		print "collectstatic <destination>"
		print "    Collects files from the 'static' directory into the specified"
		print "    destination path. The destination must be writable by the"
		print "    current user."
		print " "
		
		exit()
	
	handlers[sys.argv[1]](*sys.argv[2:])