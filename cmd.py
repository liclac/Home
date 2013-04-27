import re
import sys, os
from datetime import datetime

def timestamp(path):
	metaline = '! %s\n' % datetime.now().strftime('%d %b %Y, %H:%M')
	with open(path, 'rU') as f:
		lines = f.readlines()
	
	if lines[0].startswith('! '):
		lines[0] = metaline
	else:
		lines.insert(0, metaline)
	
	with open(path, 'w') as f:
		f.writelines(lines)

if __name__ == '__main__':
	handlers = {
		'timestamp': timestamp
	}
	
	if len(sys.argv) <= 2 or sys.argv[1] not in handlers:
		print "Usage:"
		print "    python %s <action> <slug>" % sys.argv[0]
		print " "
		print "-- Commands --"
		print "timestamp:"
		print "    Embeds the current timestamp into the given post, if one"
		print "    isn't already embedded. Posts without embedded timestamps"
		print "    will be dated using their modification timestamps, which"
		print "    is rather fragile - any change to the file will reset it."
		exit()
	
	handlers[sys.argv[1]](sys.argv[2])