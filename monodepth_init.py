import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np
from openvino.runtime import Core
from pathlib import Path
import matplotlib
from datetime import datetime

# Define the timestamp
timestamp = datetime.now().isoformat()

matplotlib.use('Agg')

DEVICE = "MYRIAD"
MODEL_FILE = "model/MiDaS_small.xml"

model_xml_path = Path(MODEL_FILE)

def normalize_minmax(data):
    return (data - data.min()) / (data.max() - data.min())

def convert_result(result, colormap="viridis"):
    # Convert result of floating point numbers to RGB
    # using values from 0-255 with a colormap
    cmap = matplotlib.cm.get_cmap(colormap)
    result = result.squeeze(0)
    result = normalize_minmax(result)
    result = cmap(result)[:, :, :3] * 255
    result = result.astype(np.uint8)
    return result

def to_rgb(image_data) -> np.ndarray:
    # convert image data from BGR to RGB
    return cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
    
# Load the engine and model
ie = Core()
ie.set_property({'CACHE_DIR' : '../cache'})
model = ie.read_model(model_xml_path)
compiled_model = ie.compile_model(model=model, device_name=DEVICE)
input_key = compiled_model.input(0)
output_key = compiled_model.output(0)
network_input_shape = list(input_key.shape)
network_image_height, network_image_width = network_input_shape[2:]

# Load image and reshape input image
IMAGE_FILE = "static/gallery/data.jpg"

def input_image():
    image = cv2.imread(IMAGE_FILE)
    return image

def resize_image():
    resized_image = cv2.resize(src=input_image(), dsize=(network_image_height, network_image_width))
    return resized_image

def expand_image():
    input_image = np.expand_dims(np.transpose(resize_image(), (2, 0, 1)), 0)
    return input_image

# Do inference
def inference_result():
    result = compiled_model([expand_image()])[output_key]
    return result

def image_result():
    # Convert the result of disparity map to an image that shows distance as colors
    result_image = convert_result(result=inference_result())
    # Resize back to original shape
    result_image = cv2.resize(result_image, input_image().shape[:2][::-1])
    return result_image
    

# Display images
# Used only for testing
def img_show():
    print("images processing")
    fig, ax = plt.subplots(1, 2, figsize=(20, 15))
    ax[0].imshow(to_rgb(input_image()))
    ax[1].imshow(image_result());
    plt.savefig("static/gallery/image_%s.jpg" % timestamp)
    print("success")

# Show the single image
def img_plt_show():
    print("single image processing")
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.imshow(image_result())
    plt.savefig("static/gallery/single_image_%s.jpg" % timestamp)
    print("success")
