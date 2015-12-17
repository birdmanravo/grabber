# 4chins image puller
# by anon
# Free as in freedom and free beer under the GNU GPL v2

import json, urllib.request, os, platform, math
url = input("URL -> ").rsplit("/")
board = url[3]
thread = url[5]
img_url = "http://i.4cdn.org/%s/" % (board)

if(platform.system() == "Windows"):
		print("Using Windows save folder")
		defaultsavefolder = "F:\\Shared\Misc\\"
else:
		print("Using Linux save folder")
		defaultsavefolder = "/media/nail/Shared/Misc/"

tally = {'records' : 0, 'ims' : 0, 'dups' : 0, 'keeps' : 0}
# records = posts found
# ims = images found
# dups = images ID'd as duplicates
# keeps = images marked for download

image = {}
# list of images to keep

if(thread.isnumeric() and board.isalpha() and len(board) < 5 ):
	# We have a valid thread, so get to work
	print("Reading JSON Data...")
	jsondata = json.loads(urllib.request.urlopen("https://a.4cdn.org/%s/thread/%s.json" % (board,thread)).read().decode('utf-8'))['posts']
	for keys in jsondata:
		# In this loop we put together all the needed information into an array
		# Everything could be performed during this loop to boost efficiency, but this way
		# I know how many images there are total.
		tally['records'] = tally['records'] + 1
		if 'tim' in keys:
			# 'tim' is the images stored filename, proof the current post in this loop has an image uploaded
			tally['ims'] = tally['ims'] + 1
			if(os.path.exists(defaultsavefolder+str(keys['tim'])+keys['ext'])):
				# If the saved filename exists in the folder assume a duplicate
				tally['dups'] = tally['dups'] + 1
			elif(os.path.exists(defaultsavefolder+keys['filename']+keys['ext']) and os.path.getsize(defaultsavefolder+keys['filename']+keys['ext']) == keys['fsize']):
				# If the original filename exists in the defaultsavefold, and the
				# filesize matches, assume a duplicate
				tally['dups'] = tally['dups'] + 1
			else:
				# If not detected as a duplicate image, pull info into a list
				tally['keeps'] = tally['keeps'] + 1
				image[tally['keeps']] = {}
				image[tally['keeps']]['original_name'] = keys['filename']
				image[tally['keeps']]['ext'] = keys['ext']
				image[tally['keeps']]['filename'] = "%s%s" % (keys['tim'], keys['ext'])
	print("FOUND \n%s Posts \n%s Images \n%s Duplicates" % (tally['records'], tally['ims'], tally['dups'])) 
	for i in range(1, tally['keeps']):
		# This loop is run against every valid image found in the previous loop
		print('{0:10}'.format("[%s/%s]" % (i, tally['keeps'])), end="")
		print('{0:45}'.format(image[i]['original_name'][:42]), end="")
		print('{0:8}'.format(image[i]['ext'][1:]), end="\n")
		u = urllib.request.urlopen(img_url+image[i]['filename'])
		image[i]['templen']=u.length
		readlen = 1024*16
		total = 0
		block = None
		with open(defaultsavefolder+image[i]['filename'], 'wb') as outfile:
			while block != '' and total < image[i]['templen']:
				block=u.read(readlen)
				outfile.write(block)
				total += len(block)
				block = None
				print("%s of %s" % (total, image[i]['templen']), end="\r")
			u.close()
	if tally['keeps'] == 0:
		print("No images found. Exiting.")
	print("Downloading Completed")
else:
	print("Given string is not a valid URL.")
