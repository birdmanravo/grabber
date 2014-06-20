import json, urllib.request, os

url = input("URL -> ").rsplit("/")
board = url[3]
thread = url[5]

img_url = "http://i.4cdn.org/%s/" % (board)
defaultsavefolder = "/media/nail/Shared/Misc/"

if(thread.isnumeric() and board.isalpha() and len(board) < 5 ):
	# We have a valid thread, so get to work
	print("Reading JSON Data...") 
	jsondata = json.loads(urllib.request.urlopen("https://a.4cdn.org/%s/thread/%s.json" % (board,thread)).read().decode('utf-8'))['posts']
	
	for keys in jsondata:
		if 'tim' in keys:
			# 'tim' is the images stored filename, proof the current post in this loop has an image uploaded
			image = "%s%s" % (keys['tim'], keys['ext'])
			filesize = str("{0:.0f}".format(keys['fsize'] / 1024))+"KB" if keys['fsize']<1048576 else str("{0:.2f}".format(keys['fsize']/1048576))+"MB"
			filedims = "%sx%s" % (keys['w'], keys['h'])
			
			print("Image: %s - %s - %s" % (image.ljust(18, ' '), filedims.ljust(9,' '), filesize.ljust(6,' ')), end='')
			# ljust to make it look pretty in the console window

			if(os.path.exists(defaultsavefolder+image)):
				# image has already been downloaded
				print(" - skipped")
				
			elif(os.path.exists(defaultsavefolder+keys['filename']+keys['ext']) and os.path.getsize(defaultsavefolder+keys['filename']+keys['ext']) == keys['fsize']):
				# image has the same original name and file size as a 
				# local file. Assume it's a duplicate
				print(" - Duplicate")
			else:
				# image is assumed new, download.
				# todo: error handling
				with urllib.request.urlopen(img_url+image) as response, open(defaultsavefolder+image, 'wb') as out_file:
					out_file.write(response.read())
				print(" - saved")
	print("Operation Complete")
else:
	# error out and exit.
	print("Given string is not a valid URL.") 
