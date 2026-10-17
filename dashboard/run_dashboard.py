import http.server
import socketserver
import webbrowser
import os
import threading
import time

PORT = 5000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def open_browser():
    time.sleep(1.2)
    url = f"http://localhost:{PORT}/index.html"
    print(f"Opening dashboard at {url}...")
    webbrowser.open(url)

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"================================================================")
        print(f"DASHBOARD IS LIVE AT: http://localhost:{PORT}/index.html")
        print(f"Press Ctrl+C to stop the dashboard server.")
        print(f"================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard server stopped.")
