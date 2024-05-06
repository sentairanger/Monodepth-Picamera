# Monodepth-Picamera
This project takes images and then performs monodepth estimation using the OpenVINO toolkit and the Intel NCS2

## Note

The `bin` file was too big to add so use this [link](https://storage.openvinotoolkit.org/repositories/openvino_notebooks/models/depth-estimation-midas/FP32/) to download the file and add it to your `model` directory.

## Getting started

To get started, you will need the following:

* Raspberry Pi 4 (1, 2, 4, or 8GB)
* MicroSD Card (At least > 16GB)
* USB-C Power
* SSH Enabled on the Pi for remote access
* Intel NCS2 for Inferencing
* OpenVINO toolkit (follow this [gist](https://gist.github.com/sentairanger/caf11a2432ceebd715c6b33c224f4960) for instructions)
* Raspberry Pi Camera (Any will suffice)
* Camera Mount (recommended if using outdoors)

This project was tested using Raspberry Pi OS Bullseye 64-bit. Once I get my hands on the Raspberry Pi 5 with Bookworm I will run tests. To run this application just type `python3 app.py` and then go to `ip-address-of-pi:5000` and the app should appear as shown below.

![image](https://github.com/sentairanger/Monodepth-Picamera/blob/main/mono-app.png)

Take a picture and then run monodepth estimation on the image. A sample image is shown below.

![sample](https://github.com/sentairanger/Monodepth-Picamera/blob/main/static/gallery/single_image_2024-04-17T14%3A24%3A26.304664.jpg)
