grabber
=======

Quick &amp; Dirty 4chan image grabber. This script, when given the URL of a thread
in any board copy & pasted from a browser, will download every image in the thread.
It has some simplistic duplicate recognition, and can ignore images posted by the 
user in a thread, and images already downloaded in a thread, allowing it to be run
multiple times per thread if needed.

Configuration:
=============
Edit the defaultsavefolder variable to set your default save folder.


Usage: 
======
$ python3 grabber.py

[paste URL]

It needs to be run in a terminal, so to launch it from a Linux desktop use the
following syntax

$ xterm -e "python3 /yourpath/to/grabber.py"
