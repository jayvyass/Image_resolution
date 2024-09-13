from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from PIL import Image
import os
import urllib.request
import uuid
import json
import mimetypes

# Define the directory to serve static files from
STATIC_DIR = 'static'

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/static/'):
            file_path = os.path.join(STATIC_DIR, self.path[len('/static/'):])
            if os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                mime_type = mime_type or 'application/octet-stream'
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    self.wfile.write(file.read())
                return
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'File not found'})
                self.wfile.write(response.encode('utf-8'))
                return
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({'error': 'Endpoint not found'})
        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        image_url = data.get('url')
        if not image_url:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': 'URL is required'})
            self.wfile.write(response.encode('utf-8'))
            return

        try:
            # Download the image
            temp_file_path = 'temp_image.png'
            urllib.request.urlretrieve(image_url, temp_file_path)

            # Enhance the image
            enhanced_img_filename = enhance_image(temp_file_path)

            # Respond with the URL of the enhanced image
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'enhanced_image_url': f'http://192.168.0.116:8000/static/{enhanced_img_filename}'})
            self.wfile.write(response.encode('utf-8'))

            # Clean up the temporary image
            os.remove(temp_file_path)

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': str(e)})
            self.wfile.write(response.encode('utf-8'))

def enhance_image(file_path):
    img = Image.open(file_path)

    # Define new width and height
    new_width = 3897
    new_height = 4896

    # Resize the image
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Define DPI
    dpi = (300, 300)

    # Save the image with the specified DPI in STATIC_DIR
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    filename = f'enhanced_image_{uuid.uuid4()}.png'
    file_path = os.path.join(STATIC_DIR, filename)
    img.save(file_path, dpi=dpi)

    return filename

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
  # def do_GET(self):      
    #     if self.path.startswith('/static/'):
    #         file_path = os.path.join(STATIC_DIR, self.path[len('/static/'):])
    #         if os.path.isfile(file_path):
    #             mime_type, _ = mimetypes.guess_type(file_path)
    #             mime_type = mime_type or 'application/octet-stream'
    #             with open(file_path, 'rb') as file:
    #                 self.send_response(200)
    #                 self.send_header('Content-type', mime_type)
    #                 self.end_headers()
    #                 self.wfile.write(file.read())
    #             return
    #         else:
    #             self.send_response(404)
    #             self.send_header('Content-type', 'application/json')
    #             self.end_headers()
    #             response = json.dumps({'error': 'File not found'})
    #             self.wfile.write(response.encode('utf-8'))
    #             return
    #     self.send_response(404)
    #     self.send_header('Content-type', 'application/json')
    #     self.end_headers()
    #     response = json.dumps({'error': 'Endpoint not found'})
    #     self.wfile.write(response.encode('utf-8'))