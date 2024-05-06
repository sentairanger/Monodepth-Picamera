from flask import Flask, request, render_template, jsonify, Response
from camera_setup import *
from monodepth_init import *
from time import sleep
import logging
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/gallery'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/data")
def data():
    try:
        image_name = 'data.jpg'
        image_file = os.path.join(UPLOAD_FOLDER, image_name)
        if os.path.exists(image_file):
            return render_template("data.html", image_file=image_file)
        else:
            return render_template("no_files.html")
    except Exception as ex:
        logging.error(f"Error in finding images: {ex}")
        return render_template("error.html")
        

@app.route("/gallery")
def gallery():
    try:
        image_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.jpg'))]
        if not image_files:
            return render_template("no_files.html")
        files = []
        for image_file in image_files:
            files.append({'filename' : image_file})
        return render_template("gallery.html", image_files=files)
    except Exception as ex:
        logging.error(f"Error in finding images: {ex}")
        return render_template("error.html")
    
    
@app.route("/capture", methods=['POST'])
def capture_photo():
    try:
        take_photo()
        sleep(1)
        return jsonify(success=True, message="Photo captured successfully")
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

@app.route("/delete_image/<filename>", methods=['DELETE'])
def delete_image(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(filepath)
        return jsonify(success=True, message="Image deleted successfully")
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

@app.route("/videofeed")
def videofeed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/monodepth", methods=['POST'])
def monodepth():
    try:
        img_plt_show()
        return jsonify(success=True, message="Monodepth performed")
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

        
@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
    

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_stream()
    app.run(host="0.0.0.0")
