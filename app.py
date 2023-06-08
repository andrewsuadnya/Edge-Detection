from flask import Flask, render_template, request
from PIL import Image
import cv2
import numpy as np
import io
import base64

app = Flask(__name__, template_folder='templates', static_folder='static')

def apply_edge_detection_operator(image, operator):
    if operator == 'sobel':
        edges = cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=3)
    elif operator == 'roberts':
        kernel_x = np.array([[1, 0], [0, -1]])
        kernel_y = np.array([[0, 1], [-1, 0]])
        gradient_x = cv2.filter2D(image.astype(np.float32), -1, kernel_x)
        gradient_y = cv2.filter2D(image.astype(np.float32), -1, kernel_y)
        edges = np.sqrt(np.square(gradient_x) + np.square(gradient_y))
        edges = cv2.convertScaleAbs(edges)
    elif operator == 'prewitt':
        kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        gradient_x = cv2.filter2D(image.astype(np.float32), -1, kernel_x)
        gradient_y = cv2.filter2D(image.astype(np.float32), -1, kernel_y)
        edges = np.sqrt(np.square(gradient_x) + np.square(gradient_y))
        edges = cv2.convertScaleAbs(edges)
    elif operator == 'laplace':
        edges = cv2.Laplacian(image, cv2.CV_64F)
    elif operator == 'frei-chen':
        gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        edges = np.sqrt(np.square(gradient_x) + np.square(gradient_y))

    edges = cv2.convertScaleAbs(edges)
    return edges
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        operator = request.form['operator']

        img = Image.open(file.stream)
        img_array = np.array(img.convert('RGB'))

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        original_image_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

        if operator:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            edges = apply_edge_detection_operator(gray, operator)

            edges_pil = Image.fromarray(edges)
            edges_pil.thumbnail((img.width, img.height))
            edges_bytes = io.BytesIO()
            edges_pil.save(edges_bytes, format='PNG')
            edges_base64 = base64.b64encode(edges_bytes.getvalue()).decode('utf-8')

            return render_template('index.html', edges_base64=edges_base64, original_image_base64=original_image_base64)

    return render_template('index.html', original_image_base64=None, edges_base64=None)

if __name__ == '__main__':
    app.run(debug=True)
