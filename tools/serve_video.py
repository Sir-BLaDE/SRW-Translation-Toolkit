# -*- coding: utf-8 -*-
"""Servidor HTTP con soporte Range para revisar el vídeo en el navegador."""
import http.server
import os
import re

ROOT = r"C:/Dev/Default Project/srwv/outputs"
PORT = 8766


class RangeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            return super().do_GET()
        size = os.path.getsize(path)
        rng = self.headers.get("Range")
        if not rng:
            return super().do_GET()
        m = re.match(r"bytes=(\d+)-(\d*)", rng)
        if not m:
            return super().do_GET()
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else size - 1
        end = min(end, size - 1)
        length = end - start + 1
        with open(path, "rb") as f:
            f.seek(start)
            data = f.read(length)
        self.send_response(206)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), RangeHandler).serve_forever()
