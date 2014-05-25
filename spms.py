import BaseHTTPServer
from cgi import parse_qs, escape
import pickle

HOST = '0.0.0.0'
PORT = 8888
KEY = '85c762d2f339a4ae1d541f4d83001a7f'
SOURCES_FILE="sources.pk"


def salvar(tipo,conteudo):
 file=None
 if tipo == "sources":
  file=open(SOURCES_FILE,"wb")
 pickle.dump(conteudo,file)

def carregar(tipo):
 file=None
 try:
  if tipo == "sources":
   file=open(SOURCES_FILE,"rb")
  return pickle.load(file)
 except:
  return []
 

def sanitizePost(postraw):
 post = parse_qs(postraw)
 for key in post:
  post[key] = escape(post[key][0])
 return post

class ConfigForm():
 def do_GET(self, response):
  configuracao=carregar("sources")
  if configuracao == ():
   configuracao = "Nenhuma fonte adicionada"
  response.write("""
<html>
<body>
<form action="/config/" method="post">
 Incluir Diretorio </br>
 Caminho: <input type="text" name="caminho"/><br>
 Tipo: <select name="tipo">
        <option value="filmes">Filmes</option>
       </select></br>
 <input type="submit" value="Adicionar">
 
</form>
%s
</html>

""" % configuracao)

 def do_POST(self,response, post_body):
  objetos = carregar("sources")
  if objetos == ():
   objetos = [{'caminho' : post_body["caminho"], 'tipo' : post_body["tipo"]},]
  else: 
   objetos.append({'caminho' : post_body["caminho"],'tipo' : post_body["tipo"]})
  salvar("sources",objetos)  
  self.do_GET(response)

FORMS=({'/config/':ConfigForm},{"/",Home})


class BaseHandler(BaseHTTPServer.BaseHTTPRequestHandler):
 def do_HEAD(self):
  self.send_response(200)
  self.send_header('Content-Type','text/html')
  self.end_headers()
 def do_GET(self):
  self.do_HEAD()
  processadora = FORMS[self.path]()
  processadora.do_GET(self.wfile)
 def do_POST(self):
  self.do_HEAD()
  content_len = int(self.headers.getheader('content-length'))
  post_body = self.rfile.read(content_len)
  processadora = FORMS[self.path]()
  processadora.do_POST(self.wfile,sanitizePost(post_body))




if __name__ == '__main__':
 server_class = BaseHTTPServer.HTTPServer
 httpd = server_class((HOST,PORT),BaseHandler)
 try:
  httpd.serve_forever()
 except KeyboardInterrupt:
  pass
 
