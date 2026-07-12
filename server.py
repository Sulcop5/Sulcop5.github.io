"""开发服务器：静态文件 + 字体列表 API。运行：py -3 server.py"""

import http.server
import socketserver
import os
import json

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(DIR, "fonts")
os.makedirs(FONTS_DIR, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        if self.path == "/api/fonts":
            fonts = [
                f
                for f in os.listdir(FONTS_DIR)
                if f.lower().endswith((".ttf", ".woff2", ".otf"))
            ]
            fonts.sort()
            self._json(fonts)
            return
        super().do_GET()

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"服务器已启动  http://localhost:{PORT}")
        httpd.serve_forever()
