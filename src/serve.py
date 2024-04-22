import socketserver
import yaml
import os
from pyprojroot import here

import http.server

# Load the app configuration from the app_config.yml file
with open(here("configs/app_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

# Get the port number from the app configuration
PORT = app_config["serve"]["port"]

# Get the data directory from the app configuration
DIRECTORY = app_config["directories"]["data_directory"]

# Define a custom request handler class
class SingleDirectoryHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    pass

# Start the server
if __name__ == "__main__":
    # Create a TCP server object that listens on the specified port
    with socketserver.TCPServer(("", PORT), SingleDirectoryHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()