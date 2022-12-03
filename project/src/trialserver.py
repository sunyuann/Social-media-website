from flask import Flask, request, send_from_directory
import urllib

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hello world"

@app.route('/save', methods=['GET'])
def save_file():
    url = 'https://images.unsplash.com/photo-1591630866811-eceedf667541?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80'
    urllib.request.urlretrieve(url, 'static/panda.jpg')
    return "Saved image"

@app.route("/image/<filename>", methods=["GET"])
def serve_file(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(port=0)
