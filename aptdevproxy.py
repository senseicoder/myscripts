from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
from requests.auth import HTTPDigestAuth

import pprint
pp = pprint.PrettyPrinter(indent=1)

import re
rexDebPack = re.compile(r'^.*[.]deb$')

import os, sys, getopt

#n'a pas marché (j'ai autorisé mon IP sur APT) : https://requests.readthedocs.io/en/master/user/authentication/
#problème NODATA : https://askubuntu.com/questions/474549/got-nodata-issue-nodata-does-the-network-require-authentication
#request : https://www.tutorialspoint.com/downloading-files-from-web-using-python
#serveur HTTP : https://blog.anvileight.com/posts/simple-python-http-server/
#cli args : https://www.tutorialspoint.com/python/python_command_line_arguments.htm

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
		global source 

		finished=False
		url = urlapt + uri
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
		global stockage 

		if rexDebPack.match(self.path.rstrip()):
			self.passthru(uri=self.path, store=stockage + self.path)
		else:
			self.passthru(uri=self.path, store=None)

def main(argv):
	global port
	global urlapt
	global pathbase
	global stockage
	global source

	help='aptdevproxy.py -p <port> -d <path cache> -u https://apt.epiconcept.fr'
	try:
		opts, args = getopt.getopt(argv,"hp:d:u:",["port=","dir=","url="])
	except getopt.GetoptError:
		print(help)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(help)
			sys.exit()
		elif opt in ("-p", "--port"): port = arg
		elif opt in ("-d", "--dir"): pathbase = arg
		elif opt in ("-u", "--url"): urlapt = arg
	print('port '+str(port)+' dir '+pathbase+' url '+urlapt)

	stockage=pathbase+'repos'
	source=pathbase+'source/'

	httpd = HTTPServer(('', int(port)), SimpleHTTPRequestHandler)
	httpd.serve_forever()

port=8000
urlapt='https://apt.epiconcept.fr'
pathbase='/home/cedric/aptdevproxy/'
stockage=''
source=''

if __name__ == "__main__":
   main(sys.argv[1:])