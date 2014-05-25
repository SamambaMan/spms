import BaseHTTPServer

HOST = '0.0.0.0'
PORT = 8888


class BaseHandler(BaseHTTPServer.BaseHTTPRequestHandler):
 def do_HEAD(self):
  self.send_response(200)
  self.send_header('Content-Type','text/html')
  self.end_headers()
 def do_GET(self):
  self.do_HEAD()
  self.wfile.write('Ola mundo')

if __name__ == '__main__':
 server_class = BaseHTTPServer.HTTPServer
 httpd = server_class((HOST,PORT),BaseHandler)
 try:
  httpd.serve_forever()
 except KeyboardInterrupt:
  pass
 
