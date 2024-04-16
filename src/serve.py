import http.server
import socketserver
import yaml
import os
from pyprojroot import here

with open(here("configs/app_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

PORT = app_config["serve"]["port"]
DIRECTORY = app_config["directories"]["data_directory"]

class SingleDirectoryHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), SingleDirectoryHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()