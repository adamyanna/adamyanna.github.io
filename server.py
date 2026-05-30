import http.server
import os
import urllib.parse

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if not path or path.endswith('/'):
            idx = os.path.join(self.translate_path(path), 'index.html')
            if os.path.isfile(idx):
                self.path = path.rstrip('/') + '/index.html'
        super().do_GET()

if __name__ == '__main__':
    http.server.HTTPServer(('', 8080), Handler).serve_forever()