from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
from requests.auth import HTTPDigestAuth

import pprint
pp = pprint.PrettyPrinter(indent=1)

import re
rexDebPack = re.compile(r'^.*[.]deb$')

import os

#n'a pas marché (j'ai autorisé mon IP sur APT) : https://requests.readthedocs.io/en/master/user/authentication/
#problème NODATA : https://askubuntu.com/questions/474549/got-nodata-issue-nodata-does-the-network-require-authentication
#request : https://www.tutorialspoint.com/downloading-files-from-web-using-python
#serveur HTTP : https://blog.anvileight.com/posts/simple-python-http-server/

stockage='/home/cedric/aptdevproxy/repos'
source='/home/cedric/aptdevproxy/source/'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	def anwser(self, code, content, length):
		self.send_response(code)
		#self.send_header('content-type', r.headers['content-type'])
		self.send_header('content-length', length)
		self.end_headers()
		self.wfile.write(content)    		

	def fromdisk(self, path):
		f = open(path, "rb")
		self.anwser(200, f.read(), os.path.getsize(path))
		f.close()

	def passthru(self, uri, store):
		finished=False
		url = 'https://apt.epiconcept.fr' + uri
		if store is not None:
			sourcepath=source+os.path.basename(store)
			if os.path.isfile(sourcepath):
				print('fromsource '+store)
				self.fromdisk(sourcepath)
				finished=True
			elif os.path.isfile(store):
				print('fromcache '+store)
				self.fromdisk(store)
				finished=True

		if not finished:
			print('download '+uri)
			r = requests.get(url, allow_redirects=True)
			if store is not None:
				print('store '+store)
				dir=os.path.dirname(store)
				if not os.path.isdir(dir): os.makedirs(dir)
				f = open(store, "wb")
				f.write(r.content)
				f.close()
			self.anwser(r.status_code, r.content, r.headers['content-length'])

	def do_GET(self):
		if rexDebPack.match(self.path.rstrip()):
			self.passthru(uri=self.path, store=stockage + self.path)
		else:
			self.passthru(uri=self.path, store=None)


httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()