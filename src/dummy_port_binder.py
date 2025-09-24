import os
import threading
import http.server
import socketserver

def keepalive():
    port = int(os.getenv("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=keepalive, daemon=True).start()
