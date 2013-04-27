About
-----
This is what I use to run [macaronicode.se](http://macaronicode.se/).

Feel free to steal anything (especially fileblog.py) for yourself. There's no license.

Requirements
------------
* Python 2.7
	* flask
	* markdown2

cmd.py
------
cmd.py is a commandline tool that's the closest I'm getting to an admin interface.

So far, it only has one command: 'timestamp', that embeds a timestamp into a post, to protect the rather fragile 'ctime' (which will change every time the file is touched).

I'm going to automate this timestamp generation, but for now, it has to be done manually.