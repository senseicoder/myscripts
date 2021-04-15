from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
#from requests.auth import HTTPDigestAuth

#import pprint
#pp = pprint.PrettyPrinter(indent=1)

#import re
#rexDebPack = re.compile(r'^.*[.]deb$')

import os, sys, getopt

#todo
#prendre un fichier avec toutes les confs, multi repos
#faire marcher repo security
#tester avec mdm

#sources
#n'a pas marché (j'ai autorisé mon IP sur APT) : https://requests.readthedocs.io/en/master/user/authentication/
#problème NODATA : https://askubuntu.com/questions/474549/got-nodata-issue-nodata-does-the-network-require-authentication
#request : https://www.tutorialspoint.com/downloading-files-from-web-using-python
#serveur HTTP : https://blog.anvileight.com/posts/simple-python-http-server/
#cli args : https://www.tutorialspoint.com/python/python_command_line_arguments.htm

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	def answer(self, code, content, length):
		self.send_response(code)
		#self.send_header('content-type', r.headers['content-type'])
		self.send_header('content-length', length)
		self.end_headers()
		self.wfile.write(content)    		

	def fromdisk(self, path):
		f = open(path, "rb")
		self.answer(200, f.read(), os.path.getsize(path))
		f.close()

	def passthru(self, uri, store):
		finished=False
		if store is not None:
			sourcepath=self.server._pathSource+'/'+os.path.basename(store)
			if os.path.isfile(sourcepath):
				print('fromsource '+sourcepath)
				self.fromdisk(sourcepath)
				finished=True
			elif os.path.isfile(store):
				print('fromcache '+store)
				self.fromdisk(store)
				finished=True

		if not finished:
			url = self.server._urlSrc + '/' + uri
			print('download '+url)
			r = requests.get(url, allow_redirects=True)
			if store is not None and r.status_code == 200:
				print('store '+store)
				dir=os.path.dirname(store)
				if not os.path.isdir(dir): os.makedirs(dir)
				f = open(store, "wb")
				f.write(r.content)
				f.close()
			self.answer(r.status_code, r.content, r.headers['content-length'])

	def do_GET(self):
		#if rexDebPack.match(self.path):
			self.passthru(uri=self.path, store=self.server._pathBase + self.path)
		#else:
		#	self.passthru(uri=self.path, store=None)

class MyHTTPServer(HTTPServer):
	def setPathBase(self, path):
		self._pathBase = path
		self._pathSource = path + '/sources'
		if not os.path.isdir(self._pathSource): os.makedirs(self._pathSource)

	def setUrlSrc(self, url):
		self._urlSrc = url

def main(argv):
	port=8000
	pathbase='/home/cedric/aptdevproxy/'
	urlapt='https://apt.epiconcept.fr'

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

	httpd = MyHTTPServer(('', int(port)), SimpleHTTPRequestHandler)
	httpd.setPathBase(pathbase)
	httpd.setUrlSrc(urlapt)
	httpd.serve_forever()

if __name__ == "__main__":
   main(sys.argv[1:])