from io import BytesIO
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import cv2
import time
import os

from pero_ocr_driver import PERO_driver

app = Flask(__name__)


@app.route("/imgshape", methods=["POST"])
def imgshape():
    image_data = request.data
    # We expect image/jpg Content type
    if image_data is None:
        return jsonify({"error": "Request contains no image data."}), 500
    width = height = depth = None

    with tempfile.TemporaryDirectory() as tmpdirname:
        # TODO write image to disk (unless you find a better way)
        file = open('image.jpg', 'wb')
        file.write(image_data)
        file.close()
        try:
            pass
            # TODO use opencv (headless) or some better choice to read the image and get its shape
            im = cv2.imread('image.jpg')
            if im is None:
                return jsonify({"error": "Cannot open image."}), 500
            height = im.shape[0]
            width = im.shape[1]
            depth = im.shape[2]
        except Exception as err:
            return jsonify({"error": f"Unknown error: {err}"}), 500

    return jsonify({"content": {"width": width, "height": height, "depth": depth}}), 200


@app.route("/ocr", methods=["POST"])
def ocr():
    image_data = request.data
    # We expect image/jpg Content type
    if image_data is None:
        return jsonify({"error": "Request contains no image data."}), 500

    with tempfile.TemporaryDirectory() as tmpdirname:
        # TODO write image to disk (unless you find a better way)
        file = open('image.jpg', 'wb')
        file.write(image_data)
        file.close()
        try:
            pass
            # TODO use opencv (headless) or some better choice to read the image and get its shape
            img = cv2.imread('image.jpg')
            if img is None:
                return jsonify({"error": "Cannot open image."}), 500
            # Init the OCR engine if needed
            print("start 'pero ocr engine' init")
            start_time = time.time()
            ocr_engine = PERO_driver(os.environ['PERO_CONFIG_DIR'])
            elapsed_time = int((time.time() - start_time) * 1000)
            print("init 'pero ocr engine' performed in %.1f ms.", elapsed_time)

            # Perform the actual computation
            ocr_results = ocr_engine.detect_and_recognize(img)
            ocr_results = "\n".join([textline.transcription for textline in ocr_results])
            print(ocr_results)

            # TODO return result as json payload
            return jsonify({"content": ocr_results}), 200

        except Exception as err:
            return jsonify({"error": f"Unknown error: {err}"}), 500


if __name__ == "__main__":
    # Simply running this file will start a Flask server in development mode.
    app.run(host="0.0.0.0", debug=True)
