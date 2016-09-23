# coding=utf-8

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs

import search


class WikiSearchServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.do_HEAD()

        _GET = parse_qs(urlparse(self.path).query)

        if 'q' in _GET:
            result = search.search(_GET['q'][0])

            self.wfile.write("<html><head><title>Search result</title></head>")
            self.wfile.write("<body>")
            self.wfile.write("<p>Result in "+str(result['time'])+" seconds</p>")
            for page in result['pages']:
                self.wfile.write("<p>"+page[1]+"</p>")
            self.wfile.write("<p>You accessed path: %s</p>" % self.path)
            self.wfile.write("</body></html>")

        self.finish()


def start(indexDir):
    search.initialize(indexDir)
    try:
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, WikiSearchServer)
        print "Serving on http://localhost:8000"
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\rShutting down server')
        httpd.socket.close()


if __name__ == "__main__":
    start()
